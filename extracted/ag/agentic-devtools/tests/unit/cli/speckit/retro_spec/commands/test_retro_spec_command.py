"""Tests for retro_spec_command in retro_spec/commands.py."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import IssueArtifact, PRArtifact
from agentic_devtools.cli.speckit.retro_spec.commands import retro_spec_command

_MOD = "agentic_devtools.cli.speckit.retro_spec.commands"


def _patch_repo(slug: str = "owner/repo"):
    return patch(f"{_MOD}.resolve_github_repo_safe", return_value=slug)


class TestRetroSpecCommand:
    """Tests for the retro_spec_command function."""

    def test_exits_when_specs_root_is_a_file(self, tmp_path: Path) -> None:
        """Test that a non-directory specs_root aborts with a clear error."""
        specs_file = tmp_path / "specs"
        specs_file.write_text("not a directory", encoding="utf-8")

        with _patch_repo():
            with pytest.raises(SystemExit):
                retro_spec_command(42, specs_root=specs_file)

    def test_exits_when_repo_cannot_be_determined(self, tmp_path: Path) -> None:
        """Test that missing repository coordinates abort execution."""
        with patch(f"{_MOD}.resolve_github_repo_safe", return_value=None):
            with pytest.raises(SystemExit):
                retro_spec_command(42, specs_root=tmp_path)

    def test_exits_when_insufficient_artifacts(self, tmp_path: Path) -> None:
        """Test abort when issue has no body, no comments, and no PRs."""
        issue = IssueArtifact(number=42, title="Empty", body="", comments=[], state="closed")
        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
        ):
            with pytest.raises(SystemExit):
                retro_spec_command(42, specs_root=tmp_path)

    def test_commit_mode_rejects_dirty_tree_before_synthesis(self, tmp_path: Path) -> None:
        """Commit mode checks repository cleanliness before invoking the LLM."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        placement = SimpleNamespace(target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False)
        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.has_local_changes", return_value=True),
            patch(f"{_MOD}.synthesize_spec") as synthesize,
        ):
            with pytest.raises(SystemExit):
                retro_spec_command(42, specs_root=tmp_path, commit=True)

        synthesize.assert_not_called()

    def test_output_mode_never_commits_even_when_requested(self, tmp_path: Path) -> None:
        """Custom output is independent of repository commits."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        output_path = tmp_path / "custom.md"
        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.create_commit") as create_commit,
        ):
            retro_spec_command(42, specs_root=tmp_path, output=str(output_path), commit=True)

        create_commit.assert_not_called()

    def test_applies_diff_budget_across_related_prs(self, tmp_path: Path) -> None:
        """A shared diff budget limits cumulative PR artifacts and reports omissions."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [
            PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z"),
            PRArtifact(number=102, title="PR 2", body="", state="merged", merged_at="2025-01-02T00:00:00Z"),
        ]
        captured_diffs: list[str] = []

        def _capture_context(
            issue_arg: IssueArtifact,
            prs_arg: list[PRArtifact],
            diffs_arg: list[str],
            commits_arg: list[str],
        ) -> str:
            del issue_arg, prs_arg, commits_arg
            captured_diffs.extend(diffs_arg)
            return "ctx"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.fetch_pr_diffs", side_effect=[["A" * 60], ["B" * 120]]),
            patch(f"{_MOD}.get_diff_budget", return_value=150),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", side_effect=_capture_context),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        assert captured_diffs[0] == "A" * 60
        assert any("included 1 PR(s), omitted 1 subsequent PR(s)" in entry for entry in captured_diffs)

    def test_handles_empty_pr_diff_entries_without_marking_omission(self, tmp_path: Path) -> None:
        """Empty diff payloads still count as analyzed PRs under shared budgeting."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z")]
        captured_diffs: list[str] = []

        def _capture_context(
            issue_arg: IssueArtifact,
            prs_arg: list[PRArtifact],
            diffs_arg: list[str],
            commits_arg: list[str],
        ) -> str:
            del issue_arg, prs_arg, commits_arg
            captured_diffs.extend(diffs_arg)
            return "ctx"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=[]),
            patch(f"{_MOD}.get_diff_budget", return_value=100),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", side_effect=_capture_context),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        assert captured_diffs == []

    def test_treats_pr_metadata_without_diffs_or_commits_as_no_implementation_artifacts(self, tmp_path: Path) -> None:
        """Fallback synthesis stays issue-only when PR metadata yields no usable artifacts."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z")]

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["[Could not retrieve diff for PR #101]"]),
            patch(f"{_MOD}.get_diff_budget", return_value=100),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec") as synthesize,
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        assert synthesize.call_args.kwargs["has_implementation_artifacts"] is False

    def test_metadata_only_path_adds_deterministic_availability_warning(self, tmp_path: Path) -> None:
        """Metadata-only artifact collection prepends an explicit availability warning."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z")]

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["[Could not retrieve diff for PR #101]"]),
            patch(f"{_MOD}.get_diff_budget", return_value=100),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec content"),
            patch(f"{_MOD}.write_spec_file") as mock_write,
        ):
            retro_spec_command(42, specs_root=tmp_path)

        args, _kwargs = mock_write.call_args
        assert args[0].startswith("## Artifact Availability")
        assert "issue evidence and PR metadata only" in args[0]

    def test_budget_omission_is_promoted_to_artifact_availability_section(self, tmp_path: Path) -> None:
        """Diff-budget omissions are rendered in the generated output, not only the LLM context."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z")]

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["A" * 40, "B" * 60]),
            patch(f"{_MOD}.get_diff_budget", return_value=80),
            patch(f"{_MOD}.collect_commit_messages", return_value=["implement feature"]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec content"),
            patch(f"{_MOD}.write_spec_file") as mock_write,
        ):
            retro_spec_command(42, specs_root=tmp_path)

        args, _kwargs = mock_write.call_args
        assert args[0].startswith("## Artifact Availability")
        assert "Diff artifacts were truncated because the shared diff budget was exhausted" in args[0]
        assert "omitted additional diff entries from 1 partially included PR(s)" in args[0]

    def test_treats_empty_diff_entries_as_no_implementation_artifacts(self, tmp_path: Path) -> None:
        """Empty diff placeholders do not count as usable implementation artifacts."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z")]

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=[""]),
            patch(f"{_MOD}.get_diff_budget", return_value=100),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec") as synthesize,
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        assert synthesize.call_args.kwargs["has_implementation_artifacts"] is False

    def test_treats_commit_messages_as_implementation_artifacts_without_real_diffs(self, tmp_path: Path) -> None:
        """Commit history alone still counts as usable implementation artifacts."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z")]

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["[Could not retrieve diff for PR #101]"]),
            patch(f"{_MOD}.get_diff_budget", return_value=100),
            patch(f"{_MOD}.collect_commit_messages", return_value=["implement retro-spec command"]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec") as synthesize,
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        assert synthesize.call_args.kwargs["has_implementation_artifacts"] is True

    def test_skips_pr_diff_fetch_when_initial_budget_is_exhausted(self, tmp_path: Path) -> None:
        """A non-positive shared budget omits all PR diffs deterministically."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z")]
        captured_diffs: list[str] = []

        def _capture_context(
            issue_arg: IssueArtifact,
            prs_arg: list[PRArtifact],
            diffs_arg: list[str],
            commits_arg: list[str],
        ) -> str:
            del issue_arg, prs_arg, commits_arg
            captured_diffs.extend(diffs_arg)
            return "ctx"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.get_diff_budget", return_value=0),
            patch(f"{_MOD}.fetch_pr_diffs") as fetch_diffs,
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", side_effect=_capture_context),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        fetch_diffs.assert_not_called()
        assert any("included 0 PR(s), omitted 1 subsequent PR(s)" in entry for entry in captured_diffs)

    def test_stops_collecting_diffs_when_budget_hits_zero(self, tmp_path: Path) -> None:
        """A fully consumed budget exits the PR loop before subsequent diff fetches."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [
            PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z"),
            PRArtifact(number=102, title="PR 2", body="", state="merged", merged_at="2025-01-02T00:00:00Z"),
        ]

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.get_diff_budget", return_value=60),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["A" * 60]) as fetch_diffs,
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        fetch_diffs.assert_called_once()

    def test_oversized_first_diff_does_not_double_count_omitted_prs(self, tmp_path: Path) -> None:
        """Oversized entries report each omitted PR exactly once."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [
            PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z"),
            PRArtifact(number=102, title="PR 2", body="", state="merged", merged_at="2025-01-02T00:00:00Z"),
            PRArtifact(number=103, title="PR 3", body="", state="merged", merged_at="2025-01-03T00:00:00Z"),
        ]
        captured_diffs: list[str] = []

        def _capture_context(
            issue_arg: IssueArtifact,
            prs_arg: list[PRArtifact],
            diffs_arg: list[str],
            commits_arg: list[str],
        ) -> str:
            del issue_arg, prs_arg, commits_arg
            captured_diffs.extend(diffs_arg)
            return "ctx"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.get_diff_budget", return_value=120),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["X" * 200]) as fetch_diffs,
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", side_effect=_capture_context),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        fetch_diffs.assert_called_once()
        assert any("included 0 PR(s), omitted 3 subsequent PR(s)" in entry for entry in captured_diffs)

    def test_partial_current_pr_overflow_reports_partial_omission(self, tmp_path: Path) -> None:
        """When one entry fits and a later one overflows, a partial-omission notice is emitted."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z")]
        captured_diffs: list[str] = []

        def _capture_context(
            issue_arg: IssueArtifact,
            prs_arg: list[PRArtifact],
            diffs_arg: list[str],
            commits_arg: list[str],
        ) -> str:
            del issue_arg, prs_arg, commits_arg
            captured_diffs.extend(diffs_arg)
            return "ctx"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.get_diff_budget", return_value=80),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["A" * 40, "B" * 60]),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", side_effect=_capture_context),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        assert captured_diffs[0] == "A" * 40
        assert any(
            "omitted additional diff entries from 1 partially included PR(s)" in entry for entry in captured_diffs
        )

    def test_inner_pr_omission_notice_is_preserved_and_stops_diff_collection(self, tmp_path: Path) -> None:
        """The file-omission notice from fetch_pr_diffs is passed through to the context
        even when remaining_diff_budget is tight, and it stops further diff collection."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [
            PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z"),
            PRArtifact(number=102, title="PR 2", body="", state="merged", merged_at="2025-02-01T00:00:00Z"),
        ]
        captured_diffs: list[str] = []

        def _capture_context(
            issue_arg: IssueArtifact,
            prs_arg: list[PRArtifact],
            diffs_arg: list[str],
            commits_arg: list[str],
        ) -> str:
            del issue_arg, prs_arg, commits_arg
            captured_diffs.extend(diffs_arg)
            return "ctx"

        inner_notice = "[Diff budget exhausted: subsequent PR files were omitted from this retroactive spec.]"
        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.get_diff_budget", return_value=50),
            # PR 1 returns one small diff + the inner omission notice
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["A" * 10, inner_notice]),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", side_effect=_capture_context),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        # The diff entry and the inner omission notice must both be present.
        assert "A" * 10 in captured_diffs
        assert inner_notice in captured_diffs
        # PR 2 should be counted as omitted (diff collection stopped after the notice).
        assert any("omitted 1 subsequent PR(s)" in entry for entry in captured_diffs)

    def test_sole_pr_with_inner_notice_after_real_content_is_counted_as_partially_omitted(self, tmp_path: Path) -> None:
        """When the only PR yields real diff entries followed by an inner budget-exhaustion
        notice, that PR must be marked as partially omitted so the spec gets an Artifact
        Availability warning even though no subsequent PR was omitted."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [
            PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z"),
        ]
        captured_diffs: list[str] = []

        def _capture_context(
            issue_arg: IssueArtifact,
            prs_arg: list[PRArtifact],
            diffs_arg: list[str],
            commits_arg: list[str],
        ) -> str:
            del issue_arg, prs_arg, commits_arg
            captured_diffs.extend(diffs_arg)
            return "ctx"

        inner_notice = "[Diff budget exhausted: subsequent PR files were omitted from this retroactive spec.]"
        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.get_diff_budget", return_value=50_000),
            # Single PR returns one real diff entry then the inner omission notice.
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["A" * 10, inner_notice]),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", side_effect=_capture_context),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        # The real diff content and the inner notice must both be present.
        assert "A" * 10 in captured_diffs
        assert inner_notice in captured_diffs
        # The PR must be counted as partially omitted so an Artifact Availability warning appears.
        assert any("partially included" in entry for entry in captured_diffs), (
            f"Expected a partial-omission budget notice. Captured diffs: {captured_diffs}"
        )

    def test_pr_with_only_inner_notice_is_counted_as_omitted(self, tmp_path: Path) -> None:
        """When fetch_pr_diffs returns only its own budget-exhaustion notice (no real diffs),
        that PR must be counted as omitted, not included."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [
            PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z"),
        ]
        captured_diffs: list[str] = []

        def _capture_context(
            issue_arg: IssueArtifact,
            prs_arg: list[PRArtifact],
            diffs_arg: list[str],
            commits_arg: list[str],
        ) -> str:
            del issue_arg, prs_arg, commits_arg
            captured_diffs.extend(diffs_arg)
            return "ctx"

        inner_notice = "[Diff budget exhausted: subsequent PR files were omitted from this retroactive spec.]"
        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.get_diff_budget", return_value=50_000),
            # PR 1 returns only its inner omission notice — no real diff was small enough
            patch(f"{_MOD}.fetch_pr_diffs", return_value=[inner_notice]),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", side_effect=_capture_context),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        # The inner notice should still be present in the context diffs.
        assert inner_notice in captured_diffs
        # With zero real diffs added, the PR should appear as omitted in the outer notice.
        assert any("omitted 1" in entry for entry in captured_diffs), (
            f"Expected PR to be counted as omitted. Captured diffs: {captured_diffs}"
        )

    def test_partial_and_subsequent_omissions_are_reported_together(self, tmp_path: Path) -> None:
        """When current and subsequent omissions both happen, one combined notice reports both."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        prs = [
            PRArtifact(number=101, title="PR 1", body="", state="merged", merged_at="2025-01-01T00:00:00Z"),
            PRArtifact(number=102, title="PR 2", body="", state="merged", merged_at="2025-02-01T00:00:00Z"),
        ]
        captured_diffs: list[str] = []

        def _capture_context(
            issue_arg: IssueArtifact,
            prs_arg: list[PRArtifact],
            diffs_arg: list[str],
            commits_arg: list[str],
        ) -> str:
            del issue_arg, prs_arg, commits_arg
            captured_diffs.extend(diffs_arg)
            return "ctx"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.get_diff_budget", return_value=80),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["A" * 40, "B" * 60]),
            patch(f"{_MOD}.collect_commit_messages", return_value=[]),
            patch(
                f"{_MOD}.resolve_placement",
                return_value=SimpleNamespace(
                    target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False
                ),
            ),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", side_effect=_capture_context),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        assert any(
            "omitted additional diff entries from 1 partially included PR(s)" in entry for entry in captured_diffs
        )
        assert any("omitted 1 subsequent PR(s)" in entry for entry in captured_diffs)

    def test_dry_run_outputs_to_stdout(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that dry-run mode prints spec to stdout without writing files."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        placement = SimpleNamespace(
            target_path=tmp_path / "42",
            parent_issue=None,
            needs_hierarchy_update=False,
        )

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="generated spec content"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        out = capsys.readouterr().out
        assert "DRY RUN" in out
        assert "**Generated**: retroactive" in out
        assert "Retroactive Spec" in out
        assert "generated spec content" in out
        # No file should be written
        assert not (tmp_path / "42" / "spec.md").exists()

    def test_dry_run_reports_pending_hierarchy_registration(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Dry-run reports parent-managed hierarchy ownership without writing files."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        placement = SimpleNamespace(
            target_path=parent_dir / "42",
            parent_issue=100,
            needs_hierarchy_update=True,
        )

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="generated spec content"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        err = capsys.readouterr().err
        assert "Would register #42 in parent hierarchy" in err
        # hierarchy.yml must not be created in dry-run mode
        assert not (parent_dir / "hierarchy.yml").exists()

    def test_exits_when_target_spec_already_exists(self, tmp_path: Path) -> None:
        """Test that existing target specs are not overwritten."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        target = tmp_path / "42"
        target.mkdir()
        (target / "spec.md").write_text("existing", encoding="utf-8")
        placement = SimpleNamespace(target_path=target, parent_issue=None, needs_hierarchy_update=False)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            with pytest.raises(SystemExit):
                retro_spec_command(42, specs_root=tmp_path)

    def test_exits_when_target_spec_is_dangling_symlink(self, tmp_path: Path) -> None:
        """Test that a dangling symlink at the spec path is treated as a conflict."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        target = tmp_path / "42"
        target.mkdir()
        spec_link = target / "spec.md"
        spec_link.symlink_to(tmp_path / "nonexistent-target.md")
        placement = SimpleNamespace(target_path=target, parent_issue=None, needs_hierarchy_update=False)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            with pytest.raises(SystemExit):
                retro_spec_command(42, specs_root=tmp_path)

    def test_dry_run_exits_when_target_spec_already_exists(self, tmp_path: Path) -> None:
        """Test that dry-run surfaces overwrite conflicts before reporting success."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        target = tmp_path / "42"
        target.mkdir()
        (target / "spec.md").write_text("existing", encoding="utf-8")
        placement = SimpleNamespace(target_path=target, parent_issue=None, needs_hierarchy_update=False)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            with pytest.raises(SystemExit):
                retro_spec_command(42, specs_root=tmp_path, dry_run=True)

    def test_output_flag_writes_to_custom_path(self, tmp_path: Path) -> None:
        """Test that --output writes spec to specified path."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        output_path = tmp_path / "custom" / "spec.md"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec content"),
            patch(f"{_MOD}.write_spec_file") as mock_write,
        ):
            retro_spec_command(42, specs_root=tmp_path, output=str(output_path))

        mock_write.assert_called_once()

    def test_output_flag_treats_nonexistent_path_as_file(self, tmp_path: Path) -> None:
        """Test that --output without suffix is treated as an explicit file path."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        output_path = tmp_path / "custom" / "retro-spec"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec content"),
            patch(f"{_MOD}.write_spec_file") as mock_write,
        ):
            retro_spec_command(42, specs_root=tmp_path, output=str(output_path))

        args, kwargs = mock_write.call_args
        assert args[0].startswith("## Artifact Availability")
        assert args[1:] == (output_path.parent,)
        assert kwargs["output_file"] == output_path

    def test_output_flag_treats_existing_directory_as_directory(self, tmp_path: Path) -> None:
        """Test that --output points to spec.md when the output path is an existing directory."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        output_path = tmp_path / "custom"
        output_path.mkdir()

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec content"),
            patch(f"{_MOD}.write_spec_file") as mock_write,
        ):
            retro_spec_command(42, specs_root=tmp_path, output=str(output_path))

        args, kwargs = mock_write.call_args
        assert args[0].startswith("## Artifact Availability")
        assert args[1:] == (output_path,)
        assert kwargs["output_file"] == output_path / "spec.md"

    def test_output_mode_ignores_specs_root_when_it_is_a_file(self, tmp_path: Path) -> None:
        """Test that --output mode does not require specs_root to be a directory."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        specs_file = tmp_path / "specs"
        specs_file.write_text("not a directory", encoding="utf-8")
        output_path = tmp_path / "custom" / "spec.md"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec content"),
            patch(f"{_MOD}.write_spec_file") as mock_write,
        ):
            retro_spec_command(42, specs_root=specs_file, output=str(output_path))

        mock_write.assert_called_once()

    def test_commit_flag_creates_git_commit(self, tmp_path: Path) -> None:
        """Test that --commit creates a git commit after writing."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        placement = SimpleNamespace(
            target_path=tmp_path / "42",
            parent_issue=None,
            needs_hierarchy_update=False,
        )

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.has_local_changes", return_value=False),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file"),
            patch(f"{_MOD}.format_commit_message", return_value="msg"),
            patch(f"{_MOD}._stage_retro_spec") as mock_stage,
            patch(f"{_MOD}.create_commit") as mock_commit,
        ):
            retro_spec_command(42, specs_root=tmp_path, commit=True)

        mock_stage.assert_called_once_with([tmp_path / "42" / "spec.md"])
        mock_commit.assert_called_once_with(message="msg", dry_run=False)

    def test_commit_exits_when_working_tree_dirty(self, tmp_path: Path) -> None:
        """Test that dirty working tree aborts when --commit is used."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        placement = SimpleNamespace(target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.has_local_changes", return_value=True),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
        ):
            with pytest.raises(SystemExit):
                retro_spec_command(42, specs_root=tmp_path, commit=True)

    def test_no_commit_flag_skips_git_operations(self, tmp_path: Path) -> None:
        """Test that without --commit, no git operations occur."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        placement = SimpleNamespace(
            target_path=tmp_path / "42",
            parent_issue=None,
            needs_hierarchy_update=False,
        )

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file"),
            patch(f"{_MOD}.has_local_changes") as mock_local,
            patch(f"{_MOD}._stage_retro_spec") as mock_stage,
            patch(f"{_MOD}.create_commit") as mock_commit,
        ):
            retro_spec_command(42, specs_root=tmp_path, commit=False)

        mock_local.assert_not_called()
        mock_stage.assert_not_called()
        mock_commit.assert_not_called()


class TestRetroSpecCommandIntegration:
    """Additional tests for retro_spec_command coverage."""

    def test_iterates_prs_and_collects_diffs(self, tmp_path: Path) -> None:
        """Test that PRs are iterated with diffs and commits collected."""
        issue = IssueArtifact(number=42, title="T", body="body", state="closed")
        prs = [
            PRArtifact(number=10, title="PR1", body="b1"),
            PRArtifact(number=11, title="PR2", body="b2"),
        ]
        placement = SimpleNamespace(target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=prs),
            patch(f"{_MOD}.fetch_pr_diffs", return_value=["diff"]) as mock_diffs,
            patch(f"{_MOD}.collect_commit_messages", return_value=["msg"]) as mock_commits,
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file"),
        ):
            retro_spec_command(42, specs_root=tmp_path)

        assert mock_diffs.call_count == 2
        assert mock_commits.call_count == 2

    def test_parent_hierarchy_is_updated(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """retro-spec registers the child in the parent hierarchy.yml on successful write."""
        issue = IssueArtifact(number=42, title="T", body="body", state="closed")
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        hierarchy_file = parent_dir / "hierarchy.yml"
        hierarchy_file.write_text("title: 'Issue #100'\nlevel: epic\nchildren: []\n", encoding="utf-8")
        placement = SimpleNamespace(target_path=parent_dir / "42", parent_issue=100, needs_hierarchy_update=True)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file"),
        ):
            retro_spec_command(42, specs_root=tmp_path, commit=False)

        err = capsys.readouterr().err
        assert "Registered issue #42 in parent hierarchy" in err
        assert "retro-spec does not modify hierarchy.yml" not in err
        updated_content = hierarchy_file.read_text(encoding="utf-8")
        assert "42" in updated_content

    def test_commit_runs_cleanup_on_error(self, tmp_path: Path) -> None:
        """Test that with --commit, write errors trigger cleanup."""
        issue = IssueArtifact(number=42, title="T", body="body", state="closed")
        placement = SimpleNamespace(target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.has_local_changes", return_value=False),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file", side_effect=RuntimeError("fail")),
            patch(f"{_MOD}._cleanup_partial_retro_spec") as mock_cleanup,
        ):
            with pytest.raises(RuntimeError, match="fail"):
                retro_spec_command(42, specs_root=tmp_path, commit=True)

        mock_cleanup.assert_called_once()

    def test_hierarchy_registration_message_emitted(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Dry-run mode reports hierarchy ownership boundary for nested placement."""
        issue = IssueArtifact(number=42, title="T", body="body", state="closed")
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        placement = SimpleNamespace(target_path=parent_dir / "42", parent_issue=100, needs_hierarchy_update=True)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file"),
        ):
            retro_spec_command(42, specs_root=tmp_path, dry_run=True)

        assert "Would register #42 in parent hierarchy" in capsys.readouterr().err

    def test_defaults_specs_root_from_cwd(self, tmp_path: Path) -> None:
        """Test that specs_root defaults to cwd/specs."""
        issue = IssueArtifact(number=42, title="T", body="body", state="closed")
        placement = SimpleNamespace(
            target_path=tmp_path / "specs" / "42", parent_issue=None, needs_hierarchy_update=False
        )

        with (
            _patch_repo(),
            patch(f"{_MOD}.Path.cwd", return_value=tmp_path),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file"),
        ):
            retro_spec_command(42, dry_run=True)

    def test_no_prs_warning_printed(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that no-PR warning is printed to stderr."""
        issue = IssueArtifact(number=42, title="T", body="body", state="closed")
        placement = SimpleNamespace(target_path=tmp_path / "42", parent_issue=None, needs_hierarchy_update=False)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file"),
        ):
            retro_spec_command(42, specs_root=tmp_path)

        assert "No related PRs found" in capsys.readouterr().err

    def test_commit_with_existing_hierarchy_stages_both_files(self, tmp_path: Path) -> None:
        """Commit mode stages both the spec file and the updated hierarchy.yml."""
        issue = IssueArtifact(number=42, title="T", body="body", state="closed")
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        hierarchy_file = parent_dir / "hierarchy.yml"
        hierarchy_file.write_text("title: 'Issue #100'\nlevel: epic\nchildren: []\n", encoding="utf-8")
        placement = SimpleNamespace(target_path=parent_dir / "42", parent_issue=100, needs_hierarchy_update=True)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.has_local_changes", return_value=False),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file"),
            patch(f"{_MOD}.format_commit_message", return_value="msg"),
            patch(f"{_MOD}._stage_retro_spec") as mock_stage,
            patch(f"{_MOD}.create_commit"),
        ):
            retro_spec_command(42, specs_root=tmp_path, commit=True)

        mock_stage.assert_called_once_with([parent_dir / "42" / "spec.md", hierarchy_file])

    def test_commit_skips_staging_unchanged_hierarchy(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Commit mode does not stage or report hierarchy files when child already registered."""
        issue = IssueArtifact(number=42, title="T", body="body", state="closed")
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        hierarchy_file = parent_dir / "hierarchy.yml"
        # Child already registered with matching title — _register_child_in_hierarchy returns False.
        hierarchy_file.write_text(
            "title: 'Issue #100'\nlevel: epic\nchildren:\n  - key: '42'\n    title: T\n    order: 0\n",
            encoding="utf-8",
        )
        placement = SimpleNamespace(target_path=parent_dir / "42", parent_issue=100, needs_hierarchy_update=True)

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.resolve_placement", return_value=placement),
            patch(f"{_MOD}.has_local_changes", return_value=False),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec"),
            patch(f"{_MOD}.write_spec_file"),
            patch(f"{_MOD}.format_commit_message", return_value="msg"),
            patch(f"{_MOD}._stage_retro_spec") as mock_stage,
            patch(f"{_MOD}.create_commit"),
        ):
            retro_spec_command(42, specs_root=tmp_path, commit=True)

        assert "Updated parent hierarchy" not in capsys.readouterr().err
        mock_stage.assert_called_once_with([parent_dir / "42" / "spec.md"])

    def test_commit_with_output_outside_repo_is_ignored(self, tmp_path: Path) -> None:
        """Test that --output prevents commit handling even outside the repository."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        outside_path = tmp_path / "outside" / "spec.md"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec content"),
            patch(f"{_MOD}.write_spec_file"),
            patch(f"{_MOD}.create_commit") as create_commit,
        ):
            retro_spec_command(42, specs_root=tmp_path, output=str(outside_path), commit=True)

        create_commit.assert_not_called()

    def test_commit_with_output_inside_repo_is_ignored(self, tmp_path: Path) -> None:
        """Test that --output prevents commit handling inside the repository too."""
        issue = IssueArtifact(number=42, title="Retro issue", body="body", state="closed")
        output_path = tmp_path / "spec.md"

        with (
            _patch_repo(),
            patch(f"{_MOD}.fetch_issue", return_value=issue),
            patch(f"{_MOD}.discover_related_prs", return_value=[]),
            patch(f"{_MOD}.has_local_changes", return_value=False),
            patch(f"{_MOD}.build_system_prompt", return_value="sys"),
            patch(f"{_MOD}.assemble_context", return_value="ctx"),
            patch(f"{_MOD}.synthesize_spec", return_value="spec content"),
            patch(f"{_MOD}.write_spec_file"),
            patch(f"{_MOD}.create_commit") as create_commit,
        ):
            retro_spec_command(42, specs_root=tmp_path, output=str(output_path), commit=True)

        create_commit.assert_not_called()
