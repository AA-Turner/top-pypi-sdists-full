# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_databind_json_proxy']

package_data = \
{'': ['*']}

install_requires = \
['databind>=4.5.2,<5.0.0']

setup_kwargs = {
    'name': 'databind.json',
    'version': '4.5.2',
    'description': 'De-/serialize Python dataclasses to or from JSON payloads. Compatible with Python 3.8 and newer. Deprecated, use `databind` module instead.',
    'long_description': '\nDeprecated since v4.5.0. This is a proxy for depending on [`databind`](https://pypi.org/project/databind/). Do not\ndepend on this package directly anymore.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
