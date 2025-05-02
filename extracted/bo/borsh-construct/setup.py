# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['borsh_construct']

package_data = \
{'': ['*']}

install_requires = \
['construct-typing>=0.5.1,<0.6.0', 'sumtypes>=0.1a5,<0.2']

setup_kwargs = {
    'name': 'borsh-construct',
    'version': '0.1.0',
    'description': 'Python implementation of Borsh serialization, built on the Construct library.',
    'long_description': '# borsh-construct\n\n[![Tests](https://github.com/near/borsh-construct-py/workflows/Tests/badge.svg)](https://github.com/near/borsh-construct-py/actions?workflow=Tests)\n[![Docs](https://github.com/near/borsh-construct-py/workflows/Docs/badge.svg)](https://near.github.io/borsh-construct-py/)\n\n`borsh-construct` is an implementation of the [Borsh](https://borsh.io/) binary serialization format for Python projects.\n\nBorsh stands for Binary Object Representation Serializer for Hashing. It is meant to be used in security-critical projects as it prioritizes consistency, safety, speed, and comes with a strict specification.\n\nRead the [Documentation](https://near.github.io/borsh-construct-py/).\n## Installation\n\n```sh\npip install borsh-construct\n\n```\n\n\n### Development Setup\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Install dev dependencies:\n```sh\npoetry install\n\n```\n3. Install [nox-poetry](https://github.com/cjolowicz/nox-poetry) (note: do not use Poetry to install this, see [here](https://medium.com/@cjolowicz/nox-is-a-part-of-your-global-developer-environment-like-poetry-pre-commit-pyenv-or-pipx-1cdeba9198bd))\n4. Activate the poetry shell:\n```sh\npoetry shell\n\n```\n\n### Quick Tests\n```sh\npytest\n\n```\n\n### Full Tests\n```sh\nnox\n\n```\n',
    'author': 'kevinheavey',
    'author_email': 'kevinheavey123@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/near/borsh-construct-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
