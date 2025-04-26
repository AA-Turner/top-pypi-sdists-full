# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydocstyle']

package_data = \
{'': ['*'], 'pydocstyle': ['data/*']}

install_requires = \
['snowballstemmer>=2.2.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=2.0.0,<5.0.0'],
 'toml:python_version < "3.11"': ['tomli>=1.2.3']}

entry_points = \
{'console_scripts': ['pydocstyle = pydocstyle.cli:main']}

setup_kwargs = {
    'name': 'pydocstyle',
    'version': '6.3.0',
    'description': 'Python docstring style checker',
    'long_description': 'pydocstyle - docstring style checker\n====================================\n\n\n.. image:: https://github.com/PyCQA/pydocstyle/workflows/Run%20tests/badge.svg\n    :target: https://github.com/PyCQA/pydocstyle/actions?query=workflow%3A%22Run+tests%22+branch%3Amaster\n\n.. image:: https://readthedocs.org/projects/pydocstyle/badge/?version=latest\n    :target: https://readthedocs.org/projects/pydocstyle/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/pyversions/pydocstyle.svg\n    :target: https://pypi.org/project/pydocstyle\n\n.. image:: https://pepy.tech/badge/pydocstyle\n    :target: https://pepy.tech/project/pydocstyle\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n    :target: https://pycqa.github.io/isort/\n\n.. image:: https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod\n    :target: https://gitpod.io/#https://github.com/PyCQA/pydocstyle\n    :alt: Gitpod ready-to-code\n\n**pydocstyle** is a static analysis tool for checking compliance with Python\ndocstring conventions.\n\n**pydocstyle** supports most of\n`PEP 257 <http://www.python.org/dev/peps/pep-0257/>`_ out of the box, but it\nshould not be considered a reference implementation.\n\n**pydocstyle** supports Python 3.6+.\n\n\nQuick Start\n-----------\n\nInstall\n^^^^^^^\n\n.. code::\n\n    pip install pydocstyle\n\n\nRun\n^^^\n\n.. code::\n\n    $ pydocstyle test.py\n    test.py:18 in private nested class `meta`:\n            D101: Docstring missing\n    test.py:27 in public function `get_user`:\n        D300: Use """triple double quotes""" (found \'\'\'-quotes)\n    test:75 in public function `init_database`:\n        D201: No blank lines allowed before function docstring (found 1)\n    ...\n\nDevelop\n^^^^^^^\n\nYou can use Gitpod to run pre-configured dev environment in the cloud right from your browser -\n\n.. image:: https://gitpod.io/button/open-in-gitpod.svg\n    :target: https://gitpod.io/#https://github.com/PyCQA/pydocstyle\n    :alt: Open in Gitpod\n    \nBefore submitting a PR make sure that you run `make all`.\n\nLinks\n-----\n\n* `Read the full documentation here <https://pydocstyle.org/en/stable/>`_.\n\n* `Fork pydocstyle on GitHub <https://github.com/PyCQA/pydocstyle>`_.\n\n* `PyPI project page <https://pypi.python.org/pypi/pydocstyle>`_.\n',
    'author': 'Amir Rachum',
    'author_email': 'amir@rachum.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.pydocstyle.org/en/stable/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
