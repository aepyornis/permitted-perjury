# Permitted Perjury

### Landlords routinely lie on their permit applications

In order to do any kind of building construction in New York City landlords must submit a form called [PW1](http://www1.nyc.gov/assets/buildings/pdf/pw1.pdf) containing basic information about the application. At the end of the PW1, there is a section called the **Property Owner's Statements and Signatures** where the property owner must certify the form and provide their contact information.

The section contains a handful of simple yes/no questions which the owner must fill out regarding their building. It also has a warning: "Falsification of any statement is a misdemeanor and is punishable by a fine or imprisonment, or both_". Two of these questions are notable (paraphrased):

1) Will one or more of the units in the building be occupied during construction

2) Does the building have "occupied housing accommodations subject to rent control or rent stabilization"

Owners must tell the department of buildings two very basic, yet crucial facts about their building: will it be vacant and is it rent stabilized?

Certainly, no one would risk **jail time** by falsifying something that can easily be proved...right?


## Data Gathering

The DOB keeps a [list](https://data.cityofnewyork.us/Housing-Development/DOB-Job-Application-Filings/ic3t-wcy2/data) of all submitted jobs on NYC's open data portal. This, unfortunately, **doesn't** include information on those questions. However, the answers to the questions on the PW1 can be found on the DOB website through the [buildings information system](http://a810-bisweb.nyc.gov/bisweb/bsqpm01.jsp).

Using a list of 45,685 Tax Lots that likely contain rent-stabilized buildings and a dataset of all Department of Buildings jobs (gathered from February version of [NYCDB](https://github.com/aepyornis/nyc-db), I derived a list of 27,00 jobs active since January 2016 for rent-stabilized buildings. Due to the volume of jobs, I excluded applications for minor alternations (A3).

Of these 27,000 the vast majority are A2 applications. It does include about 900 A1 jobs as well as hundreds of demolition and new building applications.

These 27,000 jobs are for about 11,00 unique tax lots in the city.

The data on the questions themselves were gathered by scraping the department of buildings website over a period of few weeks in March and April. The rent stabilization data was obtained by downloading and parsing the Department of Finance quarterly tax bills, which include a registration fee for rent-stabilized units.


### How the landlords answered the question

21% of all permits examined (~5000) were found to have falsely answered their question on rent-stabilization. These permits had registered rent-stabilized units with the department of finance in the year following the permit application. An additional 25% (~6,500) are likely to be liars as well. These likely liars have registered rent-stabilized units in prior years.

In short there appears to be systematic lying on permits by landlords. Many thousands of permits are regularly submitted and approved with fraudulent information.


Since 2016 is the latest year with complete Department of Finance data, so we can get a better picture. Of the 13,000 permits examined in 2016, 44% were found to contain falsified information.

### Where's there smoke there's fire: lead paint violators

Landlords who falsify their permits are often unscrupulous in other ways. 422 buildings (on 765 permits) also had lead paint violations in the past few years.




