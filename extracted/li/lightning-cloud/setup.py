import os
from importlib.util import spec_from_file_location, module_from_spec

from setuptools import find_packages, setup

PACKAGE_NAME = "lightning_cloud"
DESCRIPTION = 'Lightning Cloud'
URL = 'https://lightning.ai'
EMAIL = 'grid-eng@grid.ai'
AUTHOR = 'Grid.ai'
REQUIRES_PYTHON = '>=3.7.0'
LICENSE = "Apache Software License"

_PATH_ROOT = os.path.dirname(__file__)


def _load_py_module(fname, pkg="lightning_cloud"):
    spec = spec_from_file_location(os.path.join(pkg, fname),
                                   os.path.join(_PATH_ROOT, pkg, fname))
    py = module_from_spec(spec)
    spec.loader.exec_module(py)
    return py


version = _load_py_module("__version__.py")

#  What packages are required for this module to be executed?
REQUIRED = []
with open('requirements.txt') as f:
    for line in f.readlines():
        REQUIRED.append(line.replace('\n', ''))

#  Where the magic happens:
setup(
    name=PACKAGE_NAME,
    version=version.__version__,  # noqa
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests', 'tests.*')),
    entry_points={
        'console_scripts':
        ['lightning_cloud=lightning_cloud.cli.__main__:main'],
    },
    long_description="Lightning AI Command Line Interface",
    long_description_content_type="text/x-rst",
    install_requires=REQUIRED,
    license=LICENSE,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
    ],
)
