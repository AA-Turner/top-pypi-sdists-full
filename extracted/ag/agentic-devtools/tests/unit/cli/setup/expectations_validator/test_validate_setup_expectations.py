"""Tests for expectations_validator module."""

from pathlib import Path

from agentic_devtools.cli.setup.expectations_validator import validate_expectations

# Helper: the full exit-code table matching the new ExitCode enum
_FULL_EXIT_TABLE = (
    "| Code | Name | Description |\n"
    "|------|------|-------------|\n"
    "| 0 | OK | OK |\n"
    "| 1 | WARNINGS | Warnings |\n"
    "| 2 | MISSING_REQUIRED_DEP | Missing |\n"
    "| 3 | VERSION_BLOCKED | Blocked |\n"
    "| 4 | UPGRADED_RERUN_NEEDED | Rerun |\n"
    "| 5 | REPO_MUTATION_FAILED | Mutation |\n"
    "| 6 | AUTORUN_FAILED | Internal |\n"
)

_PHASES_SECTION = (
    "## Phases\n\n"
    "1. `version_check`\n"
    "2. `certificate_prefetch`\n"
    "3. `cli_installation`\n"
    "4. `dependency_check`\n"
    "5. `environment_persistence`\n"
    "6. `file_modifications`\n"
    "7. `autorun_setup`\n\n"
)

_MERMAID = "```mermaid\nflowchart TD\n  A-->B\n```\n"


class TestValidateSetupExpectations:
    """Covers happy path and 5 drift types."""

    def test_happy_path_passes(self) -> None:
        """Doc matches source → validation passes."""
        result = validate_expectations()
        assert result.passed, f"Expected pass but got errors: {result.errors}"

    def test_code_added_not_in_doc(self, tmp_path: Path) -> None:
        """A new exit code in source not documented → fails."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        # Write doc missing AUTORUN_FAILED
        doc.write_text(
            _PHASES_SECTION
            + "## Exit Codes\n\n"
            + "| Code | Name | Description |\n"
            + "|------|------|-------------|\n"
            + "| 0 | OK | OK |\n"
            + "| 1 | WARNINGS | Warnings |\n"
            + "| 2 | MISSING_REQUIRED_DEP | Missing |\n"
            + "| 3 | VERSION_BLOCKED | Blocked |\n"
            + "| 4 | UPGRADED_RERUN_NEEDED | Rerun |\n"
            + "| 5 | REPO_MUTATION_FAILED | Mutation |\n\n"
            + "## Report Schema\n\nSchema here.\n\n"
            + _MERMAID,
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("AUTORUN_FAILED" in e for e in result.errors)

    def test_phase_added_not_in_doc(self, tmp_path: Path) -> None:
        """Source has a phase not listed in doc → fails."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        # Write doc missing file_modifications phase
        doc.write_text(
            "## Phases\n\n"
            "1. `version_check`\n"
            "2. `certificate_prefetch`\n"
            "3. `cli_installation`\n"
            "4. `dependency_check`\n"
            "5. `environment_persistence`\n\n"
            "## Exit Codes\n\n" + _FULL_EXIT_TABLE + "\n## Report Schema\n\nSchema here.\n\n" + _MERMAID,
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("file_modifications" in e for e in result.errors)

    def test_doc_lists_nonexistent_code(self, tmp_path: Path) -> None:
        """Doc contains an exit code not in source → fails."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        doc.write_text(
            _PHASES_SECTION
            + "## Exit Codes\n\n"
            + _FULL_EXIT_TABLE
            + "| 50 | FAKE_CODE | Fake |\n\n"
            + "## Report Schema\n\nSchema here.\n\n"
            + _MERMAID,
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("FAKE_CODE" in e for e in result.errors)

    def test_phases_wrong_order(self, tmp_path: Path) -> None:
        """Phases in wrong order → fails."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        # Swap version_check and certificate_prefetch
        doc.write_text(
            "## Phases\n\n"
            "1. `certificate_prefetch`\n"
            "2. `version_check`\n"
            "3. `cli_installation`\n"
            "4. `dependency_check`\n"
            "5. `environment_persistence`\n"
            "6. `file_modifications`\n"
            "7. `autorun_setup`\n\n"
            "## Exit Codes\n\n" + _FULL_EXIT_TABLE + "\n## Report Schema\n\nSchema here.\n\n" + _MERMAID,
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("order" in e.lower() for e in result.errors)

    def test_required_section_missing(self, tmp_path: Path) -> None:
        """Missing Mermaid block → fails."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        doc.write_text(
            _PHASES_SECTION + "## Exit Codes\n\n" + _FULL_EXIT_TABLE + "\n## Report Schema\n\nSchema here.\n",
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("mermaid" in e.lower() or "Mermaid" in e for e in result.errors)

    def test_missing_doc_file(self, tmp_path: Path) -> None:
        """Missing expectations document → fails."""
        (tmp_path / ".git").mkdir()
        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("not found" in e for e in result.errors)

    def test_repo_root_auto_detect_fails(self, tmp_path: Path, monkeypatch: object) -> None:
        """When _find_repo_root returns None, validation fails with clear message."""
        monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]

        result = validate_expectations(repo_root=None)
        assert not result.passed
        assert any("repository root" in e.lower() or ".git" in e.lower() for e in result.errors)

    def test_missing_phases_section(self, tmp_path: Path) -> None:
        """Doc without ## Phases section → fails."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        doc.write_text(
            "## Exit Codes\n\n" + _FULL_EXIT_TABLE + "\n## Report Schema\n\nSchema here.\n\n" + _MERMAID,
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("## Phases" in e for e in result.errors)

    def test_missing_report_schema_section(self, tmp_path: Path) -> None:
        """Doc without ## Report Schema section → fails."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        doc.write_text(
            _PHASES_SECTION + "## Exit Codes\n\n" + _FULL_EXIT_TABLE + "\n" + _MERMAID,
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("Report Schema" in e for e in result.errors)

    def test_missing_exit_codes_section(self, tmp_path: Path) -> None:
        """Doc without ## Exit Codes section → fails with a clear section-level error."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        doc.write_text(
            _PHASES_SECTION + "## Report Schema\n\nSchema here.\n\n" + _MERMAID,
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("## Exit Codes" in e for e in result.errors)

    def test_exit_code_value_mismatch(self, tmp_path: Path) -> None:
        """Exit code with wrong numeric value → fails (covers missing_from_doc=empty branch)."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        # All source codes present, but VERSION_BLOCKED has wrong value (10 vs 3).
        doc.write_text(
            _PHASES_SECTION
            + "## Exit Codes\n\n"
            + "| Code | Name | Description |\n"
            + "|------|------|-------------|\n"
            + "| 0 | OK | OK |\n"
            + "| 1 | WARNINGS | Warnings |\n"
            + "| 2 | MISSING_REQUIRED_DEP | Missing |\n"
            + "| 10 | VERSION_BLOCKED | Blocked |\n"
            + "| 4 | UPGRADED_RERUN_NEEDED | Rerun |\n"
            + "| 5 | REPO_MUTATION_FAILED | Mutation |\n"
            + "| 6 | AUTORUN_FAILED | Internal |\n\n"
            + "## Report Schema\n\nSchema here.\n\n"
            + _MERMAID,
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("mismatch" in e.lower() and "VERSION_BLOCKED" in e for e in result.errors)

    def test_doc_has_extra_phases(self, tmp_path: Path) -> None:
        """Doc lists a phase not in source → fails."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        doc.write_text(
            "## Phases\n\n"
            "1. `version_check`\n"
            "2. `certificate_prefetch`\n"
            "3. `cli_installation`\n"
            "4. `dependency_check`\n"
            "5. `environment_persistence`\n"
            "6. `file_modifications`\n"
            "7. `autorun_setup`\n"
            "8. `fake_phase`\n\n"
            "## Exit Codes\n\n" + _FULL_EXIT_TABLE + "\n## Report Schema\n\nSchema here.\n\n" + _MERMAID,
            encoding="utf-8",
        )
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
        assert any("fake_phase" in e for e in result.errors)

    def test_empty_doc_content(self, tmp_path: Path) -> None:
        """Empty doc content → returns empty phase/code lists and fails."""
        doc = tmp_path / "docs" / "setup-expectations" / "agdt-setup.md"
        doc.parent.mkdir(parents=True)
        doc.write_text("# Some Title\n\nNo relevant sections.\n", encoding="utf-8")
        (tmp_path / ".git").mkdir()

        result = validate_expectations(repo_root=tmp_path)
        assert not result.passed
