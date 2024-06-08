# Reverse Geocode

Reverse Geocode takes a latitude / longitude coordinate and returns the nearest known country, state, and city.
This can be useful when you need to reverse geocode a large number of coordinates so a web API is not practical.

The geocoded locations are from [geonames](http://download.geonames.org/export/dump/). This data is then structured in to a [k-d tree](http://en.wikipedia.org/wiki/K-d_tree>) for efficiently finding the nearest neighbour. 

Note that as this is point based and not a polygon based lookup it will only give a rough idea of the location/city.


## Example usage

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

The module returns the nearest known location, which may not be as expected when there is a much larger city nearby.
For example querying for the following coordinate will return the Seaport area of NYC:

```
>>> nyc_coordinate = 40.71, -74.00
>>> reverse_geocode.get(nyc_coordinate)
{"city": "Seaport", "country_code": "US", "country": "United States", "state": "New York"}
```

To filter for larger cities a minimum population for results can be defined:
        
```
>>> reverse_geocode.get(nyc_coordinate, min_population=100000)
{"city": "New York City", "country_code": "US", "country": "United States", "state": "New York"}
```


## Install

```
pip install reverse-geocode
```
