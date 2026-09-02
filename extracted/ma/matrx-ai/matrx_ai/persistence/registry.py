"""Table registry — maps an exact ``schema.table`` key to a Model class.

The coordinator's flush needs to translate ``WriteOp(table="cx_message", ...)``
into a concrete ``cxm.message.model.bulk_create(...)`` / ``bulk_update(...)``
call. This registry holds the mapping.

Registration is explicit and ownership is automatic: every table in this
registry is Coordinator-owned. The host may install a package-safe policy
registrar; it is called for every new entry and replayed across existing ones.
There is no second ownership list to synchronize.

Why not import matrx-orm globally?
----------------------------------
Per the package independence rule, ``matrx_ai`` must not import matrx-orm at
module top level. The registry's values are Model classes (which are
matrx-orm constructs), but those classes are obtained via the host's
injection pattern (``matrx_ai.db._registry.get_model``) which is already
in use throughout the package. We never import matrx-orm here.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from matrx_utils import vcprint

logger = logging.getLogger("matrx_ai.persistence.registry")

# A "model-like" is any class with classmethods ``bulk_create(list[dict])``
# and ``bulk_update(list[instance], list[str])`` — i.e. matrx-orm Model.
ModelLike = Any  # type: ignore[misc]


@dataclass(frozen=True, slots=True)
class RegisteredTable:
    name: str
    model_cls: ModelLike
    write_owner: str = "coordinator"


PolicyRegistrar = Callable[[RegisteredTable], None]

_tables: dict[str, RegisteredTable] = {}
_policy_registrar: PolicyRegistrar | None = None
# Keys already screamed about — the banner fires once per bad key per process,
# while the ERROR log (and therefore public.app_log) records every occurrence.
_coerced_keys_screamed: set[str] = set()


def configure_policy_registrar(registrar: PolicyRegistrar | None) -> None:
    """Install the host policy hook and replay every existing registration."""
    global _policy_registrar
    _policy_registrar = registrar
    if registrar is None:
        return
    for entry in _tables.values():
        _apply_policy(registrar, entry)


def _apply_policy(registrar: PolicyRegistrar, entry: RegisteredTable) -> None:
    try:
        registrar(entry)
    except Exception as exc:
        message = (
            "\n"
            "████████████████████████████████████████████████████████████████████\n"
            "██  COORDINATOR POLICY INSTALLATION FAILED                        ██\n"
            "████████████████████████████████████████████████████████████████████\n"
            f"  Table       : {entry.name}\n"
            f"  Model       : {getattr(entry.model_cls, '__name__', entry.model_cls)}\n"
            f"  Error       : {type(exc).__name__}: {exc}\n"
            "  Registration remains present; release validation will keep reporting it.\n"
            "████████████████████████████████████████████████████████████████████\n"
        )
        vcprint(message, color="red", log_level="ERROR")
        logger.error("Coordinator policy installation failed for %s", entry.name)


def register_table(table: str, model_cls: ModelLike) -> None:
    """Register a Coordinator table and automatically install its write policy."""
    normalized = table.strip()
    if not normalized:
        raise ValueError("persistence registry table name cannot be blank")
    if normalized.count(".") != 1 or any(not part for part in normalized.split(".")):
        raise ValueError(
            f"persistence registry requires schema.table, got {table!r}; "
            "a bare table name is never a registry key"
        )
    meta = getattr(model_cls, "_meta", None)
    model_table = getattr(meta, "table_name", None) if meta is not None else None
    model_schema = (getattr(meta, "db_schema", None) if meta is not None else None) or "public"
    if model_table and normalized != f"{model_schema}.{model_table}":
        raise ValueError(
            f"persistence registry key {normalized!r} does not match Model identity "
            f"{model_schema}.{model_table}"
        )
    existing = _tables.get(normalized)
    if existing is not None and existing.model_cls is not model_cls:
        message = (
            "\n"
            "████████████████████████████████████████████████████████████████████\n"
            "██  COORDINATOR REGISTRY CONFLICT                                 ██\n"
            "████████████████████████████████████████████████████████████████████\n"
            f"  Table       : {normalized}\n"
            f"  Registered  : {getattr(existing.model_cls, '__name__', existing.model_cls)}\n"
            f"  Attempted   : {getattr(model_cls, '__name__', model_cls)}\n"
            "  The original registration remains authoritative.\n"
            "████████████████████████████████████████████████████████████████████\n"
        )
        vcprint(message, color="red", log_level="ERROR")
        logger.error("Coordinator registry conflict for %s", normalized)
        return
    if existing is not None:
        if _policy_registrar is not None:
            _apply_policy(_policy_registrar, existing)
        return
    entry = RegisteredTable(name=normalized, model_cls=model_cls)
    _tables[normalized] = entry
    if _policy_registrar is not None:
        _apply_policy(_policy_registrar, entry)


def _coercion_candidates(table: str) -> list[str]:
    """Registered keys whose relation part matches this lookup's relation part."""
    relation = table.rsplit(".", 1)[-1].strip()
    if not relation:
        return []
    return sorted(key for key in _tables if key.split(".", 1)[1] == relation)


def _scream_coercion(requested: str, resolved: str) -> None:
    """Loud, once-per-key alarm when a lookup key had to be reconciled.

    Reconciling is NOT approval: the call site is still a defect that
    ``scripts/check_persistence_table_keys.py`` fails the release on. This
    banner exists so the defect is impossible to miss while the user's write
    still lands.
    """
    logger.error(
        "persistence registry COERCED lookup key %r -> %r; fix the call site",
        requested,
        resolved,
    )
    if requested in _coerced_keys_screamed:
        return
    _coerced_keys_screamed.add(requested)
    vcprint(
        "\n"
        "████████████████████████████████████████████████████████████████████\n"
        "██  PERSISTENCE REGISTRY KEY COERCED — CALL SITE IS A DEFECT      ██\n"
        "████████████████████████████████████████████████████████████████████\n"
        f"  Requested   : {requested!r}\n"
        f"  Resolved to : {resolved!r}  (the ONLY registered match)\n"
        "  WHY COERCED : dropping the op would have failed the request's commit\n"
        "                barrier and lost a user's write over a spelling.\n"
        "  FIX         : pass the exact schema.table key at the call site.\n"
        "                Guard: python scripts/check_persistence_table_keys.py\n"
        "████████████████████████████████████████████████████████████████████\n",
        color="red",
        log_level="ERROR",
    )


def get_model(table: str) -> ModelLike:
    """Resolve a ``schema.table`` key to its registered Model.

    An exact key is the contract. When the key is not registered but exactly
    ONE registered table has that relation name (``'tool_call'`` /
    ``'wrong_schema.tool_call'`` → ``'chat.tool_call'``), the lookup is
    RECONCILED with a loud alarm instead of raising: there is exactly one
    thing the caller can mean, and raising here drops a user's write and kills
    a paid request over a spelling (root `CLAUDE.md` — "a guard that CAN
    reconcile MUST reconcile"). Ambiguous or unknown keys still raise, naming
    every candidate.
    """
    entry = _tables.get(table)
    if entry is not None:
        return entry.model_cls

    candidates = _coercion_candidates(table)
    if len(candidates) == 1:
        _scream_coercion(table, candidates[0])
        return _tables[candidates[0]].model_cls
    if len(candidates) > 1:
        raise KeyError(
            f"persistence registry: {table!r} is AMBIGUOUS — it matches "
            f"{candidates}. Pass the exact schema.table key."
        )
    raise KeyError(
        f"persistence registry: no Model registered for table {table!r}. "
        f"Did the queue_helpers module load before this op was queued?"
    )


def is_registered(table: str) -> bool:
    return table in _tables


def all_registered() -> dict[str, ModelLike]:
    """Return a copy of the current registry — for diagnostics only."""
    return {name: entry.model_cls for name, entry in _tables.items()}


def all_entries() -> tuple[RegisteredTable, ...]:
    return tuple(_tables.values())
