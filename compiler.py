"""
Compile vATIS station files into vATIS profiles.
Each vATIS profile must exist and contain at least a defined "name" key.
The "stations" key is added or updated.
Example:
    {
        "name": "Los Angeles ARTCC (ZLA)"
    }
"""

import json
import glob

# Search for station files in all sub-folders of ./stations/
AVAILABLE_STATIONS = glob.glob("./stations/*/*.station")

# Each profile (key) has "stations" updated to those found using the search filter (value)
# Profile: Search filter
PROFILES = {
    "./vATIS-Profile-JCF.json": ['/JCF'],
    "./vATIS-Profile-L30.json": ['/L30'],
    "./vATIS-Profile-SBA.json": ['/SBA'],
    "./vATIS-Profile-SCT.json": ['/SCT'],
    "./vATIS-Profile-ZLA.json": ['KBUR', 'KLAS', 'KLAX', 'KONT', 'KPSP', 'KSAN', 'KSBA', 'KSNA',
                                 'KVNY']
}

# Exclude these airports from all profiles.
EXCLUDE_AIRPORTS = {}

def filter_available_stations():
    """Remove airports in EXCLUDE_AIRPORTS from AVAILABLE_STATIONS."""
    for index, each_station in enumerate(AVAILABLE_STATIONS):
        for each_exclude_airport in EXCLUDE_AIRPORTS:
            if each_exclude_airport in each_station:
                AVAILABLE_STATIONS.pop(index)
    return AVAILABLE_STATIONS

def build_station_list(station_filter):
    """
    Build a list of station files matching the given filter.
    
    Args:
        station_filter (list): List of substrings to match (e.g., airport codes or folder names).
        input_station_list (list): List of all available station file paths.
    
    Returns:
        output_stations (list): A list of station file paths that match the filter.
    
    Example:
        station_filter = ['/SCT']
        input_station_list = ['./stations/SCT/KLAX.station', './stations/L30/KLAS.station']
        Result = ['./stations/SCT/KLAX.station']
    """
    output_stations = []
    for each_station in AVAILABLE_STATIONS:
        for filter_item in station_filter:
            if filter_item in each_station:
                output_stations.append(each_station)
    return output_stations

def build_profile(profile_station_list, vatis_profile):
    """
    Build a vATIS profile using a list of stations

    Args:
        profile_station_list (list): A list of station files
        vatis_profile (str): A vATIS profile
    
    Example:
        profile_station_list = ['./stations/L30/KHND.station', './stations/L30/KLAS.station',
                                './stations/L30/KVGT.station']
        vatis_profile = "./vATIS-Profile-SBA.json"
    """
    merged_stations = []

    # Open each station file from input_stations (a list of files) and appends to merged_stations
    for each_station in profile_station_list:
        with open(each_station, "r", encoding="utf-8") as station_file:
            station_data = json.load(station_file)
            merged_stations.append(station_data)

    # Open and load the vATIS profile
    with open(vatis_profile, "r", encoding="utf-8") as vatis_profile_file:
        vatis_profile_data = json.load(vatis_profile_file)

    # Write merged_stations to "stations" key and save the vATIS profile
    with open(vatis_profile, "w", encoding="utf-8") as vatis_profile_file:
        vatis_profile_data["stations"] = merged_stations
        json.dump(vatis_profile_data, vatis_profile_file, indent=2)

if len(EXCLUDE_AIRPORTS) > 0:
    filter_available_stations()

for profile_path, filters in PROFILES.items():
    station_list = sorted(build_station_list(filters))
    build_profile(station_list, profile_path)
