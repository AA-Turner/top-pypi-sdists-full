# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['convertertools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'convertertools',
    'version': '0.6.1',
    'description': 'Tools for converting python data types',
    'long_description': '# convertertools\n\n<p align="center">\n  <a href="https://github.com/bluetooth-devices/convertertools/actions/workflows/ci.yml?query=branch%3Amain">\n    <img src="https://img.shields.io/github/actions/workflow/status/bluetooth-devices/convertertools/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://convertertools.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/convertertools.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/bluetooth-devices/convertertools">\n    <img src="https://img.shields.io/codecov/c/github/bluetooth-devices/convertertools.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json" alt="Poetry">\n  </a>\n  <a href="https://github.com/astral-sh/ruff">\n    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/convertertools/">\n    <img src="https://img.shields.io/pypi/v/convertertools.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/convertertools.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/convertertools.svg?style=flat-square" alt="License">\n</p>\n\n---\n\n**Documentation**: <a href="https://convertertools.readthedocs.io" target="_blank">https://convertertools.readthedocs.io </a>\n\n**Source Code**: <a href="https://github.com/bluetooth-devices/convertertools" target="_blank">https://github.com/bluetooth-devices/convertertools </a>\n\n---\n\nTools for converting python data types\n\nThese are very simple tools for manipulating python data structures\nto avoid writing out the same code many times in libraries.\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install convertertools`\n\n## Usage\n\nNote that specific types are required for maximum performance.\n\n```python\nfrom convertertools import del_dict_tuple, del_dict_set, pop_dict_tuple, pop_dict_set\n\n# del_dict* raise KeyError on missing keys\ndel_dict_tuple(d, ("a", "b"))\ndel_dict_set(d, {"a", "b"})\n\n# pop_dict* ignores missing keys\npop_dict_tuple(d, ("a", "b"))\npop_dict_set(d, {"a", "b"})\n\n# pop_dict_set_if_none ignores missing keys and only\n# removes them if their value is None\npop_dict_set_if_none(d, {"a", "b"})\n```\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- prettier-ignore-start -->\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tbody>\n    <tr>\n      <td align="center" valign="top" width="14.28%"><a href="https://www.openhomefoundation.org/"><img src="https://avatars.githubusercontent.com/u/109550163?v=4?s=80" width="80px;" alt="Bluetooth Devices"/><br /><sub><b>Bluetooth Devices</b></sub></a><br /><a href="https://github.com/bluetooth-devices/convertertools/commits?author=Bluetooth-Devices" title="Code">💻</a> <a href="#ideas-Bluetooth-Devices" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/bluetooth-devices/convertertools/commits?author=Bluetooth-Devices" title="Documentation">📖</a></td>\n    </tr>\n  </tbody>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-end -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\nThis package was created with\n[Copier](https://copier.readthedocs.io/) and the\n[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)\nproject template.\n',
    'author': 'J. Nick Koston',
    'author_email': 'nick@koston.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bluetooth-devices/convertertools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10',
}
from build_ext import *
build(setup_kwargs)

setup(**setup_kwargs)
