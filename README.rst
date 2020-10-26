===============
Reverse Geocode
===============

Reverse Geocode takes a latitude / longitude coordinate and returns the country and city.
Example usage:

.. sourcecode:: python

    >>> import reverse_geocode
    >>> coordinates = (-37.81, 144.96), (31.76, 35.21)
    >>> reverse_geocode.search(coordinates)
    [{'city': 'Melbourne', 'country_code': 'AU', 'country': 'Australia'},
     {'city': 'Jerusalem', 'country_code': 'IL', 'country': 'Israel'}]

..

The module has a set of known geocoded locations and uses a `k-d tree <http://en.wikipedia.org/wiki/K-d_tree>`_ to efficiently find the nearest neighbour. This can be useful when you need to reverse geocode a large number of coordinates so a web API is not practical.

As this is a point based and not a polygon based lookup it will only give a rough idea of the location/city

=======
Install
=======

Supports python 2 & 3:

.. sourcecode:: bash

    pip install reverse-geocode
    pip3 install reverse-geocode

..
