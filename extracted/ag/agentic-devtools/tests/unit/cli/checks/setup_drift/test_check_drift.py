"""Tests for check_drift pure function."""

from __future__ import annotations

from agentic_devtools.cli.checks.setup_drift import check_drift


class TestCheckDrift:
    """Tests for the check_drift pure function."""

    # --- Negative: setup-source-only changes → fail (SC-001, FR-003) ---

    def test_setup_source_only_fails(self) -> None:
        """Setup source change without doc update fails."""
        result = check_drift(["agentic_devtools/cli/setup/commands.py"])
        assert not result.passed
        assert "agentic_devtools/cli/setup/commands.py" in result.triggering_files
        assert result.message

    def test_skill_injector_only_fails(self) -> None:
        """skill_injector.py change without doc update fails (FR-003)."""
        result = check_drift(["agentic_devtools/skill_injector.py"])
        assert not result.passed
        assert "agentic_devtools/skill_injector.py" in result.triggering_files

    def test_script_generators_only_fails(self) -> None:
        """script_generators change without doc update fails."""
        result = check_drift(["agentic_devtools/cli/setup/script_generators/bash.py"])
        assert not result.passed
        assert "agentic_devtools/cli/setup/script_generators/bash.py" in result.triggering_files

    def test_multiple_setup_sources_fails(self) -> None:
        """Multiple setup source files without doc update fails."""
        files = [
            "agentic_devtools/cli/setup/commands.py",
            "agentic_devtools/skill_injector.py",
        ]
        result = check_drift(files)
        assert not result.passed
        assert len(result.triggering_files) == 2

    # --- Happy path: setup-source + doc changes → pass (SC-002, FR-004) ---

    def test_source_plus_doc_passes(self) -> None:
        """Setup source + doc change passes."""
        files = [
            "agentic_devtools/cli/setup/commands.py",
            "docs/setup-expectations/README.md",
        ]
        result = check_drift(files)
        assert result.passed
        assert not result.triggering_files

    def test_multiple_sources_one_doc_passes(self) -> None:
        """Multiple setup files with one doc change passes (FR-004)."""
        files = [
            "agentic_devtools/cli/setup/commands.py",
            "agentic_devtools/skill_injector.py",
            "agentic_devtools/cli/setup/script_generators/bash.py",
            "docs/setup-expectations/agdt-setup.md",
        ]
        result = check_drift(files)
        assert result.passed

    # --- Happy path: doc-only changes → pass (SC-003, FR-005) ---

    def test_doc_only_passes(self) -> None:
        """Doc-only changes under docs/setup-expectations/ pass."""
        result = check_drift(["docs/setup-expectations/README.md"])
        assert result.passed

    def test_multiple_docs_only_passes(self) -> None:
        """Multiple doc-only changes pass."""
        files = [
            "docs/setup-expectations/README.md",
            "docs/setup-expectations/agdt-setup.md",
        ]
        result = check_drift(files)
        assert result.passed

    # --- Happy path: unrelated files only → pass (SC-005, FR-007) ---

    def test_unrelated_only_passes(self) -> None:
        """Unrelated files only pass with empty triggering_files."""
        result = check_drift(["tests/test_something.py", "README.md"])
        assert result.passed
        assert result.triggering_files == []

    # --- Edge cases ---

    def test_empty_file_list_passes(self) -> None:
        """Empty file list passes (FR-007)."""
        result = check_drift([])
        assert result.passed
        assert result.triggering_files == []

    def test_path_with_leading_dot_slash(self) -> None:
        """Leading ./ is stripped before matching."""
        result = check_drift(["./agentic_devtools/cli/setup/commands.py"])
        assert not result.passed
        assert "agentic_devtools/cli/setup/commands.py" in result.triggering_files

    def test_path_with_backslashes(self) -> None:
        """Backslashes are normalized to forward slashes."""
        result = check_drift(["agentic_devtools\\cli\\setup\\commands.py"])
        assert not result.passed
        assert "agentic_devtools/cli/setup/commands.py" in result.triggering_files

    def test_duplicate_paths_deduplicated(self) -> None:
        """Duplicate paths are deduplicated."""
        files = [
            "agentic_devtools/cli/setup/commands.py",
            "agentic_devtools/cli/setup/commands.py",
        ]
        result = check_drift(files)
        assert not result.passed
        assert len(result.triggering_files) == 1

    def test_doc_with_leading_dot_slash_passes(self) -> None:
        """Doc path with leading ./ still recognized as doc."""
        files = [
            "agentic_devtools/cli/setup/commands.py",
            "./docs/setup-expectations/README.md",
        ]
        result = check_drift(files)
        assert result.passed

    def test_mixed_unrelated_and_source_fails(self) -> None:
        """Unrelated files mixed with setup source (no doc) still fails."""
        files = [
            "tests/test_something.py",
            "agentic_devtools/cli/setup/exit_codes.py",
        ]
        result = check_drift(files)
        assert not result.passed

    def test_nested_setup_file_matches_glob(self) -> None:
        """Deeply nested file under setup/ matches the ** glob."""
        result = check_drift(["agentic_devtools/cli/setup/deep/nested/module.py"])
        assert not result.passed

    def test_failure_message_identifies_files(self) -> None:
        """Failure message lists the triggering files (NFR-002)."""
        result = check_drift(["agentic_devtools/cli/setup/commands.py"])
        assert not result.passed
        assert "agentic_devtools/cli/setup/commands.py" in result.message
        assert "docs/setup-expectations/" in result.message
