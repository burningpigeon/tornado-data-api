import pandas as pd
import numpy as np
import re
from . import tornado_util_functions as utils

def clean_tornado_details(storm_details_csv, county_dst_info=None, dst_dates=None):
    tornado_details = storm_details_csv[storm_details_csv["EVENT_TYPE"] == "Tornado"]

    tornado_details = tornado_details[[
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

    tornado_details.insert(loc=17, column='max_windspeed', value=np.nan)

    tornado_details["STATE"] = tornado_details["STATE"].apply(utils.capitalize_words)
    tornado_details["CZ_NAME"] = tornado_details["CZ_NAME"].apply(utils.capitalize_words)
    tornado_details["TOR_OTHER_CZ_NAME"] = tornado_details["TOR_OTHER_CZ_NAME"].apply(utils.capitalize_words)
    tornado_details["TOR_OTHER_CZ_STATE"] = tornado_details["TOR_OTHER_CZ_STATE"].apply(utils.state_id_to_name)

    tornado_details["EPISODE_NARRATIVE"] = tornado_details["EPISODE_NARRATIVE"].apply(utils.clean_text)
    tornado_details["EVENT_NARRATIVE"] = tornado_details["EVENT_NARRATIVE"].apply(utils.clean_text)
    tornado_details["max_windspeed"] = tornado_details.apply(lambda row: utils.regex_extract(row["EVENT_NARRATIVE"], row["TOR_F_SCALE"]), axis=1)

    tornado_details['BEGIN_DATE_TIME'] = pd.to_datetime(tornado_details['BEGIN_DATE_TIME'], format='%d-%b-%y %H:%M:%S')
    tornado_details['END_DATE_TIME'] = pd.to_datetime(tornado_details['END_DATE_TIME'], format='%d-%b-%y %H:%M:%S')

    tornado_details.rename(columns={
        'EPISODE_ID': 'episode_id',
        'EVENT_ID': 'event_id',
        'STATE': 'state',
        'CZ_FIPS': 'county_fips',
        'CZ_NAME': 'county_name',
        'WFO': 'wfo',
        'BEGIN_DATE_TIME': 'begin_date_time',
        'CZ_TIMEZONE': 'county_timezone',
        'END_DATE_TIME': 'end_date_time',
        'INJURIES_INDIRECT': 'injuries_indirect',
        'INJURIES_DIRECT': 'injuries_direct',
        'DEATHS_DIRECT': 'deaths_direct',
        'DEATHS_INDIRECT': 'deaths_indirect',
        'DAMAGE_PROPERTY': 'property_damage',
        'DAMAGE_CROPS': 'crop_damage',
        'SOURCE': 'source',
        'TOR_F_SCALE': 'tornado_rating',
        'TOR_LENGTH': 'tornado_length',
        'TOR_WIDTH': 'tornado_max_width',
        'TOR_OTHER_WFO': 'other_wfos',
        'TOR_OTHER_CZ_STATE': 'other_states',
        'TOR_OTHER_CZ_FIPS': 'other_counties_fips',
        'TOR_OTHER_CZ_NAME': 'other_counties_names',
        'BEGIN_LAT': 'begin_latitude',
        'BEGIN_LON': 'begin_longitude',
        'END_LAT': 'end_latitude',
        'END_LON': 'end_longitude',
        'EPISODE_NARRATIVE': 'episode_narrative',
        'EVENT_NARRATIVE': 'event_narrative'
    }, inplace=True)

    if county_dst_info is not None and dst_dates is not None:
        tornado_details['state_code'] = tornado_details['state'].map(utils.state_name_to_code)
        
        tornado_details[['begin_date_time_corrected', 'end_date_time_corrected']] = tornado_details.apply(
            lambda row: pd.Series(utils.correct_time_for_dst(row, dst_dates, county_dst_info)),
            axis=1
        )
        
        tornado_details['begin_time_adjusted'] = (tornado_details['begin_date_time'] != tornado_details['begin_date_time_corrected'])
        tornado_details['end_time_adjusted'] = (tornado_details['end_date_time'] != tornado_details['end_date_time_corrected'])
    return tornado_details
