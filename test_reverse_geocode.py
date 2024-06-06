import reverse_geocode
import unittest


class TestBuiltwith(unittest.TestCase):
    def test_wordpress(self):
        coordinates = (-37.81, 144.96), (31.76, 35.21)
        results = reverse_geocode.search(coordinates)
        self.assertEqual(
            results,
            [
                {"city": "Melbourne", "country_code": "AU", "country": "Australia", "state": "Victoria"},
                {"city": "Jerusalem", "country_code": "IL", "country": "Israel", "state": "Jerusalem"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
