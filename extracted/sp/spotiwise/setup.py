# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotiwise']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.3.0', 'six>=1.10.0']

setup_kwargs = {
    'name': 'spotiwise',
    'version': '0.10.8',
    'description': 'Custom Spotify library using true Python objects',
    'long_description': None,
    'author': 'Wisdom Wolf',
    'author_email': 'wisdomwolf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
