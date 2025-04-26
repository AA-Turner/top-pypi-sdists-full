# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbsqlcli',
 'dbsqlcli.packages',
 'dbsqlcli.packages.literals',
 'dbsqlcli.packages.special',
 'dbsqlcli.packages.tabular_output']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=1.6',
 'cli_helpers[styles]>=1.1.0',
 'click>=7.0',
 'configobj>=5.0.5',
 'databricks-sql-connector==v2.0.0b1',
 'prompt_toolkit>=2.0.6,<3.0.0',
 'sqlparse>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['dbsqlcli = dbsqlcli.main:cli']}

setup_kwargs = {
    'name': 'dbsqlcli',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
