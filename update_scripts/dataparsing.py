import urllib.request
import io
import xml.etree.ElementTree as ET
import zipfile
import numpy as np
import pandas as pd
from consts import URL
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(script_dir))


def get_data():
    z = load_from_url_in_memory(URL)
    stations_df, gas_types_df = parse_xml(z)
    return stations_df, gas_types_df


def load_from_url_in_memory(url):
    '''This function load the xml file from the url in memory after unziping it
       It assume only one file with a .xml extention is available in the zip
    '''

    with urllib.request.urlopen(url) as url:
        s = io.BytesIO(url.read())
        z = zipfile.ZipFile(s)

    return z


def parse_pdv(pdv, stations, oil_types):
    '''This function retrieve all the data available in a pdv element'''

    station = {}
    # Get attributes of the pdv
    station.update(pdv.attrib)

    # It is precised in the doc that lats and longs have to be divided by 100 000
    station['latitude'] = float(station['latitude'])/100000
    station['longitude'] = float(station['longitude'])/100000

    # Rename the id key
    station["station_id"] = station["id"]
    del station["id"]

    # Explore children, by type of children
    for element in pdv:
        if element.tag == "adresse":
            station["adress"] = element.text
        if element.tag == "ville":
            station["city"] = element.text
        if element.tag == "horaires":
            station = parse_schedules(element, station)
        if element.tag == 'prix':
            oil_types = parse_oil(element, station, oil_types)

    stations.append(station)
    return stations, oil_types


def parse_schedules(schedule_element, station):
    '''This function retrieve the schedules time for a schedule_element'''
    station["automate_24_24"] = "Yes" if schedule_element.attrib["automate-24-24"] == "1" else np.nan

    for day in schedule_element:
        day_of_week = day.attrib["nom"]
        for schedule in schedule_element:
            opening = np.nan
            closing = np.nan
            for time in schedule:
                opening = time.attrib["ouverture"]
                closing = time.attrib["fermeture"]

            station[f"{day_of_week}_opening"] = opening
            station[f"{day_of_week}_closing"] = closing

    return station


def parse_oil(oil_element, station, oil_types):
    '''This function retrieve information relative to a oil type in a station'''

    # Integrate the station_id as secondary key
    oil_type = {"station_id": station["station_id"]}

    # Add other attributes
    oil_type.update(oil_element.attrib)
    oil_type["oil_id"] = f'{oil_type["station_id"]}_{oil_type["id"]}'
    del oil_type["id"]

    # Add the oil to our list of oils
    oil_types.append(oil_type)
    return oil_types


def parse_xml(z):
    '''Parse the whole xml'''
    xml_file = [file for file in z.namelist() if file.endswith('.xml')][0]
    with z.open(xml_file, "r") as file:
        # Create the tree using xml parser
        tree = ET.parse(file)
        # Access the root node
        root = tree.getroot()

        # Initiate stations and oil_types
        stations = []
        oil_types = []

        for pdv in root:
            stations, oil_types = parse_pdv(pdv, stations, oil_types)

    stations_df = pd.DataFrame(stations)
    oil_types_df = pd.DataFrame(oil_types)

    return stations_df, oil_types_df
