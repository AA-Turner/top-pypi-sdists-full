"""Prompt-assertion tests for agdt.address-copilot-review.ci-repair.prompt.md."""

from __future__ import annotations

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[4]
_PROMPT_FILE = _REPO_ROOT / ".github" / "prompts" / "agdt.address-copilot-review.ci-repair.prompt.md"


def _content() -> str:
    """Return the full prompt file content."""
    return _PROMPT_FILE.read_text(encoding="utf-8")


def _commit_and_push_block() -> str:
    """Return the bash block in the Commit & Push section."""
    match = re.search(r"### Commit & Push.*?```bash\n(.*?)```", _content(), re.DOTALL)
    assert match is not None
    return match.group(1)


class TestCommitAndPushFlow:
    """The repair prompt must not continue to push after a failed commit."""

    def test_push_depends_on_successful_commit(self) -> None:
        """The commit example must chain push to a successful commit."""
        block = _commit_and_push_block()
        assert "&& git push" in block
        assert re.search(r"^\s*git push\s*$", block, re.MULTILINE) is None


def _normalize(text: str) -> str:
    """Return ``text`` with blockquote markers dropped and whitespace runs collapsed."""
    without_blockquotes = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    return re.sub(r"\s+", " ", without_blockquotes)


def _self_review_section() -> str:
    """Return the Phase 4a self-review section, up to the next ``###`` heading."""
    match = re.search(
        r"### Phase 4a: Self-Review Your Own Diff \(MANDATORY — do not skip\)\n(.*?)(?=\n### )",
        _content(),
        re.DOTALL,
    )
    assert match is not None, "The CI-repair prompt no longer contains the Phase 4a self-review section"
    return match.group(1)


class TestSelfReviewGate:
    """The repair prompt must require a read-only diff self-review before staging."""

    def test_section_precedes_staging(self) -> None:
        """The self-review heading must come before the staging/secret-scan section."""
        content = _content()
        self_review_index = content.index("### Phase 4a: Self-Review Your Own Diff (MANDATORY — do not skip)")
        staging_index = content.index("### Stage Changes and Secret Scanning Guard")
        assert self_review_index < staging_index

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

    def test_self_review_is_repeated_after_post_table_edits(self) -> None:
        """Any edit after the table must rerun Phase 4a before staging."""
        section = _normalize(_self_review_section())
        assert "This is a loop, not a one-time check" in section
        assert "return to the start of Phase 4a and re-review the updated diff before staging" in section
