# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bluetooth_data_tools']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=47.0.0']

extras_require = \
{'docs': ['Sphinx>=5,<9', 'sphinx-rtd-theme>=1,<4', 'myst-parser>=0.18,<4.1']}

setup_kwargs = {
    'name': 'bluetooth-data-tools',
    'version': '1.29.11',
    'description': 'Tools for converting bluetooth data and packets',
    'long_description': '# Bluetooth Data Tools\n\n<p align="center">\n  <a href="https://github.com/bluetooth-devices/bluetooth-data-tools/actions/workflows/ci.yml?query=branch%3Amain">\n    <img src="https://img.shields.io/github/actions/workflow/status/bluetooth-devices/bluetooth-data-tools/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://bluetooth-data-tools.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/bluetooth-data-tools.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/Bluetooth-Devices/bluetooth-data-tools">\n    <img src="https://img.shields.io/codecov/c/github/Bluetooth-Devices/bluetooth-data-tools.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n  <a href="https://codspeed.io/Bluetooth-Devices/bluetooth-data-tools"><img src="https://img.shields.io/endpoint?url=https://codspeed.io/badge.json" alt="CodSpeed Badge"/></a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/bluetooth-data-tools/">\n    <img src="https://img.shields.io/pypi/v/bluetooth-data-tools.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/bluetooth-data-tools.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/bluetooth-data-tools.svg?style=flat-square" alt="License">\n</p>\n\nTools for converting bluetooth data and packets\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install bluetooth-data-tools`\n\n## Usage\n\n### Parsing BLE GAP Advertisement Data\n\nParse raw BLE advertisement bytes into structured data:\n\n```python\nfrom bluetooth_data_tools import parse_advertisement_data_bytes\n\n# Parse raw GAP advertisement bytes\nparsed = parse_advertisement_data_bytes(raw_bytes)\nlocal_name = parsed[0]        # str | None\nservice_uuids = parsed[1]     # list[str]\nservice_data = parsed[2]      # dict[str, bytes]\nmanufacturer_data = parsed[3] # dict[int, bytes]\ntx_power = parsed[4]          # int | None\n```\n\nOr use the object-oriented interface:\n\n```python\nfrom bluetooth_data_tools import BLEGAPAdvertisement, parse_advertisement_data\n\nadv = parse_advertisement_data([raw_bytes1, raw_bytes2])\nprint(adv.local_name)\nprint(adv.service_uuids)\nprint(adv.service_data)\nprint(adv.manufacturer_data)\nprint(adv.tx_power)\n```\n\n### Bluetooth Address Utilities\n\n```python\nfrom bluetooth_data_tools import (\n    int_to_bluetooth_address,\n    mac_to_int,\n    short_address,\n    human_readable_name,\n)\n\n# Convert integer to MAC address\nint_to_bluetooth_address(0x123456789ABC)\n# "12:34:56:78:9A:BC"\n\n# Convert MAC address to integer\nmac_to_int("FF:FF:FF:FF:FF:FF")\n# 281474976710655\n\n# Get short address (last 2 octets)\nshort_address("AA:BB:CC:DD:EE:FF")\n# "EEFF"\n\n# Format a human-readable device name\nhuman_readable_name("My Sensor", "", "AA:BB:CC:DD:EE:FF")\n# "My Sensor (EEFF)"\n```\n\n### Distance Estimation\n\nEstimate distance from TX power and RSSI:\n\n```python\nfrom bluetooth_data_tools import calculate_distance_meters\n\ndistance = calculate_distance_meters(power=-59, rssi=-60)\n# ~1.135 meters\n```\n\n### Monotonic Time\n\nA fast monotonic clock optimized for Bluetooth event timing. On Linux, uses `CLOCK_MONOTONIC_COARSE` via Cython for lower overhead:\n\n```python\nfrom bluetooth_data_tools import monotonic_time_coarse\n\nnow = monotonic_time_coarse()\n```\n\n### Private Address Resolution (RPA)\n\nResolve Bluetooth Low Energy random private addresses using an Identity Resolving Key:\n\n```python\nfrom bluetooth_data_tools import get_cipher_for_irk, resolve_private_address\n\ncipher = get_cipher_for_irk(irk_bytes)  # 16-byte Identity Resolving Key\nis_match = resolve_private_address(cipher, "40:01:02:0A:C4:A6")\n```\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- prettier-ignore-start -->\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- markdownlint-disable -->\n<!-- markdownlint-enable -->\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-end -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\nThis package was created with\n[Cookiecutter](https://github.com/audreyr/cookiecutter) and the\n[browniebroke/cookiecutter-pypackage](https://github.com/browniebroke/cookiecutter-pypackage)\nproject template.\n',
    'author': 'J. Nick Koston',
    'author_email': 'nick@koston.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bdraco/bluetooth-data-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10',
}
from build_ext import *
build(setup_kwargs)

setup(**setup_kwargs)
