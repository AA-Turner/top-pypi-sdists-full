# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classes',
 'classes.contrib',
 'classes.contrib.mypy',
 'classes.contrib.mypy.features',
 'classes.contrib.mypy.semanal',
 'classes.contrib.mypy.typeops',
 'classes.contrib.mypy.validation',
 'classes.contrib.mypy.validation.validate_instance']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=3.10,<5.0']

setup_kwargs = {
    'name': 'classes',
    'version': '0.4.1',
    'description': 'Smart, pythonic, ad-hoc, typed polymorphism for Python',
    'long_description': '# classes\n\n[![classes logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/classes.png)](https://github.com/dry-python/classes)\n\n-----\n\n[![Build Status](https://travis-ci.org/dry-python/classes.svg?branch=master)](https://travis-ci.org/dry-python/classes)\n[![codecov](https://codecov.io/gh/dry-python/classes/branch/master/graph/badge.svg)](https://codecov.io/gh/dry-python/classes)\n[![Documentation Status](https://readthedocs.org/projects/classes/badge/?version=latest)](https://classes.readthedocs.io/en/latest/?badge=latest)\n[![Python Version](https://img.shields.io/pypi/pyversions/classes.svg)](https://pypi.org/project/classes/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n[![Telegram chat](https://img.shields.io/badge/chat-join-blue?logo=telegram)](https://t.me/drypython)\n\n-----\n\nSmart, pythonic, ad-hoc, typed polymorphism for Python.\n\n\n## Features\n\n- Provides a bunch of primitives to write declarative business logic\n- Enforces better architecture\n- Fully typed with annotations and checked with `mypy`, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Allows to write a lot of simple code without inheritance or interfaces\n- Pythonic and pleasant to write and to read (!)\n- Easy to start: has lots of docs, tests, and tutorials\n\n\n## Installation\n\n```bash\npip install classes\n```\n\nYou also need to [configure](https://classes.readthedocs.io/en/latest/pages/container.html#type-safety)\n`mypy` correctly and install our plugin:\n\n```ini\n# In setup.cfg or mypy.ini:\n[mypy]\nplugins =\n  classes.contrib.mypy.classes_plugin\n```\n\n**Without this step**, your project will report type-violations here and there.\n\nWe also recommend to use the same `mypy` settings [we use](https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/mypy.toml).\n\nMake sure you know how to get started, [check out our docs](https://classes.readthedocs.io/en/latest/)!\n\n\n## Example\n\nImagine, that you want to bound implementation to some particular type.\nLike, strings behave like this, numbers behave like that, and so on.\n\nThe good realworld example is `djangorestframework`.\nIt is build around the idea that different\ndata types should be converted differently to and from `json` format.\n\nWhat is the "traditional" (or outdated if you will!) approach?\nTo create tons of classes for different data types and use them.\n\nThat\'s how we end up with classes like so:\n\n```python\nclass IntField(Field):\n    def from_json(self, value):\n        return value\n\n    def to_json(self, value):\n        return value\n```\n\nIt literally has a lot of problems:\n\n- It is hard to type this code. How can I be sure that my `json` is parseable by the given schema?\n- It produces a lot of boilerplate\n- It has complex API: there are usually several methods to override, some fields to adjust. Moreover, we use a class, not a simple function\n- It is hard to extend the default library for new custom types you will have in your own project\n- It is hard to override\n\nThere should be a better way of solving this problem!\nAnd typeclasses are a better way!\n\nHow would new API look like with this concept?\n\n```python\n>>> from typing import Union\n>>> from classes import typeclass\n\n>>> @typeclass\n... def to_json(instance) -> str:\n...     """This is a typeclass definition to convert things to json."""\n\n>>> @to_json.instance(int)\n... @to_json.instance(float)\n... def _to_json_int(instance: Union[int, float]) -> str:\n...     return str(instance)\n\n>>> @to_json.instance(bool)\n... def _to_json_bool(instance: bool) -> str:\n...     return \'true\' if instance else \'false\'\n\n>>> @to_json.instance(list)\n... def _to_json_list(instance: list) -> str:\n...     return \'[{0}]\'.format(\n...         \', \'.join(to_json(list_item) for list_item in instance),\n...     )\n\n```\n\nSee how easy it is to works with types and implementation?\n\nTypeclass is represented as a regular function, so you can use it like one:\n\n```python\n>>> to_json(True)\n\'true\'\n>>> to_json(1)\n\'1\'\n>>> to_json([False, 1, 2.5])\n\'[false, 1, 2.5]\'\n\n```\n\nAnd it easy to extend this typeclass with your own classes as well:\n\n```python\n# Pretending to import the existing library from somewhere:\n# from to_json import to_json\n\n>>> import datetime as dt\n\n>>> @to_json.instance(dt.datetime)\n... def _to_json_datetime(instance: dt.datetime) -> str:\n...     return instance.isoformat()\n\n>>> to_json(dt.datetime(2019, 10, 31, 12, 28, 00))\n\'2019-10-31T12:28:00\'\n\n```\n\nThat\'s how simple, safe, and powerful typeclasses are!\nMake sure to [check out our full docs](https://github.com/dry-python/classes) to learn more.\n\n\n## More!\n\nWant more? [Go to the docs!](https://classes.readthedocs.io) Or read these articles:\n- [Typeclasses in Python](https://sobolevn.me/2021/06/typeclasses-in-python)\n\n\n<p align="center">&mdash; ⭐️ &mdash;</p>\n<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>\n<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>\n',
    'author': 'sobolevn',
    'author_email': 'mail@sobolevn.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://classes.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
