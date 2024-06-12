import os
from distutils.core import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="reverse_geocode",
    version="1.6.5",
    packages=["reverse_geocode"],
    package_dir={"reverse_geocode": "reverse_geocode"},
    package_data={"reverse_geocode": ["countries.csv", "geocode.gz"]},
    author="Richard Penman",
    author_email="richard.penman@gmail.com",
    description="Reverse geocode the given latitude / longitude",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    url="https://github.com/richardpenman/reverse_geocode/",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    license="lgpl",
    install_requires=["numpy", "scipy"],
)
