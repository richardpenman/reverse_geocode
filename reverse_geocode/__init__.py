# -*- coding: utf-8 -*-

import csv
import io
import json
import logging
import os
from scipy.spatial import cKDTree as KDTree
import sys
if sys.platform == "win32":
    csv.field_size_limit(2**31 - 1)
else:
    csv.field_size_limit(sys.maxsize)
from urllib.request import urlopen
import zipfile

# location of geocode data to download
GEOCODE_URL = "http://download.geonames.org/export/dump/cities1000.zip"
GEOCODE_FILENAME = "cities1000.txt"
STATE_CODE_URL = "http://download.geonames.org/export/dump/admin1CodesASCII.txt"


def singleton(cls):
    """Singleton pattern to avoid loading class multiple times"""
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton
class GeocodeData:
    def __init__(self, geocode_filename="geocode.json", country_filename="countries.csv"):
        def rel_path(filename):
            return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)
        # note: remove geocode_filename to get updated data
        coordinates, self.__locations = self.__extract(rel_path(geocode_filename))
        self.__tree = KDTree(coordinates)
        self.__load_countries(rel_path(country_filename))


    def __load_countries(self, country_filename):
        """Load a map of country code to name"""
        self.__countries = {}
        with open(country_filename, "r", encoding="utf-8") as handler:
            for code, name in csv.reader(handler):
                self.__countries[code] = name


    def query(self, coordinates):
        """Find closest match to this list of coordinates"""
        try:
            distances, indices = self.__tree.query(coordinates, k=1)
        except ValueError as e:
            logging.info("Unable to parse coordinates: {}".format(coordinates))
            raise e
        else:
            results = [self.__locations[index] for index in indices]
            for result in results:
                result["country"] = self.__countries.get(result["country_code"], "")
            return results


    def __download_geocode(self):
        """Download geocode data from http://download.geonames.org/export/dump/
        """
        def geocode_csv_reader(data):
            return csv.reader(data.decode('utf-8').splitlines(), delimiter="\t")

        geocode_response = urlopen(GEOCODE_URL)
        geocode_zipfile = zipfile.ZipFile(io.BytesIO(geocode_response.read()))
        geocode_reader = geocode_csv_reader(geocode_zipfile.read(GEOCODE_FILENAME))

        state_response = urlopen(STATE_CODE_URL)
        state_reader = geocode_csv_reader(state_response.read())
        return geocode_reader, self.__gen_state_code_map(state_reader)


    def __gen_state_code_map(self, state_reader):
        """Build a map of state code data from
        http://download.geonames.org/export/dump/admin1CodesASCII.txt
        """
        state_code_map = {}
        for row in state_reader:
            state_code_map[row[0]] = row[1]
        return state_code_map


    def __extract(self, local_filename):
        """Extract geocode data from zip
        """
        if os.path.exists(local_filename):
            # open compact JSON
            rows = json.load(open(local_filename, "r", encoding="utf-8"))
        else:
            geocode_reader, state_code_map = self.__download_geocode()

            # extract coordinates into more compact JSON for faster loading
            rows = []
            for row in geocode_reader:
                latitude, longitude = row[4:6]
                country_code = row[8]
                if latitude and longitude and country_code:
                    city = row[1]
                    state = state_code_map.get(row[8] + '.' + row[10])
                    row = latitude, longitude, country_code, city, state
                    rows.append(row)
            json.dump(rows, open(local_filename, "w", encoding="utf-8"))

        # load a list of known coordinates and corresponding __locations
        coordinates, __locations = [], []
        for latitude, longitude, country_code, city, state in rows:
            coordinates.append((latitude, longitude))
            __locations.append(dict(country_code=country_code, city=city, state=state))
        return coordinates, __locations


def get(coordinate):
    """Search for closest known location to this lat/lng coordinate"""
    gd = GeocodeData()
    return gd.query([coordinate])[0]


def search(coordinates):
    """Search for closest known locations to this list of lat/lng coordinates"""
    gd = GeocodeData()
    return gd.query(coordinates)


if __name__ == "__main__":
    # test some coordinate lookups
    city1 = -37.81, 144.96
    city2 = 40.71427000, -74.00597000
    print(get(city1))
    print(search([city1, city2]))
