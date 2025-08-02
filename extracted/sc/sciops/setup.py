# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sciops']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.2,<8.0.0', 'rich>=12.4.4,<13.0.0']

setup_kwargs = {
    'name': 'sciops',
    'version': '0.1.1',
    'description': 'Collection of utilities for scientific operations',
    'long_description': None,
    'author': 'Dylan Miracle',
    'author_email': 'dylan.miracle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
