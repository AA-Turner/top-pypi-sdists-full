"""Tests for supervisor candidate fingerprints."""

from agentic_devtools.cli.ci.supervisor import (
    SupervisorClassification,
    SupervisorState,
    build_supervisor_fingerprint,
)


def test_build_supervisor_fingerprint_is_stable_and_identity_specific() -> None:
    classification = SupervisorClassification(SupervisorState.STUCK_CANDIDATE, ("stale_loop_run",))

    first = build_supervisor_fingerprint("swai-factory/agentic-devtools", 7, "a" * 40, classification)
    second = build_supervisor_fingerprint("swai-factory/agentic-devtools", 7, "a" * 40, classification)
    different_head = build_supervisor_fingerprint("swai-factory/agentic-devtools", 7, "b" * 40, classification)

    assert first == second
    assert len(first) == 64
    assert first != different_head


def test_build_supervisor_fingerprint_rejects_invalid_identity() -> None:
    classification = SupervisorClassification(SupervisorState.UNKNOWN, ())
    invalid_values = [
        ("", 7, "a" * 40),
        ("o/r", 0, "a" * 40),
        ("o/r", 7, ""),
    ]

    for repository, pr_number, head_sha in invalid_values:
        try:
            build_supervisor_fingerprint(repository, pr_number, head_sha, classification)
        except ValueError:
            continue
        raise AssertionError("expected invalid fingerprint identity to raise")
