"""Tests for initiate_node."""

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.nodes.initiate import _validate_llm_config, initiate_node


class TestInitiateNode:
    def test_detects_jira_provider(self):
        with patch("agentic_devtools.orchestration.nodes.initiate._validate_llm_config", return_value=None):
            result = initiate_node({"issue_key": "PROJECT-1234"})
            assert result["issue_provider"] == "jira"

    def test_detects_github_provider(self):
        with patch("agentic_devtools.orchestration.nodes.initiate._validate_llm_config", return_value=None):
            result = initiate_node({"issue_key": "#42"})
            assert result["issue_provider"] == "github"

    def test_fails_fast_on_missing_llm_config(self):
        with patch(
            "agentic_devtools.orchestration.nodes.initiate._validate_llm_config",
            return_value="ProviderNotConfiguredError: No LLM providers configured",
        ):
            result = initiate_node({"issue_key": "TEST-1"})
            assert result["status"] == "failed"
            assert "ProviderNotConfiguredError" in result["error"]

    def test_sets_status_active_on_success(self):
        with patch("agentic_devtools.orchestration.nodes.initiate._validate_llm_config", return_value=None):
            result = initiate_node({"issue_key": "TEST-1"})
            assert result["status"] == "active"
            assert result["step"] == "initiate"

    def test_routes_to_setup_on_preflight_error(self):
        with patch("agentic_devtools.orchestration.nodes.initiate._validate_llm_config", return_value=None):
            result = initiate_node({"issue_key": "TEST-1", "error": "wrong branch"})
            assert result["needs_setup"] is True
            # ``issue_retrieved`` must not be set here — it is owned by retrieve_node.
            assert "issue_retrieved" not in result

    def test_includes_preflight_error_detail_in_signals_when_needs_setup(self):
        """When needs_setup=True, the original pre-flight error is included in signals."""
        with patch("agentic_devtools.orchestration.nodes.initiate._validate_llm_config", return_value=None):
            result = initiate_node({"issue_key": "TEST-1", "error": "wrong branch: expected feat/TEST-1"})
            signals = result["events"][0]["signals"]
            assert signals["needs_setup"] is True
            assert signals["pre_flight_error_detail"] == "wrong branch: expected feat/TEST-1"

    def test_omits_preflight_error_detail_in_signals_when_no_error(self):
        """When needs_setup=False, pre_flight_error_detail is not included in signals."""
        with patch("agentic_devtools.orchestration.nodes.initiate._validate_llm_config", return_value=None):
            result = initiate_node({"issue_key": "TEST-1"})
            signals = result["events"][0]["signals"]
            assert signals["needs_setup"] is False
            assert "pre_flight_error_detail" not in signals

    def test_omits_preflight_error_detail_when_error_is_non_string(self):
        """Non-string truthy error values do not produce pre_flight_error_detail in signals."""
        with patch("agentic_devtools.orchestration.nodes.initiate._validate_llm_config", return_value=None):
            result = initiate_node({"issue_key": "TEST-1", "error": {"code": 1}})
            signals = result["events"][0]["signals"]
            assert signals["needs_setup"] is True
            assert "pre_flight_error_detail" not in signals

    def test_routes_to_retrieve_on_no_error(self):
        with patch("agentic_devtools.orchestration.nodes.initiate._validate_llm_config", return_value=None):
            result = initiate_node({"issue_key": "TEST-1"})
            assert result["needs_setup"] is False
            # ``issue_retrieved`` must not be set here — it is owned by retrieve_node.
            assert "issue_retrieved" not in result

    def test_emits_event(self):
        with patch("agentic_devtools.orchestration.nodes.initiate._validate_llm_config", return_value=None):
            result = initiate_node({"issue_key": "TEST-1"})
            assert len(result["events"]) == 1
            assert result["events"][0]["event"] == "initiate_completed"

    def test_fails_fast_when_issue_key_missing(self):
        """Missing issue_key must return initiate_failed without calling LLM config."""
        result = initiate_node({})
        assert result["status"] == "failed"
        assert "issue_key" in result["error"]
        assert result["events"][0]["event"] == "initiate_failed"

    def test_fails_fast_when_issue_key_blank(self):
        """Blank (whitespace-only) issue_key must return initiate_failed."""
        result = initiate_node({"issue_key": "   "})
        assert result["status"] == "failed"
        assert result["events"][0]["event"] == "initiate_failed"

    def test_fails_fast_when_issue_key_not_a_string(self):
        """Non-string issue_key (e.g. int from corrupted checkpoint) must return initiate_failed."""
        result = initiate_node({"issue_key": 42})
        assert result["status"] == "failed"
        assert result["events"][0]["event"] == "initiate_failed"

    def test_fails_fast_when_issue_key_empty_string(self):
        """Empty-string issue_key must return initiate_failed."""
        result = initiate_node({"issue_key": ""})
        assert result["status"] == "failed"
        assert result["events"][0]["event"] == "initiate_failed"

    def test_fails_fast_when_issue_key_normalizes_to_empty(self):
        """Hash-only GitHub issue keys must fail before provider detection."""
        result = initiate_node({"issue_key": "#"})
        assert result["status"] == "failed"
        assert result["error"] == "issue_key must normalize to a non-empty issue identifier"
        assert result["events"][0]["event"] == "initiate_failed"


class TestValidateLlmConfig:
    def test_returns_none_when_providers_configured(self):
        mock_config = MagicMock()
        mock_config.providers = ["provider1"]
        with patch("agentic_devtools.orchestration.llm.config.load_config", return_value=mock_config):
            result = _validate_llm_config()
            assert result is None

    def test_returns_error_when_no_providers(self):
        mock_config = MagicMock()
        mock_config.providers = []
        with patch("agentic_devtools.orchestration.llm.config.load_config", return_value=mock_config):
            result = _validate_llm_config()
            assert result is not None
            assert "ProviderNotConfiguredError" in result

    def test_returns_error_on_exception(self):
        with patch(
            "agentic_devtools.orchestration.llm.config.load_config",
            side_effect=RuntimeError("config missing"),
        ):
            result = _validate_llm_config()
            assert result is not None
            assert "Failed to load LLM config" in result
            assert "config missing" in result
