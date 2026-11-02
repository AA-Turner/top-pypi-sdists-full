"""hugpy_core.imports — shared primitives.

Single source of truth for constants and helper functions that were hard-coded /
duplicated across the package. Importing this package has no side effects and
pulls in no heavy dependency.

Layout (house convention): constants.py, functions.py, classes.py, and
init_imports.py (the one-stop ``from hugpy_core.imports.init_imports import *``).
"""
from __future__ import annotations

from hugpy_core.imports import classes, constants, functions
from hugpy_core.imports.constants import (
    DEFAULT_CORE_DSN, DEFAULT_SELF_BASE, ENV_BRAIN_MODEL, ENV_CALLLOG_DSN,
    ENV_CORE_DB, ENV_CORE_SCHEMA, ENV_SELF_BASE,
    PAIR_KNOB_KEYS, PAIR_KNOB_RENAMES, PAIR_SETTING_DEFAULTS,
)
from hugpy_core.imports.functions import (
    core_dsn, effective_pair_settings, env_float, env_str, notify_channel,
    self_base, validate_pair_knobs,
)

__all__ = [
    "constants", "functions", "classes",
    "DEFAULT_CORE_DSN", "DEFAULT_SELF_BASE", "ENV_CORE_DB", "ENV_CORE_SCHEMA",
    "ENV_CALLLOG_DSN", "ENV_SELF_BASE", "ENV_BRAIN_MODEL",
    "PAIR_KNOB_KEYS", "PAIR_KNOB_RENAMES", "PAIR_SETTING_DEFAULTS",
    "core_dsn", "self_base", "env_str", "env_float",
    "effective_pair_settings", "validate_pair_knobs", "notify_channel",
]
