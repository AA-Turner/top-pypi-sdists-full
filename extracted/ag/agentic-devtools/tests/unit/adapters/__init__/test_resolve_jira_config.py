"""Tests for :func:`agentic_devtools.adapters.resolve_jira_config`."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.adapters import resolve_jira_config


class TestResolveJiraConfig:
    """Verify the shared Jira config resolver used by adapters and setup probes."""

    def test_prefers_jira_api_token_and_basic_identity(self, monkeypatch) -> None:
        """JIRA_API_TOKEN + JIRA_USER_EMAIL produce the same Basic auth config for both callers."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com")
        monkeypatch.setenv("JIRA_API_TOKEN", "api-token")
        monkeypatch.setenv("JIRA_COPILOT_PAT", "copilot-token")
        monkeypatch.setenv("JIRA_USER_EMAIL", "user@example.com")
        monkeypatch.delenv("JIRA_EMAIL", raising=False)
        monkeypatch.delenv("JIRA_USERNAME", raising=False)
        monkeypatch.delenv("JIRA_SSL_VERIFY", raising=False)
        monkeypatch.delenv("JIRA_CA_BUNDLE", raising=False)
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

        config = resolve_jira_config()

        assert config.base_url == "https://jira.example.com"
        assert config.headers["Authorization"].startswith("Basic ")
        assert "api-token" not in config.headers["Authorization"]
        assert config.ssl_verify is True

    def test_uses_ca_bundle_and_bearer_fallback(self, monkeypatch, tmp_path) -> None:
        """Unset identity falls back to bearer auth and CA bundle resolution."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com")
        monkeypatch.delenv("JIRA_API_TOKEN", raising=False)
        monkeypatch.setenv("JIRA_COPILOT_PAT", "copilot-token")
        monkeypatch.delenv("JIRA_USER_EMAIL", raising=False)
        monkeypatch.delenv("JIRA_EMAIL", raising=False)
        monkeypatch.delenv("JIRA_USERNAME", raising=False)
        monkeypatch.delenv("JIRA_SSL_VERIFY", raising=False)
        ca_bundle = tmp_path / "custom-ca.pem"
        ca_bundle.write_text("pem", encoding="utf-8")
        monkeypatch.setenv("JIRA_CA_BUNDLE", str(ca_bundle))
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

        config = resolve_jira_config()

        assert config.headers["Authorization"] == "Bearer " + "copilot-token"
        assert config.ssl_verify == str(ca_bundle)

    def test_basic_scheme_without_identity_omits_auth_header(self, monkeypatch) -> None:
        """Basic auth without an identity leaves auth unset for the caller to report."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com")
        monkeypatch.setenv("JIRA_API_TOKEN", "api-token")
        monkeypatch.setenv("JIRA_AUTH_SCHEME", "basic")
        monkeypatch.delenv("JIRA_COPILOT_PAT", raising=False)
        monkeypatch.delenv("JIRA_USER_EMAIL", raising=False)
        monkeypatch.delenv("JIRA_EMAIL", raising=False)
        monkeypatch.delenv("JIRA_USERNAME", raising=False)
        monkeypatch.delenv("JIRA_SSL_VERIFY", raising=False)
        monkeypatch.delenv("JIRA_CA_BUNDLE", raising=False)
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

        config = resolve_jira_config()

        assert "Authorization" not in config.headers

    def test_disables_ssl_verification_for_false_values(self, monkeypatch) -> None:
        """JIRA_SSL_VERIFY false-like values disable verification for both callers."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com")
        monkeypatch.delenv("JIRA_API_TOKEN", raising=False)
        monkeypatch.delenv("JIRA_COPILOT_PAT", raising=False)
        monkeypatch.delenv("JIRA_USER_EMAIL", raising=False)
        monkeypatch.delenv("JIRA_EMAIL", raising=False)
        monkeypatch.delenv("JIRA_USERNAME", raising=False)
        monkeypatch.setenv("JIRA_SSL_VERIFY", "false")
        monkeypatch.delenv("JIRA_CA_BUNDLE", raising=False)
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

        config = resolve_jira_config()

        assert config.ssl_verify is False

    def test_uses_state_ca_bundle_path_when_present(self, monkeypatch, tmp_path) -> None:
        """State CA bundle path is propagated so preflight and adapter config stay aligned."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com")
        monkeypatch.delenv("JIRA_SSL_VERIFY", raising=False)
        monkeypatch.delenv("JIRA_CA_BUNDLE", raising=False)
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
        state_ca_bundle = tmp_path / "state-ca-bundle.pem"
        state_ca_bundle.write_text("pem", encoding="utf-8")

        def _mock_state_get_value(key: str, required: bool = False):  # noqa: ARG001
            if key == "jira.ca_bundle_path":
                return str(state_ca_bundle)
            return None

        with patch("agentic_devtools.state.get_value", side_effect=_mock_state_get_value):
            config = resolve_jira_config()

        assert config.ssl_verify == str(state_ca_bundle)

    def test_missing_state_ca_bundle_path_falls_back_to_env(self, monkeypatch, tmp_path) -> None:
        """Missing state CA bundle paths are ignored so env/repo TLS fallbacks still apply."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com")
        monkeypatch.delenv("JIRA_SSL_VERIFY", raising=False)
        env_ca_bundle = tmp_path / "env-ca-bundle.pem"
        env_ca_bundle.write_text("pem", encoding="utf-8")
        monkeypatch.setenv("JIRA_CA_BUNDLE", str(env_ca_bundle))
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

        def _mock_state_get_value(key: str, required: bool = False):  # noqa: ARG001
            if key == "jira.ca_bundle_path":
                return str(tmp_path / "missing-ca-bundle.pem")
            return None

        with patch("agentic_devtools.state.get_value", side_effect=_mock_state_get_value):
            config = resolve_jira_config()

        assert config.ssl_verify == str(env_ca_bundle)

    def test_uses_repo_committed_pem_when_available(self, monkeypatch, tmp_path) -> None:
        """Repo-committed PEM is used when SSL env/state overrides are absent."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com")
        monkeypatch.delenv("JIRA_SSL_VERIFY", raising=False)
        monkeypatch.delenv("JIRA_CA_BUNDLE", raising=False)
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
        with (
            patch("agentic_devtools.state.get_value", return_value=None),
            patch(
                "agentic_devtools.cli.jira.helpers._get_repo_jira_pem_path",
                return_value=tmp_path / "jira_ca_bundle.pem",
            ),
        ):
            (tmp_path / "jira_ca_bundle.pem").write_text("pem", encoding="utf-8")
            config = resolve_jira_config()

        assert config.ssl_verify == str(tmp_path / "jira_ca_bundle.pem")

    def test_prefers_supplied_git_root_for_repo_committed_pem(self, monkeypatch, tmp_path) -> None:
        """When git_root is supplied, the repo PEM path is resolved from that root."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com")
        monkeypatch.delenv("JIRA_SSL_VERIFY", raising=False)
        monkeypatch.delenv("JIRA_CA_BUNDLE", raising=False)
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
        repo_pem = tmp_path / "scripts" / "jira_ca_bundle.pem"
        repo_pem.parent.mkdir(parents=True, exist_ok=True)
        repo_pem.write_text("pem", encoding="utf-8")
        with (
            patch("agentic_devtools.state.get_value", return_value=None),
            patch(
                "agentic_devtools.cli.jira.helpers._get_repo_jira_pem_path",
                return_value=tmp_path / "other-repo.pem",
            ),
        ):
            config = resolve_jira_config(tmp_path)

        assert config.ssl_verify == str(repo_pem)
