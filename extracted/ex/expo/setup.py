# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'expo',
    'version': '0.1.2',
    'description': 'Selectively expose module functionality',
    'long_description': None,
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
