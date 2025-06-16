# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cacheback']

package_data = \
{'': ['*']}

install_requires = \
['django>=2']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'],
 'celery': ['celery>=4'],
 'docs': ['Sphinx>=3.3.0,<4'],
 'rq': ['django-rq>=2']}

setup_kwargs = {
    'name': 'django-cacheback',
    'version': '3.0.0',
    'description': 'Caching library for Django that uses Celery or RQ to refresh cache items asynchronously',
    'long_description': "=========\nCacheback\n=========\n\n----------------------------------------\nAsynchronous cache refreshing for Django\n----------------------------------------\n\nWhat does this library do?\n--------------------------\n\nIt's an extensible caching library that refreshes stale cache items\nasynchronously using a Celery_ or rq_ task (utilizing django-rq). The key\nidea being that it's better to serve a stale item (and populate the cache\nasynchronously) than block the response process in order to populate the cache\nsynchronously.\n\n.. _Celery: http://celeryproject.org/\n.. _rq: http://python-rq.org/\n\nUsing this library, you can rework your views so that all reads are from\ncache - which can be a significant performance boost.\n\nA corollary of this technique is that cache hammering can be handled simply and\nelegantly, avoiding sudden surges of expensive reads when a cached item becomes stale.\n\n\nDo you have good docs?\n----------------------\n\nYup - `over on readthedocs.org`_.\n\n.. _`over on readthedocs.org`: http://django-cacheback.readthedocs.org/en/latest/\n\n\nSupported versions\n------------------\n\nPython 3.6+ is supported. Django 2.0+ is supported.\n\n\nDo you have tests?\n------------------\n\nYou betcha!\n\n.. image:: https://github.com/codeinthehole/django-cacheback/workflows/CI/badge.svg?branch=master\n     :target: https://github.com/codeinthehole/django-cacheback/actions?workflow=CI\n     :alt: CI Status\n\n\nCan I use this in my project?\n-----------------------------\n\nProbably - subject to the `MIT license`_.\n\n.. _`MIT license`: https://github.com/codeinthehole/django-cacheback/blob/master/LICENSE\n\n\nI want to contribute!\n---------------------\n\nBrilliant!  Here are the `contributing guidelines`_.\n\n.. _`contributing guidelines`: http://django-cacheback.readthedocs.org/en/latest/contributing.html\n",
    'author': 'David Winterbottom',
    'author_email': 'david.winterbottom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codeinthehole/django-cacheback',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
