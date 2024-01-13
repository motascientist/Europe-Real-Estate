# Porta Romana Real Estate

## Introduction

A friend is currently in search of houses in Italy, particularly in the "Porta Romana" area. Unfortunately, the websites he has explored do not provide information about the price per square meter (m²). To assist him in making a well-informed investment decision, I have developed a program that calculates the price per square meter based on the available data. This program aims to enhance his property search by providing an additional metric for evaluating potential investments.

## Streamlit App

Explore the [Streamlit App here](https://europe-real-estate-jxbcwmxjckth9gsfukbzdz.streamlit.app/).

## Project Structure

### Part 1: Data Scraping (scraping/scraper.py)

We will extract data from [Immobiliare.it](https://www.immobiliare.it/en/).


```Python
if __name__=='__main__':

    medaglie_d_oro = RealEstate('porta-romana-medaglie-d-oro')
    medaglie_d_oro.collect_data()
    medaglie_d_oro.DataFrame()

    cadore_montenero = RealEstate('porta-romana-cadore-montenero')
    cadore_montenero.collect_data()
    cadore_montenero.DataFrame()
```
    
### Part 2 → Data Treatment (data_treatment/treatment.py)

Perform ETL (Extract, Transform, Load) operations and prepare the data for the Streamlit app.

### Part 3 → Streamlit App (streamlit_app.py)

Ensure that **`requirements.txt`** and **`packages.txt`** are included.


**requirements.txt**

```plaintext
pandas==1.5.3
streamlit==1.26.0
yfinance==0.2.28
```
**packages.txt**

```plaintext
libssl-dev
libffi-dev
libxml2-dev
libxslt1-dev
zlib1g-dev
```
