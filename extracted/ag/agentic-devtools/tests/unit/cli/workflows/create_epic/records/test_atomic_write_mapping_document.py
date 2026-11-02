import json

import pytest

import agentic_devtools.cli.workflows.create_epic.records as records
from agentic_devtools.cli.workflows.create_epic.records import (
    atomic_write_mapping_document,
    initialize_mapping_document,
)


def test_atomic_write_mapping_document_is_deterministic(tmp_path):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    path = tmp_path / "mapping.json"
    atomic_write_mapping_document(path, document)
    raw = path.read_bytes()
    assert raw.endswith(b"\n")
    assert json.loads(raw) == document
    assert b'"treeId"' in raw


def test_atomic_write_mapping_document_cleans_up_after_replace_failure(tmp_path, monkeypatch):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    path = tmp_path / "mapping.json"
    monkeypatch.setattr(records.os, "replace", lambda *_args: (_ for _ in ()).throw(OSError("replace failed")))
    with pytest.raises(OSError, match="replace failed"):
        atomic_write_mapping_document(path, document)
    assert not list(tmp_path.glob(".mapping.json.*"))


def test_atomic_write_mapping_document_preserves_replace_error_when_cleanup_fails(tmp_path, monkeypatch):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    path = tmp_path / "mapping.json"
    monkeypatch.setattr(records.os, "replace", lambda *_args: (_ for _ in ()).throw(OSError("replace failed")))
    monkeypatch.setattr(records.os, "unlink", lambda *_args: (_ for _ in ()).throw(OSError("cleanup failed")))
    with pytest.raises(OSError, match="replace failed"):
        atomic_write_mapping_document(path, document)


def test_atomic_write_mapping_document_rejects_malformed_pending_timestamp(tmp_path):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["e1"] = {"status": "pending", "pending_since": "not-a-timestamp"}

    with pytest.raises(ValueError, match="pending_since"):
        atomic_write_mapping_document(tmp_path / "mapping.json", document)


def test_atomic_write_mapping_document_rejects_malformed_pending_relationship_timestamp(tmp_path):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["link_subissue:e1:f1"] = {
        "status": "pending",
        "operation_type": "link_subissue",
        "source_ref": "e1",
        "target_ref": "f1",
        "source_provider_id": "1",
        "target_provider_id": "2",
        "pending_since": "not-a-timestamp",
    }

    with pytest.raises(ValueError, match="pending_since"):
        atomic_write_mapping_document(tmp_path / "mapping.json", document)


def test_atomic_write_mapping_document_rejects_missing_pending_relationship_timestamp(tmp_path):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["link_subissue:e1:f1"] = {
        "status": "pending",
        "operation_type": "link_subissue",
        "source_ref": "e1",
        "target_ref": "f1",
        "source_provider_id": "1",
        "target_provider_id": "2",
    }

    with pytest.raises(ValueError, match="pending shape"):
        atomic_write_mapping_document(tmp_path / "mapping.json", document)


def test_atomic_write_mapping_document_rejects_missing_confirmed_relationship_timestamp(tmp_path):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["link_subissue:e1:f1"] = {
        "status": "confirmed",
        "operation_type": "link_subissue",
        "source_ref": "e1",
        "target_ref": "f1",
        "source_provider_id": "1",
        "target_provider_id": "2",
        "result": "linked",
    }

    with pytest.raises(ValueError, match="confirmed shape"):
        atomic_write_mapping_document(tmp_path / "mapping.json", document)


def test_atomic_write_mapping_document_rejects_malformed_confirmed_relationship_timestamp(tmp_path):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["link_subissue:e1:f1"] = {
        "status": "confirmed",
        "operation_type": "link_subissue",
        "source_ref": "e1",
        "target_ref": "f1",
        "source_provider_id": "1",
        "target_provider_id": "2",
        "confirmed_at": "not-a-timestamp",
        "result": "linked",
    }

    with pytest.raises(ValueError, match="confirmed_at"):
        atomic_write_mapping_document(tmp_path / "mapping.json", document)
