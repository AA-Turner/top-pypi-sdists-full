# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_rtd_size']

package_data = \
{'': ['*'], 'sphinx_rtd_size': ['_static/css/*']}

install_requires = \
['Sphinx>=2']

setup_kwargs = {
    'name': 'sphinx-rtd-size',
    'version': '0.2.0',
    'description': 'Sphinx extension for resizing your RTD theme.',
    'long_description': '# sphinx-rtd-size\nSphinx extension for resizing your RTD theme\n\n## Usage\n\nInstall the package:\n\n`pip install sphinx-rtd-size`\n\nAnd in your `conf.py`:\n```\n    extensions = [\n        ...\n        \'sphinx_rtd_size\',\n    ]\n    \n    sphinx_rtd_size_width = "90%"\n```',
    'author': 'michael tadnir',
    'author_email': 'tadnir50@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tadnir/sphinx-rtd-size',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
