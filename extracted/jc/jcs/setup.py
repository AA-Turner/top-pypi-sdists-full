# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jcs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jcs',
    'version': '0.2.1',
    'description': 'JCS - JSON Canonicalization',
    'long_description': '# JCS - JSON Canonicalization for Python 3\n\n[![Tests](https://github.com/titusz/jcs/actions/workflows/tests.yml/badge.svg)](https://github.com/titusz/jcs/actions/workflows/tests.yml)\n\nThis is a Python 3 package for\na [JCS (RFC 8785)](https://datatracker.ietf.org/doc/html/rfc8785) compliant JSON\ncanonicalization.\n\nThe main author of this code is [Anders Rundgren](https://github.com/cyberphone). The\noriginal source code is\nat [cyberphone/json-canonicalization](https://github.com/cyberphone/json-canonicalization/tree/master/python3)\nincluding comprehensive test data.\n\n## Installation\n\n```bash\n$ pip install jcs\n```\n\n## Using JCS\n\n```python\nimport jcs\ndata = jcs.canonicalize({"tag": 4})\n```\n',
    'author': 'titusz',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/titusz/jcs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
