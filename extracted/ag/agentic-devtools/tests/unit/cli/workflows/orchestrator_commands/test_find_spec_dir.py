"""Tests for _find_spec_dir."""

from agentic_devtools.cli.workflows.orchestrator_commands import _find_spec_dir


def test_direct_match_returned(tmp_path) -> None:
    (tmp_path / "specs" / "1867").mkdir(parents=True)
    result = _find_spec_dir(tmp_path, "1867")
    assert result == tmp_path / "specs" / "1867"


def test_slug_prefix_match_returned(tmp_path) -> None:
    (tmp_path / "specs" / "1234-my-feature").mkdir(parents=True)
    result = _find_spec_dir(tmp_path, "1234")
    assert result == tmp_path / "specs" / "1234-my-feature"


def test_nested_hierarchical_match_returned(tmp_path) -> None:
    (tmp_path / "specs" / "100" / "200" / "300").mkdir(parents=True)
    result = _find_spec_dir(tmp_path, "300")
    assert result == tmp_path / "specs" / "100" / "200" / "300"


def test_not_found_returns_none(tmp_path) -> None:
    (tmp_path / "specs").mkdir(parents=True)
    result = _find_spec_dir(tmp_path, "9999")
    assert result is None


def test_direct_takes_priority_over_slug(tmp_path) -> None:
    (tmp_path / "specs" / "42").mkdir(parents=True)
    (tmp_path / "specs" / "42-some-spec").mkdir(parents=True)
    result = _find_spec_dir(tmp_path, "42")
    assert result == tmp_path / "specs" / "42"


def test_slug_takes_priority_over_nested(tmp_path) -> None:
    (tmp_path / "specs" / "5-short").mkdir(parents=True)
    (tmp_path / "specs" / "100" / "5").mkdir(parents=True)
    result = _find_spec_dir(tmp_path, "5")
    assert result == tmp_path / "specs" / "5-short"


def test_missing_specs_dir_returns_none(tmp_path) -> None:
    result = _find_spec_dir(tmp_path, "1867")
    assert result is None


def test_slug_file_not_directory_is_skipped(tmp_path) -> None:
    (tmp_path / "specs").mkdir(parents=True)
    (tmp_path / "specs" / "77-some-spec").touch()
    result = _find_spec_dir(tmp_path, "77")
    assert result is None


def test_nested_file_not_directory_is_skipped(tmp_path) -> None:
    (tmp_path / "specs" / "10" / "20").mkdir(parents=True)
    (tmp_path / "specs" / "10" / "20" / "30").touch()
    result = _find_spec_dir(tmp_path, "30")
    assert result is None
