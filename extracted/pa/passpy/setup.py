# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['passpy']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=1.0.1', 'click>=2.0', 'pyperclip>=1.5', 'python-gnupg>=0.3.8']

extras_require = \
{'color': ['colorama>=0.3']}

entry_points = \
{'console_scripts': ['passpy = passpy.__main__:cli']}

setup_kwargs = {
    'name': 'passpy',
    'version': '1.0.2',
    'description': "ZX2C4's pass compatible Python library and cli",
    'long_description': "# passpy --  ZX2C4's pass compatible library and cli\n\npasspy has been written to be a platform independent library and cli\nthat is compatible with [ZX2C4's pass](http://www.passwordstore.org).\n\npasspy saves your passwords in gpg encrypted files and optionally uses git as a\nrevision tool.  All files are stored inside the directory given by the\n`PASSWORD_STORE_DIR` environment variable (`~/.password-store` if not set) and\ncan be organised into folders.  You can also just copy the whole store to have\nyour passwords available where ever you like.\n\n## Documentation\n\nThe latest documentation is available at\n[readthedocs](https://passpy.readthedocs.org).\n\n## Installation\n\n### PyPI\n\nJust do\n\n```\n$ [sudo] pip install passpy\n```\n\n### Arch Linux\n\nThe package `python-passpy` is available in the AUR for you to install\nhowever you like.\n\n### Manually\n\nEither clone the git repository using\n\n```\n$ git clone https://github.com/bfrascher/passpy.git\n```\n\nor download the source from the releases tab and extract it.\nAfterwards change into the new folder and do\n\n```\n$ [sudo] python setup.py install\n```\n\n## Dependencies\n\npasspy depends on Python 3.3 or later (it has mostly been tested using\nPython 3.5).  The program makes use of [git](https://www.git-scm.com)\nand [gpg2](https://gnupg.org) as well as either xclip or xsel on\nLinux.\n\nThe following Python packages will be installed alongside passpy:\n\n- [gitpython](https://github.com/gitpython-developers/GitPython)\n- [python-gnupg](https://bitbucket.org/vinay.sajip/python-gnupg)\n- [click](http://click.pocoo.org/)\n- [pyperclip](https://github.com/asweigart/pyperclip)\n\nIf you are on Windows and want colourised output on the command line,\nyou will additionally need to install\n[colorama](https://github.com/tartley/colorama).\n\n## Changelog\n\n### 1.0.2\n\n- Now also read the default password store location from `PASSWORD_STORE_DIR`\n  for the cli.\n- Show a better error message when the password store does not exist.\n- Always use the `path` parameter of `Store.init_store` relative to\n  `Store.store_dir`.\n\n### 1.0.1\n\n- Fix documentation.\n\n### 1.0.0\n\n- Read the default password store location from the `PASSWORD_STORE_DIR`\n  environment variable, just like `pass` does (contributed by Jonathan Waldrep).\n",
    'author': 'Benedikt Rascher-Friesenhausen',
    'author_email': 'benedikt_rascher-friesenhausen+passpy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bfrascher/passpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.3',
}


setup(**setup_kwargs)
