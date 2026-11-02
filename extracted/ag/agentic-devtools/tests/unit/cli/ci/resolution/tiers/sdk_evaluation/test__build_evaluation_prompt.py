"""Tests for the SDK evaluation prompt builder."""

from dataclasses import dataclass, field
from typing import cast

from agentic_devtools.cli.ci.models import CopilotSessionSummary
from agentic_devtools.cli.ci.resolution.github_adapter import GitHubThreadComment
from agentic_devtools.cli.ci.resolution.protocols import ResolutionContext, ReviewThread
from agentic_devtools.cli.ci.resolution.tiers.sdk_evaluation import _build_evaluation_prompt


@dataclass(frozen=True)
class _MockComment:
    body: str = "fix the typo"


@dataclass(frozen=True)
class _MockThread:
    file_path: str | None = "src/main.py"
    start_line: int | None = 10
    end_line: int | None = 10
    comments: list = field(default_factory=lambda: [_MockComment()])


@dataclass(frozen=True)
class _MockContext:
    diff_text: str = "diff content"
    head_commit_oid: str = "head123"
    post_review_copilot_comments: tuple = ()
    post_review_session_summaries: tuple = ()


def test_prompt_includes_post_review_copilot_evidence() -> None:
    context = _MockContext(
        post_review_copilot_comments=(
            GitHubThreadComment(
                body="The reviewer explicitly rejected this concern.",
                created_at="2026-01-02T00:00:00Z",
                author_login="copilot-swe-agent[bot]",
            ),
        )
    )

    prompt = _build_evaluation_prompt(
        cast(ReviewThread, _MockThread()),
        cast(ResolutionContext, context),
    )

    assert "## Post-Review Copilot Evidence" in prompt
    assert "2026-01-02T00:00:00Z" in prompt
    assert "@copilot-swe-agent[bot]" in prompt
    assert "explicitly rejected" in prompt
    assert "only when supported by the Post-Review Copilot Evidence section" in prompt


def test_prompt_includes_session_summaries() -> None:
    """Adds supplementary cloud-agent summaries to the SDK prompt."""
    prompt = _build_evaluation_prompt(
        cast(ReviewThread, _MockThread()),
        cast(
            ResolutionContext,
            _MockContext(
                post_review_session_summaries=(
                    CopilotSessionSummary("task-1", "session-1", 42, "2026-01-02", finishing_text="Ran tests."),
                )
            ),
        ),
    )

    assert "## Supplementary Copilot Cloud-Agent Summaries" in prompt
    assert "Ran tests." in prompt
