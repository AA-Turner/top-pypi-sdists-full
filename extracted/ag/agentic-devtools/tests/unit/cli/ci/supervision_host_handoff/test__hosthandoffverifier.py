from agentic_devtools.cli.ci.supervision_host_handoff import (
    HostHandoffRejectionReason,
    _HostHandoffVerifier,
)


def test_empty_candidate_collection_returns_no_record() -> None:
    verifier = _HostHandoffVerifier(
        {
            "repository": "swai-factory/agentic-devtools",
            "role": "admission",
            "mode": "maintain",
            "supervisor_run_id": "2026-10-22T00:00:00Z-a1b2c3",
            "checkpoint": "checkpoint-42",
        },
        {"hostuser"},
        (0, ""),
    )

    result = verifier.verify([])

    assert result.accepted is False
    assert result.reason is HostHandoffRejectionReason.NO_RECORD
    assert result.payload is None
