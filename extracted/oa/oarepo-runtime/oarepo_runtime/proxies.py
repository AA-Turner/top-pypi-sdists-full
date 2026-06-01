#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Proxies."""

from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING

from flask import current_app
from werkzeug.local import LocalProxy

if TYPE_CHECKING:
    from oarepo_runtime.ext import OARepoRuntime

    current_runtime: OARepoRuntime  # type: ignore[reportRedeclaration]

# note: mypy does not understand LocalProxy[OARepoRuntime], so we type it as OARepoRuntime
# and ignore the redeclaration error
current_runtime = LocalProxy(lambda: current_app.extensions["oarepo-runtime"])  # type: ignore[assignment]

current_timezone: ContextVar = ContextVar("timezone")
