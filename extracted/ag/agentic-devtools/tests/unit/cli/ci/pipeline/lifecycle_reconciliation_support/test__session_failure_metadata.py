"""Tests for _session_failure_metadata."""

from agentic_devtools.cli.ci.models import FailureCategory
from agentic_devtools.cli.ci.pipeline.lifecycle_reconciliation_support import _session_failure_metadata


def test_session_failure_metadata_preserves_category_and_status():
    error = RuntimeError("denied")
    error.status_code = 403  # type: ignore[attr-defined]

    category, status = _session_failure_metadata(error)

    assert category is FailureCategory.PERMISSION
    assert status == 403
