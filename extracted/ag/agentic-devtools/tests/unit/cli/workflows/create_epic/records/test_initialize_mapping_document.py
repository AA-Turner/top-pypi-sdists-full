import pytest

from agentic_devtools.cli.workflows.create_epic.records import initialize_mapping_document


def test_initialize_mapping_document_has_canonical_root():
    document = initialize_mapping_document("12345678-1234-5678-1234-567812345678", "GitHub", "Owner/Repo")
    assert document == {
        "schemaVersion": "2.0",
        "treeId": "12345678-1234-5678-1234-567812345678",
        "provider": {"name": "github", "target": "owner/repo"},
        "entries": {},
    }


@pytest.mark.parametrize("name,target", [("", "owner/repo"), ("github", "")])
def test_initialize_mapping_document_rejects_empty_provider_values(name, target):
    with pytest.raises(ValueError):
        initialize_mapping_document("12345678-1234-5678-1234-567812345678", name, target)


def test_initialize_mapping_document_canonicalizes_jira_url():
    document = initialize_mapping_document(
        "12345678-1234-5678-1234-567812345678",
        "JIRA",
        "https://JIRA.Example.com:443/",
    )
    assert document["provider"]["target"] == "https://jira.example.com"


@pytest.mark.parametrize("target", ["owner", "owner/repo/extra", "/repo", "owner/"])
def test_initialize_mapping_document_rejects_invalid_github_target(target):
    with pytest.raises(ValueError, match="owner/repo"):
        initialize_mapping_document("12345678-1234-5678-1234-567812345678", "github", target)
