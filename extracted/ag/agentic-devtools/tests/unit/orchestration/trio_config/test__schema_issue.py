"""Tests for ``_schema_issue``."""

from types import SimpleNamespace

import agentic_devtools.orchestration.trio_config as trio_module


def test__schema_issue_covers_required_and_additional_properties() -> None:
    required = SimpleNamespace(absolute_path=[], validator="required", message="'schemaVersion' is a required property")
    required_without_match = SimpleNamespace(absolute_path=[], validator="required", message="not a required message")
    additional = SimpleNamespace(
        absolute_path=[],
        validator="additionalProperties",
        message="('unknown' was unexpected)",
    )
    additional_without_match = SimpleNamespace(
        absolute_path=[],
        validator="additionalProperties",
        message="not an additional message",
    )
    assert trio_module._schema_issue(required).startswith("/")
    assert trio_module._schema_issue(required_without_match).startswith("/")
    assert trio_module._schema_issue(additional).startswith("/")
    assert trio_module._schema_issue(additional_without_match).startswith("/")
