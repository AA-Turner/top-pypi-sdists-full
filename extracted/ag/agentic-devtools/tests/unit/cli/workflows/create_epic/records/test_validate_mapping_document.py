import pytest

from agentic_devtools.cli.workflows.create_epic.records import (
    initialize_mapping_document,
    validate_mapping_document,
)


def test_validate_mapping_document_checks_tree_and_provider():
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    assert (
        validate_mapping_document(document, "12345678-1234-5678-1234-567812345678", "GitHub", "owner/repo") == document
    )


def test_validate_mapping_document_rejects_mismatch():
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    with pytest.raises(ValueError, match="treeId"):
        validate_mapping_document(document, "87654321-4321-8765-4321-876543218765")


@pytest.mark.parametrize(
    "document",
    [
        [],
        {"schemaVersion": "1.0"},
        {"schemaVersion": "2.0", "treeId": "bad", "provider": {}, "entries": {}},
        {
            "schemaVersion": "2.0",
            "treeId": "12345678-1234-5678-1234-567812345678",
            "provider": {"name": "", "target": "x"},
            "entries": {},
        },
        {
            "schemaVersion": "2.0",
            "treeId": "12345678-1234-5678-1234-567812345678",
            "provider": {"name": "github", "target": "x"},
            "entries": [],
        },
    ],
)
def test_validate_mapping_document_rejects_invalid_shapes(document):
    with pytest.raises(ValueError):
        validate_mapping_document(document)


def test_validate_mapping_document_rejects_provider_mismatch():
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    with pytest.raises(ValueError, match="provider name"):
        validate_mapping_document(document, provider_name="jira")
    with pytest.raises(ValueError, match="provider target"):
        validate_mapping_document(document, provider_target="other/repo")


def test_validate_mapping_document_accepts_jira_context_path_target() -> None:
    # A base URL with a context path (e.g. https://jira.example.com/path) must
    # still match once the project key is appended, since only the final path
    # segment is the project key.
    document = {
        "schemaVersion": "2.0",
        "treeId": "12345678-1234-5678-1234-567812345678",
        "provider": {"name": "jira", "target": "https://jira.example.com/path/proj"},
        "entries": {},
    }
    assert (
        validate_mapping_document(
            document,
            "12345678-1234-5678-1234-567812345678",
            "jira",
            "https://jira.example.com/path/PROJ",
        )
        == document
    )


def test_validate_mapping_document_accepts_legacy_jira_base_url_target_when_entries_empty() -> None:
    # A legacy site-only target (no project-key segment) is still accepted when
    # the mapping document has no entries yet, since there is nothing that could
    # have been created against a different project to reuse.
    document = {
        "schemaVersion": "2.0",
        "treeId": "12345678-1234-5678-1234-567812345678",
        "provider": {"name": "jira", "target": "https://jira.example.com"},
        "entries": {},
    }
    assert (
        validate_mapping_document(
            document,
            "12345678-1234-5678-1234-567812345678",
            "jira",
            "https://jira.example.com/PROJ",
        )
        == document
    )


def test_validate_mapping_document_rejects_legacy_jira_base_url_target_once_entries_exist() -> None:
    # A legacy site-only target records no project identity. Once the mapping
    # document has an entry (created against whichever project was active when
    # that entry was recorded), the target must match exactly -- otherwise
    # switching to a different project on the same Jira site would silently
    # validate and let the pipeline reuse the other project's mapped issues.
    document = {
        "schemaVersion": "2.0",
        "treeId": "12345678-1234-5678-1234-567812345678",
        "provider": {"name": "jira", "target": "https://jira.example.com"},
        "entries": {"e1": {"status": "created", "provider_id": "PROJ-1"}},
    }
    with pytest.raises(ValueError, match="provider target"):
        validate_mapping_document(
            document,
            "12345678-1234-5678-1234-567812345678",
            "jira",
            "https://jira.example.com/PROJ",
        )


def test_validate_mapping_document_rejects_case_variant_ambiguous_legacy_jira_target() -> None:
    document = {
        "schemaVersion": "2.0",
        "treeId": "12345678-1234-5678-1234-567812345678",
        "provider": {"name": "jira", "target": "https://jira.example.com/jira"},
        "entries": {"e1": {"status": "created", "provider_id": "PROJ-1"}},
    }
    with pytest.raises(ValueError, match="provider target"):
        validate_mapping_document(
            document,
            "12345678-1234-5678-1234-567812345678",
            "jira",
            "https://jira.example.com/JIRA",
        )


@pytest.mark.parametrize(
    "entry",
    [
        [],
        {"status": "unknown"},
        {"status": "created", "provider_id": 1},
        {"status": "created", "provider_id": "PROJ-1", "identifier": "PROJ-1"},
        {"status": "trusted-match", "provider_id": "PROJ-1", "match_basis": "unknown"},
        {"status": "failed", "error": ""},
        {"status": "pending", "pending_since": "not-a-timestamp"},
        {"status": "pending", "pending_since": "not-a-timestampZ"},
        {"status": "pending", "pending_since": "2026-01-01Z"},
        {
            "status": "pending",
            "pending_since": "2026-01-01T00:00:00Z",
            "orchestrationKey": "legacy-extra-field",
        },
        {
            "status": "pending",
            "pending_since": "2026-01-01T00:00:00Z",
            "provider_id": "",
            "call_outcome": "created",
        },
        {
            "status": "pending",
            "pending_since": "2026-01-01T00:00:00Z",
            "provider_id": "1",
            "call_outcome": "failed",
        },
        {
            "status": "pending",
            "pending_since": "2026-01-01T00:00:00Z",
            "provider_id": "1",
            "call_outcome": [],
        },
        {"status": "trusted-match", "provider_id": "", "match_basis": "pre-create-guard"},
        {"status": "trusted-match", "provider_id": "1"},
        {"status": "trusted-match", "provider_id": "1", "match_basis": []},
    ],
)
def test_validate_mapping_document_rejects_malformed_node_entries(entry) -> None:
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["e1"] = entry

    with pytest.raises(ValueError, match="entry"):
        validate_mapping_document(document)


def test_validate_mapping_document_rejects_non_string_entry_key() -> None:
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"][1] = {"status": "created", "provider_id": "1"}

    with pytest.raises(ValueError, match="entry key"):
        validate_mapping_document(document)


def test_validate_mapping_document_accepts_canonical_node_and_relationship_entries() -> None:
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"] = {
        "e1": {"status": "created", "provider_id": "1"},
        "f1": {"status": "trusted-match", "provider_id": "2", "match_basis": "pre-create-guard"},
        "s1": {"status": "failed", "error": "rejected"},
        "s2": {"status": "pending", "pending_since": "2026-01-01T00:00:00Z"},
        "s3": {
            "status": "pending",
            "pending_since": "2026-01-01T00:00:00Z",
            "provider_id": "3",
            "call_outcome": "created",
        },
        "link_subissue:e1:f1": {
            "status": "pending",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "1",
            "target_provider_id": None,
            "pending_since": "2026-01-01T00:00:00Z",
        },
        "add_blocked_by:s1:s2": {
            "status": "confirmed",
            "operation_type": "add_blocked_by",
            "source_ref": "s1",
            "target_ref": "s2",
            "source_provider_id": "4",
            "target_provider_id": "5",
            "confirmed_at": "2026-01-01T00:00:00Z",
            "result": "already-linked",
        },
    }

    assert validate_mapping_document(document) == document


def test_validate_mapping_document_rejects_noncanonical_relationship_key() -> None:
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["link_subissue:e1:f1"] = {
        "status": "pending",
        "operation_type": "link_subissue",
        "source_ref": "other",
        "target_ref": "f1",
        "source_provider_id": "1",
        "target_provider_id": "2",
        "pending_since": "2026-01-01T00:00:00Z",
    }

    with pytest.raises(ValueError, match="key"):
        validate_mapping_document(document)


@pytest.mark.parametrize(
    "entry",
    [
        {
            "status": "pending",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "",
            "target_provider_id": None,
            "pending_since": "2026-01-01T00:00:00Z",
        },
        {
            "status": "pending",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "1",
            "target_provider_id": None,
            "pending_since": "2026-01-01T00:00:00Z",
            "unexpected": True,
        },
        {
            "status": "pending",
            "operation_type": "add_blocked_by",
            "source_ref": "s1",
            "target_ref": "s2",
            "source_provider_id": "1",
            "target_provider_id": None,
            "pending_since": "2026-01-01T00:00:00Z",
        },
        {
            "status": "failed",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "1",
            "target_provider_id": "2",
            "pending_since": "2026-01-01T00:00:00Z",
        },
        {
            "status": "confirmed",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "1",
            "target_provider_id": "2",
            "confirmed_at": "2026-01-01T00:00:00Z",
            "result": "linked",
            "pending_since": "2026-01-01T00:00:00Z",
        },
        {
            "status": "confirmed",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "",
            "target_provider_id": "2",
            "confirmed_at": "2026-01-01T00:00:00Z",
            "result": "linked",
        },
        {
            "status": "confirmed",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "1",
            "target_provider_id": "2",
            "confirmed_at": "2026-01-01T00:00:00Z",
            "result": "failed",
        },
        {
            "status": "confirmed",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "1",
            "target_provider_id": "2",
            "confirmed_at": "2026-01-01T00:00:00Z",
            "result": [],
        },
    ],
)
def test_validate_mapping_document_rejects_malformed_relationship_entries(entry) -> None:
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    operation_type = entry["operation_type"]
    document["entries"][f"{operation_type}:{entry['source_ref']}:{entry['target_ref']}"] = entry

    with pytest.raises(ValueError, match="relationship entry"):
        validate_mapping_document(document)


def test_validate_mapping_document_rejects_colon_in_node_entry_key() -> None:
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    document["entries"]["bad:ref"] = {"status": "created", "provider_id": "1"}

    with pytest.raises(ValueError, match="key"):
        validate_mapping_document(document)
