# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['screeninfo', 'screeninfo.enumerators']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses'],
 ':sys_platform == "darwin"': ['Cython', 'pyobjc-framework-Cocoa']}

setup_kwargs = {
    'name': 'screeninfo',
    'version': '0.8.1',
    'description': 'Fetch location and size of physical screens.',
    'long_description': "screeninfo\n----------\n\n[![Build](https://github.com/rr-/screeninfo/actions/workflows/build.yml/badge.svg)](https://github.com/rr-/screeninfo/actions/workflows/build.yml)\n\nFetch location and size of physical screens.\n\n### Supported environments\n\n- MS Windows\n- MS Windows: Cygwin\n- GNU/Linux: X11 (through Xinerama)\n- GNU/Linux: DRM (experimental)\n- OSX: (through AppKit)\n\nI don't plan on testing OSX or other environments myself. For this reason,\nI strongly encourage pull requests.\n\n### Installation\n\n```\npip install screeninfo\n```\n\n### Usage\n\n```python\nfrom screeninfo import get_monitors\nfor m in get_monitors():\n    print(str(m))\n```\n\n**Output**:\n\n```python console\nMonitor(x=3840, y=0, width=3840, height=2160, width_mm=1420, height_mm=800, name='HDMI-0', is_primary=False)\nMonitor(x=0, y=0, width=3840, height=2160, width_mm=708, height_mm=399, name='DP-0', is_primary=True)\n```\n\n### Forcing environment\n\nIn some cases (emulating X server on Cygwin etc.) you might want to specify the\ndriver directly. You can do so by passing extra parameter to `get_monitors()`\nlike this:\n\n```python\nfrom screeninfo import get_monitors, Enumerator\nfor m in get_monitors(Enumerator.OSX):\n    print(str(m))\n```\n\nAvailable drivers: `windows`, `cygwin`, `x11`, `osx`.\n\n# Contributing\n\n\n```sh\ngit clone https://github.com/rr-/screeninfo.git # clone this repo\ncd screeninfo\npoetry install # to install the local venv\npoetry run pre-commit install # to setup pre-commit hooks\npoetry shell # to enter the venv\n```\n\nThis project uses [poetry](https://python-poetry.org/) for packaging,\ninstall instructions at [poetry#installation](https://python-poetry.org/docs/#installation)\n",
    'author': 'Marcin Kurczewski',
    'author_email': 'rr-@sakuya.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rr-/screeninfo',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
