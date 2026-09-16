from agentic_devtools.cli.workflows.create_epic.records import (
    atomic_write_mapping_document,
    initialize_mapping_document,
    load_mapping_document,
)


def test_load_mapping_document_round_trips(tmp_path):
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", "owner/repo")
    path = tmp_path / "mapping.json"
    atomic_write_mapping_document(path, document)
    assert load_mapping_document(path) == document
