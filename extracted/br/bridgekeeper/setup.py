# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bridgekeeper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bridgekeeper',
    'version': '0.9',
    'description': 'Django permissions that work with QuerySets.',
    'long_description': "Bridgekeeper\n------------\n\n..\n\n    | Who would cross the Bridge of Death\n    | must answer me these questions three,\n    | ere the other side he see.\n\n    -- The Bridgekeeper, *Monty Python and the Holy Grail*\n\nBridgekeeper is a permissions library for Django_ projects, where permissions are defined in your code, rather than in your database.\n\nIt's heavily inspired by django-rules_, but with one important difference: **it works on QuerySets as well as individual model instances**.\n\nThis means that you can efficiently show a list of all of the model instances that your user is allowed to edit, for instance, without having your permission-checking code in two different places.\n\n.. _django: https://djangoproject.com/\n.. _django-rules: https://github.com/dfunckt/django-rules\n\nBridgekeeper is tested on Django 2.2 and 3.0 on all Python versions Django supports, and is licensed under the MIT License.\n",
    'author': 'Leigh Brenecki',
    'author_email': 'leigh@brenecki.id.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bridgekeeper.leigh.party/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
