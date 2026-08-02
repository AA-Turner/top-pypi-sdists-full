# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_inet']

package_data = \
{'': ['*']}

entry_points = \
{'markdown.extensions': ['pymdgen = pymdgen.md:Extension']}

setup_kwargs = {
    'name': 'django-inet',
    'version': '1.1.1',
    'description': 'django internet utilities',
    'long_description': '\n# django-inet\n\n[![PyPI](https://img.shields.io/pypi/v/django-inet.svg?maxAge=3600)](https://pypi.python.org/pypi/django-inet)\n[![PyPI](https://img.shields.io/pypi/pyversions/django-inet.svg)](https://pypi.python.org/pypi/django-inet)\n[![Tests](https://github.com/20c/django-inet/workflows/tests/badge.svg)](https://github.com/20c/django-inet)\n[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/20c/django-inet)](https://lgtm.com/projects/g/20c/django-inet/alerts/)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/django-inet/master.svg?maxAge=3600)](https://codecov.io/github/20c/django-inet)\n\n\ndjango internet utilities\n\n\n## Provides\n\n```py\nASNField()\nIPAddressField(version=None)\nIPNetworkField(version=None)\nMacAddressField()\n```\n\n`IPPrefixField` has been renamed to `IPNetworkField` to conform with other python package names (like `ipaddress`).\n\nAddresses and Prefixes are stored and strings and converted to ipaddress.IPv{4,6}{Address,Prefix} classes.\n\nVersion can be set to 4 or 6 to force a version, or left as None to use\neither.\n\n## Quickstart\n\nInstall django-inet\n\n```sh\npip install django-inet\n```\n\nThen use it in a project\n\n```py\nimport django_inet\n```\n\n\n## License\n\nCopyright 2014-2021 20C, LLC\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this software except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.',
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/django-inet',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
