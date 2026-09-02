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
from __future__ import annotations

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

Extra
=========================

{pip_package_name} has the following optional groups:

- `application-utils` (requires Python 3.11+): Light async ORM over the
    DataRobot Agentic Memory Service, plus an AG-UI chat-history layer (models, repositories, and AG-UI event storage).
    This can be used in DataRobot Custom Applications and Agent Workflows.
- `auth` (requires Python 3.9+): Provides an abstraction to handle OAuth2 authentication with DataRobot API (11.1+).
    This can be used in DataRobot Custom Applications and on its own.
- `auth-authlib` (requires Python 3.9+): OAuth2 authentication handling via Authlib.
    This can be used in DataRobot Custom Applications and on its own.
- `core` (requires Python 3.8+): Platform library functions to improve building with DataRobot.
    This can be used in DataRobot Custom Applications, Custom Models, and Agent Workflows.
- `fs` (requires Python 3.9+): Provides file system implementation to work with the DataRobot file system.
- `query-engine` (requires Python 3.9+): Engine to run SQLAlchemy-compatible queries against DataRobot data stores
    and JDBC connections.

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
    "Programming Language :: Python :: 3.14",
]


with open("datarobot/_version.py") as fd:
    version_search = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE)
    if not version_search:
        raise RuntimeError("Cannot find version information")
    version = version_search.group(1)

if not version:
    raise RuntimeError("Cannot find version information")

# TODO replace with astral ty
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
    # Pillow has no prebuilt wheel for cp314 before 11.3.0, so pip builds it from
    # source. The CI test image's Dockerfile only installs libjpeg-dev/zlib1g-dev,
    # not libtiff-dev, so a from-source 10.4.0 build silently loses TIFF support
    # (OSError: encoder libtiff not available) instead of failing the build.
    # 11.3.0+ ships a prebuilt manylinux wheel with libtiff already compiled in.
    "Pillow==10.4.0; python_version >= '3.8' and python_version < '3.14'",
    "Pillow==9.5.0; python_version < '3.8'",
    "Pillow>=11.3.0; python_version >= '3.14'",
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

core_require = [
    "pydantic-settings>=2.2.0",
    "pydantic>=2.2.0",
    "psutil>=7.2.1",
]

files_require = [
    "fsspec>=2025.5.0",
]

query_engine_require = [
    "sqlalchemy>=2.0.0",
]

otel_require = [
    "opentelemetry-sdk>=1.33.0,<2.0.0",
]

# application-utils: light async ORM over the DataRobot Agentic Memory Service (the
# `persistence` sub-package) plus the `chat_history` layer, which includes the AG-UI storage
# layer over `ag-ui-protocol`. Standalone leaf — depends only on httpx, pydantic, and
# ag-ui-protocol (no DataRobot SDK or OTel weight). Requires Python 3.11+ — excluded from the
# 3.7/3.8 vermin gates in vermin.ini and checked at 3.11 by `make vermin-application-utils`.
# The `python_version` markers keep a sub-3.11 `pip install datarobot[application-utils]` from
# resolving these deps at all; `datarobot/application_utils/__init__.py` turns that into an
# explicit error. The `~=0.1.15` compatible-release pin lets a standalone install track 0.1.x
# agent-message protocol updates; keep it aligned with all consumers of AG-UI messages.
application_utils_require = [
    "httpx>=0.28.1 ; python_version >= '3.11'",
    "pydantic>=2.6.1 ; python_version >= '3.11'",
    "ag-ui-protocol~=0.1.15 ; python_version >= '3.11'",
]

# The same deps without the `python_version` markers, for `[lint]` only. The Lint stage
# runs on 3.9 (.harness/Lint.yaml), where the markers above resolve to nothing -- so
# `ag-ui-protocol` would not be installed and `make mypy-application-utils` would check
# the AG-UI layer against `Any` (`ignore_missing_imports`), failing on `Any` subclasses
# and "unused" ignores that are needed once the real types resolve. These are all
# pure-Python and support 3.9, so installing them under a 3.9 interpreter is fine; the
# shipped `[application-utils]` extra keeps its 3.11 markers, which are what make a
# sub-3.11 install resolve to nothing.
application_utils_lint_require = [
    "httpx>=0.28.1",
    "pydantic>=2.6.1",
    "ag-ui-protocol~=0.1.15",
]

lint_require = (
    [
        "ruff==0.16.0",
        "vermin>=1.8.0",
    ]
    + _mypy_require
    + images_require
    + databricks_require
    + auth_lint_require
    + core_require
    + files_require
    + query_engine_require
    + application_utils_lint_require
)

tests_require = (
    [
        "pytest>=7.3.0,<8.0.0 ; python_version < '3.8'",
        "pytest>=8.3.0,<8.4.0 ; python_version >= '3.8' and python_version < '3.14'",
        # 8.3.x (last release 8.3.5) predates Python 3.14 and never declares support for it
        # in its classifiers/requires-python metadata. 8.4.0 is the first release to
        # officially declare 3.9-3.14 support, so pin to it under 3.14 to close that gap.
        "pytest>=8.4.0 ; python_version >= '3.14'",
        "pytest-cov",
        "responses==0.21",
        # pytest-asyncio 0.21.1 calls the now-deprecated asyncio.iscoroutinefunction()
        # during collection for every test item, which balloons memory under Python 3.14
        # (see CFX-7752). 1.0.0 fixes that but requires python_version >= 3.9, so it can't
        # be used unconditionally - this repo still tests 3.7/3.8.
        "pytest-asyncio==0.21.1; python_version < '3.14'",
        "pytest-asyncio==1.0.0; python_version >= '3.14'",
        "pyarrow",
        "pymarkdownlnt",
    ]
    + images_require
    + databricks_require
    + auth_test_require
    + files_require
    + query_engine_require
    + application_utils_require
)

docs_require = [
    "Sphinx>=8.1.3 ; python_version >= '3.11'",
    "sphinx_rtd_theme>=3.0",
    "sphinx-external-toc",
    "nbsphinx>=0.9.5",
    "jupyter_contrib_nbextensions",
    "sphinx-autodoc-typehints>=2 ; python_version >= '3.8'",
    "sphinxcontrib-spelling==8.0.2",
    "pyenchant==3.2.2",
    "sphinx-copybutton",
    "sphinx-markdown-builder",
    "myst-parser==4.0.0",
]

dev_require = (
    tests_require + lint_require + images_require + docs_require + core_require + files_require + query_engine_require
)

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

pipelines_require = [
    # covalent SDK-only runtime deps (source is vendored, but these are needed at runtime)
    "aiofiles>=0.8.0",
    "aiohttp>=3.8.1",
    "cloudpickle>=2.0.0,<3",
    "filelock>=3.12.2",
    "furl>=2.1.3",
    "networkx>=2.8.6",
    "toml>=0.10.2",
    "watchdog>=2.0.3",
    "psutil>=5.9.0",
    # covalent-cloud runtime deps (source is vendored). Lower bounds mirror
    # what upstream covalent-cloud-sdk/requirements.txt was tested against.
    "arrow>=1.2.2",
    "ipywidgets>=8.1.3",
    "packaging",
    "pydantic-settings>=2.0.0",
    "rich>=12.0.0",
]


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
        "Documentation": "https://docs.datarobot.com/en/docs/api/reference/sdk/index.html",
        "Changelog": "https://docs.datarobot.com/en/docs/api/reference/changelogs/py-changelog/index.html",
    },
    license="DataRobot Tool and Utility Agreement",
    packages=None,
    # Top-level so the dr plugin manifest skips the SDK import.
    py_modules=["_dr_dev_plugin"],
    package_data={"datarobot": ["py.typed"]},
    entry_points={
        "console_scripts": [
            "drdev = datarobot.core.dev:cli_main",
            "dr-dev = _dr_dev_plugin:main",
        ],
    },
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
        "strenum>=0.4.15",
        "pytz>=2020.1",
        "python-dateutil>=2.8.2",
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
        "core": core_require,
        "fs": files_require,
        "otel": otel_require,
        "query-engine": query_engine_require,
        "application-utils": application_utils_require,
        "pipelines": pipelines_require,
    },
)
