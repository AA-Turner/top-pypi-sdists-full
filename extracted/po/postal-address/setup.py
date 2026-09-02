# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postal_address', 'postal_address.tests']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=5.0', 'boltons>=16.5', 'pycountry==22.3.5']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=2.0,<3.0']}

setup_kwargs = {
    'name': 'postal-address',
    'version': '22.4.22.1',
    'description': 'Parse, normalize and render postal addresses.',
    'long_description': "Postal Address\n==============\n\nPython module to parse, normalize and render postal addresses.\n\nStable release: |release| |versions| |license|\n\nDevelopment: |docs| |coverage| |quality|\n\n.. |release| image:: https://img.shields.io/pypi/v/postal-address.svg\n    :target: https://pypi.python.org/pypi/postal-address\n    :alt: Last release\n.. |versions| image:: https://img.shields.io/pypi/pyversions/postal-address.svg\n    :target: https://pypi.python.org/pypi/postal-address\n    :alt: Python versions\n.. |license| image:: https://img.shields.io/pypi/l/postal-address.svg\n    :target: http://opensource.org/licenses/BSD-2-Clause\n    :alt: Software license\n.. |docs| image:: https://readthedocs.org/projects/postal-address/badge/?version=master\n    :target: http://postal-address.readthedocs.io/en/develop/\n    :alt: Documentation Status\n.. |coverage| image:: https://codecov.io/gh/scaleway/postal-address/branch/develop/graph/badge.svg\n    :target: https://codecov.io/github/scaleway/postal-address?branch=master\n    :alt: Coverage Status\n.. |quality| image:: https://scrutinizer-ci.com/g/scaleway/postal-address/badges/quality-score.png?b=develop\n    :target: https://scrutinizer-ci.com/g/scaleway/postal-address/?branch=master\n    :alt: Code Quality\n\n\nMotivation\n----------\n\n    « What ties us to territory is tax. »\n    -- Kevin Deldycke, 2014-11-07\n\nThe reason above is why we need fine-grained and meticulous territory\nmanagement and normalization. This project aims to solve this problem once for\nall.\n\nDon't get me wrong, this work is a huge undertaking. Postal address parsing,\nnormalization and rendering is hard. See the collection of `falsehoods\nprogrammers believe about postal addresses\n<https://github.com/kdeldycke/awesome-falsehood#postal-addresses>`_.\n\nThis library is still in its early stages, but is good enough to implement\nthe new European Directives on VAT, which requires all e-commerce shops to\nguess the locality of their EU customers depending on their billing address.\n",
    'author': 'Scaleway',
    'author_email': 'opensource@scaleway.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Scaleway/postal-address',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
