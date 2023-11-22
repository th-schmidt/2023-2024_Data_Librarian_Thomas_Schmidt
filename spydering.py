# -*- coding: utf-8 -*-
import random
import urllib.request
import json
import pandas as pd

from random import randint


# Listing
list = [1, 3, 4, 6]

for l in list:
    er = l * 2
    
# Strings
name = 'Thomas'
print(name.replace('m', 'S'))

# Nums
num = 1.25 / 27
num = 23

# Dicts
new_dict = {
    'key1': 'Hubbard',
    'key2': 'Salmon',
    'key3': 'Pink'
    }

key_temp = new_dict['key1']

# Set
my_set = {5.2, 6.2, 4.2}

# Tuple
tups = (2.34334, 1.29393)

# Random Num
rnum = randint(1, 10000)
rnum2 = random.choice([3, 23, 2332, 'ad', 'aba'])


base_url = "https://api.datacite.org/application/vnd.datacite.datacite+json/"

dois = ["10.6084/m9.figshare.155613",
        "10.6084/m9.figshare.153821.v1",
        "10.7490/f1000research.1115338.1",
        "10.5281/zenodo.2599866"]

for doi in dois:
    # Parse full_url
    doi_json_dataset = urllib.request.urlopen(base_url + doi).read()
    doi_dataset = json.loads(doi_json_dataset)
    
    # Print doi, title, publisher
    print(f"DOI: {doi_dataset['doi']}")
    print(f"Title: {doi_dataset['titles'][0]['title']}")
    print(f"Publisher: {doi_dataset['publisher']}")
    print()

