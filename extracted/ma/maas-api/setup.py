# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maas_api']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3,<2.0', 'requests>=2.26,<3.0']

setup_kwargs = {
    'name': 'maas-api',
    'version': '0.1.1',
    'description': 'An api client library for MAAS.io',
    'long_description': '\n# Table of Contents\n\n1.  [Quickstart](#orgc1e985f)\n    1.  [Installing](#org8a0e592)\n    2.  [Using](#org155b2b6)\n2.  [Why?](#org5d3a245)\n3.  [How?](#orgfb84d69)\n\n\n\n<a id="orgc1e985f"></a>\n\n# Quickstart\n\n\n<a id="org8a0e592"></a>\n\n## Installing\n\nYou can install using pip.\n\n    pip install maas-api\n\n\n<a id="org155b2b6"></a>\n\n## Using\n\nYou can use the api client the same way you would use the CLI.\n\n    from maas_api import Client\n    \n    client = Client("http://192.0.2.10:/MAAS", api_key="your:api:key")\n    \n    # allocate a machine\n    machine = client.machines.allocate()\n    # start deploy\n    client.machine.deploy(system_id=machine["system_id"])\n    # release the machine\n    client.machine.release(system_id=machine["system_id"])\n\n\n<a id="org5d3a245"></a>\n\n# Why?\n\nThe official MAAS api client library [python-libmaas](https://pypi.org/project/python-libmaas/) did not receive any new\nfunctionality that is available with MAAS.\nThere is however a [CLI](https://github.com/maas/maas/tree/master/src) written in python. This allows all the functionality to\nbe used.\n\n\n<a id="orgfb84d69"></a>\n\n# How?\n\nBy using the same technique as the official CLI. By using the API description\navailable at [/MAAS/api/2.0/describe](file:///MAAS/api/2.0/describe). This allows us to expose the full API\nexposed by the MAAS server and to keep functional parity with the CLI.\n\n',
    'author': 'Jelle Helsen',
    'author_email': 'jelle.helsen@hcode.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jellehelsen/maas-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
