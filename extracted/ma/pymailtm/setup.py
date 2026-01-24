# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymailtm']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.2,<2.0.0',
 'random-username>=1.0.2,<2.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['pymailtm = pymailtm.cli:init']}

setup_kwargs = {
    'name': 'pymailtm',
    'version': '1.1.1',
    'description': 'A python web api wrapper and command line client for mail.tm.',
    'long_description': "[![PyPI](https://img.shields.io/pypi/v/pymailtm)](https://pypi.org/project/pymailtm/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymailtm)](https://pypi.org/project/pymailtm/) [![CI Status](https://img.shields.io/github/workflow/status/CarloDePieri/pymailtm/prod?logo=github)](https://github.com/CarloDePieri/pymailtm/actions/workflows/prod.yml) [![Coverage Status](https://coveralls.io/repos/github/CarloDePieri/pymailtm/badge.svg?branch=master)](https://coveralls.io/github/CarloDePieri/pymailtm?branch=master) [![Maintenance](https://img.shields.io/maintenance/yes/2022)](https://github.com/CarloDePieri/pymailtm/)\n\nThis is a command line interface and python web-api wrapper for [mail.tm](https://mail.tm).\n\nThe api is documented [here](https://api.mail.tm/).\n\n## Dependencies\n\n`xclip` or `xsel` for clipboard copying.\n\nA browser to open incoming html emails.\n\n## Installation\n\n#### With pip\n\n```bash\npip install pymailtm\n```\n\n#### In a virtual env\n\n```bash\npython -m venv .venv\nsource .venv/bin/activate\npip install pymailtm\n```\n\n## Usage\n\nThe utility can be called with:\n\n```bash\npymailtm\n```\n\nRemember that if you are in a virtual env you need to activate it first.\n\nBy default the command recover the last used account, copy it to the clipboard\nand wait for a new message to arrive: when it does, it's opened in the browser\nin a quick&dirty html view.\n\nExit the waiting loop by pressing `Ctrl+c`.\n\nCalling the utility with the flag `-l` will print the account credentials, open\nin the browser the [mail.tm](https://mail.tm) client and exit.\n\nThe flag `-n` can be used to force the creation of a new account.\n\n## Security warnings\n\nThis is conceived as an **insecure**, fast throwaway temp mail account generator.\n\n**DO NOT** use it with sensitive data.\n\nMails that arrive while the utility is running will be saved in **plain text**\nfiles in the system temporary folder (probably `/tmp/`) so that they can be\nopened by the browser.\n\nThe last used account's data and credentials will be saved in\n**plain text** in `~/.pymailtm`.\n\n\n## Development\n\nInstall [invoke](http://pyinvoke.org/) and [poetry](https://python-poetry.org/):\n\n```bash\npip install invoke poetry\n```\n\nNow clone the git repo:\n\n```bash\ngit clone git@github.com:CarloDePieri/pymailtm.git\ncd pymailtm\ninv install\n```\n\nThis will try to create a virtualenv based on `python3.7` and install there all\nproject's dependencies. If a different python version is preferred, it can be\nselected by specifying  the `--python` (`-p`) flag like this:\n\n```bash\ninv install -p python3.8\n```\n\nThe script can now be run directly by launching `inv run`. It also accepts flags,\nfor example:\n\n```bash\ninv run -n\n```\n\nThe test suite can be run with commands:\n\n```bash\ninv test         # run the test suite\ninv test --full  # run even tests that requires a graphical environment\ninv test-spec    # run the tests while showing the output as a spec document\ninv test-cov     # run the tests suite and produce a coverage report\n```\n\nTests take advantage of [vcrpy](https://github.com/kevin1024/vcrpy) to cache\nnetwork requests and responses. If you need to clear this cache run:\n\n```bash\ninv clear-cassettes\n```\n\nTo test the github workflow with [act](https://github.com/nektos/act):\n\n```bash\ninv act-dev           # test the dev workflow\ninv act-dev -c shell  # open a shell in the act container (the above must fail first!)\ninv act-dev -c clean  # stop and delete a failed act container\n```\n",
    'author': 'Carlo De Pieri',
    'author_email': 'depieri.carlo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CarloDePieri/pymailtm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
