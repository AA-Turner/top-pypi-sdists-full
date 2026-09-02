"""Tests for _sanitize_worktree_setup_diagnostic."""

from agentic_devtools.cli.workflows.worktree_setup import (
    _SETUP_STDERR_READ_LIMIT,
    _SETUP_STDERR_SANITIZE_OVERLAP,
    _sanitize_worktree_setup_diagnostic,
)


class TestSanitizeWorktreeSetupDiagnostic:
    """Tests for _sanitize_worktree_setup_diagnostic function."""

    def test_returns_plain_text_unchanged_within_limit(self):
        """Test that short plain text is returned as-is."""
        result = _sanitize_worktree_setup_diagnostic("setup failed: missing config")
        assert result == "setup failed: missing config"

    def test_truncates_to_read_limit(self):
        """Test that output is truncated to _SETUP_STDERR_READ_LIMIT characters."""
        long_input = "x" * (_SETUP_STDERR_READ_LIMIT + 500)
        result = _sanitize_worktree_setup_diagnostic(long_input)
        assert len(result) == _SETUP_STDERR_READ_LIMIT

    def test_redacts_api_key_credential(self):
        """Test that api_key= assignments are redacted."""
        result = _sanitize_worktree_setup_diagnostic("api_key=supersecretvalue failed")
        assert "supersecretvalue" not in result
        assert "<redacted>" in result

    def test_redacts_token_field(self):
        """Test that token= assignments are redacted."""
        result = _sanitize_worktree_setup_diagnostic("token=abc123xyz failed")
        assert "abc123xyz" not in result
        assert "<redacted>" in result

    def test_redacts_prefixed_environment_token(self):
        """Test that provider-prefixed token environment variables are redacted."""
        result = _sanitize_worktree_setup_diagnostic("GITHUB_TOKEN=abc123xyz failed")
        assert "abc123xyz" not in result
        assert "<redacted>" in result

    def test_redacts_quoted_json_token_field(self):
        """Test that quoted JSON token fields are redacted."""
        result = _sanitize_worktree_setup_diagnostic('{"token":"abc123xyz","error":"failed"}')
        assert "abc123xyz" not in result
        assert "<redacted>" in result

    def test_redacts_authorization_header(self):
        """Test that Authorization: value is redacted."""
        result = _sanitize_worktree_setup_diagnostic("Authorization: mysecrettoken")
        assert "mysecrettoken" not in result
        assert "<redacted>" in result

    def test_redacts_bearer_prefix(self):
        """Test that 'bearer TOKEN' is redacted."""
        result = _sanitize_worktree_setup_diagnostic("error: bearer mysecrettoken rejected")
        assert "mysecrettoken" not in result
        assert "<redacted>" in result

    def test_redacts_github_pat_token(self):
        """Test that ghp_ prefixed GitHub PAT tokens are redacted."""
        result = _sanitize_worktree_setup_diagnostic("error: ghp_abc123def456 is invalid")
        assert "ghp_abc123def456" not in result
        assert "[REDACTED]" in result

    def test_redacts_github_token_xox(self):
        """Test that xoxb- prefixed Slack/GitHub tokens are redacted."""
        result = _sanitize_worktree_setup_diagnostic("found xoxb-123-456-token")
        assert "xoxb-123-456-token" not in result
        assert "<redacted>" in result

    def test_redacts_sk_prefixed_token(self):
        """Test that sk- prefixed API keys (e.g. OpenAI) are redacted."""
        result = _sanitize_worktree_setup_diagnostic("sk-proj-abc123 was rejected")
        assert "sk-proj-abc123" not in result
        assert "<redacted>" in result

    def test_strips_control_characters(self):
        """Test that control characters (ASCII < 32) are replaced with spaces."""
        result = _sanitize_worktree_setup_diagnostic("error\x01\x02\x1b[31mfailed\x00")
        assert "\x01" not in result
        assert "\x02" not in result
        assert "\x1b" not in result
        assert "\x00" not in result

    def test_strips_delete_character(self):
        """Test that the DEL character (ASCII 127) is replaced with a space."""
        result = _sanitize_worktree_setup_diagnostic("error\x7ffailed")
        assert "\x7f" not in result

    def test_normalizes_whitespace(self):
        """Test that runs of whitespace are collapsed to a single space."""
        result = _sanitize_worktree_setup_diagnostic("error    multiple   spaces")
        assert "   " not in result

    def test_strips_leading_and_trailing_whitespace(self):
        """Test that leading and trailing whitespace is stripped."""
        result = _sanitize_worktree_setup_diagnostic("  error message  ")
        assert result == "error message"

    def test_coerces_non_string_input(self):
        """Test that non-string input is coerced to str before sanitization."""
        result = _sanitize_worktree_setup_diagnostic(42)
        assert result == "42"

    def test_coerces_none_input(self):
        """Test that None is coerced to the string 'None'."""
        result = _sanitize_worktree_setup_diagnostic(None)
        assert result == "None"

    def test_redacts_jira_copilot_pat(self):
        """Test that JIRA_COPILOT_PAT= assignments are redacted."""
        result = _sanitize_worktree_setup_diagnostic("JIRA_COPILOT_PAT=supersecretvalue failed")
        assert "supersecretvalue" not in result
        assert "<redacted>" in result

    def test_redacts_azure_dev_ops_copilot_pat(self):
        """Test that AZURE_DEV_OPS_COPILOT_PAT= assignments are redacted."""
        result = _sanitize_worktree_setup_diagnostic("AZURE_DEV_OPS_COPILOT_PAT=supersecretvalue")
        assert "supersecretvalue" not in result
        assert "<redacted>" in result

    def test_redacts_quoted_value_with_spaces(self):
        """Test that a quoted credential value containing spaces is fully redacted."""
        result = _sanitize_worktree_setup_diagnostic('token="super secret value"')
        assert "super secret value" not in result
        assert "<redacted>" in result

    def test_redacts_authorization_basic_header(self):
        """Test that Authorization: Basic <credential> is fully redacted including the base64 value."""
        result = _sanitize_worktree_setup_diagnostic("Authorization: Basic dXNlcjpwYXNzd29yZA==")
        assert "dXNlcjpwYXNzd29yZA==" not in result
        assert "<redacted>" in result

    def test_does_not_redact_mismatched_quote_as_quoted_value(self):
        """Test that a mismatched-quote credential has its value redacted up to the quote boundary."""
        result = _sanitize_worktree_setup_diagnostic("token=\"value' and more")
        assert "value" not in result
        assert "and more" in result
        assert "<redacted>" in result

    def test_redacts_unterminated_quoted_credential_value(self):
        """Test that an unterminated quoted credential value (no closing quote) is fully redacted."""
        result = _sanitize_worktree_setup_diagnostic('token="supersecret')
        assert "supersecret" not in result
        assert "<redacted>" in result

    def test_redacts_raw_env_var_value_without_label(self, monkeypatch):
        """Test that a raw env-var secret value emitted without a label is redacted via value-based pass."""
        monkeypatch.setenv("JIRA_COPILOT_PAT", "super-secret-raw-value")
        result = _sanitize_worktree_setup_diagnostic("provider setup failed: super-secret-raw-value")
        assert "super-secret-raw-value" not in result
        assert "[REDACTED]" in result

    def test_redacts_raw_github_token_value_without_label(self, monkeypatch):
        """Test that a raw GITHUB_TOKEN value emitted without a label is redacted via value-based pass."""
        monkeypatch.setenv("GITHUB_TOKEN", "rawgithubsecret123")
        result = _sanitize_worktree_setup_diagnostic("auth failed: rawgithubsecret123 is not valid")
        assert "rawgithubsecret123" not in result
        assert "[REDACTED]" in result

    def test_redacts_token_straddling_capture_boundary(self, monkeypatch):
        """Test that a secret placed at the capture boundary is redacted after sanitization."""
        secret = "rawboundarysecret"
        monkeypatch.setenv("GITHUB_TOKEN", secret)
        # Place the secret starting near the boundary so that the input exceeds
        # _SETUP_STDERR_READ_LIMIT but the secret is fully present within the
        # overlap (_SETUP_STDERR_SANITIZE_OVERLAP) window.
        padding = "x" * (_SETUP_STDERR_READ_LIMIT - 5)
        long_input = padding + secret + "x" * (_SETUP_STDERR_SANITIZE_OVERLAP - len(secret))
        assert len(long_input) > _SETUP_STDERR_READ_LIMIT
        result = _sanitize_worktree_setup_diagnostic(long_input)
        assert secret not in result
        assert len(result) == _SETUP_STDERR_READ_LIMIT

    def test_redacts_aws_secret_access_key(self):
        """Test that AWS_SECRET_ACCESS_KEY assignments are redacted."""
        result = _sanitize_worktree_setup_diagnostic("AWS_SECRET_ACCESS_KEY=supersecret123")
        assert "supersecret123" not in result
        assert "<redacted>" in result

    def test_redacts_aws_access_key_id(self):
        """Test that AWS_ACCESS_KEY_ID assignments are redacted."""
        result = _sanitize_worktree_setup_diagnostic("AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE")
        assert "AKIAIOSFODNN7EXAMPLE" not in result
        assert "<redacted>" in result
