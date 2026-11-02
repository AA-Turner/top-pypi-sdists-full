"""Tests for the private dispatch-marker helper."""

from agentic_devtools.cli.github.single_finding_dispatch import SingleFindingHandoff
from agentic_devtools.cli.github.single_finding_dispatch_host import _dispatch_marker


def test_dispatch_marker_identifies_repository_pr_head_and_finding(handoff: SingleFindingHandoff) -> None:
    assert _dispatch_marker(handoff) == (
        "<!-- agdt:ai-pr-loop-dispatch repo=example/project pr=7 "
        f"head={handoff.expected_head} finding={handoff.finding_id} -->"
    )
