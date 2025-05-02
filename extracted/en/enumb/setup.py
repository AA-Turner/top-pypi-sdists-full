# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enumb']

package_data = \
{'': ['*']}

install_requires = \
['cassidy>=0.1.2,<0.2.0', 'expo>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'enumb',
    'version': '0.1.5',
    'description': 'Concise, Pythonic Enums',
    'long_description': None,
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
