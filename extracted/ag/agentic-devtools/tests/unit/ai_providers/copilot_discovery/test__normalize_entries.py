from agentic_devtools.ai_providers.copilot_discovery import _normalize_entries


def test_drops_unusable_entries_and_keeps_the_rest() -> None:
    records = _normalize_entries([{"modelId": "auto"}, "junk", {"name": "no id"}, {"modelId": "gpt-5-mini"}])

    assert [record.model_id for record in records] == ["auto", "gpt-5-mini"]


def test_returns_an_empty_list_when_nothing_is_usable() -> None:
    assert _normalize_entries(["junk"]) == []
