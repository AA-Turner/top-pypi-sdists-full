# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_gladly', 'tap_gladly.tests']

package_data = \
{'': ['*'], 'tap_gladly': ['schemas/*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['tap-gladly = tap_gladly.tap:Tapgladly.cli']}

setup_kwargs = {
    'name': 'tap-gladly',
    'version': '0.4.1',
    'description': '`tap-gladly` is a Singer tap for gladly, built with the Meltano SDK for Singer Taps.',
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
