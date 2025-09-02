# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ndicts']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=9.0.0,<10.0.0']

setup_kwargs = {
    'name': 'ndicts',
    'version': '0.3.0',
    'description': 'Class to handle nested dictionaries',
    'long_description': '# Description\nNested dictionary structures emerge every time there is some sort hierarchy\nin the data. Trees, archives, the chapters and sections in a book, \nthese are all examples where you will likely find nested loops of data.\n\nPython does not have a built-in data type for nested mappings. \nDictionaries can be used, however there many inconveniences and limitations.\nTwo above all: getting items requires to open and close several square brackets \n(eg. `d[level1][level2]...[levelN]`), \nand iterating will only access the first layer, \nso nested for loops are needed to iterate through all the values.\n\nThe `ndicts` package aims to tackle the main issues of nested dictionaries, \nexposing an interface with minimum differences from dictionaries themselves.\n`NestedDict` is a `MutableMapping` at its core, \ntherefore all familiar dictionary methods are available \nand the overall behaviour similar.\n\nIf you need to perform simple mathematical operations with your nested data,\nuse `DataDict`. In addition to allowing arithmetics, \n`DataDicts` borrow some methods that you would expect from a `pandas` `DataFrame`. \n\nFinally, this is a simple project for simple needs. \nConsider using `pandas` `MultiIndex` for more functionalities!\n\n# Installation\n\nInstall `ndicts` with `pip`.\n\n```commandline\npip install ndicts\n```\n\n# Overview\n\nImport `NestedDict` and `DataDict`.\n\n```pycon\n>>> from ndicts import DataDict, NestedDict\n```\n\nCreate a `NestedDict` from a dictionary.\n\n```pycon\n>>> book = {\n...     "Book 1": {\n...         "Section 1": "The Eve of the War",\n...         "Section 2": "The Falling Star"\n...     },\n...     "Book 2": {\n...         "Section 1": "Under Foot", \n...         "Section 2": {"Paragraph 1": "After eating we crept back to the scullery"}\n...     }\n... }\n>>> nd = NestedDict(book)\n```\n\nGet items more conveniently than with standard dictionaries.\n\n```pycon\n>>> # NestedDict\n>>> nd["Book 1", "Section 1"] \n\'The Eve of the War\'\n>>> # dict\n>>> book["Book 1"]["Section 2"]\n\'The Falling Star\'\n```\n\nIterate over a `NestedDict`.\n\n```pycon\n>>> for key in nd:\n...     print(key)\n(\'Book 1\', \'Section 1\')\n(\'Book 1\', \'Section 2\')\n(\'Book 2\', \'Section 1\')\n(\'Book 2\', \'Section 2\', \'Paragraph 1\')\n```\n\n# Documentation\n\nhttps://edd313.github.io/ndicts/\n\n# Licence\n`ndicts` is licensed under the MIT license.\n\n\n\n',
    'author': 'Edoardo Cicirello',
    'author_email': 'e.cicirello@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/edd313/ndicts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
