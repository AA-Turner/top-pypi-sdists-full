# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['arsenic']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3', 'attrs>=17.4.0', 'structlog>=20.1.0,<21.0.0']

entry_points = \
{'console_scripts': ['arsenic-check-ie11 = '
                     'arsenic.helpers:check_ie11_environment_cli',
                     'arsenic-configure-ie11 = '
                     'arsenic.helpers:configure_ie11_environment_cli']}

setup_kwargs = {
    'name': 'arsenic',
    'version': '21.8',
    'description': 'Asynchronous WebDriver client',
    'long_description': "# Async Webdriver\n\n[![CircleCI](https://circleci.com/gh/HDE/arsenic/tree/main.svg?style=svg)](https://circleci.com/gh/HDE/arsenic/tree/main) [![Documentation Status](https://readthedocs.org/projects/arsenic/badge/?version=latest)](http://arsenic.readthedocs.io/en/latest/?badge=latest)\n[![BrowserStack Status](https://automate.browserstack.com/badge.svg?badge_key=QmtNVHFnWWRFSEVUdTBZNWU5NGMraVorWVltazFqRk1VNWRydW5FRXU2dz0tLVhoTlFuK2tZUTJ1UGx0UmZaWjg4R1E9PQ==--35ef3d28fbf8ea24ee7fa2a435f9271fbaaf85d4)](https://automate.browserstack.com/public-build/QmtNVHFnWWRFSEVUdTBZNWU5NGMraVorWVltazFqRk1VNWRydW5FRXU2dz0tLVhoTlFuK2tZUTJ1UGx0UmZaWjg4R1E9PQ==--35ef3d28fbf8ea24ee7fa2a435f9271fbaaf85d4)\n[![Appveyor status](https://ci.appveyor.com/api/projects/status/8l0koom7h93y1f9q?svg=true)](https://ci.appveyor.com/project/ojii/arsenic)\n[![PyPI version](https://badge.fury.io/py/arsenic.svg)](https://badge.fury.io/py/arsenic)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\n\nAsynchronous webdriver client built on asyncio.\n\n\n## Quickstart\n\nLet's run a local Firefox instance.\n\n\n```python\n\nfrom arsenic import get_session\nfrom arsenic.browsers import Firefox\nfrom arsenic.services import Geckodriver\n\n\nasync def example():\n    # Runs geckodriver and starts a firefox session\n    async with get_session(Geckodriver(), Firefox()) as session:\n          # go to example.com\n          await session.get('http://example.com')\n          # wait up to 5 seconds to get the h1 element from the page\n          h1 = await session.wait_for_element(5, 'h1')\n          # print the text of the h1 element\n          print(await h1.get_text())\n```\n\nFor more information, check [the documentation](https://arsenic.readthedocs.io/)\n\n## CI Supported by Browserstack\n\nContinuous integration for certain browsers is generously provided by [Browserstack](http://browserstack.com).\n\n[![Browserstack](./.circleci/browserstack-logo.png)](http://browserstack.com/)\n",
    'author': 'Jonas Obrist',
    'author_email': 'jonas.obrist@hennge.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HDE/arsenic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
