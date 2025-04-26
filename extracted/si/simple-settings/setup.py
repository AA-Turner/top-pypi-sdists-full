# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'simple_settings'}

packages = \
['dynamic_settings',
 'simple_settings',
 'simple_settings.dynamic_settings',
 'simple_settings.strategies',
 'strategies']

package_data = \
{'': ['*']}

extras_require = \
{'all': ['jsonpickle==2.0.0',
         'toml==0.10.2',
         'PyYAML==6.0',
         'SQLAlchemy==1.4.26',
         'pymemcache==3.5.0',
         'six==1.16.0',
         'redis==3.5.3',
         'boto3>=1.20.26,<2.0.0'],
 'database': ['SQLAlchemy==1.4.26'],
 'dynamic_settings': ['jsonpickle==2.0.0'],
 'memcache': ['pymemcache==3.5.0', 'six==1.16.0'],
 'redis': ['redis==3.5.3'],
 's3': ['boto3>=1.20.26,<2.0.0'],
 'toml': ['toml==0.10.2'],
 'yaml': ['PyYAML==6.0']}

setup_kwargs = {
    'name': 'simple-settings',
    'version': '1.2.0',
    'description': 'A simple way to manage your project settings.',
    'long_description': None,
    'author': 'Diego Garcia',
    'author_email': 'drgarcia1986@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drgarcia1986/simple-settings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
