# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flake8_breakpoint']

package_data = \
{'': ['*']}

install_requires = \
['flake8-plugin-utils>=1.0,<2.0']

entry_points = \
{u'flake8.extension': ['B60 = flake8_breakpoint.plugin:BreakpointPlugin']}

setup_kwargs = {
    'name': 'flake8-breakpoint',
    'version': '1.1.0',
    'description': 'Flake8 plugin that check forgotten breakpoints',
    'long_description': '# flake8-breakpoint\n\n[![pypi](https://badge.fury.io/py/flake8-breakpoint.svg)](https://pypi.org/project/flake8-breakpoint)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-breakpoint)\n[![Downloads](https://img.shields.io/pypi/dm/flake8-breakpoint.svg)](https://pypistats.org/packages/flake8-breakpoint)\n[![Build Status](https://travis-ci.org/Afonasev/flake8-breakpoint.svg?branch=master)](https://travis-ci.org/Afonasev/flake8-breakpoint)\n[![Code coverage](https://codecov.io/gh/afonasev/flake8-breakpoint/branch/master/graph/badge.svg)](https://codecov.io/gh/afonasev/flake8-breakpoint)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nFlake8 plugin that check forgotten breakpoints.\n\n## Installation\n\n```bash\npip install flake8-breakpoint\n```\n\n## Errors\n\n* B601 builtin function "breakpoint" found\n\n```python\ndef function():\n    breakpoint()  # error!\n```\n\n* B602 import of debug module found\n\n```python\ndef function():\n    import pdb  # error! or ipdb/pudb\n```\n\n## License\n\nMIT\n\n## Change Log\n\nUnreleased\n-----\n\n* ...\n\n1.1.0 - 2019-05-23\n-----\n\n* update flask_plugin_utils version to 1.0\n\n1.0.0 - 2019-04-02\n-----\n\n* initial\n',
    'author': 'Evgeniy Afonasev',
    'author_email': 'ea.afonasev@gmail.com',
    'url': 'https://pypi.org/project/flake8-breakpoint',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
