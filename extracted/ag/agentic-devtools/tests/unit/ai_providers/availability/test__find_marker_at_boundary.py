from agentic_devtools.ai_providers.availability import _find_marker_at_boundary


def test__find_marker_at_boundary_matches_standalone_marker() -> None:
    assert _find_marker_at_boundary("base_ref is invalid", "base_ref") == len("base_ref")


def test__find_marker_at_boundary_matches_marker_after_space() -> None:
    assert _find_marker_at_boundary("the base_ref is invalid", "base_ref") == len("the base_ref")


def test__find_marker_at_boundary_rejects_identifier_prefix_match() -> None:
    assert _find_marker_at_boundary("database_ref is invalid", "base_ref") is None


def test__find_marker_at_boundary_rejects_identifier_suffix_match() -> None:
    assert _find_marker_at_boundary("base_refx is invalid", "base_ref") is None
