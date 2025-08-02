# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib']

package_data = \
{'': ['*']}

install_requires = \
['sphinx>=4.3']

setup_kwargs = {
    'name': 'sphinxcontrib-diagrams',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'yamionp',
    'author_email': 'yami@crimsondream.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
