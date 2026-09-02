"""Tests for validate_skill_classification orchestrator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from agentic_devtools.cli.checks.skill_classification import (
    validate_skill_classification,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_skill_file(
    tmp_path: Path,
    rel_path: str,
    *,
    agdt_block: dict[str, Any] | None = None,
    raw_content: str | None = None,
) -> None:
    """Create a skill file under tmp_path with optional frontmatter."""
    full = tmp_path / rel_path
    full.parent.mkdir(parents=True, exist_ok=True)
    if raw_content is not None:
        full.write_text(raw_content, encoding="utf-8")
        return
    if agdt_block is not None:
        import yaml

        fm = yaml.dump({"agdt": agdt_block}, default_flow_style=False)
        full.write_text(f"---\n{fm}---\n# Skill\n", encoding="utf-8")
    else:
        full.write_text("---\ndescription: test\n---\n# Skill\n", encoding="utf-8")


def _write_fixture(tmp_path: Path, data: dict[str, Any]) -> Path:
    fixture = tmp_path / "fixture.json"
    fixture.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return fixture


# ---------------------------------------------------------------------------
# US1: Unregistered file detection (FR-003)
# ---------------------------------------------------------------------------


class TestUnregisteredFiles:
    """Files on disk but absent from fixture are reported as unregistered."""

    def test_single_unregistered_file(self, tmp_path: Path) -> None:
        _make_skill_file(tmp_path, ".github/agents/agdt.new-skill.agent.md")
        fixture = _write_fixture(tmp_path, {})
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert ".github/agents/agdt.new-skill.agent.md" in result.unregistered_files

    def test_multiple_unregistered_files(self, tmp_path: Path) -> None:
        _make_skill_file(tmp_path, ".github/agents/agdt.a.agent.md")
        _make_skill_file(tmp_path, ".github/agents/agdt.b.agent.md")
        _make_skill_file(tmp_path, ".github/prompts/agdt.c.prompt.md")
        fixture = _write_fixture(tmp_path, {})
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.unregistered_files) == 3


# ---------------------------------------------------------------------------
# US1: Success case (FR-006)
# ---------------------------------------------------------------------------


class TestSuccessCase:
    """All files present with correct buckets → is_valid=True."""

    def test_all_files_match(self, tmp_path: Path) -> None:
        _make_skill_file(tmp_path, ".github/agents/agdt.foo.agent.md")
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.foo.agent.md": {}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert result.is_valid
        assert result.validated_count == 1

    def test_empty_fixture_empty_repo(self, tmp_path: Path) -> None:
        (tmp_path / ".github" / "agents").mkdir(parents=True)
        (tmp_path / ".github" / "prompts").mkdir(parents=True)
        fixture = _write_fixture(tmp_path, {})
        result = validate_skill_classification(tmp_path, fixture)
        assert result.is_valid
        assert result.validated_count == 0


# ---------------------------------------------------------------------------
# US2: Bucket mismatch detection (FR-004)
# ---------------------------------------------------------------------------


class TestBucketMismatches:
    """Normalized classification ≠ fixture value → mismatch reported."""

    def test_single_mismatch(self, tmp_path: Path) -> None:
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.x.agent.md",
            agdt_block={"always": True},
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.x.agent.md": {"requires": {"issue_adapter": "jira"}}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.mismatches) == 1
        assert result.mismatches[0].file == ".github/agents/agdt.x.agent.md"
        assert result.mismatches[0].actual == {"always": True}

    def test_multiple_mismatches(self, tmp_path: Path) -> None:
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.a.agent.md",
            agdt_block={"always": True},
        )
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.b.agent.md",
            agdt_block={"requires": {"issue_adapter": "jira"}},
        )
        fixture = _write_fixture(
            tmp_path,
            {
                ".github/agents/agdt.a.agent.md": {},
                ".github/agents/agdt.b.agent.md": {"always": True},
            },
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.mismatches) == 2

    def test_always_true_with_requires_normalizes_to_always(self, tmp_path: Path) -> None:
        """always: true + requires block normalizes to {"always": true}, no false mismatch."""
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.both.agent.md",
            agdt_block={"always": True, "requires": {"issue_adapter": "jira"}},
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.both.agent.md": {"always": True}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert result.is_valid


# ---------------------------------------------------------------------------
# US5: Parse warning detection (FR-010)
# ---------------------------------------------------------------------------


class TestParseWarnings:
    """Warnings from parse_classification are treated as errors."""

    def test_invalid_axis_triggers_warning(self, tmp_path: Path) -> None:
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.w.agent.md",
            agdt_block={"requires": {"issue_adapter": "invalid_value"}},
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.w.agent.md": {}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.parse_warnings) >= 1
        assert result.parse_warnings[0].file == ".github/agents/agdt.w.agent.md"

    def test_valid_axis_not_flagged_with_invalid_sibling(self, tmp_path: Path) -> None:
        """Only the invalid axis triggers a warning, not the valid one."""
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.mixed.agent.md",
            agdt_block={"requires": {"issue_adapter": "jira", "code_hosting": "invalid"}},
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.mixed.agent.md": {"requires": {"issue_adapter": "jira"}}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.parse_warnings) >= 1
        # The warning is about code_hosting, not issue_adapter.
        assert any("code_hosting" in w.message for w in result.parse_warnings)

    def test_repeated_warnings_captured(self, tmp_path: Path) -> None:
        """simplefilter('always') captures repeated warnings from same location."""
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.r1.agent.md",
            agdt_block={"requires": {"issue_adapter": "bad1"}},
        )
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.r2.agent.md",
            agdt_block={"requires": {"issue_adapter": "bad2"}},
        )
        fixture = _write_fixture(
            tmp_path,
            {
                ".github/agents/agdt.r1.agent.md": {},
                ".github/agents/agdt.r2.agent.md": {},
            },
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.parse_warnings) >= 2


# ---------------------------------------------------------------------------
# US3: Orphan fixture entries (FR-005)
# ---------------------------------------------------------------------------


class TestOrphanEntries:
    """Fixture entries for non-existent files are reported as orphans."""

    def test_single_orphan(self, tmp_path: Path) -> None:
        (tmp_path / ".github" / "agents").mkdir(parents=True)
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.deleted.agent.md": {}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert ".github/agents/agdt.deleted.agent.md" in result.orphan_entries

    def test_multiple_orphans(self, tmp_path: Path) -> None:
        (tmp_path / ".github" / "agents").mkdir(parents=True)
        fixture = _write_fixture(
            tmp_path,
            {
                ".github/agents/agdt.gone1.agent.md": {},
                ".github/agents/agdt.gone2.agent.md": {},
                ".github/prompts/agdt.gone3.prompt.md": {},
            },
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.orphan_entries) == 3


# ---------------------------------------------------------------------------
# Parse error detection (FR-009)
# ---------------------------------------------------------------------------


class TestParseErrors:
    """Unparseable YAML frontmatter is reported as a parse error."""

    def test_invalid_yaml_reported(self, tmp_path: Path) -> None:
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.bad.agent.md",
            raw_content="---\n: :\n  - invalid: yaml: here: [\n---\n",
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.bad.agent.md": {}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.parse_errors) == 1
        assert result.parse_errors[0].file == ".github/agents/agdt.bad.agent.md"

    def test_non_utf8_file_reported_as_parse_error(self, tmp_path: Path) -> None:
        """Non-UTF-8 files raise UnicodeDecodeError, reported as parse errors."""
        rel = ".github/agents/agdt.binary.agent.md"
        full = tmp_path / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        # Write bytes that are invalid in UTF-8.
        full.write_bytes(b"---\ndescription: \xff\xfe invalid\n---\n")
        fixture = _write_fixture(tmp_path, {rel: {}})
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.parse_errors) == 1
        assert result.parse_errors[0].file == rel


# ---------------------------------------------------------------------------
# No frontmatter (FR-001)
# ---------------------------------------------------------------------------


class TestNoFrontmatter:
    """File with no YAML frontmatter parses as unrestricted {}."""

    def test_no_frontmatter_is_unrestricted(self, tmp_path: Path) -> None:
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.plain.agent.md",
            raw_content="# Plain skill\nNo frontmatter here.\n",
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.plain.agent.md": {}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert result.is_valid


# ---------------------------------------------------------------------------
# Combined violations (FR-003, FR-004, FR-005, FR-010)
# ---------------------------------------------------------------------------


class TestFrontmatterEdgeCases:
    """Edge cases in YAML frontmatter parsing."""

    def test_missing_closing_delimiter(self, tmp_path: Path) -> None:
        """Frontmatter without closing --- is treated as no frontmatter."""
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.noclose.agent.md",
            raw_content="---\nagdt:\n  always: true\n# No closing\n",
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.noclose.agent.md": {}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert result.is_valid

    def test_empty_frontmatter_block(self, tmp_path: Path) -> None:
        """Frontmatter with only whitespace between delimiters."""
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.empty.agent.md",
            raw_content="---\n   \n---\n# Content\n",
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.empty.agent.md": {}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert result.is_valid

    def test_non_dict_yaml_result(self, tmp_path: Path) -> None:
        """YAML that parses to a non-dict (e.g. a string) is treated as empty."""
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.str.agent.md",
            raw_content="---\njust a string\n---\n# Content\n",
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.str.agent.md": {}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert result.is_valid

    def test_code_hosting_only_requires(self, tmp_path: Path) -> None:
        """File requiring only code_hosting normalizes correctly."""
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.ch.agent.md",
            agdt_block={"requires": {"code_hosting": "github"}},
        )
        fixture = _write_fixture(
            tmp_path,
            {".github/agents/agdt.ch.agent.md": {"requires": {"code_hosting": "github"}}},
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert result.is_valid


class TestFixtureEdgeCases:
    """Edge cases in fixture loading."""

    def test_non_dict_fixture_raises(self, tmp_path: Path) -> None:
        """Fixture that is a JSON array raises ValueError."""
        (tmp_path / ".github" / "agents").mkdir(parents=True)
        fixture = tmp_path / "fixture.json"
        fixture.write_text("[]", encoding="utf-8")
        with pytest.raises(ValueError, match="JSON object"):
            validate_skill_classification(tmp_path, fixture)


class TestCombinedViolations:
    """Multiple violation types in a single run are all reported."""

    def test_all_violation_types_together(self, tmp_path: Path) -> None:
        # Unregistered file.
        _make_skill_file(tmp_path, ".github/agents/agdt.unreg.agent.md")
        # Mismatch.
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.mm.agent.md",
            agdt_block={"always": True},
        )
        # Parse warning (invalid axis value).
        _make_skill_file(
            tmp_path,
            ".github/agents/agdt.pw.agent.md",
            agdt_block={"requires": {"issue_adapter": "nope"}},
        )
        fixture = _write_fixture(
            tmp_path,
            {
                ".github/agents/agdt.mm.agent.md": {},
                ".github/agents/agdt.pw.agent.md": {},
                ".github/agents/agdt.orphan.agent.md": {},
            },
        )
        result = validate_skill_classification(tmp_path, fixture)
        assert not result.is_valid
        assert len(result.unregistered_files) >= 1
        assert len(result.mismatches) >= 1
        assert len(result.orphan_entries) >= 1
        assert len(result.parse_warnings) >= 1
