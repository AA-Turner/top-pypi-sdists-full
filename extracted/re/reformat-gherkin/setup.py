# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reformat_gherkin', 'reformat_gherkin.ast_node']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4',
 'attrs>=20.2',
 'cattrs>=1.1,<22.2',
 'click>=7',
 'gherkin-official==24.0.0',
 'wcwidth>=0.2.5,<0.3.0']

entry_points = \
{'console_scripts': ['reformat-gherkin = reformat_gherkin.cli:main']}

setup_kwargs = {
    'name': 'reformat-gherkin',
    'version': '3.0.1',
    'description': 'Formatter for Gherkin language',
    'long_description': "# Reformat-gherkin\n\n[![Test](https://github.com/ducminh-phan/reformat-gherkin/actions/workflows/test.yml/badge.svg)](https://github.com/ducminh-phan/reformat-gherkin/actions/workflows/test.yml)\n&nbsp; [![Coverage Status](https://coveralls.io/repos/github/ducminh-phan/reformat-gherkin/badge.svg?branch=master)](https://coveralls.io/github/ducminh-phan/reformat-gherkin?branch=master)\n\n[![Maintainability](https://api.codeclimate.com/v1/badges/16718a231901c293215d/maintainability)](https://codeclimate.com/github/ducminh-phan/reformat-gherkin/maintainability)\n&nbsp; [![Codacy Badge](https://api.codacy.com/project/badge/Grade/e675ca51b6ac436a980facbcf04b8e5a)](https://www.codacy.com/app/ducminh-phan/reformat-gherkin)\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n&nbsp; [![PyPI](https://img.shields.io/pypi/v/reformat-gherkin.svg)](https://pypi.org/project/reformat-gherkin/)\n&nbsp; [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n\n## Table of Contents\n\n- [About](#about)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Version control integration](#version-control-integration)\n- [Acknowledgements](#acknowledgements)\n\n## About\n\nReformat-gherkin automatically formats Gherkin files. It ensures a consistent\nlook regardless of who wrote the file.\n\nIt can be used either as a command-line tool, or a\n[pre-commit](https://pre-commit.com/) hook.\n\n## Installation\n\nInstall reformat-gherkin using [pip](https://pypi.org/project/pip/).\n\n```bash\npip install reformat-gherkin\n```\n\nIt requires [Python 3.7+](https://www.python.org/downloads/) to run.\n\n## Usage\n\nTo get started straight away:\n\n```bash\nreformat-gherkin {source_file_or_directory}\n```\n\nYou should get good results without specifying any options, as reformat-gherkin\nuses sensible defaults.\n\n### Command-line options\n\nYou can list the available options by running `reformat-gherkin --help`.\n\n```text\nUsage: reformat-gherkin [OPTIONS] [SRC]...\n\n  Reformat the given SRC files and all .feature files in SRC folders. If -\n  is passed as a file, reformat stdin and print the result to stdout.\n\nOptions:\n  --check                         Don't write the files back, just return the\n                                  status. Return code 0 means nothing would\n                                  change. Return code 1 means some files would\n                                  be reformatted. Return code 123 means there\n                                  was an internal error.\n\n  -a, --alignment [left|right]    Specify the alignment of step keywords\n                                  (Given, When, Then,...). If specified, all\n                                  statements after step keywords are left-\n                                  aligned, spaces are inserted before/after\n                                  the keywords to right/left align them. By\n                                  default, step keywords are left-aligned, and\n                                  there is a single space between the step\n                                  keyword and the statement.\n\n  -n, --newline [LF|CRLF]         Specify the line separators when formatting\n                                  files inplace. If not specified, line\n                                  separators are preserved.\n\n  --fast / --safe                 If --fast given, skip the sanity checks of\n                                  file contents. [default: --safe]\n\n  --single-line-tags / --multi-line-tags\n                                  If --single-line-tags given, output\n                                  consecutive tags on one line. If --multi-\n                                  line-tags given, output one tag per line.\n                                  [default: --single-line-tags]\n\n  --tab-width INTEGER             Specify the number of spaces per\n                                  indentation-level. [default: 2]\n\n  --use-tabs                      Indent lines with tabs instead of spaces.\n  --config FILE                   Read configuration from FILE.\n  --version                       Show the version and exit.\n  --help                          Show this message and exit.\n```\n\nReformat-gherkin is a well-behaved Unix-style command-line tool:\n\n- it does nothing if no sources are passed to it;\n- it will read from standard input and write to standard output if - is used as the filename;\n- it only outputs messages to users on standard error;\n- it exits with code 0 unless an internal error occurred (or --check was used).\n\n### Config file\n\nReformat-gherkin can read project-specific default values for its command line\noptions from a `.reformat-gherkin.yaml` file.\n\nBy default, `reformat-gherkin` looks for the config file starting from the\ncommon base directory of all files and directories passed on the command line.\nIf it's not there, it looks in parent directories. It stops looking when it\nfinds the file, or a .git directory, or a .hg directory, or the root of the file\nsystem, whichever comes first.\n\nExample config file:\n\n```yaml\ncheck: False\nalignment: left\ntab_width: 4\n```\n\n## Version control integration\n\nYou can integrate reformat-gherkin into your version control workflow by using\n[pre-commit](https://pre-commit.com/). Once you have installed pre-commit, add\nthis to the `.pre-commit-config.yaml` file in your repository:\n\n```text\nrepos:\n  - repo: https://github.com/ducminh-phan/reformat-gherkin\n    rev: stable\n    hooks:\n      - id: reformat-gherkin\n```\n\nThen run `pre-commit install` and you're ready to go.\n\n## Acknowledgements\n\nThis project is inspired by [black](https://github.com/psf/black). Some\nfunctions are taken from `black`'s source code.\n",
    'author': 'Duc-Minh Phan',
    'author_email': 'alephvn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ducminh-phan/reformat-gherkin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
