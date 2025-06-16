#!/usr/bin/env python3
from typing import List

from setuptools import find_packages, setup


def read_requirements(filename: str) -> List[str]:
    return [req.strip() for req in open(filename)]


requirements = read_requirements('requirements.txt')
dev_requirements = read_requirements('requirements-dev.txt')

setup(
    name='pylspci',
    version=open('VERSION').read().strip(),
    author='Lucidiot',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    entry_points={
        'console_scripts': ['pylspci=pylspci.__main__:main'],
    },
    package_data={
        '': [
            'VERSION',
            'LICENSE',
            'README.rst',
            'requirements.txt',
            'requirements-dev.txt',
        ],
        'pylspci': ['py.typed'],
    },
    python_requires='>=3.5',
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
    test_suite='pylspci.tests',
    license='GNU General Public License 3',
    description="Simple parser for lspci -mmnn.",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    keywords="lspci parser",
    url="https://tildegit.org/lucidiot/pylspci",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    project_urls={
        "Homepage": "https://tildegit.org/lucidiot/pylspci",
        "Changelog": "https://tildegit.org/lucidiot/pylspci/releases",
        "Documentation": "https://lucidiot.tildepages.org/pylspci/",
        "Issue tracker": "https://tildegit.org/lucidiot/pylspci/issues",
    }
)
