#  Permitted Perjury: finding lying landlords in nyc


## requirements

make, fish, psql, python3, pip, pyvenv, [bbler](https://github.com/aepyornis/bbler), [csvkit](https://csvkit.readthedocs.io/en/1.0.3/), pandoc


## How to recreate the entire report and dataset

See the Makefile for a better sense of what is going on. Note that downloading the data will take WEEKS!

1) ` make jobs.csv `

This produces a csv of all department of jobs for likely rent-stabilized buildings since 2016. Tt requires setting up a running instance of [nycdb](https://github.com/aepyornis/nyc-db)

2) ` make possible_liars.csv `

This will generate a list of potential liars by downloading tax bills and job filings pages from city websites. Expect this task to produce LOTS of errors and take many WEEKS. See [bbler](https://github.com/aepyornis/bbler) for the scripts to parse and download tax bills and job filings.

3) ` make liars.csv `

Filter the list of liars to those whose permit applications contain falsified or suspicious information.

4) ` make liars.zip `

This will create a zip file with a folder for each permit containing all the PDFs and documents so each lying landlord can be manually verify as needed.


To build the report ``` make report ```


To download a list of buildings with lead paint violations: ` make lead_paint_bbls.csv `. This is used for statistics in the report.

In the folder `notebook` there is a jupyter notebook used to derive the statistics in the report.

