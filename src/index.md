# Permitted Perjury

### Landlords routinely lie on their permit applications

In order to do any kind of building construction in New York City landlords must submit a form called [PW1](http://www1.nyc.gov/assets/buildings/pdf/pw1.pdf) containing basic information about the application. At the end of the PW1, there is a section called the **Property Owner's Statements and Signatures** where the property owner must certify the form and provide their contact information.

The section contains a handful of simple yes/no questions which the owner must fill out regarding their building. It also has a warning: "_Falsification of any statement is a misdemeanor and is punishable by a fine or imprisonment, or both_". Two of these questions are notable (paraphrased):

1) Will one or more of the units in the building be occupied during construction

2) Does the building have  "occupied housing accommodations subject to rent control or rent stabilization"

Owners must tell the department of buildings two very basic, yet crucial facts about their building: will it be vacant and is it rent stabilized?

Certainly, no one would risk **jail time** by falsifying something that can easily be proved...right?


## Data Gathering

The DOB keeps a [list](https://data.cityofnewyork.us/Housing-Development/DOB-Job-Application-Filings/ic3t-wcy2/data) of all submitted jobs on NYC's open data portal. This, unfortunately, **doesn't** include information on those questions. However, the answers to the questions on the PW1 can be found on the DOB website through the [buildings information system](http://a810-bisweb.nyc.gov/bisweb/bsqpm01.jsp).

![](images/jobtype.png "job types"){.right-img .jobtype}

Using a list of 45,685 Tax Lots that likely contain rent-stabilized buildings and a dataset of all Department of Buildings jobs (gathered from February version of [NYCDB](https://github.com/aepyornis/nyc-db), I derived a list of 41,00 jobs active since January 2016 for rent-stabilized buildings. Due to the volume of jobs, I excluded applications for minor alternations (A3).

Of these 41,00 the vast majority are A2 applications. It does include about 1,500 A1 jobs as well as hundreds of demolition and new building applications.

These 41,000 jobs are for about 15,00 unique tax lots in the city.

The data on the questions themselves were gathered by scraping the department of buildings website over a period of few weeks in early March.

### How the landlords answered those questions

#### Question on vacancy

![](images/stabilized.png "answers to rent stabilization question"){.right-img }


58% of all applications reported **"yes"** that their buildings would vacant during construction while 40% answered **"no"**.

Certainly some percentage of buildings were vacant. And other small percentage of the buildings could have had their rent-stabilized tenants relocated. None-the-less, it appears that fraud is widespread, as it's quite unbelievable that 40% of all applications for a permit over the past two years were vacant during construction.

The city does not keep any official record or tally of vacant units or property, although there is a pending bill, [Intro 226](http://legistar.council.nyc.gov/LegislationDetail.aspx?ID=3331929&GUID=85099135-6FB5-4169-945A-285EB17765BB&Options=ID|Text|&Search=226), in City Council that wound change that.

#### Question on rent stabilization

Of the 41,000 applications for likely rent-stabilized I examined, a mere 31% reported that the building contained a rent-stabilized unit. It is hard to image there to be any other explanation for this other than systematic lying on permits by landlords. Unlike vacancy which isn't reported to other city agencies, Rent Stabilized units appear on the property tax bills.

### Finding who lied on the question on Rent-Stablized question

If a building contains rent stabilized units, an indicator will appear on their quarterly tax bill. John Krauss has done the work of extracting those rent-stabilized unit counts (see [here](https://github.com/talos/nyc-stabilization-unit-counts) for more details). We can find out which landlords told the Department of Building something different from what they reported to the Department of Finance (DOF).

I looked for buildings that had registered rent-stabilized units with the Department of Finance and compared them with how the answered the questions on the PW1. 

Over half of all submitted applications for 25,139 (for 10,486 unique tax lots) appeared to have lied on their department of buildings permits.

### In summary, over 10,000 landlords improperly filled over 25,000 job applications with the department of buildings over past 2 years

