# -*- coding: utf-8 -*-

import csv
import gzip
import io
import json
import logging
import os
from scipy.spatial import cKDTree as KDTree
import sys
import zipfile
from urllib.request import urlopen

if sys.platform == "win32":
    csv.field_size_limit(2**31 - 1)
else:
    csv.field_size_limit(sys.maxsize)

# location of geocode data to download
GEOCODE_URL = "http://download.geonames.org/export/dump/cities1000.zip"
GEOCODE_FILENAME = "cities1000.txt"
STATE_CODE_URL = "http://download.geonames.org/export/dump/admin1CodesASCII.txt"
COUNTY_CODE_URL = "https://download.geonames.org/export/dump/admin2Codes.txt"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = cls, args
        if key not in cls._instances:
            Singleton._instances[key] = super(Singleton, cls).__call__(*args, **kwargs)
        return Singleton._instances[key]


class GeocodeData(metaclass=Singleton):
    def __init__(
        self,
        min_population=0,
        geocode_filename="geocode.gz",
        country_filename="countries.csv",
    ):
        def rel_path(filename):
            return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)

        # note: remove geocode_filename to get updated data
        self._locations = self._extract(
            rel_path(geocode_filename), min_population
        )
        coordinates = [(loc["latitude"], loc["longitude"]) for loc in self._locations]
        self._tree = KDTree(coordinates)
        self._load_countries(rel_path(country_filename))

    def _load_countries(self, country_filename):
        """Load a map of country code to name"""
        self._countries = {}
        with open(country_filename, "r", encoding="utf-8") as handler:
            for code, name in csv.reader(handler):
                self._countries[code] = name

    def query(self, coordinates):
        """Find closest match to this list of coordinates"""
        try:
            distances, indices = self._tree.query(coordinates, k=1)
        except ValueError as e:
            logging.info("Unable to parse coordinates: {}".format(coordinates))
            raise e
        else:
            results = [self._locations[index] for index in indices]
            for result in results:
                result["country"] = self._countries.get(result["country_code"], "")
            return results

    def _download_geocode(self):
        """Download geocode data from http://download.geonames.org/export/dump/"""

        def geocode_csv_reader(data):
            return csv.reader(data.decode("utf-8").splitlines(), delimiter="\t")

        #with zipfile.ZipFile(open('cities1000.zip', 'rb')) as geocode_zipfile:
        with zipfile.ZipFile(
            io.BytesIO(urlopen(GEOCODE_URL).read())
        ) as geocode_zipfile:
            geocode_reader = geocode_csv_reader(geocode_zipfile.read(GEOCODE_FILENAME))

        state_reader = geocode_csv_reader(urlopen(STATE_CODE_URL).read())
        county_reader = geocode_csv_reader(urlopen(COUNTY_CODE_URL).read())
        return (
            geocode_reader,
            self._gen_code_map(state_reader),
            self._gen_code_map(county_reader),
        )

    def _gen_code_map(self, state_reader):
        """Build a map of code data from geonames"""
        state_code_map = {}
        for row in state_reader:
            state_code_map[row[0]] = row[1]
        return state_code_map

    def _extract(self, local_filename, min_population):
        """Extract locations from geonames and store locally"""
        if os.path.exists(local_filename):
            with gzip.open(local_filename) as gz:
                locations = json.loads(gz.read())
        else:
            print('Downloading geocode data')
            geocode_reader, state_code_map, county_code_map = self._download_geocode()

            # extract coordinates into more compact JSON for faster loading
            locations = []
            for row in geocode_reader:
                latitude = float(row[4])
                longitude = float(row[5])
                country_code = row[8]
                if latitude and longitude and country_code:
                    city = row[1]
                    state_code = row[8] + "." + row[10]
                    state = state_code_map.get(state_code)
                    county_code = state_code + "." + row[11]
                    county = county_code_map.get(county_code)
                    population = int(row[14])
                    loc = {
                        "country_code": country_code,
                        "city": city,
                        "latitude": latitude,
                        "longitude": longitude,
                        "population": population,
                    }
                    if state:
                        loc["state"] = state
                    if county and county != city:
                        loc["county"] = county
                    locations.append(loc)

            with gzip.open(local_filename, 'w') as gz:
                gz.write(json.dumps(locations, separators=(',', ':')).encode('utf-8'))

        if min_population > 0:
            locations = [
                loc for loc in locations if loc["population"] >= min_population
            ]

        return locations


def get(coordinate, min_population=0):
    """Search for closest known location to this lat/lng coordinate"""
    return GeocodeData(min_population).query([coordinate])[0]


def search(coordinates, min_population=0):
    """Search for closest known location at each of given lat/lng coordinates"""
    return GeocodeData(min_population).query(coordinates)


if __name__ == "__main__":
    # test some coordinate lookups
    city1 = -37.81, 144.96
    city2 = -38.3401, 144.7365
    city3 = 40.71, -74.00
    print(get(city1))
    print(get(city2))
    print(search([city1, city3], 100000))
