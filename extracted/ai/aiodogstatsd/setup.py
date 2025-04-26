# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiodogstatsd', 'aiodogstatsd.contrib']

package_data = \
{'': ['*']}

extras_require = \
{'aiohttp': ['aiohttp>=3.0'], 'starlette': ['starlette>=0.13']}

setup_kwargs = {
    'name': 'aiodogstatsd',
    'version': '0.16.0.post0',
    'description': 'An asyncio-based client for sending metrics to StatsD with support of DogStatsD extension',
    'long_description': '# aiodogstatsd\n\n[![Build Status](https://github.com/Gr1N/aiodogstatsd/workflows/default/badge.svg)](https://github.com/Gr1N/aiodogstatsd/actions?query=workflow%3Adefault) [![codecov](https://codecov.io/gh/Gr1N/aiodogstatsd/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/aiodogstatsd) ![PyPI](https://img.shields.io/pypi/v/aiodogstatsd.svg?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aiodogstatsd.svg?label=pypi%20downloads) ![GitHub](https://img.shields.io/github/license/Gr1N/aiodogstatsd.svg)\n\nAn asyncio-based client for sending metrics to StatsD with support of [DogStatsD](https://docs.datadoghq.com/developers/dogstatsd/) extension.\n\nLibrary fully tested with [statsd_exporter](https://github.com/prometheus/statsd_exporter) and supports `gauge`, `counter`, `histogram`, `distribution` and `timing` types.\n\n`aiodogstatsd` client by default uses _9125_ port. It\'s a default port for [statsd_exporter](https://github.com/prometheus/statsd_exporter) and it\'s different from _8125_ which is used by default in StatsD and [DataDog](https://www.datadoghq.com/). Initialize the client with the proper port you need if it\'s different from _9125_.\n\n## Installation\n\nJust type:\n\n```sh\n$ pip install aiodogstatsd\n```\n\n## At a glance\n\nJust simply use client as a context manager and send any metric you want:\n\n```python\nimport asyncio\n\nimport aiodogstatsd\n\n\nasync def main():\n    async with aiodogstatsd.Client() as client:\n        client.increment("users.online")\n\n\nasyncio.run(main())\n```\n\nPlease follow [documentation](https://gr1n.github.io/aiodogstatsd) or look at [`examples/`](https://github.com/Gr1N/aiodogstatsd/tree/master/examples) directory to find more examples of library usage, e.g. integration with [`AIOHTTP`](https://aiohttp.readthedocs.io/) or [`Starlette`](https://www.starlette.io) frameworks.\n\n## Contributing\n\nTo work on the `aiodogstatsd` codebase, you\'ll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):\n\n```sh\n$ git clone git@github.com:Gr1N/aiodogstatsd.git\n$ make install\n```\n\nTo run tests and linters use command below:\n\n```sh\n$ make lint && make test\n```\n\nIf you want to run only tests or linters you can explicitly specify which test environment you want to run, e.g.:\n\n```sh\n$ make lint-black\n```\n\n## License\n\n`aiodogstatsd` is licensed under the MIT license. See the license file for details.\n',
    'author': 'Nikita Grishko',
    'author_email': 'gr1n@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gr1N/aiodogstatsd',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
