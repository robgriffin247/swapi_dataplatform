import requests
import json
from math import ceil
import pandas as pd

def api_wan(resource, verbose=True):
    if verbose: print(f'Collect page 1 of {resource}')
    # Perform initial request; this will get the first page of data and show whether more pages exist
    response = requests.get(f'https://swapi.dev/api/{resource}')
    response_json = response.json()
    
    # Store first page of data
    response_data = [item for item in response_json['results']]
    
    # Loop through remaining pages to collect data
    number_of_pages = ceil( response_json['count'] / 10 )
    for page in range(2, number_of_pages+1):
        response = requests.get(f'https://swapi.dev/api/{resource}/?page={page}')
        response_json = response.json()
        response_data = response_data + [item for item in response_json['results']]
        if verbose: print(f'Collect page {page} of {resource}')
    
    response_df = pd.DataFrame(response_data)
    response_df.rename(columns=lambda x: x.upper(), inplace=True)


    return response_df
