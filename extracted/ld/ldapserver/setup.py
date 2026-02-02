import os
import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
	long_description = f.read()

setuptools.setup(
	name='ldapserver',
	version=os.environ.get('PACKAGE_VERSION', 'local'),
	author='Julian Rother',
	author_email='python-ldapserver@jrother.eu',
	description='Library to implement special-purpose LDAP servers',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://git.cccv.de/uffd/python-ldapserver',
	classifiers=[
		'Programming Language :: Python :: 3',
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Operating System :: OS Independent',
		'Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP',
	],
	package_dir={'': '.'},
	packages=setuptools.find_packages(where='.'),
	python_requires='>=3.7',
)
