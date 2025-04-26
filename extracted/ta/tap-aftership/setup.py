# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_aftership', 'tap_aftership.tests']

package_data = \
{'': ['*'], 'tap_aftership': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['tap-aftership = tap_aftership.tap:TapAfterShip.cli']}

setup_kwargs = {
    'name': 'tap-aftership',
    'version': '0.0.4',
    'description': '`tap-aftership` is a Singer tap for AfterShip, built with the Meltano Singer SDK.',
    'long_description': 'None',
    'author': 'harrystech',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
