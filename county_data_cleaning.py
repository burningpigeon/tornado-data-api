import pandas as pd 
import numpy as np 
import re
import tornado_util_functions as utils

counties = pd.read_csv('c_16ap26.csv')

# Filter to include only the 50 states and DC (exclude territories)
us_states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
]
counties = counties[counties["STATE"].isin(us_states)]

counties = counties[[
    "STATE",
    "COUNTYNAME",
    "CWA",
    "TIME_ZONE"
]]

counties.insert(loc=4, column='DST', value=True)
counties.insert(loc=5, column='Standard Time', value=np.nan)
counties.insert(loc=6, column='Daylight Time', value=np.nan)

# Mapping of initials to full timezone names
timezone_map = {
    "V": "Atlantic Time",
    "E": "Eastern Time",
    "C": "Central Time",
    "M": "Mountain Time",
    "m": "Mountain Standard Time",# No DST
    "P": "Pacific Time",
    "A": "Alaska Time",
    "H": "Hawaii-Aleutian Standard", # No DST
    "h": "Hawaii-Aleutian Time", # yes DST
}

timezone_standard_time_map = {
    "Atlantic Time": "UTC-4",
    "Eastern Time": "UTC-5",
    "Central Time": "UTC-6",
    "Mountain Time": "UTC-7",
    "Pacific Time": "UTC-8",
    "Alaska Time": "UTC-9",
    "Hawaii-Aleutian Time": "UTC-10"
}

timezone_daylight_time_map = {
    "Atlantic Time": "UTC-3",
    "Eastern Time": "UTC-4",
    "Central Time": "UTC-5",
    "Mountain Time": "UTC-6",
    "Pacific Time": "UTC-7",
    "Alaska Time": "UTC-8",
    "Hawaii-Aleutian Time": "UTC-9"
}

counties["TIME_ZONE"] = counties["TIME_ZONE"].replace(timezone_map)

# Set DST to False for timezones that don't observe daylight saving time
counties.loc[counties["TIME_ZONE"].isin(["Mountain Standard Time", "Hawaii-Aleutian Standard"]), "DST"] = False

# Apply timezone mappings to Standard Time and Daylight Time columns
counties["Standard Time"] = counties["TIME_ZONE"].map(timezone_standard_time_map)
counties["Daylight Time"] = counties["TIME_ZONE"].map(timezone_daylight_time_map)

print(counties.head(5))

counties.to_csv('cleaned_counties_data.csv', index=False)