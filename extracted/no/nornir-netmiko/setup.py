# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_netmiko', 'nornir_netmiko.connections', 'nornir_netmiko.tasks']

package_data = \
{'': ['*']}

install_requires = \
['netmiko>=4.0.0,<5.0.0']

entry_points = \
{'nornir.plugins.connections': ['netmiko = nornir_netmiko.connections:Netmiko']}

setup_kwargs = {
    'name': 'nornir-netmiko',
    'version': '1.0.1',
    'description': "Netmiko's plugins for Nornir",
    'long_description': '# nornir_netmiko\nNetmiko Plugins for Nornir\n',
    'author': 'Kirk Byers',
    'author_email': 'ktbyers@twb-tech.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ktbyers/nornir_netmiko',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
