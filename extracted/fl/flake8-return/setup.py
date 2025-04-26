# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_return', 'flake8_return.mixins']

package_data = \
{'': ['*']}

install_requires = \
['flake8-plugin-utils>=1.0,<2.0']

entry_points = \
{'flake8.extension': ['R50 = flake8_return.plugin:ReturnPlugin']}

setup_kwargs = {
    'name': 'flake8-return',
    'version': '1.2.0',
    'description': 'Flake8 plugin that checks return values',
    'long_description': '# flake8-return\n\n[![pypi](https://badge.fury.io/py/flake8-return.svg)](https://pypi.org/project/flake8-return)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-return)\n[![Downloads](https://img.shields.io/pypi/dm/flake8-return.svg)](https://pypistats.org/packages/flake8-return)\n[![Build Status](https://travis-ci.org/Afonasev/flake8-return.svg?branch=master)](https://travis-ci.org/Afonasev/flake8-return)\n[![Code coverage](https://codecov.io/gh/afonasev/flake8-return/branch/master/graph/badge.svg)](https://codecov.io/gh/afonasev/flake8-return)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nFlake8 plugin that checks return values.\n\n## Installation\n\n```bash\npip install flake8-return\n```\n\n## Errors\n\n* R501 do not explicitly return None in function if it is the only possible return value.\n\n```python\ndef x(y):\n    if not y:\n        return\n    return None  # error!\n```\n\n* R502 do not implicitly return None in function able to return non-None value.\n\n```python\ndef x(y):\n    if not y:\n        return  # error!\n    return 1\n```\n\n* R503 missing explicit return at the end of function able to return non-None value.\n\n```python\ndef x(y):\n    if not y:\n        return 1\n    # error!\n```\n\n* R504 unnecessary variable assignment before return statement.\n\n```python\ndef x():\n    a = 1\n    # some code that not using `a`\n    print(\'test\')\n    return a  # error!\n```\n\n* R505 unnecessary else after return statement.\n\n```python\ndef x(y, z):\n    if y:  # error!\n        return 1\n    else:\n        return z\n```\n\n* R506 unnecessary else after raise statement.\n\n```python\ndef x(y, z):\n    if y:  # error!\n        raise Exception(y)\n    else:\n        raise Exception(z)\n```\n\n* R507 unnecessary else after continue statement.\n\n```python\ndef x(y, z):\n    for i in y:\n        if i < z:  # error!\n            continue\n        else:\n            a = 0\n```\n\n* R508 unnecessary else after break statement.\n\n```python\ndef x(y, z):\n    for i in y:\n        if i > z:  # error!\n            break\n        else:\n            a = 0\n```\n\nReturns in asyncio coroutines also supported.\n\n## For developers\n\n### Show help\n\n    make help\n\n### Create venv and install deps\n\n    make init\n\n### Install git precommit hook\n\n    make precommit\n\n### Run linters, autoformat, tests etc\n\n    make pretty lint test\n\n### Bump new version\n\n    make bump_major\n    make bump_minor\n    make bump_patch\n\n## Change Log\n\nUnreleased\n-----\n\n* ...\n\n1.2.0 - 2022-10-28\n-----\n\n* Port no-else-break, no-else-continue, no-else-raise, no-else-return from pylint (#122) Calum Young\n* PEP 621: Migrate more config to pyproject.toml (#123) Christian Clauss\n* Fix/116/R504-try-except (#120) Calum Young\n* Update ci (#119) Calum Young\n* Fix/47/Update-R504-for-assignment-value (#117) Calum Young\n* Upgrade GitHub Actions (#113) Christian Clauss\n* Add a space to avoid a typo in R503 (#98) Christian Clauss\n* GitHub Action to lint Python code (#97) Christian Clauss\n* Typo fixes (#92) Aarni Koskela\n* Create codeql-analysis.yml Afonasev Evgeniy\n* Bump flake8-plugin-utils from 1.1.1 to 1.3.2 (#87) dependabot\n* Bump mypy from 0.812 to 0.971 (#114) dependabot\n* Bump pytest-cov from 3.0.0 to 4.0.0 (#124) dependabot\n* Bump pytest-cov from 2.11.1 to 3.0.0 (#102) dependabot\n* Bump pytest-mock from 3.6.0 to 3.6.1 (#91) dependabot\n* Bump pytest from 6.2.4 to 6.2.5 (#99) dependabot\n* Bump pylint from 2.8.2 to 2.10.2 (#100) dependabot\n* Bump pytest from 6.2.3 to 6.2.4 (#86) dependabot\n\n1.1.3 - 2021-05-05\n-----\n\n* Error clarifications (#77) Clément Robert\n* fix linting (migrate to black 20.0b1) (#78) Clément Robert\n\n1.1.2 - 2020-07-09\n-----\n\n* Make R504 visitors handle while loops (#56) Frank Tackitt\n* Rename allows-prereleases to allow-prereleases (#55) Frank Tackitt\n* Fix typo: → haven\'t (#24) Jon Dufresne\n\n1.1.1 - 2019-09-21\n-----\n\n* fixed [#3](https://github.com/afonasev/flake8-return/issues/3) The R504 doesn\'t detect that the variable is modified in loop\n* fixed [#4](https://github.com/afonasev/flake8-return/issues/4) False positive with R503 inside async with clause\n\n1.1.0 - 2019-05-23\n-----\n\n* update flask_plugin_utils version to 1.0\n\n1.0.0 - 2019-05-13\n-----\n\n* skip assign after unpacking while unnecessary assign checking "(x, y = my_obj)"\n\n0.3.2 - 2019-04-01\n-----\n\n* allow "assert False" as last function return\n\n0.3.1 - 2019-03-11\n-----\n\n* add pypi deploy into travis config\n* add make bump_version command\n\n0.3.0 - 2019-02-26\n-----\n\n* skip functions that consist only `return None`\n* fix false positive when last return inner with statement\n* add unnecessary assign error\n* add support tuple in assign or return expressions\n* add support asyncio coroutines\n\n0.2.0 - 2019-02-21\n-----\n\n* fix explicit/implicit\n* add flake8-plugin-utils as dependency\n* allow raise as last function return\n* allow no return as last line in while block\n* fix if/elif/else cases\n\n0.1.1 - 2019-02-10\n-----\n\n* fix error messages\n\n0.1.0 - 2019-02-10\n-----\n\n* initial\n',
    'author': 'Afonasev Evgeniy',
    'author_email': 'ea.afonasev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/flake8-return',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
