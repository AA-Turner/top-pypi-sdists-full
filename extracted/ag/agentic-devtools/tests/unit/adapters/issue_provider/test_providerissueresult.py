"""Tests for ProviderIssueResult frozen dataclass and JSON serialization."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import ProviderIssueResult


class TestProviderIssueResult:
    """Verify ProviderIssueResult serialization, construction, and immutability."""

    def test_to_dict_basic(self):
        result = ProviderIssueResult(identifier="42", url="https://github.com/org/repo/issues/42", status="created")
        d = result.to_dict()
        assert d == {
            "identifier": "42",
            "url": "https://github.com/org/repo/issues/42",
            "status": "created",
            "metadata": {},
        }

    def test_to_dict_with_metadata(self):
        result = ProviderIssueResult(
            identifier="PROJ-1",
            url="https://jira.example.com/browse/PROJ-1",
            status="existing",
            metadata={"database_id": 12345},
        )
        d = result.to_dict()
        assert d["metadata"] == {"database_id": 12345}
        assert d["status"] == "existing"

    def test_to_dict_dry_run(self):
        result = ProviderIssueResult(identifier="", url="", status="dry-run")
        d = result.to_dict()
        assert d["status"] == "dry-run"
        assert d["identifier"] == ""
        assert d["url"] == ""

    def test_default_metadata_is_empty_dict(self):
        result = ProviderIssueResult(identifier="1", url="http://x", status="resolved")
        assert result.metadata == {}

    def test_status_vocabulary_created(self):
        result = ProviderIssueResult(identifier="1", url="http://x", status="created")
        assert result.status == "created"

    def test_status_vocabulary_existing(self):
        result = ProviderIssueResult(identifier="1", url="http://x", status="existing")
        assert result.status == "existing"

    def test_status_vocabulary_updated(self):
        result = ProviderIssueResult(identifier="1", url="http://x", status="updated")
        assert result.status == "updated"

    def test_status_vocabulary_no_op(self):
        result = ProviderIssueResult(identifier="1", url="http://x", status="no-op")
        assert result.status == "no-op"

    def test_status_vocabulary_resolved(self):
        result = ProviderIssueResult(identifier="1", url="http://x", status="resolved")
        assert result.status == "resolved"

    def test_frozen_immutability_identifier(self):
        result = ProviderIssueResult(identifier="1", url="http://x", status="created")
        with pytest.raises(AttributeError):
            result.identifier = "2"  # type: ignore[misc]

    def test_frozen_immutability_status(self):
        result = ProviderIssueResult(identifier="1", url="http://x", status="created")
        with pytest.raises(AttributeError):
            result.status = "updated"  # type: ignore[misc]

    def test_to_dict_metadata_is_copy(self):
        result = ProviderIssueResult(
            identifier="1",
            url="http://x",
            status="created",
            metadata={"key": "value"},
        )
        d = result.to_dict()
        d["metadata"]["key"] = "mutated"
        assert result.metadata["key"] == "value"

    def test_to_dict_metadata_nested_mutable_is_deep_copy(self):
        result = ProviderIssueResult(
            identifier="1",
            url="http://x",
            status="created",
            metadata={"labels": ["p0"]},
        )
        d = result.to_dict()
        d["metadata"]["labels"].append("p1")
        assert result.metadata["labels"] == ["p0"]

    def test_equality(self):
        a = ProviderIssueResult(identifier="1", url="http://x", status="created")
        b = ProviderIssueResult(identifier="1", url="http://x", status="created")
        assert a == b

    def test_inequality(self):
        a = ProviderIssueResult(identifier="1", url="http://x", status="created")
        b = ProviderIssueResult(identifier="2", url="http://x", status="created")
        assert a != b
