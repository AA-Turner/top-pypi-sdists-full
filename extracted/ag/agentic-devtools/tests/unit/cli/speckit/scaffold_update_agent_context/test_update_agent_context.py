"""Tests for ``update_agent_context``."""

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.scaffold_update_agent_context import (
    SPECKIT_END_MARKER,
    SPECKIT_START_MARKER,
    update_agent_context,
)


class TestUpdateAgentContext:
    """update_agent_context syncs plan.md's Technical Context into an agent file."""

    def test_returns_none_for_unknown_agent_type(self, tmp_path: Path, capsys) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        result = update_agent_context("not-an-agent", tmp_path, feature_dir, "042-x")

        assert result is None
        assert "WARNING" in capsys.readouterr().err

    def test_raises_when_plan_md_missing(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)

        with pytest.raises(FileNotFoundError, match="Run agdt-speckit-plan first"):
            update_agent_context("copilot", tmp_path, feature_dir, "042-x")

    def test_creates_agent_file_and_parents(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("**Language/Version**: Python 3.11", encoding="utf-8")

        agent_file = update_agent_context("copilot", tmp_path, feature_dir, "042-x")

        assert agent_file == tmp_path / ".github" / "copilot-instructions.md"
        assert agent_file is not None
        content = agent_file.read_text(encoding="utf-8")
        assert SPECKIT_START_MARKER in content
        assert SPECKIT_END_MARKER in content
        assert "Python 3.11" in content
        assert "042-x" in content

    def test_updates_existing_agent_file_preserving_other_content(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        agent_file_path = tmp_path / ".cursorrules"
        agent_file_path.write_text("# Existing rules\n", encoding="utf-8")

        agent_file = update_agent_context("cursor", tmp_path, feature_dir, "042-x")

        assert agent_file is not None
        content = agent_file.read_text(encoding="utf-8")
        assert "# Existing rules" in content
        assert SPECKIT_START_MARKER in content

    def test_cursor_agent_alias_writes_to_cursor_rules_mdc(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        agent_file = update_agent_context("cursor-agent", tmp_path, feature_dir, "042-x")

        assert agent_file == tmp_path / ".cursor" / "rules" / "specify-rules.mdc"
        content = agent_file.read_text(encoding="utf-8")
        assert SPECKIT_START_MARKER in content
        assert content.startswith("---\nalwaysApply: true\n---\n")

    def test_cursor_agent_preserves_existing_frontmatter_on_second_run(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("**Storage**: N/A", encoding="utf-8")

        update_agent_context("cursor-agent", tmp_path, feature_dir, "042-x")
        (feature_dir / "plan.md").write_text("**Storage**: PostgreSQL", encoding="utf-8")
        agent_file = update_agent_context("cursor-agent", tmp_path, feature_dir, "042-x")
        assert agent_file is not None

        content = agent_file.read_text(encoding="utf-8")
        assert content.count("---\nalwaysApply: true\n---\n") == 1
        assert "PostgreSQL" in content

    def test_mdc_targets_other_than_cursor_agent_receive_frontmatter(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        agent_file = update_agent_context("firebender", tmp_path, feature_dir, "042-x")

        assert agent_file == tmp_path / ".firebender" / "rules" / "specify-rules.mdc"
        content = agent_file.read_text(encoding="utf-8")
        assert content.startswith("---\nalwaysApply: true\n---\n")

    @pytest.mark.parametrize(
        ("agent_type", "expected_path"),
        [
            ("opencode", "AGENTS.md"),
            ("kilocode", ".kilocode/rules/specify-rules.md"),
            ("auggie", ".augment/rules/specify-rules.md"),
            ("roo", ".roo/rules/specify-rules.md"),
            ("codebuddy", "CODEBUDDY.md"),
            ("amp", "AGENTS.md"),
            ("shai", "SHAI.md"),
            ("q", "AGENTS.md"),
            ("bob", "AGENTS.md"),
            ("qoder", "QODER.md"),
            ("qodercli", "QODER.md"),
        ],
    )
    def test_legacy_agent_aliases_are_supported(
        self,
        tmp_path: Path,
        agent_type: str,
        expected_path: str,
    ) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        agent_file = update_agent_context(agent_type, tmp_path, feature_dir, "042-x")

        assert agent_file == tmp_path / Path(expected_path)
        assert SPECKIT_START_MARKER in agent_file.read_text(encoding="utf-8")

    def test_raises_when_plan_md_is_symlink(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        real_plan = tmp_path / "real-plan.md"
        real_plan.write_text("plan", encoding="utf-8")
        (feature_dir / "plan.md").symlink_to(real_plan)

        with pytest.raises(ValueError, match="symlinked plan.md"):
            update_agent_context("copilot", tmp_path, feature_dir, "042-x")

    def test_plan_md_symlink_is_rejected_before_read(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        feature_dir = repo_root / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        outside_plan = tmp_path / "outside-plan.md"
        outside_plan.write_text("plan", encoding="utf-8")
        plan_link = feature_dir / "plan.md"
        plan_link.symlink_to(outside_plan)

        with pytest.raises(ValueError, match="symlinked plan.md"):
            update_agent_context("copilot", repo_root, feature_dir, "042-x")

    def test_plan_md_symlink_to_directory_is_rejected_before_read(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        target_dir = tmp_path / "real-plan-dir"
        target_dir.mkdir()
        (feature_dir / "plan.md").symlink_to(target_dir)

        with pytest.raises(ValueError, match="symlinked plan.md"):
            update_agent_context("copilot", tmp_path, feature_dir, "042-x")

    def test_raises_when_agent_file_symlink_escapes_repo_root(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        github_dir = repo_root / ".github"
        github_dir.mkdir()
        outside = tmp_path / "outside.md"
        outside.write_text("sensitive", encoding="utf-8")
        symlink = github_dir / "copilot-instructions.md"
        symlink.symlink_to(outside)

        with pytest.raises(ValueError, match="outside the repository root"):
            update_agent_context("copilot", repo_root, feature_dir, "042-x")

    def test_raises_before_creating_parent_when_target_parent_symlink_escapes_repo_root(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        feature_dir = repo_root / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        outside_cursor = tmp_path / "outside-cursor"
        outside_cursor.mkdir()
        (repo_root / ".cursor").symlink_to(outside_cursor)

        with pytest.raises(ValueError, match="outside the repository root"):
            update_agent_context("cursor-agent", repo_root, feature_dir, "042-x")

        assert not (outside_cursor / "rules").exists()

    def test_uses_absolute_display_path_when_feature_dir_not_relative_to_repo_root(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "outside" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        repo_root = tmp_path / "repo"
        repo_root.mkdir()

        agent_file = update_agent_context("copilot", repo_root, feature_dir, "042-x")

        assert agent_file is not None
        content = agent_file.read_text(encoding="utf-8")
        assert feature_dir.as_posix() in content

    def test_second_run_replaces_block_idempotently(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("**Storage**: N/A", encoding="utf-8")

        update_agent_context("copilot", tmp_path, feature_dir, "042-x")
        (feature_dir / "plan.md").write_text("**Storage**: PostgreSQL", encoding="utf-8")
        agent_file = update_agent_context("copilot", tmp_path, feature_dir, "042-x")

        assert agent_file is not None
        content = agent_file.read_text(encoding="utf-8")
        assert content.count(SPECKIT_START_MARKER) == 1
        assert "PostgreSQL" in content
        assert "N/A" not in content

    def test_malformed_existing_markers_fail_without_writing(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("**Storage**: PostgreSQL", encoding="utf-8")
        agent_file = tmp_path / ".github" / "copilot-instructions.md"
        original_text = f"# Header\n\n{SPECKIT_START_MARKER}\n\n# Footer"
        agent_file.parent.mkdir(parents=True, exist_ok=True)
        agent_file.write_text(original_text, encoding="utf-8")

        with pytest.raises(ValueError, match="Malformed SpecKit marker block"):
            update_agent_context("copilot", tmp_path, feature_dir, "042-x")

        assert agent_file.read_text(encoding="utf-8") == original_text

    def test_dry_run_does_not_create_agent_file(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("**Language/Version**: Python 3.11", encoding="utf-8")

        agent_file = update_agent_context("copilot", tmp_path, feature_dir, "042-x", dry_run=True)

        assert agent_file == tmp_path / ".github" / "copilot-instructions.md"
        assert not agent_file.exists()

    def test_dry_run_does_not_modify_existing_agent_file(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("**Language/Version**: Python 3.11", encoding="utf-8")
        agent_file_path = tmp_path / ".github" / "copilot-instructions.md"
        agent_file_path.parent.mkdir(parents=True, exist_ok=True)
        original_text = "# Original content\n"
        agent_file_path.write_text(original_text, encoding="utf-8")

        result = update_agent_context("copilot", tmp_path, feature_dir, "042-x", dry_run=True)

        assert result == agent_file_path
        assert agent_file_path.read_text(encoding="utf-8") == original_text

    def test_dry_run_still_raises_for_path_escape(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        github_dir = repo_root / ".github"
        github_dir.mkdir()
        outside = tmp_path / "outside.md"
        outside.write_text("sensitive", encoding="utf-8")
        (github_dir / "copilot-instructions.md").symlink_to(outside)

        with pytest.raises(ValueError, match="outside the repository root"):
            update_agent_context("copilot", repo_root, feature_dir, "042-x", dry_run=True)

    def test_dry_run_still_raises_for_missing_plan_md(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)

        with pytest.raises(FileNotFoundError, match="Run agdt-speckit-plan first"):
            update_agent_context("copilot", tmp_path, feature_dir, "042-x", dry_run=True)
