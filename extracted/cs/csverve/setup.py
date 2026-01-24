#!/usr/bin/env python

"""The setup script."""

import versioneer

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click>=7.0',
    'pandas>=1.0.0',
    'pyyaml',
    'numpy<2',
    'pytest',
    'Sphinx==5.1.1',
    'mypy',
]

setup_requirements = []

test_requirements = []

setup(
    author="Shah Lab",
    author_email='todo@todo.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="todo: add description",
    entry_points={
        'console_scripts': [
            'csverve=csverve.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='csverve',
    name='csverve',
    packages=find_packages(include=['csverve', 'csverve.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mondrian-scwgs/csverve',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    zip_safe=False,
)
