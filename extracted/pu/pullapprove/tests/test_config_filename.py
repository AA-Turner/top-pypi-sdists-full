"""The configurable config filename prefix.

PULLAPPROVE_CONFIG_PREFIX is read once at import (a per-process constant), so
these exercise the resolver directly rather than reimporting the module.
"""

import pytest
from pullapprove.config import (
    CONFIG_FILENAME,
    CONFIG_FILENAME_PREFIX,
    _resolve_config_filename_prefix,
)


def test_default_prefix_and_filename():
    assert CONFIG_FILENAME_PREFIX == "CODEREVIEW"
    assert CONFIG_FILENAME == "CODEREVIEW.toml"


def test_unset_falls_back_to_the_default(monkeypatch):
    monkeypatch.delenv("PULLAPPROVE_CONFIG_PREFIX", raising=False)
    assert _resolve_config_filename_prefix() == "CODEREVIEW"


def test_blank_falls_back_to_the_default(monkeypatch):
    monkeypatch.setenv("PULLAPPROVE_CONFIG_PREFIX", "   ")
    assert _resolve_config_filename_prefix() == "CODEREVIEW"


def test_rename(monkeypatch):
    monkeypatch.setenv("PULLAPPROVE_CONFIG_PREFIX", "REVIEW")
    assert _resolve_config_filename_prefix() == "REVIEW"


def test_extension_is_rejected(monkeypatch):
    """A prefix is a name, not a filename — the .toml is added for you."""
    monkeypatch.setenv("PULLAPPROVE_CONFIG_PREFIX", "REVIEW.toml")
    with pytest.raises(ValueError, match="without an extension"):
        _resolve_config_filename_prefix()


@pytest.mark.parametrize("prefix", ["dir/REVIEW", "dir\\REVIEW", "../REVIEW"])
def test_paths_are_rejected(prefix, monkeypatch):
    monkeypatch.setenv("PULLAPPROVE_CONFIG_PREFIX", prefix)
    with pytest.raises(ValueError, match="not a path"):
        _resolve_config_filename_prefix()
