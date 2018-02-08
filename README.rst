===============
Reverse Geocode
===============

Reverse Geocode takes a latitude / longitude coordinate and returns the country and city.
Example usage:

.. sourcecode:: python

    >>> import reverse_geocode
    >>> coordinates = (-37.81, 144.96), (31.76, 35.21)
    >>> reverse_geocode.search(coordinates)
    [{'city': 'Melbourne', 'code': 'AU', 'country': 'Australia'},
     {'city': 'Jerusalem', 'code': 'IL', 'country': 'Israel'}]

..

The module has a set of known geocoded locations and uses a `k-d tree <http://en.wikipedia.org/wiki/K-d_tree>`_ to efficiently find the nearest neighbour. This can be useful when you need to reverse geocode a large number of coordinates so a web API is not practical.


=======
Install
=======

.. sourcecode:: bash

    pip install reverse-geocode

..
