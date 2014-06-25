===============
Reverse Geocode
===============

Find details about the location of the given latitude / longitude.
Here is example usage: ::

    >>> import reverse_geocode
    >>> coordinates = (-37.81, 144.96), (31.76, 35.21)
    >>> reverse_geocode.get(coordinates[0])
    {'city': 'Melbourne', 'code': 'AU', 'country': 'Australia'}
    >>> reverse_geocode.search(coordinates)
    [{'city': 'Melbourne', 'code': 'AU', 'country': 'Australia'},
     {'city': 'Jerusalem', 'code': 'IL', 'country': 'Israel'}]

Instead of using an web API the script works by loading a list of known geocoded locations from geonames and then using a KD Tree to efficiently find the nearest neighbour. This can be useful when you need to reverse geocode a large number of coordinates.

