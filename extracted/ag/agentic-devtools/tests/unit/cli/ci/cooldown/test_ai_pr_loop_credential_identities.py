"""Tests for ai_pr_loop_credential_identities()."""

from unittest.mock import patch

from agentic_devtools.cli.ci.cooldown import ai_pr_loop_credential_identities


class TestAiPrLoopCredentialIdentities:
    """ai_pr_loop_credential_identities() returns the full loop credential set."""

    def test_prefers_configured_identity_and_keeps_known_credentials(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "CUSTOM_ID",
            },
            clear=True,
        ):
            assert ai_pr_loop_credential_identities() == (
                "CUSTOM_ID",
                "COPILOT_GITHUB_TOKEN",
                "SPECKIT_PR_TOKEN",
                "AGDT_PR_APPROVER_PAT",
                "REPO_VARIABLE_WRITER_PAT",
            )

    def test_omits_duplicate_fallback_identity(self) -> None:
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "set"}, clear=True):
            assert ai_pr_loop_credential_identities() == (
                "COPILOT_GITHUB_TOKEN",
                "SPECKIT_PR_TOKEN",
                "AGDT_PR_APPROVER_PAT",
                "REPO_VARIABLE_WRITER_PAT",
            )

    def test_omits_duplicate_known_identity_when_already_configured(self) -> None:
        with patch.dict("os.environ", {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "SPECKIT_PR_TOKEN"}, clear=True):
            assert ai_pr_loop_credential_identities() == (
                "SPECKIT_PR_TOKEN",
                "COPILOT_GITHUB_TOKEN",
                "AGDT_PR_APPROVER_PAT",
                "REPO_VARIABLE_WRITER_PAT",
            )

    def test_adds_distinct_fallback_identity_when_configured_identity_is_invalid(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "not valid!",
                "GH_TOKEN": "set",
            },
            clear=True,
        ):
            assert ai_pr_loop_credential_identities() == (
                "COPILOT_GITHUB_TOKEN",
                "SPECKIT_PR_TOKEN",
                "AGDT_PR_APPROVER_PAT",
                "REPO_VARIABLE_WRITER_PAT",
                "GH_TOKEN",
            )
