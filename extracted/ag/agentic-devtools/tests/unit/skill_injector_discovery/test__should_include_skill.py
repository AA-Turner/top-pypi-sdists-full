"""Tests for applying skill classification filters."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.skill_injector_discovery import _should_include_skill


def test_unfiltered_skill_is_included_without_reading(tmp_path: Path) -> None:
    cache: dict[Path, dict[str, object]] = {}

    assert (
        _should_include_skill(
            tmp_path / "missing.md",
            filtering=False,
            issue_adapter=None,
            code_hosting=None,
            fm_cache=cache,
        )
        is True
    )
    assert cache == {}


def test_filtered_skill_is_included_and_cached(tmp_path: Path) -> None:
    entry = tmp_path / "SKILL.md"
    entry.write_text("---\nname: Example\ndescription: Example skill\n---\n", encoding="utf-8")
    cache: dict[Path, dict[str, object]] = {}

    with patch("agentic_devtools.skill_injector_discovery.should_inject", return_value=True):
        included = _should_include_skill(
            entry,
            filtering=True,
            issue_adapter="github",
            code_hosting=None,
            fm_cache=cache,
        )

    assert included is True
    assert cache[entry]["description"] == "Example skill"


def test_filtered_out_skill_is_not_cached(tmp_path: Path) -> None:
    entry = tmp_path / "SKILL.md"
    entry.write_text("---\nname: Example\ndescription: Example skill\n---\n", encoding="utf-8")
    cache: dict[Path, dict[str, object]] = {}

    with patch("agentic_devtools.skill_injector_discovery.should_inject", return_value=False):
        included = _should_include_skill(
            entry,
            filtering=True,
            issue_adapter="github",
            code_hosting=None,
            fm_cache=cache,
        )

    assert included is False
    assert cache == {}


def test_non_utf8_skill_is_kept_without_frontmatter_cache(tmp_path: Path) -> None:
    entry = tmp_path / "SKILL.md"
    entry.write_bytes(b"\xff")
    cache: dict[Path, dict[str, object]] = {}

    assert (
        _should_include_skill(
            entry,
            filtering=True,
            issue_adapter="github",
            code_hosting=None,
            fm_cache=cache,
        )
        is True
    )
    assert cache == {}
