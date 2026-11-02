"""Tests for _read_required_default_workflow_token()."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.audit.dispatch import _read_required_default_workflow_token


class TestReadRequiredDefaultWorkflowToken:
    """Tests for _read_required_default_workflow_token()."""

    def test_returns_trimmed_token(self) -> None:
        with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": " token-value "}, clear=True):
            assert _read_required_default_workflow_token() == "token-value"

    def test_raises_when_missing(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"):
                _read_required_default_workflow_token()
