#!/usr/bin/env python

"""
Copyright (c) 2006-2026 sqlmap developers (https://sqlmap.org)
See the file 'LICENSE' for copying permission
"""

from setuptools import setup, find_packages

setup(
    name='sqlmap',
    version='1.10.9',
    description='Automatic SQL injection and database takeover tool',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author='Bernardo Damele Assumpcao Guimaraes, Miroslav Stampar',
    author_email='bernardo@sqlmap.org, miroslav@sqlmap.org',
    url='https://sqlmap.org',
    project_urls={
        'Documentation': 'https://github.com/sqlmapproject/sqlmap/wiki',
        'Source': 'https://github.com/sqlmapproject/sqlmap/',
        'Tracker': 'https://github.com/sqlmapproject/sqlmap/issues',
    },
    download_url='https://github.com/sqlmapproject/sqlmap/archive/1.10.9.zip',
    license='GNU General Public License v2 (GPLv2)',
    packages=['sqlmap'],
    package_dir={'sqlmap':'sqlmap'},
    include_package_data=True,
    zip_safe=False,
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: Database',
        'Topic :: Security',
    ],
    entry_points={
        'console_scripts': [
            'sqlmap = sqlmap.sqlmap:main',
        ],
    },
)
