"""Tests for _credential_identity_for_token()."""

from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import _credential_identity_for_token


def test_credential_identity_never_returns_token_contents() -> None:
    with patch.dict("os.environ", {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "safe.id"}, clear=True):
        assert _credential_identity_for_token("secret") == "safe.id"
    with patch.dict(
        "os.environ",
        {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "SPECKIT_PR_TOKEN", "COPILOT_GITHUB_TOKEN": "secret"},
        clear=True,
    ):
        assert _credential_identity_for_token("secret") == "COPILOT_GITHUB_TOKEN"
    with patch.dict("os.environ", {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "safe.id"}, clear=True):
        assert _credential_identity_for_token("") == "safe.id"
    with patch.dict("os.environ", {}, clear=True):
        assert _credential_identity_for_token(None) == "GH_TOKEN"
        assert _credential_identity_for_token("secret") == "explicit-token"
    with patch.dict("os.environ", {"GH_TOKEN": "secret"}, clear=True):
        assert _credential_identity_for_token("") == "GH_TOKEN"
    with patch.dict("os.environ", {}, clear=True):
        assert _credential_identity_for_token("") == "GH_TOKEN"
    with patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "secret"}, clear=True):
        assert _credential_identity_for_token("secret") == "REPO_VARIABLE_WRITER_PAT"
    with patch.dict("os.environ", {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "bad:identity"}, clear=True):
        assert _credential_identity_for_token("secret") == "explicit-token"
