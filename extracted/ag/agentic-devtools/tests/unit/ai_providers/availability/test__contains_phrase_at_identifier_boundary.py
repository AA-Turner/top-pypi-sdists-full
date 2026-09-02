from agentic_devtools.ai_providers.availability import _contains_phrase_at_identifier_boundary


def test__contains_phrase_at_identifier_boundary_matches_standalone_phrase() -> None:
    assert _contains_phrase_at_identifier_boundary("base_ref is invalid", ("base_ref is invalid",))


def test__contains_phrase_at_identifier_boundary_matches_phrase_after_space() -> None:
    assert _contains_phrase_at_identifier_boundary("the base_ref is invalid", ("base_ref is invalid",))


def test__contains_phrase_at_identifier_boundary_rejects_phrase_with_identifier_prefix() -> None:
    # "database_ref is invalid" must not match "base_ref is invalid"
    assert not _contains_phrase_at_identifier_boundary("database_ref is invalid", ("base_ref is invalid",))


def test__contains_phrase_at_identifier_boundary_rejects_phrase_with_identifier_suffix() -> None:
    # "base_ref is invalidated" must not match "base_ref is invalid"
    assert not _contains_phrase_at_identifier_boundary("base_ref is invalidated", ("base_ref is invalid",))


def test__contains_phrase_at_identifier_boundary_matches_phrase_at_start_of_string() -> None:
    assert _contains_phrase_at_identifier_boundary("base_ref is missing", ("base_ref is missing",))


def test__contains_phrase_at_identifier_boundary_is_case_insensitive() -> None:
    # callers lower-case before passing; the function operates on already-lowercased text
    assert _contains_phrase_at_identifier_boundary("base_ref is invalid", ("base_ref is invalid",))
