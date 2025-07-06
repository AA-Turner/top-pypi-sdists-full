#!/usr/bin/env python

"""The setup script."""

import os
import acdh_xml_pyutils as module
from setuptools import setup, find_packages


def walker(base, *paths):
    file_list = set([])
    cur_dir = os.path.abspath(os.curdir)

    os.chdir(base)
    try:
        for path in paths:
            for dname, dirs, files in os.walk(path):
                for f in files:
                    file_list.add(os.path.join(dname, f))
    finally:
        os.chdir(cur_dir)

    return list(file_list)


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    author="Peter Andorfer",
    author_email='peter.andorfer@oeaw.ac.at',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Utility functions to work with XML",
    install_requires=requirements,
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='acdh_xml_pyutils',
    name='acdh_xml_pyutils',
    packages=find_packages(include=['acdh_xml_pyutils', 'acdh_xml_pyutils.*']),
    package_data={
        module.__name__: walker(
            os.path.dirname(module.__file__),
            'files'
        ),
    },
    url='https://github.com/acdh-oeaw/acdh-xml-pyutils',
    version='1.1.1',
    zip_safe=False,
)
