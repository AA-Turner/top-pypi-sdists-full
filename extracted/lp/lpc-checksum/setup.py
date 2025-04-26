# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lpc_checksum']

package_data = \
{'': ['*']}

install_requires = \
['intelhex>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['lpc_checksum = lpc_checksum:run']}

setup_kwargs = {
    'name': 'lpc-checksum',
    'version': '3.0.0',
    'description': 'Python script to calculate LPC firmware checksums',
    'long_description': '# lpc_checksum\nPython script to calculate LPC firmware checksums, based on the C version by\nRoel Verdult. It can be used as a standalone application, or as a Python module\nthat integrates directly in a build environment (e.g. SCons). It does not need\nto be compiled.\n\n[![Linting](https://github.com/basilfx/lpc_checksum/actions/workflows/lint.yml/badge.svg)](https://github.com/basilfx/lpc_checksum/actions/workflows/lint.yml)\n[![Testing](https://github.com/basilfx/lpc_checksum/actions/workflows/test.yml/badge.svg)](https://github.com/basilfx/lpc_checksum/actions/workflows/test.yml)\n[![PyPI version](https://badge.fury.io/py/lpc-checksum.svg)](https://badge.fury.io/py/lpc-checksum)\n\n## Requirements\nThe only requirement is Python 3.9 or newer.\n\n## Installation\nThis module can be installed from Pypi via `pip install lpc_checksum`.\n\nAlternatively, you can install the latest version by cloning this repository\nand run `python setup.py install`.\n\n## Usage\nThere are two ways of using `lpc_checksum`.\n\n### Standalone\nWhen installed via Pip or from source, the command `lpc_checksum` should be\navailable on your PATH. By default, it assumes the input file is a binary file.\n\n`lpc_checksum <firmware.bin|hex> [--format=bin] [--read-only]`\n\nProgram exits with a non-zero error code when it failed.\n\n### As a module\n```\nimport lpc_checksum\n\nchecksum = lpc_checksum.checksum(input_file, [read_only=True])\n```\n\nOn error, an exception will be raised.\n\n## Tests\nTo run the tests, please clone this repository and run `poetry run pytest`.\n\n## Contributing\nSee the [`CONTRIBUTING.md`](CONTRIBUTING.md) file.\n\n## License\nSee the [`LICENSE.md`](LICENSE.md) file (MIT license).\n',
    'author': 'Bas Stottelaar',
    'author_email': 'basstottelaar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/basilfx/lpc_checksum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
