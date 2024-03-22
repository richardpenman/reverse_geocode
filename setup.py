import os
from distutils.core import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="reverse_geocode",
    version="1.6.1",
    packages=["reverse_geocode"],
    package_dir={"reverse_geocode": "reverse_geocode"},
    data_files=[
        (
            "reverse_geocode",
            ["reverse_geocode/geocode.csv", "reverse_geocode/countries.csv"],
        )
    ],
    author="Richard Penman",
    author_email="richard.penman@gmail.com",
    description="Reverse geocode the given latitude / longitude",
    long_description=read("README.rst"),
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
