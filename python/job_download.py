#!/usr/bin/env python3
import os
import sys
import requests
from time import sleep

JOB_URL = "http://a810-bisweb.nyc.gov/bisweb/JobsQueryByNumberServlet?passjobnumber={}"
USER_AGENT = 'Mozilla/5.0'
HEADERS = {'User-Agent': USER_AGENT }
FOLDER = 'data'
# seconds between download
THROTTLE = 8


def job_url(job_number):
    return JOB_URL.format(job_number)


def job_html(job_number):
    try:
        r = requests.get(job_url(job_number), headers=HEADERS)
        if r.status_code == 200:
            print("✓ {}".format(job_number))
            return r.text
        else:
            print("request for job: {} failed with status code {}".format(job_number, r.status_code))
            return None
    except:
        print("failed to download job: {}".format(job_number))
        return None


def job_file_path(job_number, folder=FOLDER):
    return os.path.join(folder, "{}.html".format(job_number))


def download_job(job_number):
    html = job_html(job_number)
    if html:
        with open(job_file_path(job_number), 'w') as f:
            f.write(html)


def download_job_unless_file_exists(job_number):
    job = str(job_number).strip()
    if not os.path.isfile(job_file_path(job)):
        download_job(job)
        sleep(THROTTLE)
    else:
        print("😻 {}".format(job))


if __name__ == '__main__':
    download_job_unless_file_exists(sys.argv[1])
