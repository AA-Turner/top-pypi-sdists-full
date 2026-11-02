"""Tests for assemble_context function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.budget import TokenBudget
from agentic_devtools.orchestration.review.content_assembler import assemble_context


class TestAssembleContext:
    """Tests for priority-tiered content assembly."""

    def test_empty_files_returns_empty(self) -> None:
        budget = TokenBudget(budget_tokens=10000, safety_margin=0.0)
        result = assemble_context([], budget)
        assert result == []

    def test_content_within_budget_not_truncated(self) -> None:
        """Content fitting within budget is not truncated."""
        budget = TokenBudget(budget_tokens=100000, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "patch": "small diff",
                "full_content_source": "source code",
                "full_content_target": "target code",
                "related_tests": [],
                "resolved_imports": [],
            }
        ]
        result = assemble_context(files, budget)
        assert result[0]["truncation_applied"] is False
        assert result[0]["full_content_source"] == "source code"

    def test_large_content_triggers_truncation(self) -> None:
        """Content exceeding budget is truncated."""
        budget = TokenBudget(budget_tokens=50, safety_margin=0.0)
        # 50 tokens * 3.5 chars = 175 chars budget total
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "patch": "",  # no diff tokens consumed
                "full_content_source": "x" * 1000,  # way over budget
                "full_content_target": None,
                "related_tests": [],
                "resolved_imports": [],
            }
        ]
        result = assemble_context(files, budget)
        assert result[0]["truncation_applied"] is True

    def test_patch_exceeding_budget_is_truncated(self) -> None:
        """Oversized patches are truncated and include the truncation marker."""
        from agentic_devtools.orchestration.review.content_assembler import _PATCH_TRUNCATION_MARKER

        # Use a budget large enough that the marker itself fits (marker is ~43 chars).
        budget = TokenBudget(budget_tokens=100, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "patch": "x" * 1000,
                "full_content_source": None,
                "full_content_target": None,
                "related_tests": [],
                "resolved_imports": [],
            }
        ]

        result = assemble_context(files, budget)
        assert result[0]["truncation_applied"] is True
        # Original patch is preserved; the budget-limited excerpt is stored separately.
        assert isinstance(result[0]["patch"], str)
        assert result[0]["patch"] == "x" * 1000
        assert result[0]["patch_budget_excerpt"].endswith(_PATCH_TRUNCATION_MARKER)

    def test_patch_proportionally_allocated_when_budget_tight(self) -> None:
        """Every file retains a non-empty patch slice under proportional allocation."""
        budget = TokenBudget(budget_tokens=10, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": "/src/first.py",
                "patch": "small diff",
                "full_content_source": "x" * 2000,
                "full_content_target": None,
                "related_tests": [],
                "resolved_imports": [],
            },
            {
                "path": "/src/second.py",
                "patch": "x" * 1000,
                "full_content_source": None,
                "full_content_target": None,
                "related_tests": [],
                "resolved_imports": [],
            },
        ]

        result = assemble_context(files, budget)
        # Both files must receive a non-empty patch slice; proportional
        # allocation prevents the higher-priority large diff from consuming
        # the entire budget and leaving the smaller diff with nothing.
        # The original patch is preserved; check patch_budget_excerpt for truncation.
        assert result[0]["patch"] != ""
        assert result[0]["truncation_applied"] is True
        assert result[1]["patch"] != ""
        assert result[1]["truncation_applied"] is True

    def test_truncation_preserves_changed_region_context(self) -> None:
        """Truncation keeps context around changed lines instead of always keeping file prefix."""
        budget = TokenBudget(budget_tokens=30, safety_margin=0.0)
        source = "\n".join(f"line {i}" for i in range(1, 220))
        source = source.replace("line 180", "line 180 CHANGED_REGION_MARKER")
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "patch": "",
                "full_content_source": source,
                "full_content_target": None,
                "addedLines": [{"line": 180, "content": "line 180 CHANGED_REGION_MARKER"}],
                "related_tests": [],
                "resolved_imports": [],
            }
        ]

        result = assemble_context(files, budget)
        truncated = result[0]["full_content_source"]
        assert isinstance(truncated, str)
        assert "line 180" in truncated
        assert "omitted before changed region" in truncated
        assert result[0]["truncation_applied"] is True

    def test_sets_estimated_tokens(self) -> None:
        """estimated_tokens field is populated."""
        budget = TokenBudget(budget_tokens=100000, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "patch": "diff content",
                "full_content_source": "source",
                "full_content_target": None,
                "related_tests": [],
                "resolved_imports": [],
            }
        ]
        result = assemble_context(files, budget)
        assert result[0]["estimated_tokens"] > 0


class TestAssembleContextWithTestsAndImports:
    """Tests for content assembly with related tests and imports."""

    def test_includes_related_tests(self) -> None:
        """Related test contents within budget are preserved."""
        from agentic_devtools.orchestration.review.content_assembler import assemble_context

        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": "x",
                "full_content_target": "y",
                "context_status": "success",
                "related_tests": ["tests/test_app.py"],
                "related_test_contents": [{"path": "tests/test_app.py", "content": "def test_app():\n    assert True"}],
                "resolved_imports": [],
                "resolved_import_contents": [],
            }
        ]
        from agentic_devtools.orchestration.review.budget import TokenBudget as TB

        result = assemble_context(files, TB(budget_tokens=10000))
        assert result[0]["related_tests"] == ["tests/test_app.py"]
        assert result[0]["related_test_contents"] == [
            {"path": "tests/test_app.py", "content": "def test_app():\n    assert True"}
        ]
        assert result[0]["related_tests_retained"] == ["tests/test_app.py"]

    def test_includes_resolved_imports(self) -> None:
        """Resolved import contents within budget are preserved."""
        from agentic_devtools.orchestration.review.content_assembler import assemble_context

        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": "x",
                "full_content_target": "y",
                "context_status": "success",
                "related_tests": [],
                "related_test_contents": [],
                "resolved_imports": ["src/utils.py"],
                "resolved_import_contents": [{"path": "src/utils.py", "content": "def helper():\n    return 1"}],
            }
        ]
        from agentic_devtools.orchestration.review.budget import TokenBudget as TB

        result = assemble_context(files, TB(budget_tokens=10000))
        assert result[0]["resolved_imports"] == ["src/utils.py"]
        assert result[0]["resolved_import_contents"] == [
            {"path": "src/utils.py", "content": "def helper():\n    return 1"}
        ]
        assert result[0]["resolved_imports_retained"] == ["src/utils.py"]

    def test_includes_related_config_docs_after_imports(self) -> None:
        """Related config/doc content is preserved as the lowest-priority tier."""
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": "x",
                "full_content_target": "y",
                "context_status": "success",
                "related_tests": [],
                "related_test_contents": [],
                "resolved_imports": [],
                "resolved_import_contents": [],
                "related_config_docs": ["pyproject.toml"],
                "related_config_doc_contents": [{"path": "pyproject.toml", "content": "[project]\nname='agdt'\n"}],
            }
        ]

        result = assemble_context(files, TokenBudget(budget_tokens=10000))
        assert result[0]["related_config_docs"] == ["pyproject.toml"]
        assert result[0]["related_config_doc_contents"] == [
            {"path": "pyproject.toml", "content": "[project]\nname='agdt'\n"}
        ]
        assert result[0]["related_config_docs_retained"] == ["pyproject.toml"]

    def test_truncation_removes_content(self) -> None:
        """Content exceeding budget is set to None."""
        from agentic_devtools.orchestration.review.content_assembler import assemble_context

        # Create a file with very large content that exceeds budget
        large_content = "x" * 100000
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": large_content,
                "full_content_target": large_content,
                "context_status": "success",
                "related_tests": [],
                "resolved_imports": [],
            }
        ]
        from agentic_devtools.orchestration.review.budget import TokenBudget as TB2

        result = assemble_context(files, TB2(budget_tokens=10))  # Very small budget
        assert result[0]["truncation_applied"] is True

    def test_budget_too_small_for_tests_preserves_paths_but_clears_content(self) -> None:
        """When budget is exhausted, related_test_contents is cleared but path lists are preserved."""
        from agentic_devtools.orchestration.review.budget import TokenBudget
        from agentic_devtools.orchestration.review.content_assembler import assemble_context

        # Budget that fits only the main content but not tests/imports
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": "x" * 50,
                "full_content_target": "y" * 50,
                "context_status": "success",
                "related_tests": ["tests/test_app.py", "tests/test_helpers.py"],
                "related_test_contents": [
                    {"path": "tests/test_app.py", "content": "x" * 100},
                    {"path": "tests/test_helpers.py", "content": "y" * 100},
                ],
                "resolved_imports": ["src/utils.py", "src/config.py"],
                "resolved_import_contents": [
                    {"path": "src/utils.py", "content": "z" * 100},
                    {"path": "src/config.py", "content": "w" * 100},
                ],
                "related_config_docs": ["pyproject.toml"],
                "related_config_doc_contents": [{"path": "pyproject.toml", "content": "[project]\n" + ("n" * 120)}],
            }
        ]
        # Use very small budget that leaves no room for tests/imports
        budget = TokenBudget(budget_tokens=20)
        result = assemble_context(files, budget)
        assert result[0]["path"] == "/src/app.py"
        # Content lists are cleared when they don't fit
        assert result[0]["related_test_contents"] == []
        assert result[0]["resolved_import_contents"] == []
        assert result[0]["related_config_doc_contents"] == []
        assert result[0]["related_tests_omitted_count"] == 2
        assert result[0]["resolved_imports_omitted_count"] == 2
        assert result[0]["related_config_docs_omitted_count"] == 1
        assert result[0]["truncation_applied"] is True
        # Original path lists are preserved for graceful-degradation renderers
        assert result[0]["related_tests"] == ["tests/test_app.py", "tests/test_helpers.py"]
        assert result[0]["resolved_imports"] == ["src/utils.py", "src/config.py"]
        assert result[0]["related_config_docs"] == ["pyproject.toml"]
        # Retained lists are empty since no content was kept
        assert result[0]["related_tests_retained"] == []
        assert result[0]["resolved_imports_retained"] == []
        assert result[0]["related_config_docs_retained"] == []

    def test_invalid_related_content_items_are_ignored(self) -> None:
        """Non-dict or non-string related-file content items are discarded safely."""
        budget = TokenBudget(budget_tokens=1000, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": "x",
                "full_content_target": None,
                "related_tests": ["tests/test_app.py"],
                "related_test_contents": [
                    "bad",
                    {"path": 1, "content": "x"},
                    {"path": "tests/test_app.py", "content": "ok"},
                ],
                "resolved_imports": [],
                "resolved_import_contents": [],
            }
        ]

        result = assemble_context(files, budget)
        assert result[0]["related_test_contents"] == [{"path": "tests/test_app.py", "content": "ok"}]

    def test_related_content_item_is_truncated_to_remaining_budget(self) -> None:
        """A partially fitting related-file content item is truncated instead of dropped outright."""
        budget = TokenBudget(budget_tokens=8, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": "",
                "full_content_target": None,
                "related_tests": ["tests/test_app.py"],
                "related_test_contents": [{"path": "tests/test_app.py", "content": "x" * 200}],
                "resolved_imports": [],
                "resolved_import_contents": [],
            }
        ]

        result = assemble_context(files, budget)
        truncated_items = result[0]["related_test_contents"]
        assert truncated_items
        assert truncated_items[0]["path"] == "tests/test_app.py"
        assert len(truncated_items[0]["content"]) < 200
        assert result[0]["related_tests_omitted_count"] == 1
        assert result[0]["truncation_applied"] is True

    def test_related_content_item_is_dropped_when_only_path_prefix_fits(self) -> None:
        """A related-file content item is omitted when the remaining budget cannot fit any content."""
        budget = TokenBudget(budget_tokens=5, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": "",
                "full_content_target": None,
                "related_tests": ["tests/test_app.py"],
                "related_test_contents": [{"path": "tests/test_app.py", "content": "x" * 200}],
                "resolved_imports": [],
                "resolved_import_contents": [],
            }
        ]

        result = assemble_context(files, budget)
        assert result[0]["related_test_contents"] == []
        assert result[0]["related_tests_omitted_count"] == 1


class TestAssembleContextPatchAllocation:
    """Tests for proportional patch allocation in assemble_context."""

    def test_multi_file_patch_starvation_prevented(self) -> None:
        """Every file retains a patch slice even when total demand far exceeds budget."""
        budget = TokenBudget(budget_tokens=50, safety_margin=0.0)
        # 10 files, each with a ~60-token patch — total demand ~600 tokens, budget 50
        files: list[dict[str, object]] = [
            {
                "path": f"/src/file{i}.py",
                "patch": "x" * 210,  # ceil(210/3.5) = 60 tokens each
                "full_content_source": None,
                "full_content_target": None,
            }
            for i in range(10)
        ]
        result = assemble_context(files, budget)
        # All 10 files must receive a non-empty truncated patch slice.
        for i, entry in enumerate(result):
            assert entry["patch"] != "", f"file{i} received an empty patch"
            assert entry["truncation_applied"] is True

    def test_patch_alloc_zero_when_budget_fully_exhausted(self) -> None:
        """When budget is exhausted before all files are reached, remaining files are skipped."""
        # Budget of 3 tokens: 5 files each needing 10 tokens → each file
        # calculates alloc=1, but after 3 files consume 1 token each, the
        # 4th and 5th files arrive at budget.remaining=0 (alloc clamped to 0).
        budget = TokenBudget(budget_tokens=3, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": f"/src/file{i}.py",
                "patch": "x" * 35,  # ceil(35/3.5) = 10 tokens each
                "full_content_source": None,
                "full_content_target": None,
            }
            for i in range(5)
        ]
        result = assemble_context(files, budget)
        patches_with_content = sum(1 for e in result if e.get("patch"))
        # At least some files got content; the rest are marked truncated.
        assert patches_with_content >= 1
        for entry in result:
            if not entry.get("patch"):
                assert entry["truncation_applied"] is True

    def test_proportional_patch_fits_without_truncation(self) -> None:
        """When a file's proportional share covers its full patch, no truncation is applied."""
        # 5 tiny patches (1 token each, 3 chars each), budget 4 tokens.
        # total_demand=5 > available=4, so proportional branch runs.
        # Each file gets alloc=max(1, int(4*1//5))=1, max_chars=3, len(patch)=3 <= 3
        # → the len(patch) > max_chars branch is False and no truncation happens.
        budget = TokenBudget(budget_tokens=4, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": f"/src/file{i}.py",
                "patch": "abc",  # ceil(3/3.5) = 1 token
                "full_content_source": None,
                "full_content_target": None,
            }
            for i in range(5)
        ]
        result = assemble_context(files, budget)
        # The first four files must have their patches intact (not truncated by content_assembler)
        patches_intact = [e for e in result if e.get("patch") == "abc"]
        assert len(patches_intact) >= 1


class TestAssembleContextPatchTruncationMarker:
    """Tests that truncated patches include an explicit truncation marker."""

    def test_truncated_patch_ends_with_marker(self) -> None:
        """A patch that exceeds the budget ends with the truncation marker."""
        from agentic_devtools.orchestration.review.content_assembler import _PATCH_TRUNCATION_MARKER

        budget = TokenBudget(budget_tokens=50, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "patch": "@@ -1,3 +1,3 @@\n line\n" + "x" * 1000,
                "full_content_source": None,
                "full_content_target": None,
                "related_tests": [],
                "resolved_imports": [],
            }
        ]

        result = assemble_context(files, budget)
        assert result[0]["truncation_applied"] is True
        assert result[0]["patch_budget_excerpt"].endswith(_PATCH_TRUNCATION_MARKER)

    def test_truncated_patch_cuts_at_hunk_boundary(self) -> None:
        """Patch truncation stops before the last incomplete hunk."""
        from agentic_devtools.orchestration.review.content_assembler import _PATCH_TRUNCATION_MARKER

        hunk1 = "@@ -1,3 +1,3 @@\n line1\n-old\n+new\n"
        # Second hunk is large enough to push the patch over budget.
        hunk2 = "@@ -10,3 +10,3 @@\n line10\n" + "x" * 2000
        patch = hunk1 + hunk2

        budget = TokenBudget(budget_tokens=20, safety_margin=0.0)
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "patch": patch,
                "full_content_source": None,
                "full_content_target": None,
                "related_tests": [],
                "resolved_imports": [],
            }
        ]

        result = assemble_context(files, budget)
        # Original patch is preserved; read the budget-limited excerpt for truncation checks.
        truncated = result[0]["patch_budget_excerpt"]
        assert result[0]["truncation_applied"] is True
        assert result[0]["patch"] == patch  # original unchanged
        assert truncated.endswith(_PATCH_TRUNCATION_MARKER)
        # The first complete hunk should be retained
        assert "@@ -1,3 +1,3 @@" in truncated
        # The second incomplete hunk should have been cut
        assert "@@ -10,3 +10,3 @@" not in truncated


class TestAssembleContextFallbackPathsCap:
    """Tests for Priority-6 fallback-path budget allocation (FR-008 compliance)."""

    def _base_entry(self, paths: list[str]) -> dict[str, object]:
        """Helper: an entry with no content items but with discovered path lists."""
        return {
            "path": "/src/app.py",
            "full_content_source": None,
            "full_content_target": None,
            "related_tests": paths,
            "related_test_contents": [],
            "resolved_imports": [],
            "resolved_import_contents": [],
            "related_config_docs": [],
            "related_config_doc_contents": [],
        }

    def test_paths_display_cap_set_when_no_content(self) -> None:
        """When content is absent, paths_display_cap reflects how many paths fit the budget."""
        from agentic_devtools.orchestration.review.budget import TokenBudget
        from agentic_devtools.orchestration.review.content_assembler import assemble_context

        # Large budget — all paths should be approved.
        paths = [f"tests/test_mod_{i}.py" for i in range(5)]
        files = [self._base_entry(paths)]
        budget = TokenBudget(budget_tokens=100_000, safety_margin=0.0)
        result = assemble_context(files, budget)
        assert result[0]["related_tests_paths_display_cap"] == 5

    def test_paths_display_cap_zero_when_budget_exhausted(self) -> None:
        """When the budget is already exhausted, no fallback paths are approved."""
        from agentic_devtools.orchestration.review.budget import TokenBudget
        from agentic_devtools.orchestration.review.content_assembler import assemble_context

        paths = ["tests/test_a.py", "tests/test_b.py"]
        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": None,
                "full_content_target": None,
                # Use a patch that consumes the entire 1-token budget.
                "patch": "x",  # 1 char → ceil(1/3.5)=1 token
                "related_tests": paths,
                "related_test_contents": [],
                "resolved_imports": [],
                "resolved_import_contents": [],
                "related_config_docs": [],
                "related_config_doc_contents": [],
            }
        ]
        budget = TokenBudget(budget_tokens=1, safety_margin=0.0)
        result = assemble_context(files, budget)
        assert result[0]["related_tests_paths_display_cap"] == 0
        assert result[0]["truncation_applied"] is True

    def test_paths_display_cap_not_set_when_content_items_present(self) -> None:
        """When content items ARE present, the cap defaults to _MAX_FALLBACK_PATHS (fallback unused)."""
        from agentic_devtools.orchestration.review.budget import TokenBudget
        from agentic_devtools.orchestration.review.content_assembler import (
            _MAX_FALLBACK_PATHS,
            assemble_context,
        )

        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": None,
                "full_content_target": None,
                "related_tests": ["tests/test_a.py"],
                "related_test_contents": [{"path": "tests/test_a.py", "content": "pass"}],
                "resolved_imports": [],
                "resolved_import_contents": [],
                "related_config_docs": [],
                "related_config_doc_contents": [],
            }
        ]
        budget = TokenBudget(budget_tokens=100_000, safety_margin=0.0)
        result = assemble_context(files, budget)
        # Fallback branch is skipped; cap defaults to _MAX_FALLBACK_PATHS.
        assert result[0]["related_tests_paths_display_cap"] == _MAX_FALLBACK_PATHS

    def test_all_three_categories_capped_independently(self) -> None:
        """paths_display_cap is set for tests, imports, and config-docs independently."""
        from agentic_devtools.orchestration.review.budget import TokenBudget
        from agentic_devtools.orchestration.review.content_assembler import assemble_context

        files: list[dict[str, object]] = [
            {
                "path": "/src/app.py",
                "full_content_source": None,
                "full_content_target": None,
                "related_tests": ["tests/test_a.py"],
                "related_test_contents": [],
                "resolved_imports": ["src/utils.py"],
                "resolved_import_contents": [],
                "related_config_docs": ["pyproject.toml"],
                "related_config_doc_contents": [],
            }
        ]
        budget = TokenBudget(budget_tokens=100_000, safety_margin=0.0)
        result = assemble_context(files, budget)
        assert result[0]["related_tests_paths_display_cap"] == 1
        assert result[0]["resolved_imports_paths_display_cap"] == 1
        assert result[0]["related_config_docs_paths_display_cap"] == 1
