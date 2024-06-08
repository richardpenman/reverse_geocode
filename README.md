# Reverse Geocode

Reverse Geocode takes a latitude / longitude coordinate and returns the nearest known country, state, and city.
This can be useful when you need to reverse geocode a large number of coordinates so a web API is not practical.

The geocoded locations are from [geonames](http://download.geonames.org/export/dump/). This data is then structured in to a [k-d tree](http://en.wikipedia.org/wiki/K-d_tree>) for efficiently finding the nearest neighbour. 

Note that as this is point based and not a polygon based lookup it will only give a rough idea of the location/city.


## Example usage

Example reverse geocoding a coordinate:

```
>>> import reverse_geocode
>>> melbourne_coord = -37.81, 144.96
>>> reverse_geocode.get(melbourne_coord)
{'country_code': 'AU', 'city': 'Melbourne', 'latitude': -37.814, 'longitude': 144.96332, 'population': 4917750, 'state': 'Victoria', 'country': 'Australia'}
```

Example reverse geocoding a list of coordinates:
```
>>> nyc_coord = 40.71427000, -74.00597000
>>> reverse_geocode.search((melbourne_coord, nyc_coord))
[{'country_code': 'AU', 'city': 'Melbourne', 'latitude': -37.814, 'longitude': 144.96332, 'population': 4917750, 'state': 'Victoria', 'country': 'Australia'},
 {'country_code': 'US', 'city': 'New York City', 'latitude': 40.71427, 'longitude': -74.00597, 'population': 8804190, 'state': 'New York', 'country': 'United States'}]
```

By default the nearest known location is returned, which may not be as expected when there is a much larger city nearby.
For example querying for the following coordinate near NYC will return Seaport:

```
>>> nyc_coordinate = 40.71, -74.00
>>> reverse_geocode.get(nyc_coordinate)
{'country_code': 'US', 'city': 'Seaport', 'latitude': 40.70906, 'longitude': -74.00317, 'population': 8385, 'state': 'New York', 'county': 'New York County', 'country': 'United States'}
```

To filter for larger cities a minimum population can be set. Using a minimum population of `100000` with the above coordinate now returns NYC:
        
```
>>> reverse_geocode.get(nyc_coordinate, min_population=100000)
{'country_code': 'US', 'city': 'New York City', 'latitude': 40.71427, 'longitude': -74.00597, 'population': 8804190, 'state': 'New York', 'country': 'United States'}
```


## Install

```
pip install reverse-geocode
```
