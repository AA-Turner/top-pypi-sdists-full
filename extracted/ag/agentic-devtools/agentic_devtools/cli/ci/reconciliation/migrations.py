"""State-schema migration and legacy backfill helpers for trusted reconciliation."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from agentic_devtools.cli.ci.reconciliation.repository import normalize_immutable_entry


def migrate_manifest_schema(document: dict[str, Any]) -> dict[str, Any]:
    """Migrate legacy reconciliation documents to the trusted-manifest schema."""
    migrated = deepcopy(document)
    migrated.setdefault("schema_version", 2)
    migrated.setdefault("inventory", {})
    migrated.setdefault("ledgers", {})
    migrated.setdefault("archive_pointers", {})
    migrated.setdefault("overflow_alerts", [])
    for record_id, ledger in list(dict(migrated["ledgers"]).items()):
        migrated["ledgers"][record_id] = _normalize_ledger_entries(dict(ledger))
    return migrated


def backfill_inline_history_to_archive(
    document: dict[str, Any],
    *,
    channel: str,
) -> dict[str, Any]:
    """Normalize legacy inline immutable history before future shard rollover."""
    migrated = migrate_manifest_schema(document)
    for record_id, ledger in list(dict(migrated["ledgers"]).items()):
        entries = list(dict(ledger).get(channel, []))
        normalized = [normalize_immutable_entry(dict(entry)) for entry in entries]
        migrated["ledgers"][record_id][channel] = normalized
    return migrated


def serialize_manifest_document(document: dict[str, Any]) -> str:
    """Serialize migrated manifest deterministically."""
    return json.dumps(document, sort_keys=True, separators=(",", ":"))


def _normalize_ledger_entries(ledger: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(ledger)
    for channel in ("observations", "decisions", "invalidations", "leases"):
        values = normalized.get(channel, [])
        if isinstance(values, list):
            normalized[channel] = [normalize_immutable_entry(dict(value)) for value in values]
    return normalized
