#!/usr/bin/env python3
import sys
import json
import datetime
from pathlib import Path

if len(sys.argv) == 1:
        raise Exception("Missing argument, job number")

JOB = sys.argv[1]

def read_json(path):
    with open(path, 'r') as f:
        return json.loads(f.read())

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d")

def question_answer(answer):
    if answer == 'yes':
        return True

    if answer == 'no':
        return False

    return None


# parsed dob information
pw1_path = str(Path.home().joinpath('.nyc-data', 'dob', str(JOB), 'pw1.json'))
dob_info_path = str(Path.home().joinpath('.nyc-data', 'dob', str(JOB), '{}.json'.format(JOB)))

pw1 = read_json(pw1_path)
dob_info = read_json(dob_info_path)

rent_stab_answer = question_answer(pw1['rent_control'].lower())

prefilingdate = dob_info[0]['prefilingdate']
job_year = prefilingdate[0:4]

BBL = dob_info[0]['bbl']

bbl_info_path = str(Path.home().joinpath('.nyc-data', 'bbl', BBL, '{}.json'.format(BBL)))
bbl_info = read_json(bbl_info_path)


if job_year not in bbl_info['dof']['unitCounts']:
    stabilized_in_year = None
else:
    stabilized_in_year = (bbl_info['dof']['unitCounts'][job_year] > 0)


if (not rent_stab_answer) and bbl_info['dof']['rentStabilized']:
    if stabilized_in_year:
        is_liar = 'yes'
        liar_boolean = True
    else:
        is_liar = 'suspicious'
        liar_boolean = None
else:
    is_liar = 'no'
    liar_boolean = False


result = {
    "job": JOB,
    "date": prefilingdate,
    "rentStabAnswer": rent_stab_answer,
    "liarStatus": is_liar,
    "liar": liar_boolean
}

print(json.dumps(result))
