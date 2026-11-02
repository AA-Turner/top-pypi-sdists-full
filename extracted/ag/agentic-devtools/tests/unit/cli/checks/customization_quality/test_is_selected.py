"""Tests for the selection predicate ``is_selected``."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.checks.customization_quality import is_selected


class TestIsSelected:
    @pytest.mark.parametrize(
        "path",
        [
            ".agents/skills/demo/SKILL.md",
            ".github/instructions/python.instructions.md",
            "docs/agent-customization/authoring-standard.md",
            "./docs/agent-customization/nested/deep.md",
        ],
    )
    def test_accepts_the_canonical_tree(self, path: str) -> None:
        """Markdown files under the three canonical roots are selected."""
        assert is_selected(path) is True

    @pytest.mark.parametrize(
        "path",
        [
            ".github/agents/agdt.some.agent.md",
            ".github/prompts/agdt.some.prompt.md",
            ".github/copilot-instructions.md",
        ],
    )
    def test_rejects_the_legacy_corpus_by_name(self, path: str) -> None:
        """The legacy corpus is excluded because it is scheduled for deletion."""
        assert is_selected(path) is False

    def test_rejects_non_markdown_files(self) -> None:
        """Only Markdown files carry authoring rules."""
        assert is_selected(".github/instructions/helper.py") is False

    def test_rejects_paths_outside_the_selected_roots(self) -> None:
        """A Markdown file elsewhere in the repository is not selected."""
        assert is_selected("docs/other/readme.md") is False

    def test_rejects_a_root_itself(self) -> None:
        """A path equal to a root (no child segment) is not a selected file."""
        assert is_selected("docs/agent-customization") is False

    def test_rejects_a_path_containing_parent_traversal(self) -> None:
        """Traversal segments must be rejected before the prefix check."""
        assert is_selected(".agents/skills/../../README.md") is False
