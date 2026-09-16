"""Tests for _build_reformulated_prompt."""

from dataclasses import dataclass, field
from typing import cast

from agentic_devtools.cli.ci.resolution.github_adapter import GitHubThreadComment
from agentic_devtools.cli.ci.resolution.protocols import ResolutionContext, ReviewThread
from agentic_devtools.cli.ci.resolution.tiers.sdk_evaluation import _build_reformulated_prompt


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


def test_prompt_includes_evidence_and_basis_contract() -> None:
    context = _MockContext(
        post_review_copilot_comments=(
            GitHubThreadComment(
                body="The reviewer explicitly rejected this concern.",
                created_at="2026-01-02T00:00:00Z",
                author_login="copilot-swe-agent[bot]",
            ),
        )
    )

    prompt = _build_reformulated_prompt(
        cast(ReviewThread, _MockThread()),
        cast(ResolutionContext, context),
    )

    assert "## Post-Review Copilot Evidence" in prompt
    assert "[2026-01-02T00:00:00Z] @copilot-swe-agent[bot]" in prompt
    assert "The reviewer explicitly rejected this concern." in prompt
    assert prompt.count("BASIS: code_change | explicit_rejection | out_of_scope | unresolve") == 2
    assert prompt.endswith("EXPLANATION: <your reasoning>")
