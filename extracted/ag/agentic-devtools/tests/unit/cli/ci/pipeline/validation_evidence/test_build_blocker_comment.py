from agentic_devtools.cli.ci.pipeline.validation_evidence import (
    BLOCKER_MARKER,
    EVIDENCE_REQUIRED_LABEL,
    build_blocker_comment,
)


def test_builds_human_actionable_blocker_comment_with_final_marker() -> None:
    head_sha = "0123456789abcdef0123456789abcdef01234567"

    comment = build_blocker_comment(head_sha)

    assert not comment.startswith("@copilot")
    assert head_sha in comment
    assert "still missing" in comment
    assert "after one recovery" in comment
    assert "will not publish" in comment
    assert "obtaining or verifying an agent-authored" in comment
    assert "`## Validation evidence` comment for this exact head" in comment
    assert "configured Cloud Coding Agent identity or `Copilot`" in comment
    assert f"removing the `{EVIDENCE_REQUIRED_LABEL}` label" in comment
    assert comment.splitlines()[-1] == BLOCKER_MARKER
