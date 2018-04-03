#!/usr/bin/env python3
import os
import sys
import requests
from collections import namedtuple
from bs4 import BeautifulSoup, NavigableString
from pathlib import Path
from time import sleep

USER_AGENT = 'Mozilla/5.0'
HEADERS = {'User-Agent': USER_AGENT}
FOLDER = 'data'
THROTTLE = 2  # seconds between download

VIRTUAL_JOB_FOLDER_URL = "http://a810-bisweb.nyc.gov/bisweb/BScanVirtualJobFolderServlet?passjobnumber={}"

DOCUMENT = namedtuple('DOCUMENT', ['scancode', 'form_id'])

DESIRED_FORMS = set(['PW1'])

DOCUMENT_URL = "http://a810-bisweb.nyc.gov/bisweb/BSCANJobDocumentContentServlet?passjobnumber={job_number}&scancode={scancode}"


def document_path(document, job_number, folder=FOLDER):
    dir_path = Path(os.path.join(folder, job_number))
    dir_path.mkdir(parents=True, exist_ok=True)
    file_name = "{}_{}.pdf".format(document.form_id, document.scancode)
    return os.path.abspath(str(dir_path.joinpath(file_name)))


# DOCUMENT -> string
def document_to_link(document, job_number):
    return DOCUMENT_URL.format(job_number=job_number, scancode=document.scancode)


def job_folder_html(job_number):
    url = VIRTUAL_JOB_FOLDER_URL.format(job_number)
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.text


def documents(html):
    _documents = []
    soup = BeautifulSoup(html, 'html.parser')

    # loop through table of documents
    for tr in soup.find(id="tblVirtualJobFolder"):

        # skips rows without any links
        if isinstance(tr, NavigableString) or len(tr.find_all('a')) == 0:
            continue

        # extract 'scancode' and 'form_id'
        scancode = tr.find_all('td')[5].text.strip()
        form_id = tr.find_all('td')[1].text.strip()
        _documents.append(DOCUMENT(scancode, form_id))
    return _documents


def download_document(document, job_number):
    url = document_to_link(document, job_number)
    print("download url: {}".format(url))
    r = requests.get(url, headers=HEADERS, stream=True)
    r.raise_for_status()

    with open(document_path(document, job_number), 'wb') as f:
        for chunk in r:
                f.write(chunk)


def download_documents_for_job(job_number):
    for doc in documents(job_folder_html(job_number)):
        if doc.form_id in DESIRED_FORMS:
            print("Downloading {} ({})".format(doc.form_id, doc.scancode))
            download_document(doc, job_number)
            sleep(THROTTLE)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception("Missing argument, job number")

    download_documents_for_job(sys.argv[1])
