#  Permitted Perjury: finding lying landlords in NYC

This repo contains the code that helped produce the September [HRI](https://housingrightsny.org/) report about building permit fraud. We found over 10,000 falsified permits!

Read about our report in the [nytimes](https://www.nytimes.com/2018/09/23/nyregion/housing-rights-initiative-aaron-carr-nyc-kushner.html), [politico](https://www.politico.com/states/new-york/city-hall/story/2018/09/23/kushners-false-construction-filings-part-of-widespread-city-trend-623260), and [amNY](https://www.amny.com/real-estate/nyc-construction-permits-1.21243040).


## How to recreate the entire report and dataset

### Requirements

make, fish, psql, python3, pip, pyvenv, [csvkit](https://csvkit.readthedocs.io/en/1.0.3/), jq, pandoc, [bbler](https://github.com/aepyornis/bbler), [nycdb](https://github.com/aepyornis/nyc-db)

See the Makefile for a better sense of what's going on. Note that downloading the data will take WEEKS!

1) ` make jobs.csv `

This produces a csv of all department of buildings jobs for likely rent-stabilized buildings since 2016. It requires setting up a running instance of [nycdb](https://github.com/aepyornis/nyc-db).

2) ` make possible_liars.csv `

This will generate a list of potential liars by downloading tax bills and job filings pages from city websites. Expect this task to produce LOTS of errors and take many weeks. See [bbler](https://github.com/aepyornis/bbler) for the scripts to parse and download tax bills and job filings.

3) ` make liars.csv `

Filter the list of liars to those whose permit applications contain falsified or suspicious information.

4) ` make liars.zip `

This will create a zip file with a folder for each permit containing all the PDFs and documents so each lying landlord can be manually verify as needed.


To build the report ``` make report ```

To download a list of buildings with lead paint violations: ` make lead_paint_bbls.csv `. This is used for statistics in the report.

In the folder `notebook` there is a Jupiter notebook used to derive the statistics in the report.
