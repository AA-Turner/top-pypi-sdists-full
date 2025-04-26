# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsglue',
 'awsglue.dataframe_transforms',
 'awsglue.scripts',
 'awsglue.transforms']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'awsglue3-local',
    'version': '1.0.0',
    'description': 'AWS Glue Python package for local development',
    'long_description': None,
    'author': 'Machiel Keizer Groeneveld',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
