"""Unit tests for _resolve_review_providers."""

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def _document() -> dict:
    return {
        "providers": {
            "default": {"type": "local_model", "model": "default", "endpoint": "http://localhost"},
            "review": {"type": "local_model", "model": "review", "endpoint": "http://localhost"},
        },
        "workflows": {
            "pr_review": {
                "default_provider": "default",
                "nodes": {"review_files": {"provider": "review"}},
            }
        },
    }


def test__resolve_review_providers_returns_both_provider_references() -> None:
    error, default_provider_id, default_provider, review_provider_id, review_provider = (
        provider_configuration._resolve_review_providers(_document())
    )

    assert error is None
    assert default_provider_id == "default"
    assert default_provider == _document()["providers"]["default"]
    assert review_provider_id == "review"
    assert review_provider == _document()["providers"]["review"]


def test__resolve_review_providers_reports_missing_review_provider() -> None:
    document = _document()
    document["providers"].pop("review")

    assert provider_configuration._resolve_review_providers(document) == (
        "provider_missing",
        "default",
        document["providers"]["default"],
        "review",
        None,
    )
