import reverse_geocode
import unittest


class TestBuiltwith(unittest.TestCase):
    def test_get(self):
        coordinate = -37.81, 144.96
        results = reverse_geocode.get(coordinate)
        self.assertEqual(
            results,
            {'country_code': 'AU', 'city': 'Melbourne', 'latitude': -37.814, 'longitude': 144.96332, 'population': 4917750, 'state': 'Victoria', 'country': 'Australia'}
        )

    def test_search(self):
        coordinates = (-37.81, 144.96), (40.71427000, -74.00597000)
        results = reverse_geocode.search(coordinates)
        self.assertEqual(
            results,
            [
                {'country_code': 'AU', 'city': 'Melbourne', 'latitude': -37.814, 'longitude': 144.96332, 'population': 4917750, 'state': 'Victoria', 'country': 'Australia'},
                {'country_code': 'US', 'city': 'New York City', 'latitude': 40.71427, 'longitude': -74.00597, 'population': 8804190, 'state': 'New York', 'country': 'United States'},
            ],
        )

    def test_population(self):
        # a coordinate near NYC
        nyc_coordinate = 40.71, -74.00
        # try searching for NYC with all data and get a smaller area called Seaport
        all_cities_result = reverse_geocode.get(nyc_coordinate, 0)
        self.assertEqual(
            all_cities_result, 
            {'country_code': 'US', 'city': 'Seaport', 'latitude': 40.70906, 'longitude': -74.00317, 'population': 8385, 'state': 'New York', 'county': 'New York County', 'country': 'United States'}
        )

        # when restrict to big cities then get the expected match
        big_cities_result = reverse_geocode.get(nyc_coordinate, 100000)
        self.assertEqual(
            big_cities_result, 
            {'country_code': 'US', 'city': 'New York City', 'latitude': 40.71427, 'longitude': -74.00597, 'population': 8804190, 'state': 'New York', 'country': 'United States'}
        )



if __name__ == "__main__":
    unittest.main()
