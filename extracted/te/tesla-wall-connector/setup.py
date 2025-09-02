# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tesla_wall_connector']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'backoff>=1.11.1']

setup_kwargs = {
    'name': 'tesla-wall-connector',
    'version': '1.0.2',
    'description': 'API Library for communicating with a Tesla Wall Connector',
    'long_description': '# Python Tesla Wall Connector API <!-- omit in TOC -->\n\nPython Tesla Wall Connector API for local consumption. This package allows you to monitor your 3rd generation Tesla Wall Connector programmatically. It is mainly created to enable integration with Home Assistant and threfore exposes an asynchronous API.\n\n## Usage\n\n```python\nimport asyncio\nfrom tesla_wall_connector import WallConnector\nasync def main():\n    async with WallConnector(\'TeslaWallConnector_ABC123.localdomain\') as wall_connector:\n        lifetime = await wall_connector.async_get_lifetime()\n        print("energy_wh: {}Wh".format(lifetime.energy_wh))\n\nasyncio.run(main())\n```\n\n## Setting up development environment\n\nThis Python project is fully managed using the [Poetry][poetry] dependency\nmanager.\n\nYou need at least:\n\n- Python 3.8+\n- [Poetry][poetry-install]\n\nTo install all packages, including all development requirements:\n\n```bash\npoetry install\n```\n\nAs this repository uses the [pre-commit][pre-commit] framework, all changes\nare linted and tested with each commit. You can run all checks and tests\nmanually, using the following command:\n\n```bash\npoetry run pre-commit run --all-files\n```\n\nTo run the Python tests:\n\n```bash\npoetry run pytest\n```\n',
    'author': 'Einar Bragi Hauksson',
    'author_email': 'einar.hauksson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/einarhauks/tesla-wall-connector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
