# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioeafm']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.1,<4.0.0']

setup_kwargs = {
    'name': 'aioeafm',
    'version': '1.0.0',
    'description': 'An asyncio wrapper for the UK Environment Agency Flood Monitoring API',
    'long_description': None,
    'author': 'John Carr',
    'author_email': 'john.carr@unrouted.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
