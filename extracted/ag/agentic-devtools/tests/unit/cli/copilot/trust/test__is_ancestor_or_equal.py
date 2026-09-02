"""Tests for _is_ancestor_or_equal."""

from agentic_devtools.cli.copilot import trust
from agentic_devtools.cli.copilot.trust import _is_ancestor_or_equal


def _raise_value_error(*_args, **_kwargs):
    raise ValueError("not comparable")


class TestIsAncestorOrEqual:
    """Tests for _is_ancestor_or_equal."""

    def test_equal_paths(self, tmp_path):
        """Equal paths are covered."""
        assert _is_ancestor_or_equal(str(tmp_path), str(tmp_path)) is True

    def test_ancestor_covers_descendant(self, tmp_path):
        """An ancestor covers a nested descendant."""
        child = tmp_path / "a" / "b"
        assert _is_ancestor_or_equal(str(tmp_path), str(child)) is True

    def test_unrelated_paths(self, tmp_path):
        """Sibling paths are not covered."""
        assert _is_ancestor_or_equal(str(tmp_path / "x"), str(tmp_path / "y")) is False

    def test_value_error_returns_false(self, tmp_path, monkeypatch):
        """A commonpath ValueError (e.g. different drives) yields False."""
        monkeypatch.setattr(trust.os.path, "commonpath", _raise_value_error)
        assert _is_ancestor_or_equal(str(tmp_path / "x"), str(tmp_path / "y")) is False
