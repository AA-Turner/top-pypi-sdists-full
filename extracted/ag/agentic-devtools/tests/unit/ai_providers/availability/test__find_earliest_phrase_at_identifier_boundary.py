from agentic_devtools.ai_providers.availability import _find_earliest_phrase_at_identifier_boundary


def test__find_earliest_phrase_at_identifier_boundary_returns_none_without_match() -> None:
    assert _find_earliest_phrase_at_identifier_boundary("totally unrelated", ("model", "base_ref")) is None


def test__find_earliest_phrase_at_identifier_boundary_returns_earliest_bounded_match() -> None:
    text = "invalid custom_agent and invalid model"
    assert _find_earliest_phrase_at_identifier_boundary(text, ("invalid model", "invalid custom_agent")) == 0
    assert _find_earliest_phrase_at_identifier_boundary(text, ("invalid custom_agent", "invalid model")) == 0
