from __future__ import annotations

from agentic_devtools.cli.jira.creation_pipeline import _extract_mapping_orchestration_key


def test_returns_camel_case_key() -> None:
    assert _extract_mapping_orchestration_key({"orchestrationKey": "abc"}) == "abc"


def test_returns_snake_case_key() -> None:
    assert _extract_mapping_orchestration_key({"orchestration_key": "def"}) == "def"


def test_returns_none_for_invalid_entry() -> None:
    assert _extract_mapping_orchestration_key({"orchestrationKey": []}) is None
    assert _extract_mapping_orchestration_key("not-a-mapping") is None
