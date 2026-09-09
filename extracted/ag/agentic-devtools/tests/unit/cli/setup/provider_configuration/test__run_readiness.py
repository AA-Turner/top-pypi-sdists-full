"""Unit tests for _run_readiness."""

from typing import Any

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def _document(provider_type: str = "copilot", **provider_fields: str) -> dict:
    provider = {"type": provider_type, "model": "model-a", **provider_fields}
    return {
        "providers": {"copilot_pr_review": provider},
        "workflows": {
            "pr_review": {
                "default_provider": "copilot_pr_review",
                "nodes": {"review_files": {"provider": "copilot_pr_review"}},
            }
        },
    }


def test__run_readiness_supports_sync_and_async_callbacks(monkeypatch) -> None:
    run = provider_configuration._run_readiness
    assert run({}, lambda _doc: ("ready", "custom")) == ("ready", "custom")
    assert run({}, lambda _doc: "ready") == ("ready", "ready")
    assert run({}, lambda _doc: None) == ("ready", "ready")

    async def _ready(_doc: dict[str, Any]) -> tuple[str, str]:
        return ("ready", "async")

    assert run({}, _ready) == ("ready", "async")

    class AuthenticationError(Exception):
        pass

    class Factory:
        def __init__(self, **_kwargs):
            pass

        def preflight(self, *_args):
            raise AuthenticationError

    monkeypatch.setattr(provider_configuration, "ProviderFactory", Factory)
    assert run({}, None) == ("unavailable", "authentication_unavailable")

    class ModelNotAvailableError(Exception):
        pass

    def _model_error(*_args, **_kwargs):
        raise ModelNotAvailableError

    monkeypatch.setattr(
        provider_configuration, "ProviderFactory", lambda **_kwargs: type("F", (), {"preflight": _model_error})()
    )
    assert run({}, None) == ("unavailable", "model_unavailable")
    monkeypatch.setattr(
        provider_configuration,
        "ProviderFactory",
        lambda **_kwargs: type("F", (), {"preflight": lambda *_args: (_ for _ in ()).throw(RuntimeError())})(),
    )
    assert run({}, None) == ("unknown", "provider_unavailable")


def test__run_readiness_defaults_to_ready_when_preflight_succeeds(monkeypatch) -> None:
    class Factory:
        def __init__(self, **_kwargs):
            pass

        def preflight(self, *_args):
            return None

    monkeypatch.setattr(provider_configuration, "ProviderFactory", Factory)

    assert provider_configuration._run_readiness(_document(), None) == ("ready", "ready")
