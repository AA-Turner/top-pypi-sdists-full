"""Tests for the ``HierarchyLinkError`` typed hierarchy-failure exception.

Covers FR-007: the error signals a partial creation (issue created, subsequent
hierarchy-link step failed) and carries the created result, the failing stage,
and the underlying cause.
"""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.exceptions import AdapterError, HierarchyLinkError
from agentic_devtools.adapters.issue_provider import ProviderIssueResult


def _created_result() -> ProviderIssueResult:
    return ProviderIssueResult(
        identifier="42",
        url="https://example.test/issues/42",
        status="created",
    )


class TestHierarchyLinkError:
    def test_is_adapter_error_subclass(self):
        assert issubclass(HierarchyLinkError, AdapterError)

    def test_stores_created_result_stage_and_cause(self):
        result = _created_result()
        cause = RuntimeError("link API 500")
        err = HierarchyLinkError(
            "linking failed",
            created_result=result,
            stage="link_subissue",
            cause=cause,
        )
        assert err.created_result is result
        assert err.stage == "link_subissue"
        assert err.cause is cause
        assert str(err) == "linking failed"

    def test_cause_is_required(self):
        with pytest.raises(TypeError):
            HierarchyLinkError(
                "linking failed",
                created_result=_created_result(),
                stage="link_subissue",
            )

    def test_can_be_raised_and_caught_as_adapter_error(self):
        try:
            raise HierarchyLinkError(
                "boom",
                created_result=_created_result(),
                stage="link_subissue",
                cause=RuntimeError("inner"),
            )
        except AdapterError as caught:
            assert isinstance(caught, HierarchyLinkError)
        else:  # pragma: no cover - defensive
            raise AssertionError("HierarchyLinkError was not raised")
