# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['celery_singleton', 'celery_singleton.backends']

package_data = \
{'': ['*']}

install_requires = \
['celery>=4', 'redis']

setup_kwargs = {
    'name': 'celery-singleton',
    'version': '0.3.1',
    'description': 'Prevent duplicate celery tasks',
    'long_description': None,
    'author': 'Steinthor Palsson',
    'author_email': 'steini90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/steinitzu/celery-singleton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
