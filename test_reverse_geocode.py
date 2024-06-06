import reverse_geocode
import unittest


class TestBuiltwith(unittest.TestCase):
    def test_wordpress(self):
        coordinates = (-37.81, 144.96), (40.71427000, -74.00597000)
        results = reverse_geocode.search(coordinates)
        self.assertEqual(
            results,
            [
                {"city": "Melbourne", "country_code": "AU", "country": "Australia", "state": "Victoria"},
                {"city": "New York City", "country_code": "US", "country": "United States", "state": "New York"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
