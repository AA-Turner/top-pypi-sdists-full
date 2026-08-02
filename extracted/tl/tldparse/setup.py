# -*- config:utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'tldparse/__version__.py'), encoding='utf-8') as fp:
    try:
        version = re.findall(
            r"^__version__ = \"([^']+)\"\r?$", fp.read(), re.M
        )[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='tldparse',
    version=version,
    license='MIT',
    description='Parse a given domain and split it into its subdomain, domain and top-level domain parts.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/cnicodeme/tldparse',
    author='Cyril Nicodeme',
    author_email='contact@cnicodeme.com',
    keywords='domain parser tld top-level domain subdomain',
    project_urls={
        'Source': 'https://github.com/cnicodeme/tldparse',
    },
    packages=find_packages(),
    package_data={'': ['tldparse/public_suffix_list.dat']},
    include_package_data=True,
    platforms='any',

    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',

        'Topic :: Internet',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Networking',

        'License :: OSI Approved :: MIT License',

        "Operating System :: OS Independent",
        "Programming Language :: Python",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
