#!/usr/bin/env python3
"""
Downloads Statement of Account from Department of Finance

borrows from: https://github.com/talos/nyc-stabilization-unit-counts/blob/master/download.py

Required libraries: requests, beautifulsoup4, dateparser

Install like such: ` pip3 requests beautifulsoup4 dateparser `

Here's what going on: you submit a bbl in a form,
and that form returns an html document...with a form that's
already filled out. if you submit that second form you get
back an html document with links to the tax bills.

following? those links, however, are not to the documents
themselves but to another html page, which sadly
requires javascript to render the links to actual
documents we are looking for! anyways, the documents
seem to follow a pattern, so the titles of them can be
used to generate links using the date of the document.

"""
from collections import namedtuple
from time import sleep
import re
import sys
import os
import pathlib

import dateparser
import requests
from bs4 import BeautifulSoup

MINIMUM_YEAR = 2015

FOLDER = 'data'

INTERMEDIATE_URL = "http://webapps.nyc.gov:8084/CICS/fin1/find001i"

LIST_URL = 'http://nycprop.nyc.gov/nycproperty/nynav/jsp/stmtassesslst.jsp'

SOA_LINK = "http://nycprop.nyc.gov/nycproperty/StatementSearch?bbl={bbl}&stmtDate={date}&stmtType=SOA"

PAUSE_AFTER_INTERMEDIATE = 1
PAUSE_BETWEEN_DOWNLOAD = 2
PAUSE_BEFORE_RETRY = 15

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62 Safari/537",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": INTERMEDIATE_URL
}
DOCUMENT_HEADERS = HEADERS.copy().update({ 'Referer': LIST_URL})

DOCS_TO_DOWNLOAD = [
    'Quarterly Statement of Account',   # Amounts paid, stabilized fees, other charges, mailing address
    'Quarterly Property Tax Bill',   # Amounts paid, stabilized fees, other, charges
]

DOCS_REGEX = re.compile("({}|{})".format(*DOCS_TO_DOWNLOAD), flags=re.IGNORECASE)

###
# Helper tuples!
#
# BBL has borough, block, lot
# Link is a simple struct with a href and a title
# Document contains the link for a SOA with it's title and date

BBL = namedtuple('BBL', ['borough', 'block', 'lot'])
LINK = namedtuple('LINK', ['href', 'title'])
DOCUMENT = namedtuple('DOCUMENT', ['title', 'link', 'date'])

##
# BBL helper functions
#

def split_bbl(bbl):
    if len(bbl) != 10:
        raise Exception("BBL ({}) is not the correct length".format(bbl))
    return BBL(bbl[0], bbl[1:6], bbl[6:])


def character_bbl(bbl):
    """ BBL -> str """
    return bbl.borough + bbl.block.zfill(5) + bbl.lot.zfill(4)

##
# Document scraping and request helpers
#

# BBL -> dict

def form_data(bbl):
    """ Returns form data for post request to get intermediate html """
    return {
        "FFUNC": "C",
        "FBORO": bbl.borough,
        "FBLOCK": bbl.block,
        "FLOT": bbl.lot,
        "FEASE": ''
    }


def get_intermediate_html(bbl):
    """
    Retrives html from the first request -- called "intermediate",
    via a POST request.
    It contains a form that will be resubmitted in list_html()
    """
    r = requests.post(INTERMEDIATE_URL, data=form_data(bbl), headers=HEADERS)
    return r.text


# str -> tuple: url[str], form_data[dict]
def parse_intermediate_html(html):
    """" Retrives the url and form data from html """
    soup = BeautifulSoup(html, "html.parser")
    inputs = soup.find('form').find_all('input')
    url = soup.find('form')['action']
    form_data = dict([(i['name'], i['value']) for i in inputs])
    return (url, form_data)


# str --> str
def get_list_html(intermediate_html):
    """
    Return the html with list of documents via post request
    """
    url, post_data = parse_intermediate_html(intermediate_html)
    r = requests.post(url, data=post_data, headers=HEADERS)
    return r.text


def extract_year(docname):
    """ Extracts year from docname """
    match = re.search("(?<=[ ])(\d{4})(?=[ ])", docname)
    if match:
        return int(match.group(1))


def document_titles(list_html):
    """
    Extracts titles of the links for Quarterly Statement of Accounts
    """
    soup = BeautifulSoup(list_html, "html.parser")

    titles = []
    for a in soup.find_all('a', href=True):
        title = a.text.strip()
        if title != '' and extract_year(title):
            if DOCS_REGEX.search(title):
                titles.append(title)
    return titles


def get_titles_for_bbl(bbl):
    intermediate_html = get_intermediate_html(bbl)
    sleep(PAUSE_AFTER_INTERMEDIATE)
    list_html = get_list_html(intermediate_html)
    return document_titles(list_html)


def title_to_document(title, bbl):
    """
    turns title into a DOCUMENT with link, title, and date
    """
    date = dateparser.parse(title.split('-')[0].strip())
    link = SOA_LINK.format(bbl=character_bbl(bbl), date=date.strftime('%Y%m%d'))
    return DOCUMENT(title, link, date)


# BBL -> [DOCUMENT]
def documents_for_bbl(bbl):
    """
    Downloads and parses list of tax bills for the given bbl
    """
    titles = get_titles_for_bbl(bbl)
    return [title_to_document(title, bbl) for title in titles]

##
# Downloading document utilities
#

def file_exists(filepath):
    return os.path.isfile(filepath) and os.stat(filepath).st_size > 0


def document_exists(doc, bbl):
    return file_exists(title_to_path(doc.title, bbl, 'pdf')) or file_exists(title_to_path(doc.title, bbl, 'html'))


def find_extension(resp):
    """ Extract whether a requests response is for HTML or PDF. """
    content_type = resp.headers['Content-Type']
    if 'html' in content_type:
        return 'html'
    elif 'pdf' in content_type:
        return 'pdf'
    else:
        raise "Unknown content type: {}".format(content_type)


def title_to_path(title, bbl, ext):
    file_name = title.strip().replace(' ', '_') + '.' + ext
    return os.path.join(FOLDER, character_bbl(bbl), file_name)


def save_file(resp, doc, bbl):
    """
    Saves response to disk with file path based on content_type and bbl
    """
    filepath = title_to_path(doc.title, bbl, find_extension(resp))
    with open(filepath, 'wb') as f:
            for chunk in resp:
                f.write(chunk)


def retry(func):
    def wrapper(*args):
        try:
            func(*args)
        except requests.exceptions.RequestException:
            print("Connection Error....Waiting 15 seconds", file=sys.stderr)
            sleep(PAUSE_BEFORE_RETRY)
            try:
                func(*args)
            except requests.exceptions.RequestException:
                print("Connection Error....Waiting 30 seconds", file=sys.stderr)
                sleep(PAUSE_BEFORE_RETRY * 2)
                func(*args)
    return wrapper


@retry
def download_doc(doc, bbl):
    """
    Downloads document and saves to file.

    It won't download for the following reasons:
      - file already exists
      - year is before the minium year set at top of file
    """

    if document_exists(doc, bbl):
        print("{} exists already".format(doc.title))
        return

    if doc.date.year < MINIMUM_YEAR:
        print("{} is from before {}".format(doc.title, MINIMUM_YEAR))
        return

    r = requests.get(doc.link, headers=DOCUMENT_HEADERS, stream=True)

    if r.status_code == 200:
        save_file(r, doc, bbl)
        print("saved {}".format(doc.title))
        sleep(PAUSE_BETWEEN_DOWNLOAD)
    else:
        msg = "Tried to download {}, but it failed!".format(doc.title)
        print(msg, file=sys.stderr)


@retry
def download_docs_for_bbl(input_bbl):
    """
    downloads and saves document given a 10 character bbl
    """
    bbl = split_bbl(input_bbl)
    pathlib.Path(os.path.join(FOLDER, character_bbl(bbl))).mkdir(parents=True, exist_ok=True)
    for doc in documents_for_bbl(bbl):
        download_doc(doc, bbl)


def download_for_many(filepath):
    """
    reads the first 10 characters of each line as as bbl.
    You can use any csv file or text file as long as the first
    columns is the bbls
    """
    with open(filepath, 'r') as f:
        for line in f:
            bbl = line[0:10]
            download_docs_for_bbl(bbl)
            sleep(PAUSE_BETWEEN_DOWNLOAD)


def main():
    if len(sys.argv) == 1:
        raise "Missing argument. requires file path or bbl"

    if re.match('^(1|2|3|4|5){1}\d{9}$', sys.argv[1]):
        download_docs_for_bbl(sys.argv[1])
    else:
        download_for_many(sys.argv[1])


if __name__ == '__main__':
    main()
