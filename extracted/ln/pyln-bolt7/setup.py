# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bolt7']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyln-bolt7',
    'version': '1.0.246',
    'description': 'BOLT7',
    'long_description': None,
    'author': 'Rusty Russell',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
