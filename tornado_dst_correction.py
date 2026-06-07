import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load the data files
tornado_data = pd.read_csv('cleaned_data.csv')
county_dst_info = pd.read_csv('cleaned_counties_data.csv')
dst_dates = pd.read_csv('DST - Sheet1.csv')

# Convert date columns to datetime
tornado_data['BEGIN_DATE_TIME'] = pd.to_datetime(tornado_data['BEGIN_DATE_TIME'], format='%d-%b-%y %H:%M:%S')
tornado_data['END_DATE_TIME'] = pd.to_datetime(tornado_data['END_DATE_TIME'], format='%d-%b-%y %H:%M:%S')

# Map state names to state codes
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

# Convert state names to state codes
tornado_data['STATE_CODE'] = tornado_data['STATE'].map(state_name_to_code)

# Function to parse DST dates (format: "DD-Month")
def parse_dst_date(date_str, year):
    """Convert 'DD-Month' format to a datetime object"""
    try:
        return pd.to_datetime(f"{date_str}-{year}", format="%d-%B-%Y")
    except:
        return None

# Create a function to check if a date is in DST for a given county
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

# Apply DST correction
def correct_time_for_dst(row, dst_dates_df, county_info_df):
    """
    Correct BEGIN_DATE_TIME and END_DATE_TIME if they fall within DST period
    """
    state_code = row['STATE_CODE']
    county = row['CZ_NAME']
    begin_time = row['BEGIN_DATE_TIME']
    end_time = row['END_DATE_TIME']
    
    # Check if begin time is in DST
    if pd.notna(begin_time) and is_in_dst(begin_time, state_code, county, dst_dates_df, county_info_df):
        begin_time = begin_time + timedelta(hours=1)
    
    # Check if end time is in DST
    if pd.notna(end_time) and is_in_dst(end_time, state_code, county, dst_dates_df, county_info_df):
        end_time = end_time + timedelta(hours=1)
    
    return begin_time, end_time

# Add corrected time columns
tornado_data[['BEGIN_DATE_TIME_CORRECTED', 'END_DATE_TIME_CORRECTED']] = tornado_data.apply(
    lambda row: pd.Series(correct_time_for_dst(row, dst_dates, county_dst_info)),
    axis=1
)

# Create a flag to show which times were corrected
tornado_data['BEGIN_TIME_ADJUSTED'] = (tornado_data['BEGIN_DATE_TIME'] != tornado_data['BEGIN_DATE_TIME_CORRECTED'])
tornado_data['END_TIME_ADJUSTED'] = (tornado_data['END_DATE_TIME'] != tornado_data['END_DATE_TIME_CORRECTED'])

# Display results
print("Sample of corrected times:")
print(tornado_data[['STATE', 'CZ_NAME', 'BEGIN_DATE_TIME', 'BEGIN_DATE_TIME_CORRECTED', 'BEGIN_TIME_ADJUSTED',
                     'END_DATE_TIME', 'END_DATE_TIME_CORRECTED', 'END_TIME_ADJUSTED']].head(20))

# Save the corrected data
tornado_data.to_csv('cleaned_data_dst_corrected.csv', index=False)
print("\nData saved to 'cleaned_data_dst_corrected.csv'")

# Show statistics
corrected_count = (tornado_data['BEGIN_DATE_TIME'] != tornado_data['BEGIN_DATE_TIME_CORRECTED']).sum()
print(f"\nTotal rows with corrected BEGIN times: {corrected_count}")
corrected_count_end = (tornado_data['END_DATE_TIME'] != tornado_data['END_DATE_TIME_CORRECTED']).sum()
print(f"Total rows with corrected END times: {corrected_count_end}")
