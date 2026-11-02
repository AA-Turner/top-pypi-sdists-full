import json

import pytest

from agentic_devtools.cli.workflows.create_epic.records import (
    atomic_write_mapping_document,
    initialize_mapping_document,
    load_mapping_document,
)


def test_load_mapping_document_round_trips(tmp_path):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["link_subissue:e1:f1"] = {
        "status": "confirmed",
        "operation_type": "link_subissue",
        "source_ref": "e1",
        "target_ref": "f1",
        "source_provider_id": "1",
        "target_provider_id": "2",
        "confirmed_at": "2026-01-01T00:00:00Z",
        "result": "linked",
    }
    path = tmp_path / "mapping.json"
    atomic_write_mapping_document(path, document)
    assert load_mapping_document(path) == document


def test_load_mapping_document_allows_malformed_pending_timestamp_for_recovery(tmp_path):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["e1"] = {"status": "pending", "pending_since": "not-a-timestamp"}
    path = tmp_path / "mapping.json"
    path.write_text(json.dumps(document), encoding="utf-8")

    assert load_mapping_document(path)["entries"]["e1"] == document["entries"]["e1"]


@pytest.mark.parametrize("timestamp", ["not-a-timestampZ", None])
def test_load_mapping_document_normalizes_pending_relationship_timestamp_for_recovery(tmp_path, timestamp):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    entry = {
        "status": "pending",
        "operation_type": "link_subissue",
        "source_ref": "e1",
        "target_ref": "f1",
        "source_provider_id": "1",
        "target_provider_id": "2",
    }
    if timestamp is not None:
        entry["pending_since"] = timestamp
    document["entries"]["link_subissue:e1:f1"] = entry
    path = tmp_path / "mapping.json"
    path.write_text(json.dumps(document), encoding="utf-8")

    recovered = load_mapping_document(path)
    recovered_entry = recovered["entries"]["link_subissue:e1:f1"]
    assert recovered_entry["status"] == "pending"
    assert recovered_entry["pending_since"].endswith("Z")
    atomic_write_mapping_document(path, recovered)


@pytest.mark.parametrize("timestamp", ["not-a-timestampZ", None])
def test_load_mapping_document_recovers_inconclusive_confirmed_relationship_timestamp(tmp_path, timestamp):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    entry = {
        "status": "confirmed",
        "operation_type": "link_subissue",
        "source_ref": "e1",
        "target_ref": "f1",
        "source_provider_id": "1",
        "target_provider_id": "2",
        "result": "linked",
    }
    if timestamp is not None:
        entry["confirmed_at"] = timestamp
    document["entries"]["link_subissue:e1:f1"] = entry
    path = tmp_path / "mapping.json"
    path.write_text(json.dumps(document), encoding="utf-8")

    recovered = load_mapping_document(path)
    recovered_entry = recovered["entries"]["link_subissue:e1:f1"]
    assert recovered_entry["status"] == "pending"
    assert recovered_entry["pending_since"].endswith("Z")
    assert "confirmed_at" not in recovered_entry
    assert "result" not in recovered_entry
    atomic_write_mapping_document(path, recovered)
