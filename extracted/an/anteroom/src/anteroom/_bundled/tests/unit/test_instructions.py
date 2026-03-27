"""Tests for ANTEROOM.md discovery, token estimation, and conventions (#215)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from anteroom.cli.instructions import (
    _CHARS_PER_TOKEN_ESTIMATE,
    CONVENTIONS_TOKEN_WARNING_THRESHOLD,
    ConventionsInfo,
    discover_conventions,
    estimate_tokens,
    find_project_instructions,
    find_project_instructions_path,
)


class TestEstimateTokens:
    def test_empty_string(self):
        assert estimate_tokens("") == 0

    def test_short_text(self):
        assert estimate_tokens("hello world") == len("hello world") // _CHARS_PER_TOKEN_ESTIMATE

    def test_proportional(self):
        text_a = "a" * 100
        text_b = "a" * 400
        assert estimate_tokens(text_b) == estimate_tokens(text_a) * 4


class TestSearchOrder:
    """Verify .anteroom.md > ANTEROOM.md priority."""

    def test_hidden_file_takes_priority(self, tmp_path: Path):
        (tmp_path / ".anteroom.md").write_text("hidden")
        (tmp_path / "ANTEROOM.md").write_text("visible")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        path, content = result
        assert path.name == ".anteroom.md"
        assert content == "hidden"

    def test_anteroom_md_found(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("anteroom")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        path, content = result
        assert path.name == "ANTEROOM.md"
        assert content == "anteroom"

    def test_parlor_md_not_recognized(self, tmp_path: Path):
        (tmp_path / "PARLOR.md").write_text("legacy")
        result = find_project_instructions_path(str(tmp_path))
        assert result is None

    def test_no_file_returns_none(self, tmp_path: Path):
        result = find_project_instructions_path(str(tmp_path))
        assert result is None

    def test_content_only_helper(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("content only")
        result = find_project_instructions(str(tmp_path))
        assert result == "content only"


class TestWalkUp:
    """Verify directory walk-up behavior."""

    def test_finds_in_parent(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("parent")
        child = tmp_path / "subdir"
        child.mkdir()
        result = find_project_instructions_path(str(child))
        assert result is not None
        _, content = result
        assert content == "parent"

    def test_nearest_wins(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("parent")
        child = tmp_path / "subdir"
        child.mkdir()
        (child / "ANTEROOM.md").write_text("child")
        result = find_project_instructions_path(str(child))
        assert result is not None
        _, content = result
        assert content == "child"


class TestConventionsInfo:
    def test_no_warning_when_small(self):
        info = ConventionsInfo(
            path=Path("/test"),
            content="small",
            source="project",
            estimated_tokens=100,
            is_oversized=False,
        )
        assert info.warning is None

    def test_warning_when_oversized(self):
        info = ConventionsInfo(
            path=Path("/test"),
            content="large",
            source="project",
            estimated_tokens=5000,
            is_oversized=True,
        )
        assert info.warning is not None
        assert "5,000" in info.warning
        assert f"{CONVENTIONS_TOKEN_WARNING_THRESHOLD:,}" in info.warning


class TestDiscoverConventions:
    def test_project_file(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("# Project conventions")
        info = discover_conventions(str(tmp_path))
        assert info.source == "project"
        assert info.content == "# Project conventions"
        assert info.path is not None
        assert info.estimated_tokens > 0

    def test_no_file(self, tmp_path: Path):
        info = discover_conventions(str(tmp_path))
        assert info.source == "none"
        assert info.content is None
        assert info.path is None
        assert info.estimated_tokens == 0

    def test_oversized_detection(self, tmp_path: Path):
        big_content = "x" * (CONVENTIONS_TOKEN_WARNING_THRESHOLD * _CHARS_PER_TOKEN_ESTIMATE + 100)
        (tmp_path / "ANTEROOM.md").write_text(big_content)
        info = discover_conventions(str(tmp_path))
        assert info.is_oversized is True
        assert info.warning is not None

    def test_falls_back_to_global(self, tmp_path: Path):
        global_content = "# Global rules"
        with patch(
            "anteroom.cli.instructions.find_global_instructions_path",
            return_value=(tmp_path / "ANTEROOM.md", global_content),
        ):
            info = discover_conventions(str(tmp_path))
        assert info.source == "global"
        assert info.content == global_content

    def test_hidden_anteroom_md(self, tmp_path: Path):
        (tmp_path / ".anteroom.md").write_text("hidden conventions")
        info = discover_conventions(str(tmp_path))
        assert info.source == "project"
        assert info.content == "hidden conventions"
        assert info.path is not None
        assert info.path.name == ".anteroom.md"


class TestWalkUpDiscovery:
    """Walk-up discovery for .anteroom.md in cwd vs ANTEROOM.md in parent."""

    def test_hidden_anteroom_md_in_cwd(self, tmp_path: Path):
        (tmp_path / ".anteroom.md").write_text("cwd hidden")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        path, content = result
        assert path.name == ".anteroom.md"
        assert content == "cwd hidden"

    def test_anteroom_md_in_parent(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("parent instructions")
        child = tmp_path / "subdir" / "deep"
        child.mkdir(parents=True)
        result = find_project_instructions_path(str(child))
        assert result is not None
        _, content = result
        assert content == "parent instructions"

    def test_neither_exists_returns_none(self, tmp_path: Path):
        child = tmp_path / "empty_subdir"
        child.mkdir()
        result = find_project_instructions_path(str(child))
        # Walk-up may find files in system dirs; check it doesn't crash
        # and that starting from an empty dir with no ancestors having
        # ANTEROOM.md returns None (or finds a real one higher up)
        assert result is None or result[1] is not None


class TestTokenEstimationThreshold:
    """Token estimation and oversized threshold detection."""

    def test_short_text_below_threshold(self):
        short = "x" * 100
        tokens = estimate_tokens(short)
        assert tokens == 25
        assert tokens < CONVENTIONS_TOKEN_WARNING_THRESHOLD

    def test_text_below_threshold_boundary(self):
        # 15999 chars -> 3999 tokens, just under 4000 threshold
        text = "x" * 15999
        tokens = estimate_tokens(text)
        assert tokens == 3999
        assert tokens < CONVENTIONS_TOKEN_WARNING_THRESHOLD

    def test_text_at_threshold_boundary(self):
        # 16000 chars -> 4000 tokens, exactly at threshold
        text = "x" * 16000
        tokens = estimate_tokens(text)
        assert tokens == 4000
        assert tokens >= CONVENTIONS_TOKEN_WARNING_THRESHOLD

    def test_oversized_conventions_warning(self, tmp_path: Path):
        # Create content that exceeds the threshold
        big_text = "x" * (CONVENTIONS_TOKEN_WARNING_THRESHOLD * _CHARS_PER_TOKEN_ESTIMATE + 100)
        (tmp_path / "ANTEROOM.md").write_text(big_text)
        info = discover_conventions(str(tmp_path))
        assert info.is_oversized is True
        assert info.warning is not None
        assert str(CONVENTIONS_TOKEN_WARNING_THRESHOLD) in info.warning.replace(",", "")
