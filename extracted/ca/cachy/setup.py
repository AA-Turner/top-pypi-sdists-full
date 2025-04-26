# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cachy',
 'cachy.contracts',
 'cachy.serializers',
 'cachy.stores',
 'tests',
 'tests.stores']

package_data = \
{'': ['*']}

extras_require = \
{'memcached': ['python-memcached>=1.59,<2.0'],
 'msgpack': ['msgpack-python>=0.5,<0.6'],
 'redis': ['redis>=3.3.6,<4.0.0']}

setup_kwargs = {
    'name': 'cachy',
    'version': '0.3.0',
    'description': 'Cachy provides a simple yet effective caching library.',
    'long_description': 'Cachy\n#####\n\n.. image:: https://travis-ci.org/sdispater/cachy.png\n   :alt: Cachy Build status\n   :target: https://travis-ci.org/sdispater/cachy\n\nCachy provides a simple yet effective caching library.\n\nThe full documentation is available here: http://cachy.readthedocs.org\n\n\nResources\n=========\n\n* `Documentation <http://cachy.readthedocs.org>`_\n* `Issue Tracker <https://github.com/sdispater/cachy/issues>`_\n',
    'author': 'Sébastien Eustace',
    'author_email': 'sebastien@eustace.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdispater/cachy',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
