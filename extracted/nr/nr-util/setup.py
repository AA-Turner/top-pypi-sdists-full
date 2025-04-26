# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['util',
 'util.algorithm',
 'util.annotations',
 'util.atomic',
 'util.awsgi',
 'util.awsgi.launcher',
 'util.config',
 'util.date',
 'util.digraph',
 'util.digraph.algorithm',
 'util.exceptions',
 'util.fs',
 'util.functional',
 'util.generic',
 'util.git',
 'util.inspect',
 'util.io',
 'util.iter',
 'util.keyvalue',
 'util.logging.filters',
 'util.logging.formatters',
 'util.parsing',
 'util.parsing._tokenizer',
 'util.plugins',
 'util.preconditions',
 'util.process',
 'util.proxy',
 'util.re',
 'util.safearg',
 'util.singleton',
 'util.task',
 'util.terminal.colors',
 'util.text',
 'util.url',
 'util.weak']

package_data = \
{'': ['*']}

install_requires = \
['deprecated>=1.2.0,<2.0.0', 'typing-extensions>=3.0.0']

setup_kwargs = {
    'name': 'nr.util',
    'version': '0.8.12',
    'description': 'General purpose Python utility library.',
    'long_description': '# nr.util\n\nGeneral purpose Python utility library.\n\nCompatible with Python 3.7 and higher.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NiklasRosenstein/python-nr.util',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
