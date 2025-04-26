# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adjust_precision_for_schema']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=2.6.0']

setup_kwargs = {
    'name': 'adjust-precision-for-schema',
    'version': '0.3.4',
    'description': 'Intended for use in singer-io targets to overcome the precision differences among certain data source systems, Python, and target systems',
    'long_description': None,
    'author': 'Datateer',
    'author_email': 'dev@datateer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
