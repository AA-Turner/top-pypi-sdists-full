"""
Copyright (C) 2008 Leonard Norrgard <leonard.norrgard@gmail.com>
Copyright (C) 2015 Leonard Norrgard <leonard.norrgard@gmail.com>

This file is part of Geohash.

Geohash is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Geohash is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public
License along with Geohash.  If not, see
<http://www.gnu.org/licenses/>.
"""
from setuptools import setup, find_packages

setup(
    name="geohash2",
    version="1.1",
    packages=find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['docutils>=0.3'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst']
    },

    # metadata for upload to PyPI
    author="Leonard Norrgard, Barthelemy Delemotte",
    author_email="barthelemy.delemotte@gmail.com",
    description="(Geohash fixed for python3) Module to decode/encode Geohashes to/from latitude and longitude.  See http://en.wikipedia.org/wiki/Geohash",
    long_description="This module provides functions to decode and encode Geohashes to and from latitude and longitude coordinates.",
    license="GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.",
    keywords="Geohash GIS latitude longitude encode decode Galileo GPS WGS84 coordinates geotagging",
    url="https://github.com/dbarthe/geohash/",  # project home page, if any
)
