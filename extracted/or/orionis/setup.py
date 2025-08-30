from setuptools import setup, find_packages
from orionis.metadata.framework import *

"""
Configures the packaging and distribution settings for the Orionis Framework Python project.

This script uses setuptools to define the metadata, dependencies, and configuration required
to build, install, and distribute the Orionis Framework package.

Attributes
----------
NAME : str
    The name of the project, imported from orionis.metadata.framework.
VERSION : str
    The version of the project, imported from orionis.metadata.framework.
AUTHOR : str
    The author's name, imported from orionis.metadata.framework.
AUTHOR_EMAIL : str
    The author's email, imported from orionis.metadata.framework.
DESCRIPTION : str
    A short description of the project, imported from orionis.metadata.framework.
FRAMEWORK : str
    The project homepage URL, imported from orionis.metadata.framework.
DOCS : str
    The documentation URL, imported from orionis.metadata.framework.
CLASSIFIERS : list of str
    List of PyPI classifiers, imported from orionis.metadata.framework.
PYTHON_REQUIRES : str
    Minimum required Python version, imported from orionis.metadata.framework.
REQUIRES : list of str
    List of required dependencies, imported from orionis.metadata.framework.
KEYWORDS : list of str
    List of keywords for the project, imported from orionis.metadata.framework.

Notes
-----
- Reads the long description from the README.md file.
- Includes additional files as specified in MANIFEST.in.
- Excludes specified packages from the distribution.
- Sets up the test suite directory.
- The project is marked as zip safe.
"""

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    url=FRAMEWORK,
    docs_url=DOCS,
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(
        exclude=[
            'app', 'app.*',
            'bootstrap', 'bootstrap.*',
            'config', 'config.*',
            'database', 'database.*',
            'routes', 'routes.*',
            'storage', 'storage.*',
            'tests', 'tests.*'
        ]
    ),
    include_package_data=True,
    classifiers=CLASSIFIERS,
    python_requires=PYTHON_REQUIRES,
    install_requires=REQUIRES,
    keywords=KEYWORDS,
    zip_safe=False
)