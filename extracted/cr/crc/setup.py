# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['crc']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['crc = crc._crc:main']}

setup_kwargs = {
    'name': 'crc',
    'version': '7.1.0',
    'description': 'Pure Python CRC library',
    'long_description': '<h1 align="center">CRC</h1>\n<p align="center">\n\nCalculate CRC checksums, verify CRC checksum, predefined CRC configurations, custom CRC configurations\n</p>\n\n<p align="center">\n\n<a href="https://github.com/Nicoretti/crc/actions">\n    <img src="https://img.shields.io/github/checks-status/nicoretti/crc/master" alt="Checks Master">\n</a>\n<a href="https://coveralls.io/github/Nicoretti/crc">\n    <img src="https://img.shields.io/coverallsCoverage/github/Nicoretti/crc" alt="Coverage">\n</a>\n<a href="https://opensource.org/licenses/BSD-2-Clause">\n    <img src="https://img.shields.io/pypi/l/crc" alt="License">\n</a>\n<a href="https://pypi.org/project/crc/">\n    <img src="https://img.shields.io/pypi/dm/crc" alt="Downloads">\n</a>\n<a href="https://pypi.org/project/crc/">\n    <img src="https://img.shields.io/pypi/pyversions/crc" alt="Supported Python Versions">\n</a>\n<a href="https://pypi.org/project/crc/">\n    <img src="https://img.shields.io/pypi/v/crc" alt="PyPi Package">\n</a>\n</p>\n\n---\n* Documentation: [https://nicoretti.github.io/crc](https://nicoretti.github.io/crc)\n* Source Code: [https://github.com/Nicoretti/crc](https://github.com/Nicoretti/crc)\n---\n\n## Available CRC Configurations\nFor convenience various frequently used crc configurations ship with the library out of the box.\n\n| CRC8          | CRC16    | CRC32   | CRC64 |\n|---------------|----------|---------|-------|\n| CCITT         | XMODEM   | CRC32   | CRC64 |\n| AUTOSAR       | GSM      | AUTOSAR |       |\n| SAEJ1850      | PROFIBUS | BZIP2   |       |\n| SAEJ1850_ZERO | MODBUS   | POSIX   |       |\n| BLUETOOTH     | IBM-3740 |         |       |\n| MAXIM-DOW     | KERMIT   |         |       | \n\nIf you find yourself in the position, where having a new configuration available out of the\nbox would be desirable, feel free to create a [PR](https://github.com/Nicoretti/crc/pulls) or file an [issue](https://github.com/Nicoretti/crc/issues).\n\n## Custom Configurations\n\nIf you want to create a custom configuration, you should have the following information available:\n\n🗒 Note:\n\n    This library currently only supports bit widths of full bytes 8, 16, 24, 32, ...\n\n* **width**\n* **polynom**\n* **init value**\n* **final xor value**\n* **reversed input**\n* **reversed output**\n\nIn case you only have a name of a specific crc configuration/algorithm and you are unsure what are the specific parameters\nof it, a look into this [crc-catalogue](http://reveng.sourceforge.net/crc-catalogue/all.htm) might help.\n\n\n## Requirements\n* [\\>= Python 3.8](https://www.python.org)\n\n## Installation\n\n```shell\npip install crc\n```\n\n## Examples\n\n### Create a Calculator\n\n#### Pre defined configuration\n\n```python\nfrom crc import Calculator, Crc8\n\ncalculator = Calculator(Crc8.CCITT)\n```\n#### Custom configuration\n\n```python\nfrom crc import Calculator, Configuration\n\nconfig = Configuration(\n    width=8,\n    polynomial=0x07,\n    init_value=0x00,\n    final_xor_value=0x00,\n    reverse_input=False,\n    reverse_output=False,\n)\n\ncalculator = Calculator(config)\n```\n\n### Calculate a checksum\n\n#### Standard\n\n```python\nfrom crc import Calculator, Crc8\n\nexpected = 0xBC\ndata = bytes([0, 1, 2, 3, 4, 5])\ncalculator = Calculator(Crc8.CCITT)\n\nassert expected == calculator.checksum(data)\n```\n\n#### Optimized for speed\n\n```python\nfrom crc import Calculator, Crc8\n\nexpected = 0xBC\ndata = bytes([0, 1, 2, 3, 4, 5])\ncalculator = Calculator(Crc8.CCITT, optimized=True)\n\nassert expected == calculator.checksum(data)\n```\n\n### Verify a checksum\n\n#### Standard\n\n```python\nfrom crc import Calculator, Crc8\n\nexpected = 0xBC\ndata = bytes([0, 1, 2, 3, 4, 5])\ncalculator = Calculator(Crc8.CCITT)\n\nassert calculator.verify(data, expected)\n```\n\n#### Optimized for speed\n\n```python\nfrom crc import Calculator, Crc8\n\nexpected = 0xBC\ndata = bytes([0, 1, 2, 3, 4, 5])\ncalculator = Calculator(Crc8.CCITT, optimized=True)\n\nassert calculator.verify(data, expected)\n```\n\n### Calculate a checksum with raw registers\n\n#### Register\n\n```python\nfrom crc import Crc8, Register\n\nexpected = 0xBC\ndata = bytes([0, 1, 2, 3, 4, 5])\nregister = Register(Crc8.CCITT)\n\nregister.init()\nregister.update(data)\nassert expected == register.digest()\n```\n#### TableBasedRegister\n\n```python\nfrom crc import Crc8, TableBasedRegister\n\nexpected = 0xBC\ndata = bytes([0, 1, 2, 3, 4, 5])\nregister = TableBasedRegister(Crc8.CCITT)\n\nregister.init()\nregister.update(data)\nassert expected == register.digest()\n```\n\nReferences & Resources\n-----------------------\n* [A Painless guide to crc error detection algorithms](http://www.zlib.net/crc_v3.txt)\n* [CRC-Catalogue](http://reveng.sourceforge.net/crc-catalogue/all.htm)\n',
    'author': 'Nicola Coretti',
    'author_email': 'nico.coretti@gmail.com',
    'maintainer': 'Nicola Coretti',
    'maintainer_email': 'nico.coretti@gmail.com',
    'url': 'https://github.com/Nicoretti/crc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
