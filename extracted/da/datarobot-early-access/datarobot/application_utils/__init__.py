#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
"""Utilities for building DataRobot agentic applications.

Ships in the ``[application-utils]`` install extra::

    pip install datarobot[application-utils]

Unlike the rest of the SDK this sub-package requires Python 3.11+ and pulls in
``httpx`` / ``pydantic``, so both the interpreter floor and the extra are checked
here — at package import, before any sub-module runs — to turn what would
otherwise be a confusing downstream ``SyntaxError`` or ``ModuleNotFoundError``
into an actionable message.

This module is deliberately written in widely-compatible syntax: a 3.9
interpreter must be able to *parse* it in order to reach the version check below.
"""

from __future__ import annotations

import sys

# The whole sub-package targets 3.11+ (see `make vermin-application-utils`).  The
# `python_version` markers on the extra's dependencies mean a sub-3.11 install
# resolves to no dependencies at all, so check the interpreter before the imports.
if sys.version_info < (3, 11):
    raise RuntimeError(
        "datarobot.application_utils requires Python 3.11 or later "
        "(running {}.{}.{}).  The rest of the datarobot package supports older "
        "interpreters; only this sub-package has the higher floor.".format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2]
        )
    )

try:
    import httpx  # noqa: F401
    import pydantic  # noqa: F401
except ImportError as exc:
    raise ImportError(
        "datarobot.application_utils requires installation of the datarobot library "
        "with its optional `application-utils` dependencies. To install the library "
        "with application-utils support please use "
        "`pip install datarobot[application-utils]`"
    ) from exc
