#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as f:
	long_description = f.read()

setup(
	name = 'pytest-depends',
	version = '1.0.1',
	license = 'MIT',
	description = 'Tests that depend on other tests',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	author = 'Michon van Dooren',
	author_email = 'michon1992@gmail.com',
	url = 'https://gitlab.com/maienm/pytest-depends',
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Framework :: Pytest',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Testing',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: Implementation :: CPython',
		'Programming Language :: Python :: Implementation :: PyPy',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: MIT License',
	],
	keywords = [
		'pytest',
	],

	packages = find_packages('src'),
	package_dir = { '': 'src' },
	zip_safe = False,
	install_requires = [
		'colorama',
		'future-fstrings',
		'networkx',
		'pytest >= 3',
	],
	entry_points={
		'pytest11': [
			'depends = pytest_depends',
		],
	},
)
