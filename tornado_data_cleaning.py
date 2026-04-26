import pandas as pd 
import numpy as np 
import re
import tornado_util_functions as utils

storm_details_2025 = pd.read_csv('StormEvents_details-ftp_v1.0_d2025_c20260323.csv')

tornado_details_2025 = storm_details_2025[storm_details_2025["EVENT_TYPE"] == "Tornado"]

tornado_details_2025 = tornado_details_2025[[
    "EPISODE_ID", #ID assigned by NWS to denote the storm episode; links to location & fatality files
    "EVENT_ID", #ID assigned by NWS to note a single, small part that goes into a specific storm episode; links to location & fatality files
    "STATE", # The state name where the event occurred
    "CZ_FIPS", # The county FIPS number, a unique number assigned to the country by NIST or NWS Forecast Zone Number
    "CZ_NAME", # The name of the County
    "WFO", # NWS Forecast Office's area of responsibility (County Warning Area) in which the event occurred
    "BEGIN_DATE_TIME", # Date and time the event began: MM/DD/YYYY 24 Hour Time AM/PM
    "CZ_TIMEZONE", # Time Zone for the County
    "END_DATE_TIME", # Date and time the event ended: MM/DD/YYYY 24 Hour Time AM/PM
    "INJURIES_DIRECT", # The number of injuries directly related to the weather event
    "INJURIES_INDIRECT", # The number of injuries indirectly related to the weather event
    "DEATHS_DIRECT", # The number of deaths directly related to the weather event
    "DEATHS_INDIRECT", # The number of deaths indirectly related to the weather event
    "DAMAGE_PROPERTY", # The estimated amount of damage to property incurred by the weather event
    "DAMAGE_CROPS", # The estimated amount of damage to crop incurred by the weather event
    "SOURCE", # The source reporting the weather event (Trained Spotter, Storm Chaser, Law Enforcement etc.)
    "TOR_F_SCALE", # The F or EF Scale that describes the strength of the tornado based on the amount and type of damange caused by the tornado
    "TOR_LENGTH", # The length of the tornado or tornado segment while on the ground
    "TOR_WIDTH", # Width of the tornado or tornado segment while on the ground
    "TOR_OTHER_WFO", # Indicates the continuation of a Tornado as it crossed from one NWS Forecast Office to another. The subsequent WFO identifier is provided within this field
    "TOR_OTHER_CZ_STATE", # The two character representation for the state name of the continuing tornado segment as it crossed from one county or zone to another. The subsequent 2-Letter State ID is provide.
    "TOR_OTHER_CZ_FIPS", # The FIPS number of the county entered by the continuing tornado segment as it crossed from one county to another.  The subsequent FIPS number is provided within this field. 
    "TOR_OTHER_CZ_NAME", # The FIPS name of the county entered by the continuing tornado segment as it crossed from one county to another.  The subsequent county or zone name is provided within this field in ALL CAPS. 
    "BEGIN_LAT", # The latitude in decimal degrees of the begin point of the event or damage path. 
    "BEGIN_LON", # The longitude in decimal degrees of the begin point of the event or damage path. 
    "END_LAT", # The latitude in decimal degrees of the end point of the event or damage path.
    "END_LON", # The longitude in decimal degrees of the end point of the event or damage path.
    "EPISODE_NARRATIVE", # The episode narrative depicting the general nature and overall activity of the episode.  The narrative is created by NWS.
    "EVENT_NARRATIVE" # The event narrative provides more specific details of the individual event. The event narrative is provided by NWS
]]

tornado_details_2025.insert(loc=2, column='TORNADO_OUTBREAK', value=np.nan)
tornado_details_2025.insert(loc=17, column='MAX_WINDSPEED', value=np.nan)
tornado_details_2025.to_csv('cleaned_data.csv', index=False)

storm_fatalities = pd.read_csv('StormEvents_fatalities-ftp_v1.0_d2025_c20260323.csv')

# Filter fatalities to only include rows with EVENT_IDs that match tornado_details_2025
tornado_fatalities_2025 = storm_fatalities[storm_fatalities['EVENT_ID'].isin(tornado_details_2025['EVENT_ID'])]

tornado_fatalities_2025 = tornado_fatalities_2025[[
    "EVENT_ID", #ID assigned by NWS to note a single, small part that goes into a specific storm episode; links to location & fatality files
    "FATALITY_TYPE", # Whether the death was direct, indirect or unknown
    "FATALITY_DATE", # the date the fatality happened.
    "FATALITY_AGE", # the age of the victim
    "FATALITY_SEX", # The gender of the victim
    "FATALITY_LOCATION" # Where the fatality occured (Permanent Home, Mobile Home, Vehicle etc)
]]

tornado_fatalities_2025["FATALITY_AGE"] = tornado_fatalities_2025["FATALITY_AGE"].fillna("Unknown")
tornado_fatalities_2025["FATALITY_AGE"] = tornado_fatalities_2025["FATALITY_AGE"].apply(lambda x: int(x) if isinstance(x, (int, float)) and x != "Unknown" else x)
tornado_fatalities_2025["FATALITY_DATE"] = tornado_fatalities_2025["FATALITY_DATE"].str[:10]
tornado_fatalities_2025["FATALITY_TYPE"] = tornado_fatalities_2025["FATALITY_TYPE"].apply(lambda x: "Direct" if x == "D" else ("Indirect" if x == "I" else "Unknown"))
tornado_fatalities_2025["FATALITY_SEX"] = tornado_fatalities_2025["FATALITY_SEX"].fillna("Unknown")

tornado_details_2025["STATE"] = tornado_details_2025["STATE"].apply(utils.capitalize_words)
tornado_details_2025["CZ_NAME"] = tornado_details_2025["CZ_NAME"].apply(utils.capitalize_words)
tornado_details_2025["TOR_OTHER_CZ_NAME"] = tornado_details_2025["TOR_OTHER_CZ_NAME"].apply(utils.capitalize_words)
tornado_details_2025["TOR_OTHER_CZ_STATE"] = tornado_details_2025["TOR_OTHER_CZ_STATE"].apply(utils.state_id_to_name)

tornado_details_2025["EPISODE_NARRATIVE"] = tornado_details_2025["EPISODE_NARRATIVE"].apply(utils.clean_text)
tornado_details_2025["EVENT_NARRATIVE"] = tornado_details_2025["EVENT_NARRATIVE"].apply(utils.clean_text)
tornado_details_2025["MAX_WINDSPEED"] = tornado_details_2025.apply(lambda row: utils.regex_extract(row["EVENT_NARRATIVE"], row["TOR_F_SCALE"]), axis=1)

tornado_details_2025.to_csv('cleaned_data.csv', index=False)
print(tornado_fatalities_2025.head(50))