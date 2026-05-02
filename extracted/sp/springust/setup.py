# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['springust', 'springust.command']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['APPLICATION-NAME = springust:main']}

setup_kwargs = {
    'name': 'springust',
    'version': '0.1.0',
    'description': 'springust',
    'long_description': None,
    'author': 'Boris Korogvich',
    'author_email': 'b.korogvich@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
