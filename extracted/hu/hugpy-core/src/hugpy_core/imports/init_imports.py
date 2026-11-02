"""One-stop import surface (the house ``init_imports`` convention): common stdlib
plus the shared hugpy_core primitives, so a module can do
``from hugpy_core.imports.init_imports import *``.

Note on heavy deps: ``flask`` is a hard dependency imported at module level across
hugpy_core, so importing it eagerly here is fine; ``psycopg`` is imported lazily
inside the functions that use it (46 of 49 sites) to keep import light and DB
contact deferred, so it is NOT re-exported here — import it at its use site.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import time
from typing import Any, Iterable, Optional

from hugpy_core.imports import classes as classes
from hugpy_core.imports import constants as C
from hugpy_core.imports import functions as functions
from hugpy_core.imports.constants import (
    DEFAULT_CORE_DSN, DEFAULT_SELF_BASE, ENV_BRAIN_MODEL, ENV_CALLLOG_DSN,
    ENV_CORE_DB, ENV_SELF_BASE,
)
from hugpy_core.imports.functions import core_dsn, env_float, env_str, self_base

__all__ = [
    "os", "sys", "json", "time", "logging", "Optional", "Any", "Iterable",
    "C", "constants", "functions", "classes",
    "DEFAULT_CORE_DSN", "DEFAULT_SELF_BASE", "ENV_CORE_DB", "ENV_CALLLOG_DSN",
    "ENV_SELF_BASE", "ENV_BRAIN_MODEL",
    "core_dsn", "self_base", "env_str", "env_float",
]
