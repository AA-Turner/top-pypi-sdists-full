# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['html_table_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'html-table-parser-python3',
    'version': '0.3.1',
    'description': 'A small and simple HTML table parser not requiring any external dependency.',
    'long_description': "# html-table-parser-python3.5+\n\nThis module consists of just one small class. Its purpose is to parse HTML\ntables without help of external modules. Everything I use is part of python 3.\nInstead of installing this module, you can just copy the class located in\n*parse.py* into your own code.\n\n## How to use\n\nProbably best shown by example using [pyenv](https://github.com/pyenv/pyenv)\nfor convenience:\n\n    pyenv local\n    python ./example_of_usage.py\n\nThe parser returns a nested lists of tables containing rows containing cells\nas strings. Tags in cells are stripped and the tags text content is joined.\nThe console output for parsing all tables on the twitter home page looks\nlike this:\n\n```\n>>> \n[[['', 'Anmelden']],\n [['Land', 'Code', 'Für Kunden von'],\n  ['Vereinigte Staaten', '40404', '(beliebig)'],\n  ['Kanada', '21212', '(beliebig)'],\n  ...\n  ['3424486444', 'Vodafone'],\n  ['Zeige SMS-Kurzwahlen für andere Länder']]]\n```\n\n## CLI\n\nThere is also a command line interface which you can use directly to\ngenerate a CSV:\n\n    ./html_table_converter -u http://web.archive.org/web/20180524092138/http://metal-train.de/index.php/fahrplan.html -o metaltrain\n\nIf you need help for the supported parameters append `-h`:\n\n    ./html_table_converter -h\n\n## Tests\n\nA set of rudimentary tests have been implemented using Python's built-in unittest framework. Tests must be ran on Python 3.X. To run, use the following command:\n\n    python -m unittest\n",
    'author': 'Josua Schmid',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/schmijos/html-table-parser-python3',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
