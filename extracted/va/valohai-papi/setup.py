# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['papi']

package_data = \
{'': ['*']}

install_requires = \
['valohai-yaml>=0.14.1']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6']}

setup_kwargs = {
    'name': 'valohai-papi',
    'version': '0.1.3',
    'description': 'Experimental imperative Valohai pipeline API',
    'long_description': None,
    'author': 'Aarni Koskela',
    'author_email': 'aarni@valohai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/valohai/papi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
