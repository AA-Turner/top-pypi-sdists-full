from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Mapping, MutableMapping

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from cerberus import Validator

# Re-export from _paths for backwards compatibility
from ._paths import KoloWriteError, create_kolo_directory  # noqa: F401

__all__ = ["KoloWriteError", "create_kolo_directory"]

DEFAULT_FLUSH_SUBTREE_MB = 500
DEFAULT_FLUSH_SUBTREE_BYTES = DEFAULT_FLUSH_SUBTREE_MB * 1024 * 1024

logger = logging.getLogger("kolo")


class InvalidConfig(Exception):
    pass


# This same list exists in config.rs
CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE = [
    "filters",
    "processors",
    "auto_emit",
    "flush_subtree_mb",
    "trace_points",
]

schema = {
    # Be careful about adding (non-omitted) keys here that don't have string or bool values
    # rust might not be able to dump them out in `pub fn collect_config`
    "filters": {
        "type": "dict",
        "schema": {
            "include_frames": {"type": "list"},
            "ignore_frames": {"type": "list"},
            "ignore_request_paths": {"type": "list"},
        },
    },
    "hide_startup_message": {"type": "boolean"},
    "lightweight_repr": {"type": "boolean"},
    "line_events": {"type": "boolean"},
    "omit_return_locals": {"type": "boolean"},
    "processors": {"type": "list"},
    "production_beta": {"type": "boolean"},
    "sqlite_busy_timeout": {"type": "integer"},
    "threading": {"type": "boolean"},
    "use_monitoring": {"type": "boolean"},
    "use_msgpack": {"type": "boolean"},
    "use_rust": {"type": "boolean"},
    "auto_emit": {"type": "boolean"},
    # trace_points: when one of the listed functions returns, kolo
    # snapshots its frame slice and saves it as a standalone top-level
    # trace via a daemon save worker.
    #
    # Healthy saves are async on a long-lived worker. If the worker is
    # unavailable or saturated, kolo falls back to inline save so the
    # trace still persists instead of being silently dropped. Process
    # crash can still lose unfinished work. "Function returned"
    # therefore does NOT imply "trace persisted now". Reach for trace
    # points for low-cardinality observability sampling, not for durable
    # audit trails.
    "trace_points": {
        "type": "dict",
        "schema": {
            "on_return": {
                "type": "list",
                "schema": {"type": "string"},
            },
        },
    },
    # Flush threshold in megabytes. Accepts integer or float (fractional
    # MB) so tests can pin sub-megabyte thresholds to force flushes on
    # small fixtures. Also accepts ``false`` to disable flushing entirely
    # (TOML has no null literal). Converted to bytes at read time.
    "flush_subtree_mb": {
        "type": ["integer", "float", "boolean"],
        "nullable": True,
        "min": 0,
    },
}
pyproject_schema = {
    "tool": {
        "type": "dict",
        "schema": {
            "kolo": {
                "type": "dict",
                "schema": schema,
                "allow_unknown": False,
            },
        },
    },
}
validator = Validator(schema, allow_unknown=False)
pyproject_validator = Validator(pyproject_schema, allow_unknown=True)


def clear_errors(config: MutableMapping[str, Any], errors) -> None:
    for error in errors:
        key = error.document_path[-1]
        if error.info:
            for info in error.info:
                clear_errors(config[key], info)
        else:
            del config[key]


def load_config_from_toml(path: Path) -> MutableMapping[str, Any]:
    try:
        with open(path, "rb") as conf:
            config = tomllib.load(conf)
    except FileNotFoundError:
        logger.info(
            'Kolo config file "%s" not found. Using default configuration.', path
        )
        return {}
    if not validator.validate(config):
        logger.warning("Kolo config file has errors: %s", validator.errors)
        clear_errors(config, validator._errors)
    return config


def load_config_from_pyproject_toml(path: Path) -> MutableMapping[str, Any]:
    try:
        with open(path, "rb") as conf:
            config = tomllib.load(conf)
    except FileNotFoundError:
        logger.info("%s config file not found. Trying next configuration option.", path)
        raise InvalidConfig()
    if not pyproject_validator.validate(config):
        logger.warning(
            "pyproject.toml config file has errors: %s", pyproject_validator.errors
        )
        clear_errors(config, pyproject_validator._errors)
    try:
        return config["tool"]["kolo"]
    except KeyError:
        raise InvalidConfig()


def _merge_dicts(*dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result


def _merge_with(func, *dicts):
    collected: dict[str, list] = {}
    for d in dicts:
        for k, v in d.items():
            if k in collected:
                collected[k].append(v)
            else:
                collected[k] = [v]
    return {k: func(v) for k, v in collected.items()}


def merge_or_last(args):
    if all(isinstance(arg, dict) for arg in args):
        return _merge_dicts(*args)
    return args[-1]


def resolve_flush_subtree_bytes(config: Mapping[str, Any]) -> int | None:
    """Pick the flush-subtree threshold (in bytes) from the user config.

    Reads ``flush_subtree_mb`` (integer or float megabytes, or ``false``
    to disable flushing — TOML has no null literal). Returns the
    threshold in bytes, ``None`` if flushing is explicitly disabled, or
    ``DEFAULT_FLUSH_SUBTREE_BYTES`` if the key is unset.
    """
    import math

    if "flush_subtree_mb" not in config:
        return DEFAULT_FLUSH_SUBTREE_BYTES
    mb = config.get("flush_subtree_mb")
    if mb is None:
        return None
    if isinstance(mb, bool):
        if mb:
            raise ValueError(
                "flush_subtree_mb = true is not valid; use false to disable "
                "or a non-negative number to set the threshold"
            )
        return None
    if isinstance(mb, float) and not math.isfinite(mb):
        raise ValueError(
            "flush_subtree_mb must be a finite non-negative number or false"
        )
    if mb < 0:
        raise ValueError("flush_subtree_mb must be >= 0 or false")
    return int(mb * 1024 * 1024)


def load_config(
    extra_config: Mapping[str, Any] | None = None,
) -> MutableMapping[str, Any]:
    kolo_directory = create_kolo_directory()
    pyproject_toml_path = Path("pyproject.toml")
    try:
        config = load_config_from_pyproject_toml(pyproject_toml_path)
    except InvalidConfig:
        config = load_config_from_toml(kolo_directory / "config.toml")
    if extra_config:
        return _merge_with(merge_or_last, config, extra_config)
    return config
