"""Unit tests for _document_for_provider_preflight."""

import pytest

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def test__document_for_provider_preflight_rewrites_review_mapping() -> None:
    document = {"providers": {"custom": {"type": "copilot", "model": "m"}}, "workflows": {"pr_review": {"nodes": {}}}}

    preflight = provider_configuration._document_for_provider_preflight(document, "custom")

    assert preflight["workflows"]["pr_review"]["default_provider"] == "custom"
    assert preflight["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] == "custom"


@pytest.mark.parametrize(
    ("document", "reason"),
    [
        ({"workflows": []}, "workflow_mapping_invalid"),
        ({"workflows": {"pr_review": []}}, "workflow_mapping_invalid"),
        ({"workflows": {"pr_review": {"nodes": []}}}, "workflow_mapping_invalid"),
        ({"workflows": {"pr_review": {"nodes": {"review_files": []}}}}, "review_files_mapping_invalid"),
    ],
)
def test__document_for_provider_preflight_rejects_invalid_mapping_shapes(document: dict, reason: str) -> None:
    with pytest.raises(ValueError, match=reason):
        provider_configuration._document_for_provider_preflight(document, "custom")
