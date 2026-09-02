"""Tests for instruction file resolver."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.audit.instruction_resolver import resolve_instruction_files


class TestResolveInstructionFiles:
    """Tests for resolve_instruction_files() covering directory walk-up and deduplication."""

    def test_always_includes_root_instruction(self, tmp_path: Path) -> None:
        """Root .github/copilot-instructions.md and AGENTS.md are always included."""
        root_dir = tmp_path / ".github"
        root_dir.mkdir()
        root_file = root_dir / "copilot-instructions.md"
        root_file.write_text("# Root instructions")
        (tmp_path / "AGENTS.md").write_text("# Root agents")

        result = resolve_instruction_files([], str(tmp_path))
        by_path = {entry.path: entry for entry in result}
        assert set(by_path) == {".github/copilot-instructions.md", "AGENTS.md"}
        assert by_path[".github/copilot-instructions.md"].exists is True
        assert by_path[".github/copilot-instructions.md"].content == "# Root instructions"
        assert by_path["AGENTS.md"].exists is True
        assert by_path["AGENTS.md"].content == "# Root agents"

    def test_nonexistent_root_included_as_not_exists(self, tmp_path: Path) -> None:
        """Root instruction files are included even when missing."""
        result = resolve_instruction_files([], str(tmp_path))
        by_path = {entry.path: entry for entry in result}
        assert set(by_path) == {".github/copilot-instructions.md", "AGENTS.md"}
        assert by_path[".github/copilot-instructions.md"].exists is False
        assert by_path["AGENTS.md"].exists is False

    def test_walks_up_directory_tree(self, tmp_path: Path) -> None:
        """Finds instruction files in parent directories."""
        # Create directory structure
        (tmp_path / ".github").mkdir()
        (tmp_path / "src" / "cli").mkdir(parents=True)
        src_instructions = tmp_path / "src" / "copilot-instructions.md"
        src_instructions.write_text("# Src instructions")

        result = resolve_instruction_files(["src/cli/main.py"], str(tmp_path))

        paths = [r.path for r in result]
        assert ".github/copilot-instructions.md" in paths
        assert "src/copilot-instructions.md" in paths

    def test_walks_up_for_agents_files(self, tmp_path: Path) -> None:
        """Directory-scoped AGENTS.md files are found and preloaded."""
        (tmp_path / ".github").mkdir()
        (tmp_path / "src" / "cli").mkdir(parents=True)
        (tmp_path / "src" / "AGENTS.md").write_text("# Src agent instructions")

        result = resolve_instruction_files(["src/cli/main.py"], str(tmp_path))

        by_path = {r.path: r for r in result}
        assert by_path["src/AGENTS.md"].exists is True
        assert by_path["src/AGENTS.md"].content == "# Src agent instructions"

    def test_missing_agents_file_offered_for_creation(self, tmp_path: Path) -> None:
        """A missing AGENTS.md is offered as a creatable path in every parent dir.

        This includes the repository root itself.
        """
        (tmp_path / ".github").mkdir()
        (tmp_path / "src" / "cli").mkdir(parents=True)

        result = resolve_instruction_files(["src/cli/main.py"], str(tmp_path))

        by_path = {r.path: r for r in result}
        assert by_path["src/cli/AGENTS.md"].exists is False
        assert by_path["src/AGENTS.md"].exists is False
        assert by_path["AGENTS.md"].exists is False

    def test_root_agents_md_preloaded_when_it_exists(self, tmp_path: Path) -> None:
        """A repository-root AGENTS.md is preloaded when it exists.

        The walk now descends all the way to index 0, so a root AGENTS.md is
        discovered for any file path provided.
        """
        (tmp_path / ".github").mkdir()
        (tmp_path / "src").mkdir()
        (tmp_path / "AGENTS.md").write_text("# Root agent rules")

        result = resolve_instruction_files(["src/main.py"], str(tmp_path))

        by_path = {r.path: r for r in result}
        assert by_path["AGENTS.md"].exists is True
        assert by_path["AGENTS.md"].content == "# Root agent rules"

    def test_missing_legacy_instruction_file_not_offered(self, tmp_path: Path) -> None:
        """A missing directory-local copilot-instructions.md is never proposed.

        GitHub does not read ``<dir>/copilot-instructions.md``, so offering it as
        a creation target would strand any guidance written there.
        """
        (tmp_path / ".github").mkdir()
        (tmp_path / "src" / "cli").mkdir(parents=True)

        result = resolve_instruction_files(["src/cli/main.py"], str(tmp_path))

        paths = [r.path for r in result]
        assert "src/copilot-instructions.md" not in paths
        assert "src/cli/copilot-instructions.md" not in paths
        # The repository-wide root file is still always included.
        assert ".github/copilot-instructions.md" in paths

    def test_existing_legacy_instruction_file_still_preloaded(self, tmp_path: Path) -> None:
        """An existing legacy file is preloaded so its content stays visible."""
        (tmp_path / ".github").mkdir()
        (tmp_path / "src" / "cli").mkdir(parents=True)
        (tmp_path / "src" / "copilot-instructions.md").write_text("# Legacy")

        result = resolve_instruction_files(["src/cli/main.py"], str(tmp_path))

        by_path = {r.path: r for r in result}
        assert by_path["src/copilot-instructions.md"].exists is True
        assert by_path["src/copilot-instructions.md"].content == "# Legacy"
        assert by_path["src/copilot-instructions.md"].can_update is False

    def test_deduplicates_across_paths(self, tmp_path: Path) -> None:
        """Same instruction file is not included twice."""
        (tmp_path / ".github").mkdir()
        (tmp_path / "src").mkdir()
        src_instructions = tmp_path / "src" / "copilot-instructions.md"
        src_instructions.write_text("# Src instructions")

        result = resolve_instruction_files(
            ["src/file1.py", "src/file2.py"],
            str(tmp_path),
        )

        src_results = [r for r in result if r.path == "src/copilot-instructions.md"]
        assert len(src_results) == 1

    def test_handles_leading_slash(self, tmp_path: Path) -> None:
        """Normalizes leading slash in file paths."""
        (tmp_path / ".github").mkdir()
        result = resolve_instruction_files(["/src/main.py"], str(tmp_path))
        # Should not crash and should include root
        assert len(result) >= 1

    def test_unreadable_file_returns_empty_content(self, tmp_path: Path) -> None:
        """Existing files that fail UTF-8 decoding get empty content."""
        root_dir = tmp_path / ".github"
        root_dir.mkdir()
        root_file = root_dir / "copilot-instructions.md"
        root_file.write_bytes(b"\x80\x81\x82\xff\xfe")

        result = resolve_instruction_files([], str(tmp_path))

        by_path = {entry.path: entry for entry in result}
        assert by_path[".github/copilot-instructions.md"].exists is True
        assert by_path[".github/copilot-instructions.md"].content == ""

    def test_path_with_dotdot_segments_skipped(self, tmp_path: Path) -> None:
        """File paths containing '..' traversal segments are skipped silently."""
        (tmp_path / ".github").mkdir()
        result = resolve_instruction_files(["../../etc/passwd"], str(tmp_path))
        # Only root instruction file should be present; traversal path produces nothing
        paths = [r.path for r in result]
        assert ".github/copilot-instructions.md" in paths
        # No path outside the root should appear
        assert not any(".." in p for p in paths)

    def test_path_with_dotdot_in_middle_skipped(self, tmp_path: Path) -> None:
        """A path like 'src/../../../etc/passwd' is skipped."""
        (tmp_path / ".github").mkdir()
        result = resolve_instruction_files(["src/../../../etc/passwd"], str(tmp_path))
        paths = [r.path for r in result]
        assert not any(".." in p for p in paths)

    def test_add_instruction_file_rejects_path_outside_root(self, tmp_path: Path) -> None:
        """_add_instruction_file skips paths that resolve outside the repo root."""
        from agentic_devtools.cli.audit.instruction_resolver import _add_instruction_file

        # Create a real file outside the tmp repo directory
        outside_dir = tmp_path.parent / "outside"
        outside_dir.mkdir(exist_ok=True)
        (outside_dir / "copilot-instructions.md").write_text("# Leaked")

        repo_root = tmp_path / "repo"
        repo_root.mkdir()

        seen: set[str] = set()
        results: list = []
        # Supply a relative_path that resolves outside repo_root via the parent
        _add_instruction_file("../outside/copilot-instructions.md", repo_root, seen, results)

        # The outside file must not appear in results
        assert all("Leaked" not in (r.content or "") for r in results)

    def test_add_instruction_file_handles_resolve_oserror(self, tmp_path: Path) -> None:
        """_add_instruction_file skips paths when Path.resolve raises OSError."""
        from agentic_devtools.cli.audit.instruction_resolver import _add_instruction_file

        repo_root = tmp_path / "repo"
        repo_root.mkdir()

        seen: set[str] = set()
        results: list = []

        with patch("agentic_devtools.cli.audit.instruction_resolver.Path.resolve", side_effect=OSError("mocked")):
            _add_instruction_file(".github/copilot-instructions.md", repo_root, seen, results)

        # The path should have been skipped due to the OSError
        assert results == []

    def test_add_instruction_file_handles_resolve_valueerror(self, tmp_path: Path) -> None:
        """_add_instruction_file skips paths when Path.resolve raises ValueError."""
        from agentic_devtools.cli.audit.instruction_resolver import _add_instruction_file

        repo_root = tmp_path / "repo"
        repo_root.mkdir()

        seen: set[str] = set()
        results: list = []

        with patch("agentic_devtools.cli.audit.instruction_resolver.Path.resolve", side_effect=ValueError("mocked")):
            _add_instruction_file(".github/copilot-instructions.md", repo_root, seen, results)

        # The path should have been skipped due to the ValueError
        assert results == []

    def test_add_instruction_file_preserves_can_update_for_missing_file(self, tmp_path: Path) -> None:
        """Missing entries preserve explicit can_update metadata."""
        from agentic_devtools.cli.audit.instruction_resolver import _add_instruction_file

        repo_root = tmp_path / "repo"
        repo_root.mkdir()

        seen: set[str] = set()
        results: list = []

        _add_instruction_file("src/AGENTS.md", repo_root, seen, results, can_update=False)

        assert len(results) == 1
        assert results[0].path == "src/AGENTS.md"
        assert results[0].exists is False
        assert results[0].can_update is False


class TestGithubInstructionsLoading:
    """Tests for .github/instructions/*.instructions.md preloading behaviour."""

    def _make_instructions_dir(self, tmp_path: Path) -> Path:
        instr_dir = tmp_path / ".github" / "instructions"
        instr_dir.mkdir(parents=True, exist_ok=True)
        return instr_dir

    def test_matching_instructions_file_is_preloaded(self, tmp_path: Path) -> None:
        """An instructions file whose applyTo glob matches a reviewed path is included."""
        instr_dir = self._make_instructions_dir(tmp_path)
        (instr_dir / "code-review.instructions.md").write_text('---\napplyTo: "**/*.py"\n---\n# Review rules')

        result = resolve_instruction_files(["agentic_devtools/cli/foo.py"], str(tmp_path))

        by_path = {r.path: r for r in result}
        assert ".github/instructions/code-review.instructions.md" in by_path
        assert by_path[".github/instructions/code-review.instructions.md"].content == (
            '---\napplyTo: "**/*.py"\n---\n# Review rules'
        )

    def test_non_matching_instructions_file_is_skipped(self, tmp_path: Path) -> None:
        """An instructions file whose applyTo does not match any reviewed path is omitted."""
        instr_dir = self._make_instructions_dir(tmp_path)
        (instr_dir / "specs.instructions.md").write_text('---\napplyTo: "specs/**"\n---\n# Spec rules')

        result = resolve_instruction_files(["agentic_devtools/cli/foo.py"], str(tmp_path))

        paths = [r.path for r in result]
        assert ".github/instructions/specs.instructions.md" not in paths

    def test_instructions_file_without_apply_to_always_included(self, tmp_path: Path) -> None:
        """An instructions file with no applyTo directive applies to all paths."""
        instr_dir = self._make_instructions_dir(tmp_path)
        (instr_dir / "general.instructions.md").write_text("# No frontmatter")

        result = resolve_instruction_files(["agentic_devtools/cli/foo.py"], str(tmp_path))

        paths = [r.path for r in result]
        assert ".github/instructions/general.instructions.md" in paths

    def test_instructions_file_is_not_offered_for_creation(self, tmp_path: Path) -> None:
        """Preloaded instructions files carry can_update=False."""
        instr_dir = self._make_instructions_dir(tmp_path)
        (instr_dir / "code-review.instructions.md").write_text('---\napplyTo: "**/*.py"\n---\n# Review rules')

        result = resolve_instruction_files(["src/main.py"], str(tmp_path))

        by_path = {r.path: r for r in result}
        assert by_path[".github/instructions/code-review.instructions.md"].can_update is False

    def test_multi_pattern_apply_to_matches_any(self, tmp_path: Path) -> None:
        """Comma-separated applyTo patterns: file is included if any pattern matches."""
        instr_dir = self._make_instructions_dir(tmp_path)
        (instr_dir / "pre-push.instructions.md").write_text(
            '---\napplyTo: ".github/prompts/**,.github/agents/**"\n---\n# Hook rules'
        )

        result = resolve_instruction_files([".github/prompts/my.prompt.md"], str(tmp_path))

        paths = [r.path for r in result]
        assert ".github/instructions/pre-push.instructions.md" in paths

    def test_instructions_not_loaded_when_dir_missing(self, tmp_path: Path) -> None:
        """No error and no extra entries when .github/instructions does not exist."""
        (tmp_path / ".github").mkdir()
        result = resolve_instruction_files(["src/main.py"], str(tmp_path))
        paths = [r.path for r in result]
        assert not any(".instructions.md" in p for p in paths)

    def test_instructions_file_deduplicated(self, tmp_path: Path) -> None:
        """The same instructions file is not included twice for multiple file paths."""
        instr_dir = self._make_instructions_dir(tmp_path)
        (instr_dir / "code-review.instructions.md").write_text('---\napplyTo: "**/*.py"\n---\n# Review rules')

        result = resolve_instruction_files(["agentic_devtools/a.py", "agentic_devtools/b.py"], str(tmp_path))

        matches = [r for r in result if r.path == ".github/instructions/code-review.instructions.md"]
        assert len(matches) == 1

    def test_unreadable_instructions_file_included_with_empty_content(self, tmp_path: Path) -> None:
        """An unreadable instructions file is still included with empty content."""
        instr_dir = self._make_instructions_dir(tmp_path)
        bad = instr_dir / "bad.instructions.md"
        bad.write_bytes(b"\x80\x81\x82\xff")

        result = resolve_instruction_files([], str(tmp_path))

        by_path = {r.path: r for r in result}
        assert ".github/instructions/bad.instructions.md" in by_path
        assert by_path[".github/instructions/bad.instructions.md"].content == ""
        assert by_path[".github/instructions/bad.instructions.md"].can_update is False

    def test_symlink_outside_repo_is_skipped(self, tmp_path: Path) -> None:
        """A symlink in the instructions dir pointing outside the repo root is never read.

        The confinement check must happen *before* read_text() so that a target such as
        ``/dev/zero`` cannot hang the runner and so that secrets outside the checkout
        cannot be included in audit output.
        """
        # Create a file outside the repo that should never be read
        secret_file = tmp_path / "outside_secret.md"
        secret_file.write_text("SECRET_CONTENT")

        repo_root = tmp_path / "repo"
        instructions_dir = repo_root / ".github" / "instructions"
        instructions_dir.mkdir(parents=True)

        # Symlink inside the instructions dir pointing to the outside file
        symlink = instructions_dir / "evil.instructions.md"
        symlink.symlink_to(secret_file)

        read_text_calls: list[Path] = []
        original_read_text = Path.read_text

        def tracking_read_text(self: Path, *args: object, **kwargs: object) -> str:
            read_text_calls.append(self)
            return original_read_text(self, *args, **kwargs)  # type: ignore[arg-type]

        with patch.object(Path, "read_text", tracking_read_text):
            result = resolve_instruction_files(["any/file.py"], str(repo_root))

        # The symlink target must never have been opened, regardless of content checks
        assert symlink not in read_text_calls, (
            "read_text() was called on the out-of-repo symlink before the confinement check"
        )
        contents = " ".join(r.content for r in result)
        paths = [r.path for r in result]
        assert "SECRET_CONTENT" not in contents
        assert ".github/instructions/evil.instructions.md" not in paths

    def test_resolve_oserror_in_confinement_check_skips_entry(self, tmp_path: Path) -> None:
        """An OSError raised during Path.resolve() in the confinement check skips that entry."""
        instr_dir = self._make_instructions_dir(tmp_path)
        (instr_dir / "python.instructions.md").write_text('---\napplyTo: "**/*.py"\n---\n# Python\n')

        original_resolve = Path.resolve

        def patched_resolve(self: Path, *, strict: bool = False) -> Path:  # type: ignore[override]
            if self.name == "python.instructions.md":
                raise OSError("mocked resolve error")
            return original_resolve(self, strict=strict)

        with patch.object(Path, "resolve", patched_resolve):
            result = resolve_instruction_files(["agentic_devtools/cli/audit/apply.py"], str(tmp_path))

        paths = [r.path for r in result]
        assert ".github/instructions/python.instructions.md" not in paths
