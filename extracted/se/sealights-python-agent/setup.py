"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

import python_agent

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    readme = f.read()

with open(path.join(here, "CHANGES.rst"), encoding="utf-8") as f:
    changes = f.read()

with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read().splitlines()
    # python 3.3 use case where dependencies are read as bytes of the form b'APScheduler==3.0.6'
    requirements = [
        requirement.decode() if isinstance(requirement, bytes) else requirement
        for requirement in requirements
    ]

setup(
    name=python_agent.__package_name__,
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=python_agent.__version__,
    description="Tricentis Sealights Python Agent - Quality Intelligence and Code Coverage",
    long_description="\n\n".join([readme, changes]),
    long_description_content_type="text/x-rst",
    url="https://www.tricentis.com/products/sealights",
    project_urls={
        "Documentation": "https://docs.sealights.io/knowledgebase",
        "Support": "https://support.tricentis.com/",
    },
    author="Tricentis Sealights",
    author_email="support@sealights.io",
    maintainer="Tricentis Sealights",
    maintainer_email="support@sealights.io",
    license="Other/Proprietary License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    python_requires=">=3.10, <4",
    # What does your project relate to?
    keywords="sealights tricentis python agent coverage testing quality intelligence",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs", "*tests*"]),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=requirements,
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
        # The >=7.0 floor is functional, not conventional: Listener API v3
        # gained start_keyword / end_keyword only in Robot Framework 7.0. On
        # 6.x Robot assigns both to None for a v3 listener and never calls
        # them, which would silently delete every navigation re-color and the
        # flush-before-close on all three browser stacks (Rule 30bis, AC57).
        "robot": ["robotframework>=7.0", "opentelemetry-api"],
    },
    # Ensure console message templates ship with the package.
    package_data={
        "python_agent.console_messages.common": ["*.json"],
    },
    include_package_data=True,
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        "console_scripts": [
            "sealights-admin=python_agent.admin:cli",
            "sl-python=python_agent.admin:cli",
        ],
    },
)
