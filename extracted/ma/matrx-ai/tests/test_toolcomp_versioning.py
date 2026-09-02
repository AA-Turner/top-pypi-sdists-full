from __future__ import annotations

from matrx_ai.tools.implementations.tool_component import _bump_semver_patch


def test_bump_semver_patch_increments_trailing_segment() -> None:
    assert _bump_semver_patch("1.0.2") == "1.0.3"
    assert _bump_semver_patch("2.1.9") == "2.1.10"


def test_bump_semver_patch_defaults_when_missing() -> None:
    assert _bump_semver_patch(None) == "1.0.1"
    assert _bump_semver_patch("") == "1.0.1"


def test_bump_semver_patch_non_numeric_tail() -> None:
    assert _bump_semver_patch("1.0.0-beta") == "1.0.0-beta.1"
