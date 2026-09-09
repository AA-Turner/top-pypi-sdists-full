"""Unit tests for _resolve_review_provider."""

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def _document() -> dict:
    return {
        "providers": {"custom": {"type": "local_model", "model": "model-a", "endpoint": "http://localhost"}},
        "workflows": {
            "pr_review": {
                "default_provider": "custom",
                "nodes": {"review_files": {"provider": "custom"}},
            }
        },
    }


def test__resolve_review_provider_reports_missing_mapping_branches() -> None:
    resolver = provider_configuration._resolve_review_provider

    assert resolver({}) == ("workflow_mapping_missing", None, None)

    default_missing = _document()
    default_missing["workflows"]["pr_review"]["default_provider"] = " "
    assert resolver(default_missing) == ("default_provider_missing", None, None)

    node_missing = _document()
    node_missing["workflows"]["pr_review"]["nodes"] = {}
    assert resolver(node_missing) == ("review_files_mapping_missing", "custom", None)

    node_provider_missing = _document()
    node_provider_missing["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = " "
    assert resolver(node_provider_missing) == ("review_files_mapping_missing", "custom", None)

    provider_missing = _document()
    provider_missing["providers"] = {}
    assert resolver(provider_missing) == ("provider_missing", "custom", None)

    providers_invalid = _document()
    providers_invalid["providers"] = []
    assert resolver(providers_invalid) == ("provider_missing", "custom", None)

    dangling_default = _document()
    dangling_default["workflows"]["pr_review"]["default_provider"] = "missing"
    assert resolver(dangling_default) == ("provider_missing", "missing", None)

    dangling_node = _document()
    dangling_node["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "missing"
    assert resolver(dangling_node) == ("provider_missing", "missing", None)


def test__resolve_review_provider_returns_selected_provider_mapping() -> None:
    document = _document()

    error, provider_id, provider = provider_configuration._resolve_review_provider(document)

    assert error is None
    assert provider_id == "custom"
    assert provider == document["providers"]["custom"]
