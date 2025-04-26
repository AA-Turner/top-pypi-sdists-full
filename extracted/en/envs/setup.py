# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envs']

package_data = \
{'': ['*'], 'envs': ['templates/*']}

extras_require = \
{':extra == "cli"': ['click[cli]>=8.0.3,<9.0.0',
                     'Jinja2[cli]>=3.0.3,<4.0.0',
                     'terminaltables[cli]>=3.1.10,<4.0.0']}

entry_points = \
{'console_scripts': ['envs = envs.cli:envs']}

setup_kwargs = {
    'name': 'envs',
    'version': '1.4',
    'description': 'Easy access of environment variables from Python with support for strings, booleans, list, tuples, and dicts.',
    'long_description': None,
    'author': 'Brian Jinwright',
    'author_email': 'bjinwright@qwigo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
