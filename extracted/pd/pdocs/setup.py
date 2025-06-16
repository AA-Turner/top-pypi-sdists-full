# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdocs']

package_data = \
{'': ['*'], 'pdocs': ['templates/*']}

install_requires = \
['Mako>1.2.2', 'Markdown>=3.0.0', 'docstring_parser>=0.7.2', 'hug>=2.6']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7']}

entry_points = \
{'console_scripts': ['pdocs = pdocs.cli:__hug__.cli']}

setup_kwargs = {
    'name': 'pdocs',
    'version': '1.2.0',
    'description': 'A simple program and library to auto generate API documentation for Python modules.',
    'long_description': "[![pdocs - Documentation Powered by Your Python Code.](https://raw.github.com/timothycrosley/pdocs/master/art/logo_large.png)](https://timothycrosley.github.io/pdocs/)\n_________________\n\n[![PyPI version](https://badge.fury.io/py/pdocs.svg)](http://badge.fury.io/py/pdocs)\n[![Build Status](https://travis-ci.org/timothycrosley/pdocs.svg?branch=master)](https://travis-ci.org/timothycrosley/pdocs)\n[![codecov](https://codecov.io/gh/timothycrosley/pdocs/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/pdocs)\n[![Join the chat at https://gitter.im/pdocs/community](https://badges.gitter.im/pdocs/community.svg)](https://gitter.im/pdocs/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/pdocs/)\n[![Downloads](https://pepy.tech/badge/pdocs)](https://pepy.tech/project/pdocs)\n_________________\n\n[Read Latest Documentation](https://timothycrosley.github.io/pdocs/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/pdocs/)\n_________________\n\n\n`pdocs` is a library and a command line program to discover the public\ninterface of a Python module or package. The `pdocs` script can be used to\ngenerate Markdown or HTML of a module's public interface, or it can be used\nto run an HTTP server that serves generated HTML for installed modules.\n\n`pdocs` is an MIT Licensed fork of [pdoc](https://github.com/mitmproxy/pdoc)'s original implementation by Andrew Gallant (@BurntSushi).\n with the goal of staying true to the original vision layed out by the project's creator.\n\nNOTE: For most projects, the best way to use `pdocs` is using [portray](https://timothycrosley.github.io/portray/).\n\n[![asciicast](https://asciinema.org/a/265744.svg)](https://asciinema.org/a/265744)\n\nFeatures\n--------\n\n* Support for documenting data representation by traversing the abstract syntax\n  to find docstrings for module, class and instance variables.\n* For cases where docstrings aren't appropriate (like a\n  [namedtuple](http://docs.python.org/2.7/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields)),\n  the special variable `__pdocs__` can be used in your module to\n  document any identifier in your public interface.\n* Usage is simple. Just write your documentation as Markdown. There are no\n  added special syntax rules.\n* `pdocs` respects your `__all__` variable when present.\n* `pdocs` will automatically link identifiers in your docstrings to its\n  corresponding documentation.\n* When `pdocs` is run as an HTTP server, external linking is supported between\n  packages.\n* The `pdocs` HTTP server will cache generated documentation and automatically\n  regenerate it if the source code has been updated.\n* When available, source code for modules, functions and classes can be viewed\n  in the HTML documentation.\n* Inheritance is used when possible to infer docstrings for class members.\n\nThe above features are explained in more detail in pdocs's documentation.\n\n`pdocs` is compatible with Python 3.6 and newer.\n\n## Quick Start\n\nThe following guides should get you up using pdocs in no time:\n\n1. [Installation](https://timothycrosley.github.io/pdocs/docs/quick_start/1.-installation/) - TL;DR: Run `pip3 install pdocs` within your projects virtual environment.\n2. [Command Line Usage](https://timothycrosley.github.io/pdocs/docs/quick_start/2.-cli/) - TL;DR: Run `pdocs server YOUR_MODULES` to test and `pdocs as_html YOUR_MODULES` to generate HTML.\n3. [API Usage](https://timothycrosley.github.io/pdocs/docs/quick_start/3.-api/) - TL;DR: Everything available via the CLI is also easily available programmatically from within Python.\n\n## Differences Between pdocs and pdoc\n\nBelow is a running list of intentional differences between [pdoc](https://github.com/mitmproxy/pdoc) and [pdocs](https://github.com/timothycrosley/pdocs):\n\n- pdocs has built-in support for Markdown documentation generation (as needed by [portray](https://timothycrosley.github.io/portray/)).\n- pdocs has built-in support for the inclusion of Type Annotation information in reference documentation.\n- pdocs requires Python 3.6+; pdoc maintains Python2 compatibility as of the latest public release.\n- pdocs uses the most recent development tools to ensure long-term maintainability (mypy, black, isort, flake8, bandit, ...)\n- pdocs generates project documentation to a temporary folder when serving locally, instead of including a live server. An intentional trade-off between simplicity and performance.\n- pdocs provides a simplified Python API in addition to CLI API.\n- pdocs is actively maintained.\n- pdocs uses [hug CLI and sub-commands](https://github.com/timothycrosley/pdocs/blob/master/pdocs/cli.py#L1), pdoc uses [argparse and a single command](https://github.com/mitmproxy/pdoc/blob/master/pdoc/cli.py#L1).\n- pdoc provides textual documentation from the command-line, pdocs removed this feature for API simplicity.\n\n## Notes on Licensing and Fork\n\nThe original pdoc followed the [Unlicense license](https://unlicense.org/), and as such so does the initial commit to this fork [here](https://github.com/timothycrosley/pdocs/commit/7cf925101e4ffc5690f2952ac9ad0b7b0410b4f8).\nUnlicense is fully compatible with MIT, and the reason for the switch going forward is because MIT is a more standard and well-known license.\n\nAs seen by that commit, I chose to fork with fresh history, as the project is very old (2013) and I felt many of the commits that happened in the past might, instead of helping to debug issues, lead to red herrings due to the many changes that have happened\nin the Python eco-system since that time. If you desire to see the complete history for any reason, it remains available on the original [pdoc repository](https://github.com/mitmproxy/pdoc).\n\n## Why Create `pdocs`?\n\nI created `pdocs` to help power [portray](https://timothycrosley.github.io/portray/) while staying true to the original vision of `pdoc` and maintain\nMIT license compatibility. In the end I created it to help power better documentation websites for Python projects.\n\nI hope you, too, find `pdocs` useful!\n\n~Timothy Crosley\n",
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
