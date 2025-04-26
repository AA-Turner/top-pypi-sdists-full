# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xdg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xdg',
    'version': '6.0.0',
    'description': 'Variables defined by the XDG Base Directory Specification',
    'long_description': '# xdg\n\n`xdg` has been renamed to `xdg-base-dirs` due to an import collision with\n[`PyXDG`](https://pypi.org/project/pyxdg/). Therefore the\n[`xdg`](https://pypi.org/project/xdg/) package is deprecated. Install\n[`xdg-base-dirs`](https://pypi.org/project/xdg-base-dirs/) instead.\n',
    'author': 'Scott Stevenson',
    'author_email': 'scott@stevenson.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/srstevenson/xdg-base-dirs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
