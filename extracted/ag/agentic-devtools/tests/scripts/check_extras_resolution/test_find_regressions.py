"""Tests for check_extras_resolution.find_regressions."""

from __future__ import annotations

from tests.scripts.check_extras_resolution import checker


def test_find_regressions_detects_downgraded_package() -> None:
    """A package that resolves lower with the extra than without it is reported."""
    base = {"langgraph": "1.2.11"}
    with_extra = {"langgraph": "1.0.1"}

    regressions = checker.find_regressions(base, with_extra)

    assert len(regressions) == 1
    assert "langgraph" in regressions[0]
    assert "1.2.11" in regressions[0]
    assert "1.0.1" in regressions[0]


def test_find_regressions_returns_empty_when_extra_matches_or_upgrades() -> None:
    """No regression is reported when the extra keeps or upgrades the base version."""
    base = {"requests": "2.31.0", "langgraph": "1.2.11"}
    with_extra = {"requests": "2.31.0", "langgraph": "1.3.0"}

    assert checker.find_regressions(base, with_extra) == []


def test_find_regressions_ignores_packages_only_in_base() -> None:
    """Packages absent from the extra's resolution (not requested by it) are ignored."""
    base = {"requests": "2.31.0"}
    with_extra: dict[str, str] = {}

    assert checker.find_regressions(base, with_extra) == []


def test_find_regressions_ignores_invalid_versions() -> None:
    """Unparseable version strings are skipped rather than raising."""
    base = {"weird-pkg": "not-a-version"}
    with_extra = {"weird-pkg": "also-not-a-version"}

    assert checker.find_regressions(base, with_extra) == []
