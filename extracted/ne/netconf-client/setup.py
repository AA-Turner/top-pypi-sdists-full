# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netconf_client']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.3,<7', 'paramiko>=2.7.2,<4']

setup_kwargs = {
    'name': 'netconf-client',
    'version': '3.3.0',
    'description': 'A Python NETCONF client',
    'long_description': '![Build Status](https://github.com/ADTRAN/netconf_client/workflows/CI%20Checks/badge.svg)\n[![PyPI version](https://badge.fury.io/py/netconf-client.svg)](https://badge.fury.io/py/netconf-client)\n[![Coverage Status](https://coveralls.io/repos/github/ADTRAN/netconf_client/badge.svg?branch=main)](https://coveralls.io/github/ADTRAN/netconf_client?branch=main)\n\n# netconf_client\n\nA NETCONF client for Python 3.8+.\n\n## Basic Usage\n\n```python\nfrom netconf_client.connect import connect_ssh\nfrom netconf_client.ncclient import Manager\n\nsession = connect_ssh(host="localhost", port=830, username="admin", password="password")\nmgr = Manager(session, timeout=120)\n\nmgr.edit_config(config="""<config> ... </config>""")\nprint(mgr.get(filter="""<filter> ... </filter>""").data_xml)\n```\n\nMore complete documentation can be found in the [User Guide]\n\n## Comparison with `ncclient`\n\nCompared to [ncclient](https://github.com/ncclient/ncclient),\n`netconf_client` has several advantages:\n\n - It\'s simpler (at the time of writing: 789 LoC vs 2889 LoC)\n - lxml can be bypassed, which can work around issues where lxml\n   breaks namespaces of e.g. identityrefs\n - Support for TLS sessions\n\nAnd a few disadvantages:\n\n - Support for non-RFC-compliant devices isn\'t really included in\n   `netconf_client`\n - `netconf_client` does a lot less error checking and assumes you\'re\n   sending valid messages to the server (however this can be useful\n   for testing edge-case behavior of a server)\n\n\n[User Guide]: https://adtran.github.io/netconf_client/\n',
    'author': 'ADTRAN, Inc.',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ADTRAN/netconf_client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
