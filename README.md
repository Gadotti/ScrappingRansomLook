This project **ScrappingRansomLook** is a simple python script to scraping results from https://www.ransomlook.io, which comes from https://github.com/RansomLook/RansomLook and based on *ransomwatch* https://github.com/joshhighet/ransomwatch

## Features
* Check new posts on https://www.ransomlook.io/recent
* Save the results in a *csv* file, only saving the new ones
* Set monitoring word tags do inhance the results
* Enable/Disable e-mail alerts based on monitoring tags
* Logs and *csv* file will be automatically created on *source* folder

## Prerequisites

#### Python 3
You can find the official download and instalation guide here > https://www.python.org/downloads/

## Requirements

The ```requirements.txt``` file should list all Python libraries that tis project depends on, and they will be installed using:

```
pip install -r requirements.txt
```

## Saving CSV File

The result will be saved and checked from ```source/breachs_posts```. Example of content:

```
2023-12-17;DSG-US.COM;clop;
2023-12-13;cms.law;lockbit3;['law']
2023-12-14;Chaney, Couch, Callaway, Carter & Associates Family Dentistry;bianlian;['law']
2023-12-17;Biomatrix LLC;medusa;
2023-12-17;ATCO Products Inc;medusa;
```