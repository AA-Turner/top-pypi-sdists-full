# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['annotatedyaml']

package_data = \
{'': ['*']}

install_requires = \
['propcache>0.1', 'pyyaml>=6.0.1', 'voluptuous>0.15']

setup_kwargs = {
    'name': 'annotatedyaml',
    'version': '1.0.0',
    'description': 'Annotated YAML that supports secrets for Python',
    'long_description': '# annotatedyaml\n\n<p align="center">\n  <a href="https://github.com/home-assistant-libs/annotatedyaml/actions/workflows/ci.yml?query=branch%3Amain">\n    <img src="https://img.shields.io/github/actions/workflow/status/home-assistant-libs/annotatedyaml/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://annotatedyaml.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/annotatedyaml.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/home-assistant-libs/annotatedyaml">\n    <img src="https://img.shields.io/codecov/c/github/home-assistant-libs/annotatedyaml.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://github.com/astral-sh/uv">\n    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">\n  </a>\n  <a href="https://github.com/astral-sh/ruff">\n    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/annotatedyaml/">\n    <img src="https://img.shields.io/pypi/v/annotatedyaml.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/annotatedyaml.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/annotatedyaml.svg?style=flat-square" alt="License">\n</p>\n\n---\n\n**Documentation**: <a href="https://annotatedyaml.readthedocs.io" target="_blank">https://annotatedyaml.readthedocs.io </a>\n\n**Source Code**: <a href="https://github.com/home-assistant-libs/annotatedyaml" target="_blank">https://github.com/home-assistant-libs/annotatedyaml </a>\n\n---\n\nAnnotated YAML that supports secrets for Python\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install annotatedyaml`\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- prettier-ignore-start -->\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- markdownlint-disable -->\n<!-- markdownlint-enable -->\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-end -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\n[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)\n\nThis package was created with\n[Copier](https://copier.readthedocs.io/) and the\n[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)\nproject template.\n',
    'author': 'Home Assistant Devs',
    'author_email': 'hello@home-assistant.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/home-assistant-libs/annotatedyaml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.13',
}
from build_ext import *
build(setup_kwargs)

setup(**setup_kwargs)
