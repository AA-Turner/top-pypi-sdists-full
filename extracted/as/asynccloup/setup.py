#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup


def make_long_description(write_file=False):
    readme = Path('README.rst').read_text(encoding='utf-8')
    # PyPI doesn't support the `raw::` directive. Skip it.
    start = readme.find('.. docs-index-start')
    long_description = readme[start:]
    if write_file:
        Path('PYPI_README.rst').write_text(long_description, encoding='utf-8')
    return long_description


setup(
    name='asynccloup',
    setup_requires=['setuptools_scm'],
    use_scm_version={
        'write_to': 'asynccloup/_version.py'
    },
    author='Matthias Urlichs',
    author_email='matthias@urlichs.de',
    description="Adds features to AsyncClick: option groups, constraints, subcommand "
                "sections and help themes. A fork of Gianluca Gippetto's 'Cloup'.",
    long_description_content_type='text/x-rst',
    long_description=make_long_description(),
    url='https://github.com/M-o-a-T/asynccloup',
    license="BSD 3-Clause",
    keywords=['CLI', 'click', 'argument groups', 'option groups', 'constraints',
              'help colors', 'help themes', 'help styles'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    packages=find_packages(include=['asynccloup', 'asynccloup.*']),
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=[
        'anyio >= 4.10, < 5.0',
        'asyncclick >= 8.0, < 9.0',
        'typing_extensions; python_version<="3.10"',
    ],
)
