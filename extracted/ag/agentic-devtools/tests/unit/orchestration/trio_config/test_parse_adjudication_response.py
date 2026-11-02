"""Tests for ``parse_adjudication_response``."""

import pytest

from agentic_devtools.orchestration.trio_config import (
    AdjudicationPolicy,
    AdjudicationResult,
    parse_adjudication_response,
)


def test_parse_adjudication_response_counts_all_verdict_types_and_empty_results() -> None:
    policy = AdjudicationPolicy(True, True, True)
    text = "\n".join(
        [
            "POINT one: ACCEPT | EVIDENCE: clause: A",
            "POINT two: REJECT | EVIDENCE: line: 2",
            "POINT three: OVERTURN | EVIDENCE: clause: C",
            "POINT four: UPHOLD_REJECTION | EVIDENCE: line: 4",
            "RESPONSE_COMPLETE: accepted=2 rejected=2 total=4",
        ]
    )
    result = parse_adjudication_response(text, ["one", "two", "three", "four"], policy=policy)
    assert result.accepted == 2
    assert result.rejected == 2
    assert result.total == 4
    assert result.decisions == result.point_verdicts
    assert AdjudicationResult(()) == parse_adjudication_response(
        "RESPONSE_COMPLETE: accepted=0 rejected=0 total=0",
        [],
        policy=policy,
    )
    ordered_from_set = parse_adjudication_response(
        "POINT beta: ACCEPT | EVIDENCE: clause: B\n"
        "POINT alpha: ACCEPT | EVIDENCE: clause: A\n"
        "RESPONSE_COMPLETE: accepted=2 rejected=0 total=2",
        {"beta", "alpha"},
        policy=policy,
    )
    assert [decision.point_id for decision in ordered_from_set.point_verdicts] == ["alpha", "beta"]


def test_parse_adjudication_response_rejects_invalid_inputs_and_disputes() -> None:
    policy = AdjudicationPolicy(True, True, True)
    with pytest.raises(ValueError):
        parse_adjudication_response(None, [], policy=policy)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        parse_adjudication_response("", "one", policy=policy)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        parse_adjudication_response("", 1, policy=policy)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        parse_adjudication_response("", ["one", "one"], policy=policy)
    with pytest.raises(ValueError):
        parse_adjudication_response("", [1], policy=policy)  # type: ignore[list-item]
    with pytest.raises(ValueError):
        parse_adjudication_response("", [[]], policy=policy)  # type: ignore[list-item]
    with pytest.raises(ValueError):
        parse_adjudication_response("POINT one: ACCEPT | EVIDENCE: clause: A", ["one"], policy=policy)
    with pytest.raises(ValueError):
        parse_adjudication_response(
            "POINT one: ACCEPT | EVIDENCE: clause: unresolved dispute\n"
            "RESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
            ["one"],
            policy=policy,
        )
    with pytest.raises(ValueError):
        parse_adjudication_response(
            "POINT one: ACCEPT | EVIDENCE: line: 4 confirms there is no unresolved dispute, "
            "but line: 6 remains disputed\nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
            ["one"],
            policy=policy,
        )
    with pytest.raises(ValueError):
        parse_adjudication_response(
            "POINT one: ACCEPT | EVIDENCE: clause: A\nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
            ["one", "two"],
            policy=policy,
        )


@pytest.mark.parametrize(
    "evidence",
    [
        "line: 4 resolves the dispute",
        "line: 4 is not disputed",
        "line: 4 confirms there is no unresolved dispute",
    ],
)
def test_parse_adjudication_response_allows_resolved_dispute_language(evidence: str) -> None:
    policy = AdjudicationPolicy(True, True, True)
    text = f"POINT one: ACCEPT | EVIDENCE: {evidence}\nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1"
    result = parse_adjudication_response(text, ["one"], policy=policy)
    assert result.accepted == 1
    assert result.rejected == 0


@pytest.mark.parametrize(
    "text",
    [
        "POINT one: OVERTURN | EVIDENCE: clause: A\nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
        "POINT one: ACCEPT | EVIDENCE: no reference\nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
        "POINT one: ACCEPT | EVIDENCE: declause: A\nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
        "POINT one: ACCEPT | EVIDENCE: clause:   \nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
        "POINT one: ACCEPT | EVIDENCE: line:\nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
        "POINT one: ACCEPT | EVIDENCE: clause: A\n"
        "POINT one: REJECT | EVIDENCE: clause: B\n"
        "RESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
        "POINT other: ACCEPT | EVIDENCE: clause: A\nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
        "POINT one: ACCEPT | EVIDENCE: clause: A\nextra\nRESPONSE_COMPLETE: accepted=1 rejected=0 total=1",
        "POINT one: ACCEPT | EVIDENCE: clause: A\nRESPONSE_COMPLETE: accepted=0 rejected=1 total=1",
    ],
)
def test_parse_adjudication_response_rejects_policy_grammar_and_count_errors(text: str) -> None:
    policy = AdjudicationPolicy(False, True, True)
    with pytest.raises(ValueError):
        parse_adjudication_response(text, ["one"], policy=policy)
