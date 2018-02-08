import os
from distutils.core import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='reverse_geocode', 
    version='1.1',
    packages=['reverse_geocode'],
    package_dir={'reverse_geocode' : '.'}, # look for package contents in current directory
    package_data={'reverse_geocode' : ['geocode.csv', 'countries.csv']},
    author='Richard Penman',
    author_email='richard@webscraping.com',
    description='Reverse geocode the given latitude / longitude',
    long_description=read('README.rst'),
    url='https://bitbucket.org/richardpenman/reverse_geocode',
    license='lgpl',
    install_requires=['numpy', 'scipy']
)
