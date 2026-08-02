# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['twentyc', 'twentyc.rpc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.10.0']

entry_points = \
{'markdown.extensions': ['pymdgen = pymdgen.md:Extension']}

setup_kwargs = {
    'name': 'twentyc.rpc',
    'version': '1.0.0',
    'description': "client for 20c's RESTful API",
    'long_description': "\n# RPC\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twentyc.rpc)\n[![PyPI version](https://badge.fury.io/py/twentyc.rpc.svg)](https://badge.fury.io/py/twentyc.rpc)\n[![Build Status](https://travis-ci.org/20c/twentyc.rpc.svg?branch=master)](https://travis-ci.org/20c/twentyc.rpc)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/twentyc.rpc/master.svg?maxAge=2592000)](https://codecov.io/github/20c/twentyc.rpc)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/20c/twentyc.rpc.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/20c/twentyc.rpc/context:python)\n\n\nclient for 20c's RESTful API\n\n",
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/twentyc.rpc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
