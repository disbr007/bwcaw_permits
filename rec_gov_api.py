# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 13:47:42 2019

@author: disbr007
"""

import requests
from pprint import pprint
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import json
import os

"""
BWCAW Facility ID: 233396
"""

def create_points(row):
    '''
    Create points from latitudes and longitudes in dataframe
    '''
    lat = row['Latitude']
    long = row['Longitude']
    point = Point(long, lat)
    
    return point


prj_path = r'C:\temp\bwcaw_webmap'

api_key = '2554475800AD4953A1CCAADF79FD2AE1'
facility_url = 'https://ridb.recreation.gov/api/v1/facilities/233396'
permit_url = 'https://ridb.recreation.gov/api/v1/facilities/233396/permitentrances?'

params = {'apikey':api_key,
          'offset':0}

print('Initial request...')
r = requests.get(permit_url, params=params)
j = r.json()
master_ep = j["RECDATA"]


## For looping through all entry points as request is limited to 50
metadata = r.json()["METADATA"]
current_count = metadata["RESULTS"]["CURRENT_COUNT"]
total_count = metadata["RESULTS"]["TOTAL_COUNT"]
offset = metadata["SEARCH_PARAMETERS"]["OFFSET"]


while current_count + offset <= total_count:
    print('Current count: {}/nOffset: {}'.format(current_count, offset))
    print('Additional request...')
    params['offset'] = offset + current_count
    r = requests.get(permit_url, params=params)
    j = r.json()
    ## Request metadata
    metadata = j["METADATA"]
    current_count = metadata["RESULTS"]["CURRENT_COUNT"]
    offset = metadata["SEARCH_PARAMETERS"]["OFFSET"]
    params['offset'] = offset
    ## Entry point data only
    ep = j["RECDATA"]
    
    final_json = {**master_ep, **ep}
    
print('Request status: {}'.format(r.status_code))

#with open(r'C:\temp\bwcaw_webmap\request.txt', 'w') as f:
#    f.write(json.dumps(r.json()))
    
df = pd.DataFrame.from_dict(final_json)
df['geometry'] = df.apply(lambda x: create_points(x))
df.to_csv(os.path.join(prj_path, 'df.csv'))
