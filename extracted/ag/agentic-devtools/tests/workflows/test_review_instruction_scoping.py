"""Guardrail tests for Copilot code review instruction files.

Verifies that the repo-wide review instruction file keeps its repository-wide
`applyTo: "**"` scope — it is the single source of the review prohibition and focus
lists, so narrowing it would strip YAML and Markdown changes of that guidance — and
that the `specs/**` instruction file carries the markdown prohibitions forward, so the
two files stack without conflicting.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTRUCTIONS_DIR = REPO_ROOT / ".github" / "instructions"
CODE_REVIEW_INSTRUCTIONS = INSTRUCTIONS_DIR / "code-review.instructions.md"
SPECS_INSTRUCTIONS = INSTRUCTIONS_DIR / "specs.instructions.md"


def _frontmatter_block(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.DOTALL)
    assert match, f"Missing opening frontmatter block in {path.name}"
    return match.group(1)


def _apply_to_patterns(path: Path) -> set[str]:
    match = re.search(r'^applyTo:\s*"([^"]+)"', _frontmatter_block(path), re.MULTILINE)
    assert match, f"Missing applyTo directive in frontmatter of {path.name}"
    return {pattern.strip() for pattern in match.group(1).split(",")}


class TestReviewInstructionScoping:
    """The review instruction files stack: repo-wide rules plus `specs/**` overrides."""

    def test_code_review_instructions_are_scoped_repo_wide(self) -> None:
        assert _apply_to_patterns(CODE_REVIEW_INSTRUCTIONS) == {"**"}

    def test_specs_instructions_exist_and_are_scoped_to_specs(self) -> None:
        assert SPECS_INSTRUCTIONS.is_file(), f"Missing instruction file: {SPECS_INSTRUCTIONS}"
        assert _apply_to_patterns(SPECS_INSTRUCTIONS) == {"specs/**"}

    def test_specs_instructions_carry_markdown_prohibitions_forward(self) -> None:
        content = SPECS_INSTRUCTIONS.read_text(encoding="utf-8").lower()
        assert "must not comment on" in content
        for expected in ("markdownlint", "md013", "formatting"):
            assert expected in content, f"specs instructions must retain the {expected} prohibition"

    def test_specs_instructions_avoid_unsupported_directives(self) -> None:
        """Copilot does not support vague-quality or output-shape/UX directives."""
        content = SPECS_INSTRUCTIONS.read_text(encoding="utf-8").lower()
        for forbidden in ("don't miss any issues", "do not miss any issues"):
            assert forbidden not in content
        # No numeric per-document finding caps (e.g. "at most 5 comments per document").
        assert not re.search(r"\b(?:at most|no more than|maximum of|max)\s+\d+\s+\w*\s*(?:comments|findings)", content)
