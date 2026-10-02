# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_new_union_types']
install_requires = \
['attrs>=21.4.0', 'flake8>=3.0.0']

entry_points = \
{'flake8.extension': ['NU = flake8_new_union_types:PEP604Checker']}

setup_kwargs = {
    'name': 'flake8-new-union-types',
    'version': '0.4.1',
    'description': 'Flake8 plugin to enforce the new Union and Optional annotation syntax defined in PEP 604',
    'long_description': '# flake8-new-union-types\n[![Build Status](https://github.com/xome4ok/flake8-new-union-types/actions/workflows/check.yml/badge.svg?branch=main)](https://github.com/xome4ok/flake8-new-union-types/actions/workflows/check.yml)\n[![PyPI](https://img.shields.io/pypi/v/flake8-new-union-types)](https://pypi.org/project/flake8-new-union-types/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-new-union-types)](https://pypi.org/project/flake8-new-union-types/)\n[![PyPI - License](https://img.shields.io/pypi/l/flake8-new-union-types)](https://pypi.org/project/flake8-new-union-types/)\n\nFlake8 plugin to enforce the new `Union` and `Optional` annotation syntax defined in [PEP 604](https://peps.python.org/pep-0604/).\n\n```python\nUnion[X, Y] = X | Y\n\nOptional[X] = X | None\n```\n\nNote that it\'s impossible to use forward references in the new syntax, like this:\n\n```python\n"X" | int\n```\n\nsuch a case [can be expressed](https://bugs.python.org/issue45857) as a string containing both union terms:\n\n```python\n"X | int"\n```\n\n## Installation\n\n```\npip install flake8-new-union-types\n```\n\nor if you use [poetry](https://python-poetry.org/):\n\n```\npoetry add --dev flake8-new-union-types\n```\n\n## Usage\n\n## Error list\n\n* NU001 Use `Foo | Bar` syntax instead of Union (PEP 604)\n* NU002 Use `Foo | None` syntax instead of Optional (PEP 604)\n* NU003 Present the whole expression as a string to annotate forward refs, e.g. `"int | Foo"` (PEP 604)\n\n## Configuration\n\nThere is no way to configure the plugin at the moment.\n',
    'author': 'Dmitriy Pryanichnikov',
    'author_email': 'dmitrii.prianichnikov@incountry.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xome4ok/flake8-new-union-types',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
