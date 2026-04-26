import re

print("tornado_util_functions loaded...")

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
    - Lowercases text
    - Standardizes 'mph'
    - Collapses whitespace
    - Returns empty string for non-text values
    """

    if not isinstance(text, str):
        return ""

    # Remove unwanted characters
    text = re.sub(r"[|�]", "", text)

    # Normalize
    # text = text.lower()
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
    
