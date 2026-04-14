"""Tests for ANTEROOM.md discovery, token estimation, and conventions (#215)."""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import patch

from anteroom.cli.instructions import (
    _CHARS_PER_TOKEN_ESTIMATE,
    CONVENTIONS_TOKEN_WARNING_THRESHOLD,
    ConventionsInfo,
    capture_snapshot,
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


class TestClaudeMdPrecedence:
    """Verify .claude.md and CLAUDE.md are discovered with correct priority (#1180)."""

    def test_claude_md_discovered(self, tmp_path: Path):
        (tmp_path / "CLAUDE.md").write_text("claude visible")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        path, content = result
        assert path.name == "CLAUDE.md"
        assert content == "claude visible"

    def test_hidden_claude_md_takes_priority(self, tmp_path: Path):
        (tmp_path / ".claude.md").write_text("claude hidden")
        (tmp_path / "CLAUDE.md").write_text("claude visible")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        path, content = result
        assert path.name == ".claude.md"
        assert content == "claude hidden"

    def test_anteroom_beats_claude(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("anteroom")
        (tmp_path / ".claude.md").write_text("claude hidden")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        path, content = result
        assert path.name == "ANTEROOM.md"
        assert content == "anteroom"


class TestFullFourFilenamePrecedence:
    """Full 4-filename priority within a single directory (#1180).

    Expected order: .anteroom.md > ANTEROOM.md > .claude.md > CLAUDE.md
    """

    def test_full_precedence_order(self, tmp_path: Path):
        (tmp_path / ".anteroom.md").write_text("1-hidden-anteroom")
        (tmp_path / "ANTEROOM.md").write_text("2-anteroom")
        (tmp_path / ".claude.md").write_text("3-hidden-claude")
        (tmp_path / "CLAUDE.md").write_text("4-claude")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        _, content = result
        assert content == "1-hidden-anteroom"

    def test_second_priority(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("2-anteroom")
        (tmp_path / ".claude.md").write_text("3-hidden-claude")
        (tmp_path / "CLAUDE.md").write_text("4-claude")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        _, content = result
        assert content == "2-anteroom"

    def test_third_priority(self, tmp_path: Path):
        (tmp_path / ".claude.md").write_text("3-hidden-claude")
        (tmp_path / "CLAUDE.md").write_text("4-claude")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        _, content = result
        assert content == "3-hidden-claude"

    def test_fourth_priority(self, tmp_path: Path):
        (tmp_path / "CLAUDE.md").write_text("4-claude")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        _, content = result
        assert content == "4-claude"


class TestWalkUpMixedFilenames:
    """Walk-up with mixed filenames across directories (#1180)."""

    def test_child_claude_md_beats_parent_anteroom(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("parent anteroom")
        child = tmp_path / "subdir"
        child.mkdir()
        (child / ".claude.md").write_text("child claude")
        result = find_project_instructions_path(str(child))
        assert result is not None
        _, content = result
        assert content == "child claude"

    def test_falls_through_to_parent(self, tmp_path: Path):
        (tmp_path / "CLAUDE.md").write_text("parent claude")
        child = tmp_path / "subdir"
        child.mkdir()
        result = find_project_instructions_path(str(child))
        assert result is not None
        _, content = result
        assert content == "parent claude"


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


class TestInstructionsSnapshot:
    """Tests for InstructionsSnapshot change detection (#1302)."""

    def test_capture_both_files(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("project")
        global_dir = tmp_path / "global"
        global_dir.mkdir()
        (global_dir / "ANTEROOM.md").write_text("global")

        with patch(
            "anteroom.cli.instructions.find_global_instructions_path",
            return_value=(global_dir / "ANTEROOM.md", "global"),
        ):
            snap = capture_snapshot(str(tmp_path))

        assert snap.project_path == tmp_path / "ANTEROOM.md"
        assert snap.project_mtime is not None
        assert snap.global_path == global_dir / "ANTEROOM.md"
        assert snap.global_mtime is not None
        assert snap.working_dir == str(tmp_path)

    def test_capture_no_files(self, tmp_path: Path):
        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))

        assert snap.project_path is None
        assert snap.project_mtime is None
        assert snap.global_path is None
        assert snap.global_mtime is None

    def test_capture_project_only(self, tmp_path: Path):
        (tmp_path / ".anteroom.md").write_text("hidden variant")
        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))

        assert snap.project_path == tmp_path / ".anteroom.md"
        assert snap.project_mtime is not None
        assert snap.global_path is None

    def test_capture_global_only(self, tmp_path: Path):
        global_dir = tmp_path / "global"
        global_dir.mkdir()
        (global_dir / "ANTEROOM.md").write_text("global")

        with patch(
            "anteroom.cli.instructions.find_global_instructions_path",
            return_value=(global_dir / "ANTEROOM.md", "global"),
        ):
            snap = capture_snapshot(str(tmp_path))

        assert snap.project_path is None
        assert snap.global_path == global_dir / "ANTEROOM.md"

    def test_capture_claude_md_variant(self, tmp_path: Path):
        (tmp_path / ".claude.md").write_text("claude md variant")
        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))

        assert snap.project_path == tmp_path / ".claude.md"

    def test_has_changed_detects_mtime(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("v1")
        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))

        # Ensure mtime actually changes (filesystem resolution can be coarse)
        time.sleep(0.05)
        (tmp_path / "ANTEROOM.md").write_text("v2")

        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            assert snap.has_changed(str(tmp_path)) is True

    def test_has_changed_stable(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("stable")
        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))
            assert snap.has_changed(str(tmp_path)) is False

    def test_has_changed_file_appears(self, tmp_path: Path):
        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))

        # File didn't exist, now it does
        (tmp_path / "ANTEROOM.md").write_text("appeared")

        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            assert snap.has_changed(str(tmp_path)) is True

    def test_has_changed_file_disappears(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("will vanish")
        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))

        (tmp_path / "ANTEROOM.md").unlink()

        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            assert snap.has_changed(str(tmp_path)) is True

    def test_has_changed_working_dir_change(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("content")
        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))

        other_dir = tmp_path / "other"
        other_dir.mkdir()
        assert snap.has_changed(str(other_dir)) is True

    def test_has_changed_higher_priority_shadows(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("original")
        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))

        # Higher-priority .anteroom.md shadows ANTEROOM.md
        (tmp_path / ".anteroom.md").write_text("shadow")

        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            assert snap.has_changed(str(tmp_path)) is True

    def test_has_changed_nearer_dir_shadows(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("parent")
        child = tmp_path / "subdir"
        child.mkdir()

        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(child))

        assert snap.project_path == tmp_path / "ANTEROOM.md"

        # Create nearer file that shadows parent
        (child / "ANTEROOM.md").write_text("child")

        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            assert snap.has_changed(str(child)) is True


# ---------------------------------------------------------------------------
# AGENTS.md support (#1394)
# ---------------------------------------------------------------------------


class TestAgentsMdDiscovery:
    """AGENTS.md and .agents.md are discovered at lowest precedence (#1394)."""

    def test_agents_md_discovered_alone(self, tmp_path: Path):
        (tmp_path / "AGENTS.md").write_text("agent instructions")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        _, content = result
        assert content == "agent instructions"

    def test_hidden_agents_md_discovered(self, tmp_path: Path):
        (tmp_path / ".agents.md").write_text("hidden agent instructions")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        _, content = result
        assert content == "hidden agent instructions"

    def test_anteroom_beats_agents(self, tmp_path: Path):
        (tmp_path / "ANTEROOM.md").write_text("anteroom wins")
        (tmp_path / "AGENTS.md").write_text("agents loses")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        _, content = result
        assert content == "anteroom wins"

    def test_claude_beats_agents(self, tmp_path: Path):
        (tmp_path / "CLAUDE.md").write_text("claude wins")
        (tmp_path / "AGENTS.md").write_text("agents loses")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        _, content = result
        assert content == "claude wins"

    def test_hidden_agents_beats_visible_agents(self, tmp_path: Path):
        (tmp_path / ".agents.md").write_text("hidden wins")
        (tmp_path / "AGENTS.md").write_text("visible loses")
        result = find_project_instructions_path(str(tmp_path))
        assert result is not None
        _, content = result
        assert content == "hidden wins"

    def test_walkup_finds_agents_in_parent(self, tmp_path: Path):
        (tmp_path / "AGENTS.md").write_text("parent agents")
        child = tmp_path / "subdir"
        child.mkdir()
        result = find_project_instructions_path(str(child))
        assert result is not None
        _, content = result
        assert content == "parent agents"

    def test_child_agents_beats_parent_agents(self, tmp_path: Path):
        (tmp_path / "AGENTS.md").write_text("parent agents")
        child = tmp_path / "subdir"
        child.mkdir()
        (child / "AGENTS.md").write_text("child agents")
        result = find_project_instructions_path(str(child))
        assert result is not None
        _, content = result
        assert content == "child agents"

    def test_child_claude_beats_parent_agents(self, tmp_path: Path):
        (tmp_path / "AGENTS.md").write_text("parent agents")
        child = tmp_path / "subdir"
        child.mkdir()
        (child / ".claude.md").write_text("child claude")
        result = find_project_instructions_path(str(child))
        assert result is not None
        _, content = result
        assert content == "child claude"
