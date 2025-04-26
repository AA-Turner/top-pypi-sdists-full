# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avro_schema']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'avro-schema',
    'version': '0.3.3',
    'description': '',
    'long_description': '# avro-schema\nAvro schema utilities\n',
    'author': 'Sam',
    'author_email': 'sam.mosleh@ut.ac.ir',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sam-mosleh/avro-schema',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
