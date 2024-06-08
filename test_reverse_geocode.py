import reverse_geocode
import unittest


class TestBuiltwith(unittest.TestCase):
    def test_get(self):
        coordinate = -37.81, 144.96
        results = reverse_geocode.get(coordinate)
        self.assertEqual(
            results,
            {"city": "Melbourne", "country_code": "AU", "country": "Australia", "state": "Victoria"}
        )

    def test_search(self):
        coordinates = (-37.81, 144.96), (40.71427000, -74.00597000)
        results = reverse_geocode.search(coordinates)
        self.assertEqual(
            results,
            [
                {"city": "Melbourne", "country_code": "AU", "country": "Australia", "state": "Victoria"},
                {"city": "New York City", "country_code": "US", "country": "United States", "state": "New York"},
            ],
        )

    def test_population(self):
        # a coordinate near NYC
        nyc_coordinate = 40.71, -74.00
        # try searching for NYC with all data and get a nearby smaller suburb
        all_cities_result = reverse_geocode.get(nyc_coordinate, 0)
        self.assertEqual(
            all_cities_result, 
            {"city": "Seaport", "country_code": "US", "country": "United States", "state": "New York"}
        )

        # when restrict to big cities then get the correct match
        big_cities_result = reverse_geocode.get(nyc_coordinate, 100000)
        self.assertEqual(
            big_cities_result, 
            {"city": "New York City", "country_code": "US", "country": "United States", "state": "New York"}
        )



if __name__ == "__main__":
    unittest.main()
