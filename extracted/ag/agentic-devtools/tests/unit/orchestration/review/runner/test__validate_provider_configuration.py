"""Tests for _validate_provider_configuration()."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agentic_devtools.orchestration.review.runner import _validate_provider_configuration


def _snapshot(*, providers=None, workflows=None, defaults=None):
    """Build the minimal configuration snapshot used by validation tests."""
    return SimpleNamespace(
        providers={"configured": object()} if providers is None else providers,
        workflows={} if workflows is None else workflows,
        defaults={"provider": "configured"} if defaults is None else defaults,
    )


@pytest.fixture(autouse=True)
def configured_llm_snapshot(monkeypatch) -> None:
    """Keep provider-validation tests independent from repository configuration."""
    snapshot = _snapshot()
    monkeypatch.setattr(
        "agentic_devtools.orchestration.llm.config.load_config",
        lambda _path=None: snapshot,
    )


def test_validates_routing_models_before_graph_creation():
    provider = MagicMock()
    provider.preflight = AsyncMock()
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        _validate_provider_configuration(
            {
                "default-model": "default",
                "rules": [{"model": "rule"}, "invalid"],
            }
        )

    factory_instance.get_provider.assert_called_once_with("review_files", "pr_review")
    provider.preflight.assert_awaited_once_with(["default", "rule"])


def test_validation_rejects_empty_provider_configuration(monkeypatch):
    """Validation reports an actionable error when no providers are configured."""
    monkeypatch.setattr(
        "agentic_devtools.orchestration.llm.config.load_config",
        lambda _path=None: _snapshot(providers={}),
    )

    with pytest.raises(RuntimeError, match="No providers configured for pr_review.review_files"):
        _validate_provider_configuration()


def test_validation_rejects_missing_workflow_provider(monkeypatch):
    """Validation rejects a workflow provider id absent from the provider map."""
    monkeypatch.setattr(
        "agentic_devtools.orchestration.llm.config.load_config",
        lambda _path=None: _snapshot(workflows={"pr_review": {"default_provider": "missing"}}),
    )

    with pytest.raises(RuntimeError, match="provider 'missing' is not configured"):
        _validate_provider_configuration()


def test_validation_accepts_non_mapping_workflow(monkeypatch):
    """Validation treats malformed workflow data as absent and uses defaults."""
    monkeypatch.setattr(
        "agentic_devtools.orchestration.llm.config.load_config",
        lambda _path=None: _snapshot(workflows={"pr_review": ["invalid"]}),
    )
    provider = MagicMock(preflight=None)
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", return_value=factory_instance):
        _validate_provider_configuration()

    factory_instance.get_provider.assert_called_once_with("review_files", "pr_review")


def test_validation_accepts_non_mapping_nodes(monkeypatch):
    """Validation treats malformed node data as absent and uses workflow defaults."""
    monkeypatch.setattr(
        "agentic_devtools.orchestration.llm.config.load_config",
        lambda _path=None: _snapshot(workflows={"pr_review": {"default_provider": "configured", "nodes": ["invalid"]}}),
    )
    provider = MagicMock(preflight=None)
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", return_value=factory_instance):
        _validate_provider_configuration()

    factory_instance.get_provider.assert_called_once_with("review_files", "pr_review")


def test_validation_prefers_node_provider_mapping(monkeypatch):
    """Validation resolves the node-level provider before broader defaults."""
    monkeypatch.setattr(
        "agentic_devtools.orchestration.llm.config.load_config",
        lambda _path=None: _snapshot(
            providers={"node": object()},
            workflows={"pr_review": {"nodes": {"review_files": {"provider": "node"}}}},
            defaults={"provider": "configured"},
        ),
    )
    provider = MagicMock(preflight=None)
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", return_value=factory_instance):
        _validate_provider_configuration()

    factory_instance.get_provider.assert_called_once_with("review_files", "pr_review")


def test_validation_accepts_non_mapping_node_config(monkeypatch):
    """Validation treats malformed per-node data as absent and uses workflow defaults."""
    monkeypatch.setattr(
        "agentic_devtools.orchestration.llm.config.load_config",
        lambda _path=None: _snapshot(
            workflows={
                "pr_review": {
                    "default_provider": "configured",
                    "nodes": {"review_files": ["invalid"]},
                }
            }
        ),
    )
    provider = MagicMock(preflight=None)
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", return_value=factory_instance):
        _validate_provider_configuration()

    factory_instance.get_provider.assert_called_once_with("review_files", "pr_review")


def test_validation_returns_none_when_no_provider_mapping(monkeypatch):
    """Validation lets the provider factory resolve configurations without an explicit mapping."""
    monkeypatch.setattr(
        "agentic_devtools.orchestration.llm.config.load_config",
        lambda _path=None: _snapshot(defaults={}),
    )
    provider = MagicMock(preflight=None)
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", return_value=factory_instance):
        _validate_provider_configuration()

    factory_instance.get_provider.assert_called_once_with("review_files", "pr_review")


def test_validates_routing_raises_for_non_string_default_model():
    provider = MagicMock()
    provider.preflight = None
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        with pytest.raises(ValueError, match="default-model.*must be a string"):
            _validate_provider_configuration({"default-model": 1})


def test_validates_routing_raises_for_non_string_rule_model():
    provider = MagicMock()
    provider.preflight = None
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        with pytest.raises(ValueError, match=r"rules\[0\].*must be a string"):
            _validate_provider_configuration({"rules": [{"model": 42}]})


def test_requested_model_is_validated_before_configured_routing_models():
    provider = MagicMock()
    provider.preflight = AsyncMock()
    provider.close = AsyncMock()
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        _validate_provider_configuration(
            {
                "default-model": "default",
                "rules": [{"model": "rule"}],
            },
            requested_model="gemini-3.7-flash",
        )

    provider.preflight.assert_awaited_once_with(["gemini-3.7-flash"])


def test_provider_default_is_validated_when_routing_rules_have_no_default_model():
    provider = MagicMock()
    provider.preflight = AsyncMock()
    provider.close = AsyncMock()
    provider._model = "provider-default"
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        _validate_provider_configuration({"rules": [{"model": "rule"}]})

    provider.preflight.assert_awaited_once_with(["provider-default", "rule"])


def test_preflight_provider_is_not_closed_before_graph_execution():
    provider = MagicMock()
    provider.preflight = AsyncMock(side_effect=RuntimeError("preflight failed"))
    provider.close = AsyncMock()
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        with pytest.raises(RuntimeError, match="preflight failed"):
            _validate_provider_configuration({})

    provider.close.assert_not_awaited()


def test_preflight_close_is_not_called_when_close_is_none():
    provider = MagicMock()
    provider.preflight = AsyncMock()
    provider.close = None
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        _validate_provider_configuration({})

    provider.preflight.assert_awaited_once_with([])


def test_validation_accepts_missing_or_non_list_routing_rules():
    provider = MagicMock()
    provider.preflight = None
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        _validate_provider_configuration(None)
        _validate_provider_configuration({"default-model": "model", "rules": "invalid"})

    assert factory.call_count == 2


def test_validation_skips_rule_with_none_model():
    provider = MagicMock()
    provider.preflight = AsyncMock()
    provider.close = AsyncMock()
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        _validate_provider_configuration({"rules": [{"pattern": "*.py"}]})

    provider.preflight.assert_awaited_once_with([])


def test_validation_skips_whitespace_only_rule_model():
    provider = MagicMock()
    provider.preflight = AsyncMock()
    provider.close = AsyncMock()
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        _validate_provider_configuration({"rules": [{"model": "  "}]})

    provider.preflight.assert_awaited_once_with([])


def test_validation_skips_whitespace_only_default_model():
    provider = MagicMock()
    provider.preflight = AsyncMock()
    provider.close = AsyncMock()
    factory_instance = MagicMock()
    factory_instance.get_provider.return_value = provider
    factory = MagicMock(return_value=factory_instance)

    with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory", factory):
        _validate_provider_configuration({"default-model": "  "})

    provider.preflight.assert_awaited_once_with([])
