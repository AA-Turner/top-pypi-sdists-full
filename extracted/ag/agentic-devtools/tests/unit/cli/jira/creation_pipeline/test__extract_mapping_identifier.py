from __future__ import annotations

from agentic_devtools.cli.jira.creation_pipeline import _extract_mapping_identifier


def test_returns_string_entry_verbatim() -> None:
    assert _extract_mapping_identifier("123") == "123"


def test_returns_identifier_alias_from_dict() -> None:
    assert _extract_mapping_identifier({"providerId": 7, "identifier": "456"}) == "456"


def test_returns_none_for_invalid_entry() -> None:
    assert _extract_mapping_identifier({"identifier": []}) is None
