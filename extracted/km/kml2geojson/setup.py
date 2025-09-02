# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kml2geojson']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['k2g = kml2geojson.cli:k2g']}

setup_kwargs = {
    'name': 'kml2geojson',
    'version': '5.1.0',
    'description': 'A Python library to covert KML files to GeoJSON files',
    'long_description': "kml2geojson\n************\n.. image:: https://github.com/mrcagney/kml2geojson/actions/workflows/run_tests.yml/badge.svg\n    :target: https://github.com/mrcagney/kml2geojson\n    \nkml2geojson is a Python 3.8+ package to convert KML files to GeoJSON files.\nMost of its code is a translation into Python of the Node.js package `togeojson <https://github.com/mapbox/togeojson>`_, but kml2geojson also adds the following features.\n\n- Preserve KML object styling, such as color and opacity\n- Optionally create a style dictionary cataloging all the KML styles used\n- Optionally create several GeoJSON FeatureCollections, one for each KML folder present\n\n\nInstallation\n=============\nCreate a Python 3.8+ virtual environment and run ``poetry add kml2geojson``.\n\n\nUsage\n======\nUse as a library or from the command line.\nFor instructions on the latter, type ``k2g --help``.\n\n\nDocumentation\n==============\nIn the ``docs`` directory and published at `mrcagney.github.io/kml2geojson_docs <https://mrcagney.github.io/kml2geojson_docs/>`_.\n\n\nNotes\n========\n- Development status is Alpha.\n- This project uses semantic versioning.\n- Thanks to `MRCagney <https://mrcagney.com>`_ for funding this project.\n\n\nAuthors\n========\n- Alex Raichev (2015-10-03), maintainer\n\n\nContributing\n===================\nIf you want to help develop this project, here is some background reading.\n\n- The `KML reference <https://developers.google.com/kml/documentation/kmlreference?hl=en>`_ \n- Python's `Minimal DOM implementation <https://docs.python.org/3.4/library/xml.dom.minidom.html>`_, which this project uses to parse KML files\n\n\nChanges\n========\n\n5.1.0, 2022-04-29\n-----------------\n- Extended ``convert()`` to accept a KML file object.\n- Added type hints.\n- Updated dependencies and removed version caps.\n- Dropped support for Python versions less than 3.8.\n- Switched from Travis CI to Github Actions.\n\n\n5.0.1, 2021-10-11\n-----------------\n- Re-included the MIT License file and added more metadata to the file ``pyproject.toml`` for a more informative listing on PyPi.\n\n\n5.0.0, 2021-10-07\n-----------------\n- Upgraded to Python 3.9 and dropped support for Python versions < 3.6.\n- Switched to Poetry.\n- Breaking change: refactored the ``convert`` function to return dictionaries instead of files.\n- Moved docs from Rawgit to Github Pages.\n\n\n4.0.2, 2017-04-26\n-------------------\n- Fixed the bug where ``setup.py`` could not find the license file.\n\n\n4.0.1, 2017-04-22\n-------------------\n- Moved the name of a FeatureCollection into a 'name' attribute, because `RFC 7946 says that a GeoJSON FetaureCollection must not have a 'properties' attribute <https://tools.ietf.org/html/rfc7946#section-7>`_\n- Stripped leanding and trailing whitespace from text content to avoid cluttered or blank name and description attribute values\n- Switched to pytest for testing\n\n\n4.0.0, 2016-11-24\n-------------------\n- Moved command line functionality to separate module\n- Renamed some functions\n\n\n3.0.4, 2015-10-15\n-------------------\nDisambiguated filenames in ``main()``.\n\n\n3.0.3, 2015-10-13\n-------------------\nImproved ``to_filename()`` again.\n\n\n3.0.2, 2015-10-12\n-------------------\nImproved ``to_filename()`` and removed the lowercasing.\n\n\n3.0.1, 2015-10-12\n-------------------\nTweaked ``to_filename()`` to lowercase and underscore results. \nForgot to do that last time.\n\n\n3.0.0, 2015-10-12\n------------------\nChanged the output of ``build_layers()`` and moved layer names into the GeoJSON FeatureCollections\n\n\n2.0.2, 2015-10-12\n-------------------\n- Replaced underscores with dashes in command line options\n\n\n2.0.1, 2015-10-12\n-------------------\n- Set default border style for colored polygons\n \n\n2.0.0, 2015-10-08\n------------------\n- Added documentation\n- Tweaked the command line tool options \n\n\n1.0.0, 2015-10-05\n------------------\n- Changed some names \n- Added lots of tests\n\n\n0.1.1, 2015-10-03\n-------------------\nFixed packaging to find ``README.rst``\n\n\n0.1.0, 2015-10-03\n-----------------\nFirst\n\n\n",
    'author': 'Alex Raichev',
    'author_email': 'alex@raichev.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrcagney/kml2geojson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
