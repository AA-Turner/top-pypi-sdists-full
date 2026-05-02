# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sprawl']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'sprawl',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Sprawl\n\nA utility package for printing formatted, colorized log messages. \n\n## Why? \n\nSometimes we fall back to good ol\' print-driven development ("PDD") \nwhen we need to inspect values at runtime. It can be annoying to search through \na terminal window filled with other logs to find the one log statement you\'re looking \nfor. This makes it easy for your log messages to stand out. \n\n## Installation\n\n`$ pip install sprawl`\n\n## Usage\n\nImport the log function:\n\n```python\nfrom sprawl.loud_log import log\n\n```\n\nConfigure logging however you normally would, for example:\n\n\n```python\nlogging.basicConfig(format=\'%(asctime)s \\n %(message)s\', level=logging.INFO)\n```  \n\nlog a message using the defaults:\n\n```python\nlog(\'my log message\')\n```\n\nprints:\n\n```\n##################################\n my log message\n##################################\n\n```\n\nCenter the log message:\n\n```python\nlog(\'my log message\', center_message=True)\n\n```\n\nprints:\n\n```\n##################################\n           my log message\n##################################\n```\n\nChange the surrounding character:\n\n```python\nlog(\'my log message\', center_message=True, char_to_surround_with=\'~\')\n\n```\n\nprints:\n\n```\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n           my log message\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n```\n\nAdd some color:\n\n```python\nlog(\'my log message\', center_message=True, color=\'yellow\')\n\n```\n\nprints:\n\n<img width="450" alt="Screen Shot 2019-12-11 at 8 55 38 PM" src="https://user-images.githubusercontent.com/514174/70675962-a50cca00-1c58-11ea-8484-8ca40617d518.png">\n\nLog the name of the function or module from within which this log() was called\n\n\n```python\ndef my_amazing_function():\n    log(\'my log message\', center_message=True, print_func_name=True)\n    \nmy_amazing_function()\n\n```\n\nprints:\n\n```\nlog called from my_amazing_function\n#################################\n           my log message\n#################################\n```\n\n',
    'author': 'Levi Notik',
    'author_email': 'projects@levinotik.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
