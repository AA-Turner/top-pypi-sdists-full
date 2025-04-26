# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ceja']

package_data = \
{'': ['*']}

install_requires = \
['jellyfish>=0.8.2,<0.9.0']

setup_kwargs = {
    'name': 'ceja',
    'version': '0.4.0',
    'description': 'PySpark string and phonetic matching',
    'long_description': 'None',
    'author': 'MrPowers',
    'author_email': 'matthewkevinpowers@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.5',
}


setup(**setup_kwargs)
