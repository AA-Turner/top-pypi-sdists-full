# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['issubclass']
setup_kwargs = {
    'name': 'issubclass',
    'version': '0.1.2',
    'description': "issubclass() builtin that doesn't raise TypeError when arguments are not classes",
    'long_description': 'None',
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
