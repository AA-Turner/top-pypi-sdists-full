# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adutils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'adutils',
    'version': '0.6.2',
    'description': 'Helper and utilities for AppDaemon apps.',
    'long_description': '# adutils\n\n[![PyPI](https://img.shields.io/pypi/v/adutils)](https://pypi.org/project/adutils/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/adutils)](https://pypi.org/project/adutils/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/adutils)](https://pypi.org/project/adutils/)\n\nHelper functions for AppDaemon apps. Currently there is just code, no documentation. Sorry ¯\\\\_(ツ)_/¯\n\n## Install\n\n```bash\npip install adutils\n```\n\n## Apps using **adutils**\n\n* [AutoMoLi](https://github.com/benleb/ad-automoli)\n* [EnCh](https://github.com/benleb/ad-ench)\n* [Notifreeze](https://github.com/benleb/ad-notifreeze)\n* [Healthcheck](https://github.com/benleb/ad-healthcheck)\n',
    'author': 'Ben Lebherz',
    'author_email': 'git@benleb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benleb/adutils',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
