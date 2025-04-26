# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colorclass']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'colorclass',
    'version': '2.2.2',
    'description': 'Colorful worry-free console applications for Linux, Mac OS X, and Windows.',
    'long_description': '# colorclass\n\nYet another ANSI color text library for Python. Provides "auto colors" for dark/light terminals. Works on Linux, OS X,\nand Windows. For Windows support you just need to call ``Windows.enable()`` in your application.\n\nOn Linux/OS X ``autocolors`` are toggled by calling ``set_light_background()`` and ``set_dark_background()``. On Windows\nthis can be done automatically if you call ``Windows.enable(auto_colors=True)``. Even though the latest Windows 10 does\nsupport ANSI color codes natively, you still need to run Windows.enable() to take advantage of automatically detecting\nthe console\'s background color.\n\nIn Python2.x this library subclasses ``unicode``, while on Python3.x it subclasses ``str``.\n\n* Python 2.6, 2.7, PyPy, PyPy3, 3.3, 3.4, and 3.5 supported on Linux and OS X.\n* Python 2.6, 2.7, 3.3, 3.4, and 3.5 supported on Windows (both 32 and 64 bit versions of Python).\n\n## Quickstart\nInstall:\n```bash\n    pip install colorclass\n```\n\n## Piped Command Line\nIt is possible to pipe curly-bracket tagged (or regular ANSI coded) text to Python in the command line to produce color\ntext. Some examples:\n\n```bash\n    echo "{red}Red{/red}" |python -m colorclass  # Red colored text.\n    echo -e "\\033[31mRed\\033[0m" | COLOR_DISABLE=true python -m colorclass  # Strip colors\n    echo -e "\\033[31mRed\\033[0m" | COLOR_ENABLE=true python -m colorclass &> file.txt  # Force colors.\n```\nExport these environment variables as "true" to enable/disable some features:\n\n    =============== ============================================\n    Env Variable    Description\n    =============== ============================================\n    COLOR_ENABLE    Force colors even when piping to a file.\n    COLOR_DISABLE   Strip all colors from incoming text.\n    COLOR_LIGHT     Use light colored text for dark backgrounds.\n    COLOR_DARK      Use dark colored text for light backgrounds.\n    =============== ============================================\n\n## Example Implementation\n\n![Example Script Screenshot](https://github.com/Robpol86/colorclass/raw/master/example.png?raw=true)\n\n![Example Windows Screenshot](https://github.com/Robpol86/colorclass/raw/master/example_windows.png?raw=true)\n\nSource code for the example code is: [example.py](https://github.com/Robpol86/colorclass/blob/master/example.py)\n\n## Usage\n\nDifferent colors are chosen using curly-bracket tags, such as ``{red}{/red}``. For a list of available colors, call\n``colorclass.list_tags()``.\n\nThe available "auto colors" tags are:\n\n* autoblack\n* autored\n* autogreen\n* autoyellow\n* autoblue\n* automagenta\n* autocyan\n* autowhite\n* autobgblack\n* autobgred\n* autobggreen\n* autobgyellow\n* autobgblue\n* autobgmagenta\n* autobgcyan\n* autobgwhite\n\nMethods of Class instances try to return sane data, such as:\n\n```python\n    from colorclass import Color\n    color_string = Color(\'{red}Test{/red}\')\n\n    >>> color_string\n    u\'\\x1b[31mTest\\x1b[39m\'\n\n    >>> len(color_string)\n    4\n\n    >>> color_string.istitle()\n    True\n```\nThere are also a couple of helper attributes for all Color instances:\n\n```python\n    >>> color_string.value_colors\n    \'\\x1b[31mTest\\x1b[39m\'\n\n    >>> color_string.value_no_colors\n    \'Test\'\n```\n\n[Change Log](https://github.com/matthewdeanmartin/colorclass/blob/master/CHANGELOG.md)',
    'author': 'Robpol86',
    'author_email': 'robpol86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matthewdeanmartin/colorclass',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.6',
}


setup(**setup_kwargs)
