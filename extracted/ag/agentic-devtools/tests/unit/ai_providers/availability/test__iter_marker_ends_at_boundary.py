from agentic_devtools.ai_providers.availability import _iter_marker_ends_at_boundary


def test__iter_marker_ends_at_boundary_returns_all_occurrences() -> None:
    seg = "base_ref is invalid, base_ref is invalid"
    ends = _iter_marker_ends_at_boundary(seg, "base_ref")
    assert ends == [len("base_ref"), seg.index("base_ref", 1) + len("base_ref")]


def test__iter_marker_ends_at_boundary_skips_identifier_prefix_and_suffix_matches() -> None:
    seg = "database_ref is invalid and base_refx is invalid"
    assert _iter_marker_ends_at_boundary(seg, "base_ref") == []


def test__iter_marker_ends_at_boundary_returns_empty_list_when_marker_absent() -> None:
    assert _iter_marker_ends_at_boundary("model is invalid", "base_ref") == []
