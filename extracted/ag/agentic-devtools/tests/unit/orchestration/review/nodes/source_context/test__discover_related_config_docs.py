"""Tests for _discover_related_config_docs helper."""

from __future__ import annotations

from agentic_devtools.orchestration.review.nodes.source_context import _discover_related_config_docs


class TestDiscoverRelatedConfigDocs:
    """Tests for _discover_related_config_docs."""

    def test_blank_or_config_doc_source_returns_empty(self) -> None:
        """Blank paths and config/doc files do not discover related config/doc context."""
        assert _discover_related_config_docs("", [{"path": "/README.md"}]) == []
        assert _discover_related_config_docs("/README.md", [{"path": "/pyproject.toml"}]) == []

    def test_same_dir_and_ancestor_readme_and_root_config_are_included(self) -> None:
        """Nearby README files and repo-root config files are considered related."""
        related = _discover_related_config_docs(
            "/agentic_devtools/orchestration/review/nodes/source_context.py",
            [
                {"path": "/agentic_devtools/orchestration/review/nodes/notes.md"},
                {"path": "/agentic_devtools/orchestration/review/README.md"},
                {"path": "/pyproject.toml"},
                {"path": "/specs/1888-implement-source-context-retrieval/plan.md"},
            ],
        )

        assert related == [
            "agentic_devtools/orchestration/review/README.md",
            "agentic_devtools/orchestration/review/nodes/notes.md",
            "pyproject.toml",
        ]

    def test_non_string_candidates_and_unrelated_docs_are_ignored(self) -> None:
        """Invalid candidate values and unrelated docs are skipped safely."""
        related = _discover_related_config_docs(
            "/agentic_devtools/state.py",
            [
                {"path": None},
                {"path": 123},
                {"path": "/docs/setup.md"},
            ],
        )

        assert related == []
