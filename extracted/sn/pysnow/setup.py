# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysnow']

package_data = \
{'': ['*']}

install_requires = \
['ijson>=2.5.1,<3.0.0',
 'oauthlib>=3.1.0,<4.0.0',
 'python-magic>=0.4.15,<0.5.0',
 'pytz>=2019.3,<2020.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests>=2.21.0,<3.0.0',
 'six>=1.13.0,<2.0.0']

setup_kwargs = {
    'name': 'pysnow',
    'version': '0.7.17',
    'description': 'ServiceNow HTTP client library',
    'long_description': '```\n ______   __  __    ______    __   __    ______    __     __\n/\\  == \\ /\\ \\_\\ \\  /\\  ___\\  /\\ "-.\\ \\  /\\  __ \\  /\\ \\  _ \\ \\\n\\ \\  _-/ \\ \\____ \\ \\ \\___  \\ \\ \\ \\-.  \\ \\ \\ \\/\\ \\ \\ \\ \\/ ".\\ \\\n \\ \\_\\    \\/\\_____\\ \\/\\_____\\ \\ \\_\\\\"\\_\\ \\ \\_____\\ \\ \\__/".~\\_\\\n  \\/_/     \\/_____/  \\/_____/  \\/_/ \\/_/  \\/_____/  \\/_/   \\/_/\n\t\t- Python library for ServiceNow\n```\n\n[![image](https://travis-ci.org/rbw/pysnow.svg?branch=master)](https://travis-ci.org/rbw/pysnow)\n[![image](https://coveralls.io/repos/github/rbw0/pysnow/badge.svg?branch=master)](https://coveralls.io/github/rbw0/pysnow?branch=master)\n[![image](https://badge.fury.io/py/pysnow.svg)](https://pypi.python.org/pypi/pysnow)\n[![image](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)\n[![image](https://pepy.tech/badge/pysnow/month)](https://pepy.tech/project/pysnow)\n\n\nDocumentation\n---\n\nThe documentation is available at [https://pysnow.readthedocs.io](https://pysnow.readthedocs.io)\n\n\nDevelopment status\n---\n\nThe development status of pysnow is stable; maintenence will be performed, but no new features added.\n\nNew features goes into [rbw/aiosnow](https://github.com/rbw/aiosnow): a modern, asynchronous library for interacting with ServiceNow.\n\nAuthor\n---\n\nRobert Wikman \\<rbw@vault13.org\\>\n\nCredits\n---\n\nThank you [@contributors](https://github.com/rbw/pysnow/graphs/contributors), and [Jetbrains](http://www.jetbrains.com) for IDE licenses.\n\n',
    'author': 'Robert Wikman',
    'author_email': 'rbw@vault13.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rbw/pysnow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
