# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['case_insensitive_dict']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata<4.3']}

setup_kwargs = {
    'name': 'case-insensitive-dictionary',
    'version': '0.2.1',
    'description': 'Typed Python Case Insensitive Dictionary',
    'long_description': '# Case Insensitive Dict\n\nTyped Python Case Insensitive Dictionary\n\n[![Publish](https://github.com/DeveloperRSquared/case-insensitive-dict/actions/workflows/publish.yml/badge.svg)](https://github.com/DeveloperRSquared/case-insensitive-dict/actions/workflows/publish.yml)\n\n[![Python 3.7+](https://img.shields.io/badge/python-3.7+-brightgreen.svg)](#case-insensitive-dict)\n[![PyPI - License](https://img.shields.io/pypi/l/case-insensitive-dictionary.svg)](LICENSE)\n[![PyPI - Version](https://img.shields.io/pypi/v/case-insensitive-dictionary.svg)](https://pypi.org/project/case-insensitive-dictionary)\n\n[![CodeQL](https://github.com/DeveloperRSquared/case-insensitive-dict/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/DeveloperRSquared/case-insensitive-dict/actions/workflows/codeql-analysis.yml)\n[![codecov](https://codecov.io/gh/DeveloperRSquared/case-insensitive-dict/branch/main/graph/badge.svg?token=45JCHX8KT9)](https://codecov.io/gh/DeveloperRSquared/case-insensitive-dict)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DeveloperRSquared/case-insensitive-dict/main.svg)](https://results.pre-commit.ci/latest/github/DeveloperRSquared/case-insensitive-dict/main)\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n## Install\n\nInstall and update using [pip](https://pypi.org/project/case-insensitive-dictionary/).\n\n```sh\n$ pip install -U case-insensitive-dictionary\n```\n\n## API Reference\n\n| Method                    | Description                                                                                                                                         |\n| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------- |\n| clear()                   | Removes all elements from the dictionary.                                                                                                           |\n| copy()                    | Returns a copy of the dictionary.                                                                                                                   |\n| get(key, default)         | Returns the value (case-insensitively), of the item specified with the key.<br>Falls back to the default value if the specified key does not exist. |\n| fromkeys(iterable, value) | Returns a dictionary with the specified keys and the specified value.                                                                               |\n| keys()                    | Returns the dictionary\'s keys.                                                                                                                      |\n| values()                  | Returns the dictionary\'s values.                                                                                                                    |\n| items()                   | Returns the key-value pairs.                                                                                                                        |\n| pop(key)                  | Remove the specified item (case-insensitively).<br>The value of the removed item is the return value.                                               |\n| popitem()                 | Remove the last item that was inserted into the dictionary.<br>For Python version <3.7, popitem() removes a random item.                            |\n\n## Example\n\nCaseInsensitiveDict:\n\n```py\n>>> from typing import Union\n\n>>> from case_insensitive_dict import CaseInsensitiveDict\n\n>>> case_insensitive_dict = CaseInsensitiveDict[Union[str, int], str](data={"Aa": "b", 1: "c"})\n>>> case_insensitive_dict["aa"]\n\'b\'\n>>> case_insensitive_dict[1]\n\'c\'\n\n```\n\nwhich also supports json encoding/decoding:\n\n```py\n>>> import json\n\n>>> from case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveDictJSONEncoder, case_insensitive_dict_json_decoder\n\n>>> case_insensitive_dict = CaseInsensitiveDict[str, str](data={"Aa": "b"})\n>>> json_string = json.dumps(obj=case_insensitive_dict, cls=CaseInsensitiveDictJSONEncoder)\n>>> json_string\n\'{"Aa": "b"}\'\n\n>>> case_insensitive_dict = json.loads(s=json_string, object_hook=case_insensitive_dict_json_decoder)\n>>> case_insensitive_dict\nCaseInsensitiveDict({\'Aa\': \'b\'})\n```\n\n## Contributing\n\nContributions are welcome via pull requests.\n\n### First time setup\n\n```sh\n$ git clone git@github.com:DeveloperRSquared/case-insensitive-dict.git\n$ cd case-insensitive-dict\n$ poetry install\n$ poetry shell\n```\n\nTools including black, mypy etc. will run automatically if you install [pre-commit](https://pre-commit.com) using the instructions below\n\n```sh\n$ pre-commit install\n$ pre-commit run --all-files\n```\n\n### Running tests\n\n```sh\n$ poetry run pytest\n```\n\n## Links\n\n- Source Code: <https://github.com/DeveloperRSquared/case-insensitive-dict/>\n- PyPI Releases: <https://pypi.org/project/case-insensitive-dictionary/>\n- Issue Tracker: <https://github.com/DeveloperRSquared/case-insensitive-dict/issues/>\n',
    'author': 'rikhilrai',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeveloperRSquared/case-insensitive-dict',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
