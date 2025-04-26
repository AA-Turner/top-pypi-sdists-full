""" Copyright 2021 MosaicML. All Rights Reserved. """

import os

import setuptools
from setuptools import setup

long_description = """
#  MosaicML CLI (MCLI)

### MCLI is the interface for interacting with Databricks Mosaic AI Training

To get started with MCLI, read the [documentation](https://mcli.docs.mosaicml.com/)
"""

# pylint: disable-next=exec-used,consider-using-with
exec(open('mcli/version.py', 'r', encoding='utf-8').read())

install_requires = [
    'argcomplete>=2.0.0',
    'arrow>=1.2.2',
    'backoff>=2.2.1',
    'gql[websockets]>=3.4.0',
    'prompt_toolkit>=3.0.29',
    'protobuf>=3.20.0',
    'pyyaml>=5.4.1',
    'questionary>=1.10.0',
    'rich>=12.6.0',
    'ruamel.yaml>=0.17.21',
    'typing_extensions>=4.0.1',
    'validators>=0.20.0',
    'requests>=2.26.0,<3',
    'urllib3>=1.23',
    'termcolor>=1.1.0',
]

extra_deps = {}

extra_deps['dev'] = [
    'build>=0.10.0',
    'isort>=5.9.3',
    'pre-commit>=2.17.0',
    'pylint>=2.12.2',
    'pyright==1.1.256',
    'pytest-cov>=4.0.0',
    'pytest-mock>=3.7.0',
    'pytest>=6.2.5',
    'radon>=5.1.0',
    'twine>=4.0.2',
    'toml>=0.10.2',
    'yapf>=0.33.0',
]

extra_deps['sphinx'] = [
    'furo==2022.9.29',
    'sphinx==4.4.0',
    'sphinx-argparse==0.4.0',
    'sphinx-copybutton==0.5.2',
    'sphinx-markdown-tables==0.0.17',
    'sphinx-panels==0.6.0',
    'sphinx-rtd-theme==1.0.0',
    'sphinx_external_toc==0.3.0',
    'sphinxcontrib-applehelp==1.0.2',
    'sphinxcontrib-devhelp==1.0.2',
    'sphinxcontrib-htmlhelp==2.0.0',
    'sphinxcontrib-images>=0.9.4',
    'sphinxcontrib-jsmath>=1.0.1',
    'sphinxcontrib-katex==0.9.4',
    'sphinxcontrib-qthelp==1.0.3',
    'sphinxcontrib-serializinghtml==1.1.5',
    'sphinxemoji==0.2.0',
    'sphinxext-opengraph==0.8.2',
    'myst-parser>=0.16.1',
    'docutils>=0.17.0',
    'sphinx-design',
]


def package_files(directory: str):
    # from https://stackoverflow.com/a/36693250
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_deps['all'] = set(dep for deps in extra_deps.values() for dep in deps)

setup(
    name='mosaicml-cli',
    version=__version__,  # type: ignore pylint: disable=undefined-variable
    author='MosaicML',
    author_email='team@mosaicml.com',
    description='Interact with Databricks Mosaic AI training from python or a command line interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mosaicml/mosaicml-cli',
    include_package_data=True,
    package_data={},
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['mcli = mcli.cli.cli:main', 'mcli-admin = mcli.cli.cli:admin'],
    },
    extras_require=extra_deps,
    python_requires='>=3.8',
    ext_package='mcli',
)
