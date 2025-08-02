# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_logger']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.4.1,<4.0.0']

setup_kwargs = {
    'name': 'asgi-logger',
    'version': '0.1.0',
    'description': 'Middleware based uvicorn access logger! :tada:',
    'long_description': '<h1 align="center">\n    <strong>asgi-logger</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/asgi-logger" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/asgi-logger" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/asgi-logger/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/asgi-logger">\n    <br />\n    <a href="https://pypi.org/project/asgi-logger" target="_blank">\n        <img src="https://img.shields.io/pypi/v/asgi-logger" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/asgi-logger">\n    <img src="https://img.shields.io/github/license/Kludex/asgi-logger">\n</p>\n\n\n## Installation\n\n``` bash\npip install asgi-logger\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/asgi-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
