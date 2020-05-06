# Libraries

# HTTP and URL Libraries
import urllib3  # URL request library
import certifi  # Certifications library for secure url requests

from datetime import datetime # Datetime data manipulation Library

# Path Libraries
from pathlib import Path  # Path manipulation
import shutil  # high-level operations on files and collections of files

# System Libraries
import os  # OS library

# Data science Libraries
import pandas as pd  # Data import, manipulation and processing


# Functions

def get_date():
    return datetime.today().strftime('%Y-%m-%d')

def get_csv_in_html(html):
    return "https://covid19.isciii.es/" + html.rsplit('" target="_blank">aqu')[0].rsplit('Si desea descargarse los datos pulse <a href="')[1]


def get_spain_data(url, dest_folder):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    r = http.request('GET', url, preload_content=False)
    html = r.data.decode('utf-8')
    csv_url = get_csv_in_html(html)
    r.release_conn()

    print(csv_url)

    r = http.request('GET', csv_url, preload_content=False)
    with open(dest_folder / 'spain_covid19_data_{}.csv'.format(get_date()), "wb") as out:
        shutil.copyfileobj(r, out)
    r.release_conn()

def read_data():
    pass

# Variables

url = "https://covid19.isciii.es/"
data_base_folder = Path("../data")
spain_data_folder = data_base_folder / "spain_isciii"

# Execution

get_spain_data(url, spain_data_folder)