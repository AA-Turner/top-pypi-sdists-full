# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['springdata_sqlalchemy', 'springdata_sqlalchemy.asyncio']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4,<2.0', 'spring-data-python>=0.1.0,<1']

setup_kwargs = {
    'name': 'spring-data-sqlachemy',
    'version': '0.1.4',
    'description': 'Spring Data SQLAlchemy is an offshoot of the Java-based Spring Data Framework, targeted for SQLAlchemy.',
    'long_description': '# spring-data-sqlalchemy\nSpring Data SQLAlchemy is an offshoot of the Java-based Spring Data Framework, targeted for SQLAlchemy.\n',
    'author': 'Vincent TERESE',
    'author_email': 'vincent.terese@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kobibleu/spring-data-sqlalchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
