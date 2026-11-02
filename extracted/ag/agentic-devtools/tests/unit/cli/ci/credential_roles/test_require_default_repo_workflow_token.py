"""Tests for require_default_repo_workflow_token()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.credential_roles import require_default_repo_workflow_token


def test_returns_default_pat_when_configured() -> None:
    with patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token-value"}, clear=True):
        assert require_default_repo_workflow_token("dispatch workflows") == "token-value"


def test_accepts_gh_token_when_identity_is_default_pat() -> None:
    with patch.dict(
        "os.environ",
        {"GH_TOKEN": "token-value", "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"},
        clear=True,
    ):
        assert require_default_repo_workflow_token("dispatch workflows") == "token-value"


def test_rejects_writer_token_fallback() -> None:
    with patch.dict(
        "os.environ",
        {"GH_TOKEN": "writer-token", "AI_PR_LOOP_CREDENTIAL_IDENTITY": "REPO_VARIABLE_WRITER_PAT"},
        clear=True,
    ):
        with pytest.raises(RuntimeError, match="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"):
            require_default_repo_workflow_token("read repository contents")
