# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['factory-stubs']

package_data = \
{'': ['*']}

install_requires = \
['factory-boy>=3.2.0', 'typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'types-factory-boy',
    'version': '0.4.1',
    'description': 'Typing stubs for factory-boy',
    'long_description': '## Typing stubs for factory-boy\n\nThis is a PEP 561 type stub package for the `factory-boy` package.\nIt can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code\nthat uses `factory-boy`.\n\n### Installation\n\n```shell\npip install types-factory-boy\n```\n',
    'author': 'Alessio Bogon',
    'author_email': '778703+youtux@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/youtux/types-factory-boy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
