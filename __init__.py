import os
import sys
import csv
csv.field_size_limit(sys.maxint)
import urllib
import zipfile
import collections
from scipy.spatial import cKDTree as KDTree

# location of geocode data to download
GEOCODE_URL = 'http://download.geonames.org/export/dump/cities1000.zip'
GEOCODE_FILENAME = 'cities1000.txt'


def singleton(cls):
    """Singleton pattern to avoid loading class multiple times
    """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class GeocodeData:

    def __init__(self, geocode_filename='geocode.csv', country_filename='countries.csv'):
        coordinates, self.locations = self.extract(rel_path(geocode_filename))
        self.tree = KDTree(coordinates)
        self.load_countries(rel_path(country_filename))
  

    def load_countries(self, country_filename):
        """Load a map of country code to name
        """
        self.countries = {}
        for code, name in csv.reader(open(country_filename)):
            self.countries[code] = name


    def query(self, coordinates):
        """Find closest match to this list of coordinates
        """
        try:
            distances, indices = self.tree.query(coordinates, k=1)
        except ValueError as e:
            print 'Unable to parse coordinates:', coordinates
            raise e
        else:
            results = [self.locations[index] for index in indices]
            for result in results:
                result['country'] = self.countries.get(result['country_code'], '')
            return results


    def download(self):
        """Download geocode file
        """
        local_filename = abs_path(os.path.basename(GEOCODE_URL))
        if not os.path.exists(local_filename):
            print 'Downloading:', GEOCODE_URL
            urllib.urlretrieve(GEOCODE_URL, local_filename)
        return local_filename


    def extract(self, local_filename):
        """Extract geocode data from zip
        """
        if os.path.exists(local_filename):
            # open compact CSV
            rows = csv.reader(open(local_filename))
        else:
            if not os.path.exists(GEOCODE_FILENAME):
                local_filename = self.download()
                z = zipfile.ZipFile(open(local_filename))
                print 'Extracting:', GEOCODE_FILENAME
                open(GEOCODE_FILENAME, 'w').write(z.read(GEOCODE_FILENAME))

            # extract coordinates into more compact CSV for faster loading
            writer = csv.writer(open(local_filename, 'w'))
            rows = []
            for row in csv.reader(open(GEOCODE_FILENAME), delimiter='\t'):
                latitude, longitude = row[4:6]
                country_code = row[8]
                if latitude and longitude and country_code:
                    city = row[1]
                    row = latitude, longitude, country_code, city
                    writer.writerow(row)
                    rows.append(row)

        # load a list of known coordinates and corresponding locations
        coordinates, locations = [], []
        for latitude, longitude, country_code, city in rows:
            coordinates.append((latitude, longitude))
            locations.append(dict(country_code=country_code, city=city))
        return coordinates, locations


def rel_path(filename):
    """Return the path of this filename relative to the current script
    """
    return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)


def get(coordinate):
    """Search for closest known location to this coordinate
    """
    gd = GeocodeData()
    return gd.query([coordinate])[0]

def search(coordinates):
    """Search for closest known locations to these coordinates
    """
    gd = GeocodeData()
    return gd.query(coordinates)


if __name__ == '__main__':
    # test some coordinate lookups
    city1 = (-37.81, 144.96)
    city2 = (31.76, 35.21)
    print get(city1)
    print search([city1, city2])
