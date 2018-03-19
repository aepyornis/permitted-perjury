# Report

### Landlords routinely lie on their permit applications

In order to do any kind of building construction in New York City landlords must submit a form called [PW1](http://www1.nyc.gov/assets/buildings/pdf/pw1.pdf) containing basic information about the application. At the end, there is a section called the **Property Owner's Statements and Signatures** where the property owner must certify the form and provide their contact information.

The section contains a handful of simple yes/no questions about their building. It also has a warning: "_Falsification of any statement is a misdemeanor and is punishable by a fine or imprisonment, or both_". Two of these questions are notable (paraphrased):

1) Will one or more of the units in the building be occupied during construction

2) Does the building have  "occupied housing accommodations subject to rent control or rent stabilization"

Owners must tell the department of buildings two very basic, yet crucial facts about their building: will it be vacant and is it rent stabilized?

Certainly, no one would risk **jail time** by falsifying something that can easily be proved...right?


## Data Gathering

The DOB keeps a list of all submitted jobs on NYC's open data portal. This, unfortunately, **doesn't** include information on those question. However, the answers the questions on the PW1 can found on the DOB website through the biz information system.

![](images/jobtype.png "job types"){.right-img .jobtype}

Using a list of 45,685 Tax Lots that likely contain rent-stabilized buildings and a dataset of all Department of Buildings jobs (gathered from February version of [NYCDB](https://github.com/aepyornis/nyc-db), I derived a list of 41,00 jobs active since January 2016 for rent-stabilized buildings. Due to the volume of jobs, I excluded applications for minor alternations (A3).

Of these 41,00 the vast majority are A2 applications. It does include about 1,500 A1 jobs as well as hundreds of demolition and new building applications.

These 41,000 jobs are for about 15,00 unique tax lots in the city.

The data on the questions themselves were gathered by scraping the department of buildings website over a period of few weeks in early March.

### How the landlords answered those questions

#### question on vacancy

![](images/stabilized.png "answers to rent stabilization question"){.right-img }


58% of all applications reported **"yes"** that their buildings would vacant during construction while 40% answered **"no"**.

While some percentage  of buildings could be vacant, it's quite unbelievable that 40% of all buildings application for a permit over the past two years were vacant during construction.

It's possible that some of the buildings had their rent-stabilized tennats relocated, noneless, it appears that fraud is widespread.

#### question on rent stabilization


Of the 41,000 application for buildings that are likely rent-stabilized a mere 31% reported that the building contained a rent-stabilized unit. It is hard to image there to be any other explanation for this other than systematic lying on permits by landlords.


### Finding who lied on the question on Rent-Stablized question

If a building contains rent stabilized units, an indicator will appear on their quarterly tax bill. John Krauss has done the work of extracting those rent-stabilized unit counts( see [here](https://github.com/talos/nyc-stabilization-unit-counts) for more details). We can find out which landlord one the Department of Building something different from what they reported to the Department of Finance (DOF).


I looked for buildings that had registered rent-stabilized units with the Department of Finance and found that about 25,139 jobs for unique 10,486 tax lots, over half of all submitted permits, likely lied on their department of buildings permits.

### In summary, over 10,000 landlords inproperly filled over 25,000 job applicactions with the deparment of buildings. 




