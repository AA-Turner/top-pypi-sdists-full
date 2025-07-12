#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
import re
import sys

DESCRIPTION_TEMPLATE = """
About {package_name}
============================
.. image:: https://img.shields.io/pypi/v/{package_name}.svg
   :target: {pypi_url_target}
.. image:: https://img.shields.io/pypi/pyversions/{package_name}.svg
.. image:: https://img.shields.io/pypi/status/{package_name}.svg

DataRobot is a client library for working with the `DataRobot`_ platform API. {extra_desc}

This package is released under the terms of the DataRobot Tool and Utility Agreement, which
can be found on our `Legal`_ page, along with our privacy policy and more.

Installation
=========================
Python {python_versions} are supported.
You must have a datarobot account.

::

   $ pip install {pip_package_name}

Usage
=========================
The library will look for a config file `~/.config/datarobot/drconfig.yaml` by default.
This is an example of what that config file should look like.

::

   token: your_token
   endpoint: https://app.datarobot.com/api/v2

Alternatively a global client can be set in the code.

::

   import datarobot as dr
   dr.Client(token='your_token', endpoint='https://app.datarobot.com/api/v2')

Alternatively environment variables can be used.

::

   export DATAROBOT_API_TOKEN='your_token'
   export DATAROBOT_ENDPOINT='https://app.datarobot.com/api/v2'

See `documentation`_ for example usage after configuring.

Extra
=========================

{pip_package_name} has the following optional groups:

- `auth` (requires Python 3.9+): Provides an abstraction to handle OAuth2 authentication with DataRobot API (11.1+).
    This can be used in DataRobot Custom Applications and on its own.
- `auth-authlib` (requires Python 3.9+): OAuth2 authentication handling via Authlib.
    This can be used in DataRobot Custom Applications and on its own.

You can install these optional groups by specifying them in the pip command, for example:

::

    $ pip install {pip_package_name}[auth]


Helpful links
=========================
- `API quickstart guide <https://docs.datarobot.com/en/docs/api/api-quickstart/index.html>`_
- `Code examples <https://docs.datarobot.com/en/docs/api/guide/python/index.html>`_
- `Common use cases <https://docs.datarobot.com/en/docs/api/guide/common-case/index.html>`_

Bug Reporting and Q&A
=========================
To report issues or ask questions, send email to `the team <api-maintainer@datarobot.com>`_.

.. _datarobot: https://datarobot.com
.. _documentation: {docs_link}
.. _legal: https://www.datarobot.com/legal/
"""


DEFAULT_CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]


with open("datarobot/_version.py") as fd:
    version_search = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE)
    if not version_search:
        raise RuntimeError("Cannot find version information")
    version = version_search.group(1)

if not version:
    raise RuntimeError("Cannot find version information")

_mypy_require = [
    "mypy==1.16.0",
    "types-PyYAML==6.0.12",
    "types-python-dateutil==2.8.19",
    "types-pytz==2022.2.1.0",
    "types-requests==2.28.11",
    "types-urllib3==1.26.25",
    "types-decorator==5.1.8",
]

images_require = [
    "Pillow==10.4.0; python_version >= '3.8'",
    "Pillow==9.5.0; python_version < '3.8'",
]

databricks_require = ["databricks-connect>=13.0"]
if sys.version_info < (3, 8, 0):
    databricks_require.append("databricks-sdk==0.44.1")

auth_require = [
    "pydantic>=2.11.3",
    "httpx>=0.28.1",
    "eval-type-backport; python_version < '3.10'",  # For compatibility with Python 3.10+ typing
]

authlib_require = ["authlib>=1.6.0"] + auth_require
auth_lint_require = authlib_require + ["respx"]
auth_test_require = auth_lint_require

lint_require = (
    [
        "black==24.4.2",
        "black[jupyter]==24.4.2",
        "isort==5.10.1",
        "flake8==5.0.4",
        "pylint==2.15.0",
    ]
    + _mypy_require
    + images_require
    + databricks_require
    + auth_lint_require
)

tests_require = (
    [
        "pytest>=7.3.0,<8.0.0 ; python_version < '3.8'",
        "pytest>=8.3.0,<8.4.0 ; python_version >= '3.8'",
        "pytest-cov",
        "responses==0.21",
        "pytest-asyncio==0.21.1",
        "pyarrow",
    ]
    + images_require
    + databricks_require
    + auth_test_require
)

docs_require = [
    "Sphinx>=8.1.3 ; python_version >= '3.11'",
    "sphinx_rtd_theme>=3.0",
    "sphinx-external-toc",
    "nbsphinx>=0.9.5",
    "jupyter_contrib_nbextensions",
    "sphinx-autodoc-typehints>=2 ; python_version >= '3.8'",
    "sphinxcontrib-spelling==8.0.0",
    "pyenchant==3.2.2",
    "sphinx-copybutton",
    "sphinx-markdown-builder",
    "myst-parser==4.0.0",
]

dev_require = tests_require + lint_require + images_require + docs_require

example_require = [
    "jupyter<=5.0",
    "fredapi==0.4.0",
    "matplotlib>=2.1.0",
    "seaborn<=0.8",
    "scikit-learn<=0.18.2",
    "wordcloud<=1.3.1",
    "colour<=0.1.4",
]

release_require = ["zest.releaser[recommended]==6.22.0"]


# The None-valued kwargs should be updated by the caller
common_setup_kwargs = dict(
    name=None,
    version=None,
    description="This client library is designed to support the DataRobot API.",
    author="datarobot",
    author_email="api-maintainer@datarobot.com",
    maintainer="datarobot",
    maintainer_email="api-maintainer@datarobot.com",
    url="https://datarobot.com",
    project_urls={
        "Documentation": "https://docs.datarobot.com/en/docs/api/reference/sdk/",
        "Changelog": "https://docs.datarobot.com/en/docs/api/reference/changelogs/py-changelog/index.html",
    },
    license="DataRobot Tool and Utility Agreement",
    packages=None,
    package_data={"datarobot": ["py.typed"]},
    python_requires=">=3.7",
    long_description=None,
    classifiers=None,
    install_requires=[
        "pandas>=0.15",
        "numpy",
        "pyyaml>=3.11",
        "requests>=2.28.1",
        "requests_toolbelt>=0.6",
        "trafaret>=0.7,<2.2,!=1.1.0",
        "urllib3>=1.23",
        "typing-extensions>=4.3.0,<5",
        "mypy-extensions>=0.4.0,<2",
        "strenum>=0.4.15",
    ],
    extras_require={
        "dev": dev_require,
        "examples": example_require,
        "release": release_require,
        "lint": lint_require,
        "docs": docs_require,
        "images": images_require,
        "test": tests_require,
        "databricks": databricks_require,
        "auth": auth_require,
        "auth-authlib": authlib_require,
    },
)
