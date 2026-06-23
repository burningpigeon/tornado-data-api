import pandas as pd
import numpy as np
import re
from . import tornado_util_functions as utils

def clean_tornado_fatalities(storm_details_csv, storm_fatalities_csv):
    tornado_fatalities = storm_fatalities_csv[storm_fatalities_csv['EVENT_ID'].isin(storm_details_csv['event_id'])]
    tornado_fatalities = tornado_fatalities[[
        "EVENT_ID", #ID assigned by NWS to note a single, small part that goes into a specific storm episode; links to location & fatality files
        "FATALITY_TYPE", # Whether the death was direct, indirect or unknown
        "FATALITY_DATE", # the date the fatality happened.
        "FATALITY_AGE", # the age of the victim
        "FATALITY_SEX", # The gender of the victim
        "FATALITY_LOCATION" # Where the fatality occured (Permanent Home, Mobile Home, Vehicle etc)
    ]]
    tornado_fatalities["FATALITY_AGE"] = tornado_fatalities["FATALITY_AGE"].fillna("Unknown")
    tornado_fatalities["FATALITY_AGE"] = tornado_fatalities["FATALITY_AGE"].apply(lambda x: int(x) if isinstance(x, (int, float)) and x != "Unknown" else x)
    tornado_fatalities["FATALITY_DATE"] = tornado_fatalities["FATALITY_DATE"].str[:10]
    tornado_fatalities["FATALITY_TYPE"] = tornado_fatalities["FATALITY_TYPE"].apply(lambda x: "Direct" if x == "D" else ("Indirect" if x == "I" else "Unknown"))
    tornado_fatalities["FATALITY_SEX"] = tornado_fatalities["FATALITY_SEX"].fillna("Unknown")

    tornado_fatalities.rename(columns={
        'EVENT_ID': 'event_id',
        'FATALITY_TYPE': 'fatality_type',
        'FATALITY_AGE': 'fatality_age',
        'FATALITY_SEX': 'fatality_sex',
        'FATALITY_LOCATION': 'fatality_location'
    }, inplace=True)
    
    return tornado_fatalities

storm_details = pd.read_csv('cleaned_data/tornado_data_cleaned.csv')
storm_fatalities = pd.read_csv('imported_data/storm_fatalities/StormEvents_fatalities-ftp_v1.0_d2025_c20260323.csv')

cleaned_data = clean_tornado_fatalities(storm_details, storm_fatalities)
print(cleaned_data.head(5))