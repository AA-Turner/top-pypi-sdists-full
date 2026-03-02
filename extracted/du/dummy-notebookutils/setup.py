import io
import os
import re
from setuptools import setup, find_packages

import sys

DESCRIPTION = "A package that allows to use synapse mssparkutils without actual functionality. This helps to generate the build."

NAME = "dummy-notebookutils"
AUTHOR = "Microsoft Corporation"
AUTHOR_EMAIL='runtimeexpdg@microsoft.com'
URL = 'https://github.com/Azure/azure-synapse-analytics'

PACKAGES = find_packages(
    exclude=["*.tests"]
)

def read(path, encoding='utf-8'):
    with open(path, encoding=encoding) as fp:
        return fp.read()

def version(path):
    """Obtain the package version from a python file e.g. pkg/__init__.py

    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

print("arguments:" + str(sys.argv[:]))

README = read("README.md")
VERSION = version(os.path.join('notebookutils', '__init__.py'))

# replace build version
if "--version" in sys.argv:
    index = sys.argv.index("--version")
    if index < len(sys.argv) - 1:
        VERSION = sys.argv[index + 1]
        sys.argv.remove(VERSION)
        if VERSION.endswith("-SNAPSHOT"):  # Remove SNAPSHOT suffix
            VERSION = VERSION[:-len("SNAPSHOT") - 1]
        print("current version " + VERSION)
    else:
        raise RuntimeError("Unable to get the version from argument")
    sys.argv.remove("--version")

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    author=AUTHOR,
    author_email = AUTHOR_EMAIL,
    url=URL,
    packages=PACKAGES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'],
    install_requires=[
    ])
