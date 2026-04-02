# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['antiword']
entry_points = \
{'console_scripts': ['antiword = antiword:main']}

setup_kwargs = {
    'name': 'antiword',
    'version': '0.1.0',
    'description': 'Spew anything out as text to stdout',
    'long_description': '# Basic Antiword via libreoffice\n\nThis package is nothing more than a convenience wrapper around `libreoffice\n--convert-to txt` which dumps to stdout, cleaning up the generated temporary\nfile as it goes.\n\n\nI probably should have written it in bash, but there we go.\n',
    'author': 'John Maximilian',
    'author_email': '2e0byo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/2e0byo/antiword',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
