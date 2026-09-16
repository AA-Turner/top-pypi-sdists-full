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
