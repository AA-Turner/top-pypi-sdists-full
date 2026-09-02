"""Tests for sanitize() in agentic_devtools.cli.setup.log_sanitizer."""

from __future__ import annotations

import time
from unittest.mock import patch

from agentic_devtools.cli.setup.log_sanitizer import REDACTION_PLACEHOLDER, sanitize

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _env(**kwargs: str) -> dict[str, str]:
    """Build a minimal environment dict for patching os.environ."""
    return kwargs


# ---------------------------------------------------------------------------
# User Story 1: Redact Known PAT Values
# ---------------------------------------------------------------------------


class TestRedactsAzureDevopsPat:
    """FR-001/FR-002: AZURE_DEV_OPS_COPILOT_PAT value is redacted."""

    def test_redacts_azure_devops_pat(self) -> None:
        secret = "my-azure-pat-value-12345"
        text = f"Connecting with token {secret} to Azure DevOps"
        with patch.dict("os.environ", _env(AZURE_DEV_OPS_COPILOT_PAT=secret), clear=True):
            result = sanitize(text)
        assert secret not in result
        assert REDACTION_PLACEHOLDER in result


class TestRedactsJiraPat:
    """FR-001/FR-002: JIRA_COPILOT_PAT value is redacted."""

    def test_redacts_jira_pat(self) -> None:
        secret = "jira-secret-token-abc"
        text = f"Jira auth: {secret}"
        with patch.dict("os.environ", _env(JIRA_COPILOT_PAT=secret), clear=True):
            result = sanitize(text)
        assert secret not in result
        assert REDACTION_PLACEHOLDER in result


class TestRedactsGithubToken:
    """FR-001/FR-002: GITHUB_TOKEN value is redacted."""

    def test_redacts_github_token(self) -> None:
        secret = "github-token-xyz-987"
        text = f"Using GITHUB_TOKEN={secret}"
        with patch.dict("os.environ", _env(GITHUB_TOKEN=secret), clear=True):
            result = sanitize(text)
        assert secret not in result
        assert REDACTION_PLACEHOLDER in result


class TestMultipleOccurrences:
    """FR-009: All occurrences of a secret value are replaced."""

    def test_multiple_occurrences(self) -> None:
        secret = "repeated-secret"
        text = f"first={secret} second={secret} third={secret}"
        with patch.dict("os.environ", _env(AZURE_DEV_OPS_COPILOT_PAT=secret), clear=True):
            result = sanitize(text)
        assert result.count(REDACTION_PLACEHOLDER) == 3
        assert secret not in result


class TestRegexMetacharactersInSecret:
    """FR-008: Secrets with regex metacharacters are treated as literals."""

    def test_regex_metacharacters_in_secret(self) -> None:
        secret = "a+b.*c[d]e(f)"
        text = f"token={secret}"
        with patch.dict("os.environ", _env(JIRA_COPILOT_PAT=secret), clear=True):
            result = sanitize(text)
        assert secret not in result
        assert REDACTION_PLACEHOLDER in result


class TestValueBasedBeforePrefix:
    """FR-010: Value-based replacement runs before prefix matching."""

    def test_value_based_before_prefix(self) -> None:
        # A full GitHub token in the env should be replaced by value first,
        # not partially matched by the prefix regex.
        secret = "ghp_abc123def456ghi789"
        text = f"token={secret}"
        with patch.dict("os.environ", _env(GITHUB_TOKEN=secret), clear=True):
            result = sanitize(text)
        # Should have exactly one REDACTED (value-based), not a partial match
        assert result == f"token={REDACTION_PLACEHOLDER}"


# ---------------------------------------------------------------------------
# User Story 2: Detect GitHub Token Prefixes
# ---------------------------------------------------------------------------


class TestRedactsGithubPrefixPatterns:
    """FR-003: All four GitHub token prefixes are redacted."""

    def test_redacts_github_prefix_patterns(self) -> None:
        text = "ghp_abcdef123456 gho_xyz789abc ghs_token123 github_pat_longtoken456"
        with patch.dict("os.environ", {}, clear=True):
            result = sanitize(text)
        assert "ghp_" not in result
        assert "gho_" not in result
        assert "ghs_" not in result
        assert "github_pat_" not in result
        assert result.count(REDACTION_PLACEHOLDER) == 4


class TestMinimumSuffixLength:
    """FR-003: Even a 1-char suffix after the prefix is redacted."""

    def test_minimum_suffix_length(self) -> None:
        text = "ghp_x"
        with patch.dict("os.environ", {}, clear=True):
            result = sanitize(text)
        assert result == REDACTION_PLACEHOLDER


# ---------------------------------------------------------------------------
# User Story 3: Benign Text Passes Through
# ---------------------------------------------------------------------------


class TestBenignTextUnchanged:
    """FR-004/FR-005: Clean text (including regex-like chars) is unchanged."""

    def test_benign_text_unchanged(self) -> None:
        text = (
            "Hello world! This is normal text with regex chars: "
            "a+b.*c[d]e(f) and base64-ish: YWJjZGVmZw== but no secrets."
        )
        with patch.dict("os.environ", {}, clear=True):
            result = sanitize(text)
        assert result == text


class TestEmptyInput:
    """FR-005: Empty string returns empty string."""

    def test_empty_input(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            result = sanitize("")
        assert result == ""


# ---------------------------------------------------------------------------
# User Story 4: Idempotent Sanitization
# ---------------------------------------------------------------------------


class TestIdempotent:
    """FR-006: sanitize(sanitize(x)) == sanitize(x)."""

    def test_idempotent(self) -> None:
        secret = "my-secret-pat"
        text = f"auth={secret} and ghp_token123abc"
        with patch.dict("os.environ", _env(AZURE_DEV_OPS_COPILOT_PAT=secret), clear=True):
            first_pass = sanitize(text)
            second_pass = sanitize(first_pass)
        assert first_pass == second_pass

    def test_placeholder_not_re_redacted(self) -> None:
        """The uniform [REDACTED] placeholder does not trigger re-redaction."""
        text = f"Previously sanitized: {REDACTION_PLACEHOLDER}"
        with patch.dict("os.environ", {}, clear=True):
            result = sanitize(text)
        assert result == text


# ---------------------------------------------------------------------------
# User Story 5: Safe Behavior When Secrets Absent
# ---------------------------------------------------------------------------


class TestMissingEnvVarsNoError:
    """FR-007: No exception when all secret env vars are unset."""

    def test_missing_env_vars_no_error(self) -> None:
        text = "Normal setup log output"
        with patch.dict("os.environ", {}, clear=True):
            result = sanitize(text)
        assert result == text


class TestEmptySecretSkipped:
    """FR-007: Empty string env var doesn't corrupt text."""

    def test_empty_secret_skipped(self) -> None:
        text = "Some log output with spaces"
        with patch.dict("os.environ", _env(GITHUB_TOKEN=""), clear=True):
            result = sanitize(text)
        assert result == text


class TestEnvChangeBetweenCalls:
    """NFR-004: Env var change between calls is reflected (statelessness)."""

    def test_env_change_between_calls(self) -> None:
        secret_v1 = "first-secret-value"
        secret_v2 = "second-secret-value"
        text = f"token={secret_v1}"

        with patch.dict("os.environ", _env(AZURE_DEV_OPS_COPILOT_PAT=secret_v1), clear=True):
            result1 = sanitize(text)
        assert secret_v1 not in result1

        # Change env var — second call should redact only the new value.
        text2 = f"old={secret_v1} new={secret_v2}"
        with patch.dict("os.environ", _env(AZURE_DEV_OPS_COPILOT_PAT=secret_v2), clear=True):
            result2 = sanitize(text2)
        assert secret_v1 in result2
        assert secret_v2 not in result2
        assert REDACTION_PLACEHOLDER in result2


# ---------------------------------------------------------------------------
# Final Phase: Performance
# ---------------------------------------------------------------------------


class TestPerformance1mb:
    """NFR-001: 1 MB input with embedded secrets completes without error."""

    def test_performance_1mb(self) -> None:
        secret = "performance-test-secret-value-abc123"
        # Build ~1 MB of text with 10 embedded secrets
        chunk = "x" * 100_000  # 100 KB
        parts = [chunk] * 9  # 900 KB
        # Insert secret in 10 locations within the remaining ~100 KB
        padding_len = max(0, 100_000 - 10 * (len(secret) + 7))
        secret_chunk = f"token={secret} " * 10 + "y" * padding_len
        parts.append(secret_chunk)
        text = "".join(parts)
        assert len(text) >= 1_000_000

        with patch.dict("os.environ", _env(JIRA_COPILOT_PAT=secret), clear=True):
            start = time.perf_counter()
            result = sanitize(text)
            elapsed = time.perf_counter() - start

        # Print timing for manual benchmark reference (no assertion on timing)
        print(f"1 MB sanitization elapsed: {elapsed:.4f}s")
        assert secret not in result
        assert result.count(REDACTION_PLACEHOLDER) >= 10
