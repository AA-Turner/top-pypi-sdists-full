"""Tests for trusted reconciliation migration helpers."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.migrations import (
    backfill_inline_history_to_archive,
    migrate_manifest_schema,
    serialize_manifest_document,
)


def test_migrate_manifest_schema_adds_defaults() -> None:
    migrated = migrate_manifest_schema(
        {"repo": "owner/repo", "ledgers": {"r1": {"observations": [{"reason": "x" * 5000}]}}}
    )
    assert migrated["schema_version"] == 2
    assert migrated["inventory"] == {}
    assert migrated["archive_pointers"] == {}
    assert "_truncation" in migrated["ledgers"]["r1"]["observations"][0]


def test_backfill_inline_history_normalizes_channel_entries() -> None:
    document = {"repo": "owner/repo", "ledgers": {"r1": {"decisions": [{"reason": "ok"}]}}}
    migrated = backfill_inline_history_to_archive(document, channel="decisions")
    assert migrated["ledgers"]["r1"]["decisions"][0]["reason"] == "ok"


def test_serialize_manifest_document_is_deterministic() -> None:
    document = {"b": 1, "a": 2}
    assert serialize_manifest_document(document) == '{"a":2,"b":1}'


def test_migrate_manifest_ignores_non_list_ledger_channels() -> None:
    migrated = migrate_manifest_schema({"ledgers": {"r1": {"observations": "invalid"}}})
    assert migrated["ledgers"]["r1"]["observations"] == "invalid"
