# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynats']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.6.0']}

setup_kwargs = {
    'name': 'nats-python',
    'version': '0.8.0',
    'description': 'Python client for NATS messaging system',
    'long_description': '# nats-python\n\n[![Build Status](https://github.com/Gr1N/nats-python/workflows/default/badge.svg)](https://github.com/Gr1N/nats-python/actions?query=workflow%3Adefault) [![codecov](https://codecov.io/gh/Gr1N/nats-python/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/nats-python) ![PyPI](https://img.shields.io/pypi/v/nats-python.svg?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dm/nats-python.svg?label=pypi%20downloads)\n\nPython client for NATS messaging system.\n\nThis project is a replacement for abandoned [pynats](https://github.com/mcuadros/pynats). `nats-python` supports only Python 3.6+ and fully covered with typings.\n\nGo to the [asyncio-nats](https://github.com/nats-io/asyncio-nats) project, if you\'re looking for `asyncio` implementation.\n\n## Installation\n\n```sh\n$ pip install nats-python\n```\n\n## Usage\n\n```python\nfrom pynats import NATSClient\n\nwith NATSClient() as client:\n    client.publish("test-subject", payload=b"test-payload")\n```\n\n## Contributing\n\nTo work on the `nats-python` codebase, you\'ll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):\n\n```sh\n$ git clone git@github.com:Gr1N/nats-python.git\n$ make install\n```\n\nTo run tests and linters use command below:\n\n```sh\n$ make lint && make test\n```\n\nIf you want to run only tests or linters you can explicitly specify which test environment you want to run, e.g.:\n\n```sh\n$ make lint-black\n```\n\n## License\n\n`nats-python` is licensed under the MIT license. See the license file for details.\n',
    'author': 'Nikita Grishko',
    'author_email': 'gr1n@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gr1N/nats-python',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
