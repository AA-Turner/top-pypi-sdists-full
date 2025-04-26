# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strip_ansi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'strip-ansi',
    'version': '0.1.1',
    'description': 'Strip ANSI escape sequences from a string',
    'long_description': 'strip-ansi\n----------\n\n    Strip ANSI escape sequences from a string\n\n\nInstallation\n============\n\n`strip-ansi` is available on `on PyPI <https://pypi.org/project/strip-ansi>`_:\n\n.. code:: shell\n   \n   pip install strip_ansi\n\nUsage\n=====\n\n.. WARNING::\n   This package only supports python 3.6 and up. It may work on older versions (maybe even python 2)\n   but I\'m not sure.\n\n.. code:: python\n\n   >>> from strip_ansi import strip_ansi\n   >>> strip_ansi("\\033[38mLorem ipsum\\033[0m")\n   "Lorem ipsum"\n',
    'author': 'Ewen Le Bihan',
    'author_email': 'ewen.lebihan7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ewen-lbh/python-strip-ansi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
