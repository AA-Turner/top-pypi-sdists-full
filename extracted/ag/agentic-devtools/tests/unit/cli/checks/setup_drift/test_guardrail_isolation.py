"""Tests for setup-expectations guardrail isolation (FR-001, FR-002, FR-006)."""

from __future__ import annotations

import re
from pathlib import Path


class TestSetupExpectationsGuardrailIsolation:
    """Verify instruction file exists and scope remains isolated."""

    _REPO_ROOT = Path(__file__).resolve().parents[5]

    def test_instruction_file_exists(self) -> None:
        """The setup-expectations instruction file exists (FR-001)."""
        path = self._REPO_ROOT / ".github" / "instructions" / "setup-expectations.instructions.md"
        assert path.is_file(), f"Missing instruction file: {path}"

    def test_instruction_apply_to_matches_spec(self) -> None:
        """The applyTo glob matches the exact FR-002 path list — no more, no less."""
        path = self._REPO_ROOT / ".github" / "instructions" / "setup-expectations.instructions.md"
        content = path.read_text(encoding="utf-8")

        match = re.search(r'^applyTo:\s*"([^"]+)"', content, re.MULTILINE)
        assert match, "Missing applyTo directive in instruction file frontmatter"
        actual_patterns = {p.strip() for p in match.group(1).split(",")}

        expected_patterns = {
            "agentic_devtools/cli/setup/**",
            "agentic_devtools/skill_injector.py",
            "agentic_devtools/cli/setup/script_generators/**",
            "docs/setup-expectations/**",
        }
        assert actual_patterns == expected_patterns, (
            f"applyTo patterns do not exactly match FR-002 spec.\n"
            f"  Extra patterns: {actual_patterns - expected_patterns}\n"
            f"  Missing patterns: {expected_patterns - actual_patterns}"
        )

    def test_workflow_expectations_not_widened(self) -> None:
        """workflow-expectations.instructions.md is NOT widened with setup paths (FR-006, SC-004)."""
        path = self._REPO_ROOT / ".github" / "instructions" / "workflow-expectations.instructions.md"
        assert path.is_file(), "workflow-expectations instruction file must exist"
        content = path.read_text(encoding="utf-8")

        # These setup-specific paths must NOT appear in the workflow-expectations file
        forbidden = [
            "agentic_devtools/cli/setup/**",
            "agentic_devtools/cli/setup/script_generators/**",
            "agentic_devtools/skill_injector.py",
            "docs/setup-expectations/**",
        ]
        for pattern in forbidden:
            assert pattern not in content, (
                f"workflow-expectations.instructions.md must not contain setup path: {pattern}"
            )
