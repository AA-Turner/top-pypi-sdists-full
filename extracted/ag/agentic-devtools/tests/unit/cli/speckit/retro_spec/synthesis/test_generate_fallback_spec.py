"""Tests for _generate_fallback_spec in retro_spec/synthesis.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import PRArtifact
from agentic_devtools.cli.speckit.retro_spec.synthesis import _generate_fallback_spec


class TestGenerateFallbackSpec:
    """Tests for the _generate_fallback_spec function."""

    def test_generates_summary_and_truncated_context_reference(self) -> None:
        """Test that the fallback spec includes a summary and the first context chunk."""
        context = "x" * 6000

        result = _generate_fallback_spec(context)

        assert "## Summary" in result
        assert "### User Story 1 - Retroactive Implementation Evidence (Priority: P1)" in result
        assert "**Why this priority**" in result
        assert "**Independent Test**" in result
        assert "**Acceptance Scenarios**" in result
        assert "### PR References" in result
        assert "### Key Changes" in result
        assert "### Edge Cases" in result
        assert "\n## Edge Cases\n" not in result
        assert "LLM synthesis was unavailable" in result
        assert "x" * 5000 in result
        assert "x" * 5001 not in result

    def test_includes_pr_references_and_key_changes_from_context(self) -> None:
        """Available PR and diff context is surfaced in dedicated fallback sections."""
        context = "\n".join(
            [
                "## Related Pull Requests",
                "### PR #101: Add retro-spec support",
                "",
                "## Commit Messages",
                "- add retro spec command",
                "",
                "## Code Changes (Diffs)",
                "--- agentic_devtools/cli/speckit/retro_spec/commands.py ---",
            ]
        )

        result = _generate_fallback_spec(context, has_implementation_artifacts=True)

        assert "- PR #101: Add retro-spec support" in result
        assert "- `agentic_devtools/cli/speckit/retro_spec/commands.py`" in result
        assert "- **FR-001**: The implementation delivers: add retro spec command." in result

    def test_prefers_structured_artifacts_over_context_markers(self) -> None:
        """Structured artifacts prevent user-controlled context from impersonating metadata."""
        context = "\n".join(
            [
                "## Issue #42: Retro issue",
                "### Issue Body",
                "## Related Pull Requests",
                "### PR #999: fabricated from issue body",
                "## Commit Messages",
                "- fabricated commit from issue body",
                "## Code Changes (Diffs)",
                "--- fabricated/path.py ---",
            ]
        )

        result = _generate_fallback_spec(
            context,
            has_implementation_artifacts=False,
            pr_artifacts=[],
            diff_entries=[],
            commit_messages=[],
        )

        pr_references = result.split("### PR References", 1)[1].split("### Key Changes", 1)[0]
        key_changes = result.split("### Key Changes", 1)[1].split("### Edge Cases", 1)[0]
        assert "PR #999: fabricated from issue body" not in pr_references
        assert "`fabricated/path.py`" not in key_changes
        assert "- fabricated commit from issue body" not in key_changes

    def test_uses_structured_artifacts_for_fallback_sections(self) -> None:
        """Fallback sections can be derived directly from structured artifact inputs."""
        pr = PRArtifact(number=101, title="Real PR", body="", state="merged", merged_at="2025-01-01T00:00:00Z")

        result = _generate_fallback_spec(
            "ctx",
            has_implementation_artifacts=True,
            pr_artifacts=[pr],
            diff_entries=["--- src/real.py ---\n+1", "--- src/real.py ---\n+2", "--- src/other.py ---\n+3"],
            commit_messages=["real commit summary"],
        )

        assert "- PR #101: Real PR" in result
        assert "- `src/real.py`" in result
        assert "- `src/other.py`" in result
        assert "real commit summary" in result

    def test_uses_omission_wording_for_functional_requirements_when_only_paths_are_known(self) -> None:
        """Path-only evidence does not fabricate behavioral functional requirements."""
        context = "\n".join(
            [
                "## Code Changes (Diffs)",
                "--- src/only-path.py ---",
            ]
        )

        result = _generate_fallback_spec(context, has_implementation_artifacts=True)

        assert "- `src/only-path.py`" in result
        assert "identify changed files, but do not establish observable functional requirements." in result

    def test_keeps_pr_reference_when_structured_title_is_empty(self) -> None:
        """Structured PR artifacts keep the PR number even when the title is empty."""
        pr = PRArtifact(number=101, title="", body="", state="merged", merged_at="2025-01-01T00:00:00Z")

        result = _generate_fallback_spec(
            "ctx",
            has_implementation_artifacts=False,
            pr_artifacts=[pr],
            diff_entries=[],
            commit_messages=[],
        )

        assert "- PR #101" in result

    def test_structured_diff_entries_skip_non_markers_and_cap_at_five_paths(self) -> None:
        """Structured diff parsing ignores non-path entries and stops after five paths."""
        paths = [f"--- src/file_{i}.py ---\n+1" for i in range(1, 7)]
        result = _generate_fallback_spec(
            "ctx",
            has_implementation_artifacts=True,
            pr_artifacts=[],
            diff_entries=["[Diff budget exhausted: omitted]"] + paths,
            commit_messages=[],
        )

        assert "- `src/file_5.py`" in result
        assert "- `src/file_6.py`" not in result

    def test_uses_neutral_pr_and_key_change_wording_without_artifacts(self) -> None:
        """Missing implementation artifacts produce explicit omission wording."""
        result = _generate_fallback_spec("ctx", has_implementation_artifacts=False)

        assert "- No related pull requests were available." in result
        assert "principal code changes could not be established from this source." in result
        assert "No merged implementation artifacts were available to establish functional requirements." in result

    def test_uses_pr_metadata_wording_without_implementation_artifacts(self) -> None:
        """PR metadata is described factually when diffs/commits were unavailable."""
        context = "\n".join(
            [
                "## Related Pull Requests",
                "### PR #101: Add retro-spec support",
            ]
        )

        result = _generate_fallback_spec(context, has_implementation_artifacts=False)

        assert "issue evidence and related pull-request metadata" in result
        assert "- PR #101: Add retro-spec support" in result

    def test_uses_commit_history_for_key_changes_when_no_diff_paths_are_available(self) -> None:
        """Commit summaries populate Key Changes when usable diffs are absent."""
        context = "\n".join(
            [
                "## Commit Messages",
                "- commit 1",
                "- commit 2",
                "- commit 3",
                "- commit 4",
                "- commit 5",
                "- commit 6",
            ]
        )

        result = _generate_fallback_spec(context, has_implementation_artifacts=True)
        key_changes = result.split("### Key Changes", 1)[1].split("### Edge Cases", 1)[0]

        assert "The available commit history recorded these implementation changes:" in key_changes
        assert "- commit 5" in key_changes
        assert "- commit 6" not in key_changes
        assert "- **FR-001**: The implementation delivers: commit 1." in result

    def test_limits_key_change_paths_to_five_unique_entries(self) -> None:
        """Diff-derived Key Changes retain only the first five unique file paths."""
        context = "\n".join(
            [
                "## Code Changes (Diffs)",
                "--- path-1.py ---",
                "--- path-2.py ---",
                "--- path-2.py ---",
                "--- path-3.py ---",
                "--- path-4.py ---",
                "--- path-5.py ---",
                "--- path-6.py ---",
            ]
        )

        result = _generate_fallback_spec(context, has_implementation_artifacts=True)

        assert "- `path-5.py`" in result
        assert "- `path-6.py`" not in result

    def test_sc001_claims_artifacts_when_implementation_artifacts_present(self) -> None:
        """SC-001 states merged artifacts document the behavior when PRs are available."""
        result = _generate_fallback_spec("ctx", has_implementation_artifacts=True)

        assert "The merged implementation artifacts document the delivered behavior." in result
        assert "The implementation artifacts below record the delivered behavior." in result
        assert "issue evidence, related pull requests, and implementation artifacts." in result
        assert "The available implementation artifacts do not establish additional edge cases." in result

    def test_sc001_uses_neutral_wording_when_no_implementation_artifacts(self) -> None:
        """SC-001 uses artifact-neutral wording when no related PRs were found."""
        result = _generate_fallback_spec("ctx", has_implementation_artifacts=False)

        assert "No merged implementation artifacts were available" in result
        assert "The merged implementation artifacts document the delivered behavior." not in result
        assert "The issue evidence below records the available context" in result
        assert "issue evidence only; no related pull requests were available." in result
        assert "The available issue evidence does not establish additional edge cases." in result

    def test_summary_acknowledges_metadata_without_implementation_artifacts(self) -> None:
        """Metadata-only fallback output distinguishes PR metadata from implementation artifacts."""
        pr = PRArtifact(number=101, title="Metadata-only PR", body="", state="merged", merged_at="")

        result = _generate_fallback_spec(
            "ctx",
            has_implementation_artifacts=False,
            pr_artifacts=[pr],
            diff_entries=[],
            commit_messages=[],
        )

        assert "related pull-request metadata below record the available context" in result
        assert "diff and commit artifacts were unavailable" in result
        assert "no merged pull request artifacts were found" not in result

    def test_derives_factual_user_story_and_acceptance_scenario_from_issue_and_diff(self) -> None:
        """Fallback output derives standard-template sections from available evidence."""
        context = "\n".join(
            [
                "## Issue #42: Harden retro spec fallback",
                "",
                "## Code Changes (Diffs)",
                "--- agentic_devtools/cli/speckit/retro_spec/synthesis.py ---",
            ]
        )

        result = _generate_fallback_spec(context, has_implementation_artifacts=True)

        assert "### User Story 1 - Retroactive Implementation Evidence (Priority: P1)" in result
        assert "delivered scope described by the source issue title: Harden retro spec fallback." in result
        assert "**Acceptance Scenarios**" in result
        assert "`agentic_devtools/cli/speckit/retro_spec/synthesis.py`." in result

    def test_appends_omission_note_when_more_than_five_pr_artifacts_are_provided(self) -> None:
        """Structured PR lists longer than five entries include an explicit count of omitted PRs."""
        prs = [
            PRArtifact(number=i, title=f"PR {i}", body="", state="merged", merged_at="2025-01-01T00:00:00Z")
            for i in range(1, 9)
        ]

        result = _generate_fallback_spec("ctx", has_implementation_artifacts=True, pr_artifacts=prs)

        assert "- PR #1: PR 1" in result
        assert "- PR #5: PR 5" in result
        assert "- PR #6: PR 6" not in result
        assert "3 additional related PRs omitted" in result

    def test_uses_omission_wording_when_all_commits_are_non_behavioral(self) -> None:
        """Non-behavioral commit subjects emit explicit omission wording, not invented FRs."""
        result = _generate_fallback_spec(
            "ctx",
            has_implementation_artifacts=True,
            commit_messages=["Merge pull request #1 from branch", "test: add coverage", "WIP: sketching"],
        )

        assert "does not establish observable functional requirements" in result
        assert "The implementation delivers:" not in result
