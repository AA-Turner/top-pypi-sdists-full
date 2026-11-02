"""Tests for OperationDescriptor (FR-006)."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.adapters.operation_plan import OperationDescriptor


class TestOperationDescriptor:
    """Verify OperationDescriptor construction, immutability, and serialization."""

    def test_construction(self):
        desc = OperationDescriptor(
            operation_type="create_issue",
            orchestration_key="a" * 64,
            refs=("feature-1",),
            status="dry-run",
            provider_params={"title": "Test", "issue_type": "feature"},
        )
        assert desc.operation_type == "create_issue"
        assert desc.orchestration_key == "a" * 64
        assert desc.refs == ("feature-1",)
        assert desc.status == "dry-run"
        assert desc.provider_params == {"title": "Test", "issue_type": "feature"}
        assert desc.result is None

    def test_immutability(self):
        desc = OperationDescriptor(
            operation_type="create_issue",
            orchestration_key="a" * 64,
            refs=("ref-1",),
            status="dry-run",
        )
        with pytest.raises(Exception):
            desc.status = "created"  # type: ignore[misc]

    def test_to_dict_json_serializable(self):
        desc = OperationDescriptor(
            operation_type="link_subissue",
            orchestration_key="b" * 64,
            refs=("parent-ref", "child-ref"),
            status="dry-run",
            provider_params={"parent_id": "1", "child_id": "2"},
        )
        d = desc.to_dict()
        # Must be JSON-serializable
        serialized = json.dumps(d)
        assert serialized
        assert d["operation_type"] == "link_subissue"
        assert d["refs"] == ["parent-ref", "child-ref"]
        assert d["result"] is None

    def test_to_dict_with_result(self):
        result = ProviderIssueResult(identifier="42", url="http://x/42", status="created")
        desc = OperationDescriptor(
            operation_type="create_issue",
            orchestration_key="c" * 64,
            refs=("ref-1",),
            status="created",
            result=result,
        )
        d = desc.to_dict()
        assert d["result"]["identifier"] == "42"
        assert d["result"]["status"] == "created"

    def test_default_provider_params(self):
        desc = OperationDescriptor(
            operation_type="create_issue",
            orchestration_key="d" * 64,
            refs=("ref-1",),
            status="dry-run",
        )
        assert desc.provider_params == {}

    def test_is_dry_run(self):
        desc = OperationDescriptor(
            operation_type="create_issue",
            orchestration_key="e" * 64,
            refs=("ref-1",),
            status="dry-run",
        )
        assert desc.is_dry_run is True

    def test_is_existing(self):
        desc = OperationDescriptor(
            operation_type="create_issue",
            orchestration_key="f" * 64,
            refs=("ref-1",),
            status="existing",
        )
        assert desc.is_existing is True

    def test_is_existing_already_linked(self):
        desc = OperationDescriptor(
            operation_type="link_subissue",
            orchestration_key="0" * 64,
            refs=("p", "c"),
            status="already-linked",
        )
        assert desc.is_existing is True


class TestPartialCreatedStatus:
    """Verify the ``partial-created`` operation status (FR-010)."""

    def test_partial_created_in_valid_status_set(self):
        from agentic_devtools.adapters.operation_plan import OPERATION_STATUSES

        assert "partial-created" in OPERATION_STATUSES

    def test_invalid_status_is_rejected(self):
        with pytest.raises(ValueError, match="Unsupported operation status"):
            OperationDescriptor(
                operation_type="create_issue",
                orchestration_key="a" * 64,
                refs=("ref-1",),
                status="not-a-real-status",
            )

    def test_is_partial_created_true(self):
        result = ProviderIssueResult(identifier="7", url="u", status="created")
        desc = OperationDescriptor(
            operation_type="create_issue",
            orchestration_key="b" * 64,
            refs=("subtask-1",),
            status="partial-created",
            result=result,
        )
        assert desc.is_partial_created is True
        assert desc.is_dry_run is False
        assert desc.is_existing is False

    def test_is_partial_created_false_for_created(self):
        desc = OperationDescriptor(
            operation_type="create_issue",
            orchestration_key="c" * 64,
            refs=("subtask-1",),
            status="created",
        )
        assert desc.is_partial_created is False

    def test_partial_created_serializes_with_result(self):
        result = ProviderIssueResult(identifier="7", url="u", status="created")
        desc = OperationDescriptor(
            operation_type="create_issue",
            orchestration_key="d" * 64,
            refs=("subtask-1",),
            status="partial-created",
            result=result,
        )
        payload = desc.to_dict()
        assert payload["status"] == "partial-created"
        assert payload["result"]["identifier"] == "7"
        # Round-trips through JSON.
        assert json.loads(json.dumps(payload))["status"] == "partial-created"
