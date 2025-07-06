# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpeparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cpeparser',
    'version': '0.0.2',
    'description': 'CPE - Common platform enumeration parser in Python',
    'long_description': '\n# Cpe-parser\n\nThe cpe-parser libray is a parses for CPE value. This cpe value can be either uri biding cpe or formatted binding value.\n\n\n###  🔨  Installation ###\n\n```sh\n $ pip install cpe-parser\n```\n\n\n### Guide\n\n\n```python\nfrom cpeparser import CpeParser\ncpe = CpeParser()\nresult = cpe.parser("cpe:2.3:a:ipython:ipython:*:*:*:*:*:*:*:*")\nprint(result)\n{\n    \'part\': \'a\',\n    \'vendor\': \'ipython\',\n    \'product\': \'ipython\',\n    \'version\': \'*\',\n    \'update\': \'*\',\n    \'edition\': \'*\',\n    \'language\': \'*\',\n    \'sw_edition\': \'*\',\n    \'target_sw\': \'*\',\n    \'target_hw\': \'*\',\n    \'other\': \'*\'\n}\n```\nDefault values are returned as asterisks \'*\' that represent ANY.\n\n### NIST Documentation\nThis library follows the guidelines outline here: \nhttps://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7695.pdf',
    'author': 'sabuhish',
    'author_email': 'sabuhi.shukurov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sabuhish/cpe-parser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.12,<4.0.0',
}


setup(**setup_kwargs)
