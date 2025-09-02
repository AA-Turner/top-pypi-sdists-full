# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_awair']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.1,<4.0.0', 'voluptuous>=0.11.7']

setup_kwargs = {
    'name': 'python-awair',
    'version': '0.2.4',
    'description': 'asyncio client for the Awair GraphQL and Local APIs',
    'long_description': '# python_awair\n\n![Latest PyPI version](https://img.shields.io/pypi/v/python_awair.svg)\n![CI](https://github.com/ahayworth/python_awair/workflows/CI/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/ahayworth/python_awair/branch/master/graph/badge.svg)](https://codecov.io/gh/ahayworth/python_awair)\n[![Documentation Status](https://readthedocs.org/projects/python-awair/badge/?version=latest)](https://python-awair.readthedocs.io/en/latest/?badge=latest)\n\nThis is an async library which accesses portions of the [Awair](https://getawair.com) REST API. It exists primarily\nto support the Home Assistant integration, but is considered active and supported by its author. PRs welcome!\n\nFeatures:\n- Object-oriented approach to querying and handling data\n- Supports the "user" portion of the API.\n- Possible to list devices, user information, and to query for a variety of sensor data over various timeframes.\n\nNot yet supported:\n- Device API usage\n- Organization API\n- Device management (such as changing the display of a device)\n\nDive into our [documentation](https://python-awair.readthedocs.io/en/latest) to get started!\n\n# Development\n\n- We manage dependencies and builds via [poetry](https://python-poetry.org)\n- We use [pytest](https://github.com/pytest-dev/pytest) and [tox](https://github.com/tox-dev/tox) to test\n- A variety of linters are available and CI enforces them\n\nAfter installing and configuring poetry:\n- Run `poetry install` to install dev dependencies\n- Run `poetry shell` to drop into a virtualenv\n- Run `poetry run tox` (or just `tox` if you\'re in a virtualenv) to test\n  - Run `poetry run tox -e lint` (or just `tox -e lint` if you\'re in a virtualenv) to run linters.\n',
    'author': 'Andrew Hayworth',
    'author_email': 'ahayworth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ahayworth/python_awair',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
