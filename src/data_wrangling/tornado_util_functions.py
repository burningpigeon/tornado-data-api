import re
import pandas as pd
from datetime import timedelta

print("tornado_util_functions loaded...")

# State name to code mapping
state_name_to_code = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC"
}

def state_id_to_name(state_id):
    """
    Changes state_id to state name
    """
    if not isinstance(state_id, str):
        return state_id
    
    states = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming",
        "DC": "District of Columbia"
    }
    return states.get(state_id.upper(), "Unknown State")

def capitalize_words(input_string):
    """
    Capitalizes the first letter in each word of a phrase
    """
    if not isinstance(input_string, str) or not input_string:
        return input_string
    return input_string.title()

def clean_text(text):
    """
    Cleans and normalizes tornado event text.

    - Removes unwanted characters (|, �)
    - Standardizes 'mph'
    - Collapses whitespace
    - Returns empty string for non-text values
    """

    if not isinstance(text, str):
        return ""

    # Remove unwanted characters
    text = re.sub(r"[|�]", "", text)

    # Normalize
    text = text.replace("m.p.h.", "mph")
    text = text.replace("m.p.h", "mph")
    text = text.replace("MPH","mph")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text

regex_patterns = [

    # wind ranges like "85 to 95 mph"
    ("range", r'(\d{2,3})\s*(?:to|-)\s*(\d{2,3})\s*mph'),

    # maximum wind speed statements
    ("max_wind_speed",
     r'max(?:imum)? wind speed (?:was|were)?\s*(?:estimated\s*)?(?:at|near|around)?\s*(\d{2,3})\s*mph'),

    # maximum estimated winds
    ("max_estimated_winds",
     r'max(?:imum)? estimated winds?\s*(?:were|was|at|near|around|of)?\s*(\d{2,3})\s*mph'),

    # maximum winds estimated
    ("maximum_winds_estimated",
     r'max(?:imum)? winds?\s*(?:were\s*)?estimated\s*(?:at|near|around|to be)?\s*(\d{2,3})\s*mph'),

    # estimated maximum winds
    ("estimated_max_winds",
     r'estimated max(?:imum)? winds?\s*(?:at|near|around|of)?\s*(\d{2,3})\s*mph'),

    # estimated peak winds
    ("estimated_peak_winds",
     r'estimated peak winds?\s*(?:were|of|at|near|around)?\s*(\d{2,3})\s*mph'),

    # peak winds estimated
    ("peak_winds_estimated",
     r'peak winds?\s*(?:are\s*)?estimated\s*(?:to be|at|near|around)?\s*(\d{2,3})\s*mph'),

    # peak winds of X mph
    ("peak_winds_of",
     r'peak winds?\s*(?:of|were)?\s*(\d{2,3})\s*mph'),

    # peak winds in location were X mph
    ("peak_winds_location",
     r'peak winds?\s+(?:in|at)\s+[a-z\s]+were\s*(\d{2,3})\s*mph'),

    # general winds estimated
    ("winds_estimated",
     r'winds?\s*(?:were\s*)?estimated\s*(?:to be|at|near|around)?\s*(\d{2,3})\s*mph'),

    # simple winds statement
    ("winds_simple",
     r'winds?\s*(?:were|was|are)?\s*(\d{2,3})\s*mph'),

    # wind speeds of X mph (general)
    ("wind_speeds_of",
     r'wind speeds?\s+(?:of|at|near|around)?\s*(\d{2,3})\s*mph'),

    # max wind speeds of X mph
    ("max_wind_speeds_of",
     r'max(?:imum)? wind speeds?\s+(?:of|at|near|around)?\s*(\d{2,3})\s*mph'),

    # peak winds of at least X mph
    ("peak_winds_at_least",
     r'peak winds?\s+of\s+at\s+least\s*(\d{2,3})\s*mph'),

    # maximum estimated wind speeds in location were X mph
    ("max_estimated_winds_location",
     r'max(?:imum)? estimated winds?\s+(?:in|at)\s+[a-z\s]+were\s*(\d{2,3})\s*mph'),

    # estimated maximum wind speeds in location were X mph
    ("estimated_max_winds_location",
     r'estimated max(?:imum)? winds?\s+(?:in|at)\s+[a-z\s]+were\s*(\d{2,3})\s*mph'),

    # maximum estimated wind speeds (with optional location)
    ("max_estimated_wind_speeds",
     r'max(?:imum)? estimated winds?\s+(?:in|at|are)?\s*(?:[a-z\s]*?\s+)?(?:are|were)?\s*(?:around|of)?\s*(\d{2,3})\s*mph'),

    # peak wind gusts were X mph
    ("peak_wind_gusts",
     r'peak wind gusts?\s+(?:were|are)?\s*(\d{2,3})\s*mph'),

    # tornado with maximum winds
    ("tornado_max_winds",
     r'tornado .*? max(?:imum)? winds?\s*(?:of|at|near|around)?\s*(\d{2,3})\s*mph'),

]

def regex_extract(text, ef_rating):
    speeds = []
    ranges = []
    for label, pattern in regex_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                # Handle range pattern (tuple like ('85','95'))
                if label == "range":
                    min_speed = int(match[0])
                    max_speed = int(match[1])
                    ranges.append(f"{min_speed}-{max_speed} mph")
                    speeds.append(max_speed)  # also track max for comparison
                else:
                    if isinstance(match, tuple):
                        speeds.append(int(match[0]))
                    else:
                        speeds.append(int(match))
            except:
                continue
    
    # If we found a range, return it as a string
    if ranges:
        return ranges[0]
    
    # TO DO: AI step if I want to
    
    # Otherwise return the max speed found
    if not speeds:
        if ef_rating == "EFU":
            return "Unknown"
        elif ef_rating == "EF0":
            return "65-85 mph"
        elif ef_rating == "EF1":
            return "86-110 mph"
        elif ef_rating == "EF2":
            return "111-135 mph"
        elif ef_rating =="EF3":
            return "136-165 mph"
        elif ef_rating == "EF4":
            return "166-200 mph"
        elif ef_rating =="EF5":
            return "200+ mph"
        else:
            return "Unknown"
    return f"{max(speeds)} mph"

def parse_dst_date(date_str, year):
    """
    Convert 'DD-Month' format to a datetime object
    """
    try:
        return pd.to_datetime(f"{date_str}-{year}", format="%d-%B-%Y")
    except:
        return None

def is_in_dst(event_date, state, county_name, dst_dates_df, county_info_df):
    """
    Check if an event date falls within DST for a specific county.
    Returns True if in DST, False if not.
    """
    # Get county DST info
    county_row = county_info_df[(county_info_df['STATE'] == state) & 
                                 (county_info_df['COUNTYNAME'] == county_name)]
    
    if county_row.empty:
        return False
    
    dst_status = county_row['DST'].values[0]
    
    # If county doesn't observe DST, return False
    if not dst_status:
        return False
    
    # Get the year from the event date
    year = event_date.year
    
    # Find DST dates for this year
    dst_year_row = dst_dates_df[dst_dates_df['Year'] == year]
    
    if dst_year_row.empty:
        return False
    
    dst_start_str = dst_year_row['DST Start'].values[0]
    dst_end_str = dst_year_row['DST End'].values[0]
    
    # Parse the DST start and end dates
    dst_start = parse_dst_date(dst_start_str, year)
    dst_end = parse_dst_date(dst_end_str, year)
    
    if dst_start is None or dst_end is None:
        return False
    
    # Check if event date is between DST start and end (exclusive of end date)
    return dst_start <= event_date < dst_end

def correct_time_for_dst(row, dst_dates_df, county_info_df):
    """
    Correct BEGIN_DATE_TIME and END_DATE_TIME if they fall within DST period
    """
    state_code = row['state_code']
    county = row['county_name']
    begin_time = row['begin_date_time']
    end_time = row['end_date_time']
    
    # Check if begin time is in DST
    if pd.notna(begin_time) and is_in_dst(begin_time, state_code, county, dst_dates_df, county_info_df):
        begin_time = begin_time + timedelta(hours=1)
    
    # Check if end time is in DST
    if pd.notna(end_time) and is_in_dst(end_time, state_code, county, dst_dates_df, county_info_df):
        end_time = end_time + timedelta(hours=1)
    
    return begin_time, end_time
    
