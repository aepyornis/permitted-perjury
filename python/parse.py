import csv
import os
from bs4 import BeautifulSoup, NavigableString

JOB_URL = "http://a810-bisweb.nyc.gov/bisweb/JobsQueryByNumberServlet?passjobnumber={}"
JOBS_FILE = './dobjobs_active_since_2016.csv'

TEXT = {
    'remain_occupied': "(Remain Occupied)",
    'rent_control': "(Rent Control / Stabilization)",
    'dhcr_notification': "Owner DHCR Notification",
    'directive_14': "Certification for Directive 14"
}


def owners_info_table(soup):
    for table in tables(soup):
        for td in table.find_all('td', class_="colhdg"):
            if td.text[0:2] == '26':
                return table
    raise "failed to find owners table"


class HowCanItBeYesAndNoAtTheSameTimeError(Exception):
    pass


class MissingTableError(Exception):
    pass


def job_file_path(job_number, folder='data'):
    return os.path.join(folder, "{}.html".format(job_number))


def get_soup(job):
    path = job_file_path(job)
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return BeautifulSoup(f, "lxml")
    else:
        print('no file found for: {}'.format(job))
        return None


def tables(soup):
    for table in soup.find_all('table'):
        yield table


# yes_box.gif / no_box.gif
def has_yes_img(tr):
    return bool(tr.find('img', src='images/yes_box.gif'))


def has_no_img(tr):
    return bool(tr.find('img', src='images/no_box.gif'))


def tr_for(soup, text):
    for table in tables(soup):
        for tr in table.find_all('tr'):
            for td in tr:
                if not isinstance(td, NavigableString):
                    if text in td.text:
                        return tr


def remain_occupied_tr(soup):
    """ soup -> tag """
    return tr_for(soup, TEXT['remain_occupied'])


def parse_table(soup, question):
    tr = tr_for(soup, TEXT[question])
    if tr is None:
        raise MissingTableError
    if has_yes_img(tr) and has_no_img(tr):
        raise HowCanItBeYesAndNoAtTheSameTimeError
    if has_yes_img(tr):
        return 'yes'
        # return True
    if has_no_img(tr):
        return 'no'
        # return False
    return 'blank'
    #return None


def blank_parse(job):
    return {
        "job_url": JOB_URL.format(job),
        "remain_occupied": '',
        "rent_control": '',
        "dhcr_notification": '',
        "directive_14": ''
    }


def parse(soup, job):
    """
    input: BeautifulSoup, str/int
    out: Dictionary
    """
    return {
        "job_url": JOB_URL.format(job),
        "remain_occupied": parse_table(soup, 'remain_occupied'),
        "rent_control": parse_table(soup, 'rent_control'),
        "dhcr_notification": parse_table(soup, 'dhcr_notification'),
        "directive_14": parse_table(soup, 'directive_14')
    }


def parse_jobs_csv():
    with open(JOBS_FILE, 'r') as f:
        with open('./out.csv', 'w') as out:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames + ['remain_occupied', 'rent_control', 'dhcr_notification', 'directive_14', 'job_url']
            writer = csv.DictWriter(out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                try:
                    # print("parsing: {}".format(row['job']))
                    soup = get_soup(row['job'])
                    if soup:
                        writer.writerow({**row, **parse(soup, row['job'])})
                    else:
                        writer.writerow({**row, **blank_parse(row['job'])})
                except MissingTableError:
                    print("ERROR WITH job number: {}".format(row['job']))
                    writer.writerow({**row, **blank_parse(row['job'])})


if __name__ == '__main__':
    parse_jobs_csv()
