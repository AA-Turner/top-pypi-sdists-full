"""Dependency-injection registry for DB models, base managers, and singleton
manager instances used by matrx-graph.

Mirrors matrx-ai's `matrx_ai.db._registry` exactly. The host app (aidream)
calls `configure_db(models=..., bases=..., instances=...)` at startup with
the matrx-orm-generated models + managers. matrx-graph code then calls
`get_model('WfDefinition')` / `get_base('WfDefinitionBase')` /
`get_instance('wf_definition_manager')` at runtime.

This inversion keeps matrx-graph free of direct imports on aidream's
`db/models.py` — the models can live wherever the host app wants, and
matrx-graph discovers them by name.

Before configure_db() has been called, all `get_*` calls raise
DBNotConfiguredError with a message explaining how to fix it.
"""

from __future__ import annotations

from typing import Any


class DBNotConfiguredError(RuntimeError):
    pass


_models: dict[str, Any] = {}
_bases: dict[str, Any] = {}
_instances: dict[str, Any] = {}
_extras: dict[str, Any] = {}
_configured: bool = False


def configure_db(
    *,
    models: dict[str, Any] | None = None,
    bases: dict[str, Any] | None = None,
    instances: dict[str, Any] | None = None,
    extras: dict[str, Any] | None = None,
) -> None:
    """Register DB artifacts with matrx-graph.

    Called once at app startup by the host app (e.g. aidream/package_integration.py).
    Subsequent calls merge additional entries without clearing existing ones,
    so packages can register in phases.
    """
    global _configured
    if models:
        _models.update(models)
        _declare_value_semantics(models)
    if bases:
        _bases.update(bases)
    if instances:
        _instances.update(instances)
    if extras:
        _extras.update(extras)
    _configured = True


def _declare_value_semantics(models: dict[str, Any]) -> None:
    """The run's value store keeps strings that look like JSON ON PURPOSE (an agent's answer is often JSON
    text): its ``value`` field stores them as strings, and must not raise matrx-orm's once-per-field
    "a str that looks like JSON" WARNING. The host's model is generated, so the package declares it here."""
    value_field = getattr(models.get("WfCheckpointValue"), "_fields", {}).get("value")
    if value_field is not None and hasattr(value_field, "strings_are_values"):
        value_field.strings_are_values = True


def is_configured() -> bool:
    return _configured


def _require(kind: str, name: str, bucket: dict[str, Any]) -> Any:
    if name not in bucket:
        known = sorted(bucket)
        raise DBNotConfiguredError(
            f"matrx-graph DB {kind} '{name}' is not registered. "
            f"Known {kind}s: {known!r}. "
            f"Call matrx_graph.db.configure_db({kind}s={{...}}) at startup."
        )
    return bucket[name]


def get_model(name: str) -> Any:
    return _require("model", name, _models)


def get_base(name: str) -> Any:
    return _require("base", name, _bases)


def get_instance(name: str) -> Any:
    return _require("instance", name, _instances)


def get_extra(name: str) -> Any:
    return _require("extra", name, _extras)


def try_get_model(name: str) -> Any | None:
    return _models.get(name)


def try_get_instance(name: str) -> Any | None:
    return _instances.get(name)


def reset_for_tests() -> None:
    """Wipe the registry. For tests only."""
    global _configured
    _models.clear()
    _bases.clear()
    _instances.clear()
    _extras.clear()
    _configured = False
