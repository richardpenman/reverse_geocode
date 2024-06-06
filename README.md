# Reverse Geocode

Reverse Geocode takes a latitude / longitude coordinate and returns the country and city.
Example usage:

```
>>> import reverse_geocode
>>> melbourne_coord = -37.81, 144.96
>>> reverse_geocode.get(melbourne_coord)
{'city': 'Melbourne', 'country_code': 'AU', 'country': 'Australia', 'state': 'Victoria'}
>>> nyc_coord = 40.71427000, -74.00597000
>>> reverse_geocode.search((melbourne_coord, nyc_coord))
[{'city': 'Melbourne', 'country_code': 'AU', 'country': 'Australia', 'state': 'Victoria'},
 {'city': 'New York City', 'country_code': 'US', 'country': 'United States', 'state': 'New York'}]
```

The module has a set of known geocoded locations and uses a [k-d tree](http://en.wikipedia.org/wiki/K-d_tree>) to efficiently find the nearest neighbour. This can be useful when you need to reverse geocode a large number of coordinates so a web API is not practical.

As this is a point based and not a polygon based lookup it will only give a rough idea of the location/city

# Install

Supports python 3:

```
pip install reverse-geocode
```
