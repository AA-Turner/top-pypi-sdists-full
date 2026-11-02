"""Tests for ProviderLinkResult frozen dataclass and JSON serialization."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import ProviderLinkResult


class TestProviderLinkResult:
    """Verify ProviderLinkResult serialization, construction, and immutability."""

    def test_to_dict_basic(self):
        result = ProviderLinkResult(source_id="1", target_id="2", status="linked")
        d = result.to_dict()
        assert d == {
            "source_id": "1",
            "target_id": "2",
            "status": "linked",
        }

    def test_to_dict_already_linked(self):
        result = ProviderLinkResult(source_id="PROJ-1", target_id="PROJ-2", status="already-linked")
        d = result.to_dict()
        assert d["status"] == "already-linked"

    def test_to_dict_dry_run(self):
        result = ProviderLinkResult(source_id="A", target_id="B", status="dry-run")
        d = result.to_dict()
        assert d["status"] == "dry-run"

    def test_status_vocabulary_linked(self):
        result = ProviderLinkResult(source_id="1", target_id="2", status="linked")
        assert result.status == "linked"

    def test_status_vocabulary_already_linked(self):
        result = ProviderLinkResult(source_id="1", target_id="2", status="already-linked")
        assert result.status == "already-linked"

    def test_status_vocabulary_dry_run(self):
        result = ProviderLinkResult(source_id="1", target_id="2", status="dry-run")
        assert result.status == "dry-run"

    def test_frozen_immutability_source_id(self):
        result = ProviderLinkResult(source_id="1", target_id="2", status="linked")
        with pytest.raises(AttributeError):
            result.source_id = "3"  # type: ignore[misc]

    def test_frozen_immutability_status(self):
        result = ProviderLinkResult(source_id="1", target_id="2", status="linked")
        with pytest.raises(AttributeError):
            result.status = "already-linked"  # type: ignore[misc]

    def test_equality(self):
        a = ProviderLinkResult(source_id="1", target_id="2", status="linked")
        b = ProviderLinkResult(source_id="1", target_id="2", status="linked")
        assert a == b

    def test_inequality(self):
        a = ProviderLinkResult(source_id="1", target_id="2", status="linked")
        b = ProviderLinkResult(source_id="1", target_id="3", status="linked")
        assert a != b

    def test_no_link_type_field(self):
        """ProviderLinkResult no longer has a link_type field (FR-003)."""
        result = ProviderLinkResult(source_id="1", target_id="2", status="linked")
        assert not hasattr(result, "link_type")
        assert "link_type" not in result.to_dict()
