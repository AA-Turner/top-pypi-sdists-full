"""Prompt-assertion tests for agdt.address-copilot-review.evaluate-and-respond.prompt.md.

These tests verify that the prompt contains the correct instructions per the defect
fixes described in the issue: no force-push default, push verification, mandatory
repair-satisfied marker, terminal guard, and CCR body-only review handling.
"""

from __future__ import annotations

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[4]
_PROMPT_FILE = _REPO_ROOT / ".github" / "prompts" / "agdt.address-copilot-review.evaluate-and-respond.prompt.md"
_INSTRUCTIONS_FILE = _REPO_ROOT / ".github" / "copilot-instructions.md"


def _content() -> str:
    """Return the full prompt file content."""
    return _PROMPT_FILE.read_text(encoding="utf-8")


def _instructions_content() -> str:
    """Return the repo-wide Copilot instructions content."""
    return _INSTRUCTIONS_FILE.read_text(encoding="utf-8")


def _normalize(text: str) -> str:
    """Return ``text`` with blockquote markers dropped and whitespace runs collapsed.

    Assertions on prose that wraps across lines (or sits inside a ``>`` blockquote) stay
    valid when the markdown is re-wrapped.
    """
    without_blockquotes = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    return re.sub(r"\s+", " ", without_blockquotes)


def _normalized() -> str:
    """Return the full prompt content, normalized by :func:`_normalize`."""
    return _normalize(_content())


def _evidence_gate() -> str:
    """Return the normalized Phase 6 evidence-gate paragraph.

    The slice runs from the gate's opening line to the end of its blockquote paragraph
    (the next blank ``>`` line or the first non-blockquote line), so a growing gate can
    never push text under test outside the searched region.
    """
    lines = _content().splitlines()
    for index, line in enumerate(lines):
        if line.startswith("> **Evidence gate:**"):
            start = index
            break
    else:  # pragma: no cover - guarded by test_evidence_gate_* assertions
        raise AssertionError("The prompt no longer contains an evidence-gate blockquote paragraph")
    end = start + 1
    while end < len(lines) and lines[end].startswith(">") and lines[end].strip() != ">":
        end += 1
    return _normalize("\n".join(lines[start:end]))


def _decision_vocabulary() -> str:
    """Return the normalized Phase 7 Decision Vocabulary section.

    The slice ends at the next markdown heading or horizontal rule, so a growing table can
    never push the row under test outside the searched region.
    """
    content = _content()
    heading = "### Decision Vocabulary"
    body = content[content.index(heading) + len(heading) :]
    boundary = re.search(r"(?m)^(?:#{1,6} |---\s*$)", body)
    return _normalize(heading + body[: boundary.start() if boundary else len(body)])


class TestCommitFlowIsNewCommitNotAmend:
    """Defect 1 — The default commit flow must be new-commit + plain push."""

    def test_no_force_with_lease_in_prompt(self) -> None:
        """force-with-lease must not appear in any bash code block (execute path)."""
        content = _content()
        # Extract bash code blocks and check none contain force-with-lease
        code_blocks = re.findall(r"```bash[^\n]*\n(.*?)```", content, re.DOTALL)
        for block in code_blocks:
            assert "--force-with-lease" not in block, f"Found --force-with-lease in bash code block: {block[:200]}"

    def test_no_git_commit_amend_as_primary_flow(self) -> None:
        """git commit --amend must not appear as the primary/default commit action."""
        assert "git commit --amend" not in _content()

    def test_plain_git_push_present(self) -> None:
        """Plain 'git push' (new commit, no force flags) must be the default."""
        content = _content()
        assert re.search(r"^\s*git push\s*$", content, re.MULTILINE) is not None

    def test_ai_repair_marker_in_commit_body(self) -> None:
        """The [ai-repair] marker must still appear in the commit body template."""
        assert "[ai-repair]" in _content()

    def test_new_commit_instruction_present(self) -> None:
        """Prompt must instruct cloud agents to push a new commit (not amend)."""
        content = _content()
        assert "new commit" in content.lower()

    def test_no_amend_in_copilot_cloud_agent_restriction(self) -> None:
        """COPILOT CLOUD AGENT RESTRICTIONS must not recommend amend."""
        content = _content()
        # The restrictions block must say not to amend
        assert "Do NOT use `--amend`" in content


class TestPushVerification:
    """Defect 2 — Push verification via headRefOid comparison must be present."""

    def test_headrefoid_verification_present(self) -> None:
        """Prompt must include headRefOid comparison to verify push landed."""
        assert "headRefOid" in _content()

    def test_verify_push_section_present(self) -> None:
        """A 'Verify Push Was Successful' section must exist."""
        assert "Verify Push Was Successful" in _content()

    def test_retry_on_mismatch_instruction(self) -> None:
        """Prompt must instruct the agent to retry push on SHA mismatch."""
        content = _content()
        assert "do not match" in content.lower() or "still do not match" in content.lower()

    def test_hard_error_on_push_failure(self) -> None:
        """Prompt must require a hard error when push cannot be verified."""
        content = _content()
        assert "hard error" in content.lower() or "do NOT proceed" in content


class TestMandatoryRepairSatisfiedMarker:
    """Defect 3a — The repair-satisfied marker must be mandatory on the no-changes path."""

    def test_mandatory_marker_instruction_present(self) -> None:
        """Prompt must state the repair-satisfied marker is mandatory."""
        content = _content()
        assert "mandatory" in content.lower()
        assert "repair-satisfied" in content

    def test_marker_mandatory_for_suppressed_only_case(self) -> None:
        """Mandatory marker instruction must cover the suppressed-only case."""
        content = _content()
        assert "suppressed-only" in content

    def test_marker_mandatory_for_body_only_case(self) -> None:
        """Mandatory marker instruction must cover the CCR body-only case."""
        content = _content()
        assert "CCR body-only" in content or "body-only" in content


class TestTerminalGuard:
    """Defect 3b — An explicit terminal guard must prevent narration-only turns."""

    def test_terminal_guard_section_present(self) -> None:
        """A terminal guard section must exist."""
        assert "Terminal Turn Guard" in _content()

    def test_must_not_end_with_only_narration(self) -> None:
        """Prompt must explicitly prohibit ending a turn with only narrative description."""
        content = _content()
        assert "MUST NOT end your turn" in content or "must not end" in content.lower()

    def test_either_verified_push_or_marker_required(self) -> None:
        """Prompt must require either a verified push+summary or the repair-satisfied marker."""
        content = _content()
        assert "verified" in content
        assert "repair-satisfied" in content

    def test_narrating_fix_without_executing_is_failure(self) -> None:
        """Prompt must state that narrating an unexecuted fix is a failure."""
        content = _content()
        assert "failure" in content.lower()


class TestMalformedSuppressedEntries:
    """The repair gate must tolerate suppressed entries carrying no actionable anchor."""

    def test_malformed_subsection_present(self) -> None:
        """A 'Malformed suppressed entries' subsection must exist in Phase 2."""
        assert "#### Malformed suppressed entries" in _content()

    def test_malformed_definition_lists_all_three_disqualifiers(self) -> None:
        """The definition must cover missing path, non-repo-relative path, and short body."""
        prompt = _normalized()
        assert "it has no file path" in prompt
        assert "its path is not a repo-relative tracked file path" in prompt
        assert "git ls-files --error-unmatch -- <path>" in prompt
        assert "its body is under 80 characters with no actionable verb" in prompt

    def test_recovery_fetch_is_the_first_step(self) -> None:
        """Step 1 must be the one-attempt recovery fetch of the full review body."""
        prompt = _normalized()
        assert "1. Attempt one recovery: fetch the full review body with" in prompt
        assert "/reviews/{source_review_id}\" --jq '.body'` and locate the entry" in prompt
        assert "using that block's own `<!-- source-review-id:{id} -->` marker" in prompt

    def test_recovered_actionable_entry_is_evaluated_normally(self) -> None:
        """A recovered, actionable entry must still be evaluated like any other comment."""
        assert "If recovery yields an actionable comment, evaluate it normally." in _normalized()

    def test_recovery_fetch_failure_blocks_malformed_classification(self) -> None:
        """A failed recovery fetch must stop the malformed classification path."""
        prompt = _normalized()
        assert "If that recovery fetch fails, do NOT classify the entry as malformed" in prompt
        assert "report the failure instead" in prompt

    def test_malformed_entry_does_not_block_the_marker(self) -> None:
        """A malformed entry must be declared non-blocking for the repair-satisfied marker."""
        assert "A malformed entry does NOT block the `repair-satisfied` marker" in _normalized()

    def test_evidence_gate_names_the_malformed_classification(self) -> None:
        """The evidence gate must name the malformed class as a permitted classification."""
        gate = _evidence_gate()
        assert "classified it `⚪ Malformed (parser artifact)`" in gate
        assert "only after a successful recovery fetch confirmed that no actionable comment exists" in gate

    def test_evidence_gate_still_forbids_valid_actionable_entries(self) -> None:
        """The gate must still force a commit + push when any entry is valid and actionable."""
        gate = _evidence_gate()
        assert "`repair-satisfied` is FORBIDDEN" in gate
        assert "If even one entry is valid and actionable, you MUST commit + push a fix" in gate

    def test_decision_vocabulary_includes_malformed(self) -> None:
        """Phase 7's Decision Vocabulary must carry the malformed row."""
        assert "| Malformed | `⚪ Malformed (parser artifact)` |" in _decision_vocabulary()

    def test_justification_table_allows_dash_file_for_malformed(self) -> None:
        """The no-changes table's mandatory-File rule must except malformed entries."""
        prompt = _normalized()
        assert "The only exception is an entry classified `⚪ Malformed (parser artifact)`" in prompt

    def test_malformed_with_path_must_keep_path(self) -> None:
        """A malformed entry that still carries a path must not discard it."""
        prompt = _normalized()
        assert "that lacks a repo-relative path" in prompt
        assert "MUST keep that path" in prompt

    def test_no_non_termination_claim(self) -> None:
        """The prompt must not claim the loop is non-terminating or cannot converge."""
        prompt = _normalized().lower()
        assert "structurally non-terminating" not in prompt
        assert "cannot converge" not in prompt


class TestCCRBodyOnlyHandling:
    """Defect 3c — The CCR body-only review format must be explicitly handled."""

    def test_ccr_body_only_section_present(self) -> None:
        """A section explaining CCR body-only review format must exist."""
        content = _content()
        assert "CCR Body-Only Review" in content or "Body-Only Review" in content

    def test_fetch_review_body_instruction_present(self) -> None:
        """Prompt must instruct fetching the review body via the reviews API."""
        content = _content()
        assert "/reviews/{review_id}" in content

    def test_not_ready_to_approve_handling(self) -> None:
        """Prompt must handle 'Not ready to approve' body verdict."""
        content = _content()
        assert "Not ready to approve" in content

    def test_body_prose_triage_instruction(self) -> None:
        """Prompt must triage body prose just like inline comments."""
        content = _content()
        assert "body prose" in content or "prose" in content


class TestRepairNonNegotiables:
    """Repo-wide repair instructions must keep malformed-entry handling fail-closed."""

    def test_malformed_exception_requires_successful_recovery(self) -> None:
        """The repo-wide instructions must require a successful recovery fetch first."""
        instructions = _normalize(_instructions_content())
        assert "only after one successful recovery fetch confirmed no actionable comment exists" in instructions
        assert "`⚪ Malformed (parser artifact)`" in instructions


def _self_review_section() -> str:
    """Return the Phase 6a self-review section, up to the next ``###`` heading."""
    match = re.search(
        r"### Phase 6a: Self-Review Your Own Diff \(MANDATORY — do not skip\)\n(.*?)(?=\n### )",
        _content(),
        re.DOTALL,
    )
    assert match is not None, "The prompt no longer contains the Phase 6a self-review section"
    return match.group(1)


class TestSelfReviewGate:
    """The repair prompt must require a read-only diff self-review before staging."""

    def test_section_sits_between_targeted_tests_and_secret_scanning(self) -> None:
        """Phase 6a must be positioned between the targeted-test and secret-scan sections."""
        content = _content()
        tests_index = content.index("### Verify Changes with Targeted Tests")
        self_review_index = content.index("### Phase 6a: Self-Review Your Own Diff (MANDATORY — do not skip)")
        secret_index = content.index("### Secret Scanning Guard")
        assert tests_index < self_review_index < secret_index

    def test_all_seven_checks_present(self) -> None:
        """All seven review checks must be listed in the section."""
        section = _self_review_section()
        for check in (
            "Scope",
            "Minimality",
            "Surroundings",
            "Contract drift",
            "Claim accuracy",
            "New surface",
            "Cross-platform",
        ):
            assert f"| {check} |" in section

    def test_read_only_carve_out_present(self) -> None:
        """The section must state that `git diff` does not violate test-execution constraints."""
        section = _normalize(_self_review_section())
        assert "This step is **read-only**." in section
        assert "does not violate the test-execution constraints elsewhere in this prompt" in section

    def test_statistical_wording_is_hedged(self) -> None:
        """The measured share must be stated as a hedged bound, never as `88%`."""
        section = _normalize(_self_review_section())
        assert (
            "roughly 85% of review findings arrive after round 1, and **up to about half** of those "
            "sit on content that changed since the previous review" in section
        )
        assert "88%" not in _content()

    def test_output_table_is_required(self) -> None:
        """A self-review output table must be produced, not optionally offered."""
        section = _self_review_section()
        assert "Produce a short self-review table in your output:" in section
        assert (
            "| File | Hunk purpose | Scope OK | Minimal | Surroundings | Contract updated | "
            "Claim accuracy | New surface | Cross-platform |" in section
        )

    def test_diff_review_includes_staged_and_untracked_files(self) -> None:
        """The section must review staged/unstaged tracked changes and list untracked files."""
        section = _self_review_section()
        assert "git --no-pager diff --stat HEAD" in section
        assert "git --no-pager diff HEAD" in section
        assert "git ls-files --others --exclude-standard" in section

    def test_failing_row_blocks_staging(self) -> None:
        """A failing check must be fixed before staging."""
        section = _normalize(_self_review_section())
        assert "If any row fails, fix it **before** staging." in section

    def test_self_review_loops_until_final_diff_passes(self) -> None:
        """Post-table edits must force a repeat self-review and targeted re-test."""
        section = _normalize(_self_review_section())
        assert "This is a loop, not a one-time check:" in section
        assert "return to the start of Phase 6a and re-review the new diff" in section
        assert "Re-run targeted tests for affected files before staging the revised diff" in section


class TestScopeGuardConsistency:
    """Phase 4 scope guard must align with the expanded self-review scope rule."""

    def test_scope_guard_allows_directly_required_companion_changes(self) -> None:
        """Scope guard must allow files directly required to complete a named fix."""
        normalized = _normalized()
        assert "named by a review comment/CI failure" in normalized
        assert "directly required to complete that fix" in normalized


class TestTriggerTemplateMatchesBuilder:
    """The reference template must carry the same literals the builder emits."""

    def test_reference_template_contains_every_structural_literal(self) -> None:
        """Mirror of ``test_rendered_body_emits_the_documented_structural_literals``.

        That builder-side test pins the same literals on the producing side; this one pins
        them on the consuming side, so a one-sided edit reds exactly one of the pair.
        """
        content = _content()
        assert "<!-- repair-section:author-comments -->" in content
        assert "<!-- repair-section:code-review-agent-comments -->" in content
        assert "<!-- repair-comment-section -->" in content
        assert "**Link to original comment:**" in content
        assert "**File:**" in content
        assert "**Lines:**" in content
        assert "Comment:" in content
        assert "<!-- source-review-id:" in content
        assert "## How to decide on each comment" in content
        assert "## Comments from the PR author" in content
        assert "## Comments from the Code Review Agent" in content
        assert "## CI failures" in content
        assert "## Instructions" in content
        assert "## Original Code Review Thread" in content

    def test_reference_template_documents_metadata_path_decoding(self) -> None:
        """The consumer must decode escaped metadata paths before shelling out."""
        normalized = _normalized()
        assert "Decode JSON-style escapes (`\\\\n`, `\\\\r`, `\\\\t`, `\\\\uXXXX`) before using the path" in normalized
        assert "decode those escapes before passing the path to `git` or any shell command" in normalized

    def test_reference_template_contains_no_removed_literal(self) -> None:
        """Literals the builder no longer emits must not survive in the prompt."""
        content = _content()
        assert "Diff context:" not in content
        assert "(suppressed comment)" not in content
        assert "lives in the review body" not in content
        assert "<summary>Comment " not in content
        assert "<summary>Failure " not in content
        assert "<summary>Instructions</summary>" not in content
        assert "<summary>Original Code Review Thread</summary>" not in content
        assert "follow this prompt rather than any stale copy of the older collapsed-markup guidance" not in content

    def test_reference_template_links_both_files_and_keeps_prompt_authoritative(self) -> None:
        """The Instructions block must link both files while keeping the prompt authoritative."""
        prompt = _normalized()
        assert "You are the [`.github/agents/agdt.address-copilot-review.evaluate-and-respond.agent.md`](" in prompt
        assert "The authoritative dispatch-format instructions for this run are in" in prompt
        assert "Read and follow both referenced files before beginning your work." in prompt
        assert "the agent file supplies the workflow contract" in prompt
        assert "this prompt supplies the authoritative dispatch-format contract" in prompt

    def test_reference_template_carries_the_full_section_lead_in_paragraphs(self) -> None:
        """Both lead-ins must be reproduced unabbreviated, ending clause included."""
        prompt = _normalized()
        assert "so I know what was decided in each case and why." in prompt
        assert "Therefore, for each comment you have 4 options:" in prompt
        assert (
            "After you have replied to each comment, ensure that it is resolved and closed as well, "
            "so that those comments no longer block a merge." in prompt
        )


class TestValidationRules:
    """Summary-table and validation rules that depend on the partitioned format."""

    def test_row_count_rule_counts_comment_blocks_across_both_sections(self) -> None:
        """The one-row-per-comment rule must span both sections, not just one."""
        assert (
            "Numbering is global and monotonic across both sections, so this is a single count "
            "over the whole trigger comment." in _normalized()
        )

    def test_validation_refetch_rule_still_names_the_comment_block_token(self) -> None:
        """The block token the fallback keys on must survive verbatim."""
        assert "### Comment {N} - " in _content()


class TestAuthorSectionHandling:
    """Author-section comments must never be round-tripped to the review."""

    def test_author_section_must_not_be_round_tripped_to_the_review(self) -> None:
        """An empty inline-comment fetch is not evidence an author comment does not exist."""
        assert (
            "fetching the review to look for them will find nothing and MUST NOT be read as "
            '"there were no such comments"' in _normalized()
        )
