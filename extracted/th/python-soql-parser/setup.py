# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_soql_parser']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=2.4.7,<3.0.0']

setup_kwargs = {
    'name': 'python-soql-parser',
    'version': '0.2.0',
    'description': 'A pyparsing-based library for parsing SOQL statements',
    'long_description': '**CONTRIBUTORS WANTED!!**\n\n# Installation\n\n`pip install python-soql-parser`\n\nor, with poetry\n\n`poetry add python-soql-parser`\n\n# Usage\n\n```python\nfrom python_soql_parser import parse\n\n\nparse_result = parse("SELECT Id FROM Account")\n```\n\nwhere `parse_result` is a [ParseResults](https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html#parseresults) object from [pyparsing](https://github.com/pyparsing/pyparsing/).\n\n# Notable caveats\n\n## Unsupported features\n\n- Subqueries (e.g., `SELECT Name, (SELECT LastName FROM Contacts) FROM Account`)\n- Aggregate queries\n- SOQL specific WHERE-clause tokens (e.g., `LAST_N_DAYS:<integer>`)\n\n## Partially supported\n\nThese are either partially supported or weakly supported\n\n- Related attributes (e.g., `SELECT Id, Account.Name FROM Contact`). The object name is not yet parsed out on its own. This will simply parse out `"Account.Name"`\n\n# Contributing\n\nA lot of work remains to be done. Practically no SOQL-specific features are supported as of yet.\nIf you want to contribute, just open a PR! (and add a test for your new feature)\n\n## Setting up locally\n\nFirst install [poetry](https://python-poetry.org/). Afterwards, to install the dependencies, run\n\n```\npoetry install\n```\n\n## Running the tests\n\nSimply execute\n\n```\npytest\n```\n\n## House cleaning\n\nPlease sort imports with `isort` and format the code with `black` (in that order).\n',
    'author': 'Alex Drozd',
    'author_email': 'drozdster@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Kicksaw-Consulting/python-soql-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
