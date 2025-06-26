# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taktile_auth',
 'taktile_auth.entities',
 'taktile_auth.parser',
 'taktile_auth.schemas',
 'taktile_auth.test_utils',
 'taktile_auth.utils']

package_data = \
{'': ['*'], 'taktile_auth': ['assets/*']}

install_requires = \
['PyJWT[crypto]==2.10.1',
 'PyYAML>=6.0,<7.0',
 'cryptography>=44.0.1,<45.0.0',
 'pydantic<3.0',
 'requests==2.32.3']

setup_kwargs = {
    'name': 'taktile-auth',
    'version': '1.1.43',
    'description': 'Auth Package for Taktile',
    'long_description': '# Taktile Auth\n\n[![pypi status](https://img.shields.io/pypi/v/taktile-auth.svg)](https://pypi.python.org/pypi/taktile-auth)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)\n\nThis package is part of the Taktile ecosystem.\n\nTaktile enables data science teams to industrialize, scale, and maintain machine learning models. Our ML development platform makes it easy to create your own end-to-end ML applications:\n\n- Turn models into auto-scaling APIs in a few lines of code\n- Easily add model tests\n- Create and share model explanations through the Taktile UI\n\nFind more information in our [docs](https://docs.taktile.com).\n',
    'author': 'Taktile GmbH',
    'author_email': 'devops@taktile.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
