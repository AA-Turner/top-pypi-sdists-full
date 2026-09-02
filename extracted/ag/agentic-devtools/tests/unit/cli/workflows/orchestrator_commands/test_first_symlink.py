"""Tests for _first_symlink."""

from agentic_devtools.cli.workflows.orchestrator_commands import _first_symlink


def test_first_symlink_returns_first_symlink_candidate(tmp_path) -> None:
    target = tmp_path / "target"
    target.write_text("x", encoding="utf-8")
    plain = tmp_path / "plain"
    plain.write_text("y", encoding="utf-8")
    first = tmp_path / "first-link"
    second = tmp_path / "second-link"
    first.symlink_to(target)
    second.symlink_to(target)

    assert _first_symlink((plain, first, second)) == first


def test_first_symlink_returns_none_when_no_symlink_exists(tmp_path) -> None:
    one = tmp_path / "one"
    two = tmp_path / "two"
    one.write_text("1", encoding="utf-8")
    two.mkdir()

    assert _first_symlink((one, two)) is None
