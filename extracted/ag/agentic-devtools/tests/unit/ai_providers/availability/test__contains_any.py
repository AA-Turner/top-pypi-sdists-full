from agentic_devtools.ai_providers.availability import _contains_any


def test__contains_any_matches_case_insensitively() -> None:
    assert _contains_any("Base_Ref was not found", ("base_ref",))
    assert not _contains_any("custom_agent is invalid", ("base_ref",))
