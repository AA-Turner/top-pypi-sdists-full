"""Tests for classify_writer_outcome."""

import pytest

from agentic_devtools.cli.ci.pipeline.writer_outcome import WriterOutcome, classify_writer_outcome

_DISPATCH = "a" * 40
_CURRENT = "b" * 40


@pytest.mark.parametrize(
    ("dispatch", "current", "evidence", "expected"),
    [
        (_DISPATCH, _DISPATCH, [_DISPATCH], WriterOutcome.NO_PUSH),
        (_DISPATCH, _CURRENT, [_CURRENT], WriterOutcome.PUSHED_WITH_EVIDENCE),
        (_DISPATCH, _CURRENT, ["c" * 40], WriterOutcome.PUSHED_WITHOUT_EVIDENCE),
        (_DISPATCH, _CURRENT, [], WriterOutcome.PUSHED_WITHOUT_EVIDENCE),
    ],
)
def test_classifies_valid_finished_heads(
    dispatch: str, current: str, evidence: list[str], expected: WriterOutcome
) -> None:
    """Valid finished heads distinguish unchanged, evidenced, and unevidenced outcomes."""
    assert (
        classify_writer_outcome(
            dispatch_head_sha=dispatch,
            current_head_sha=current,
            session_finished=True,
            evidence_head_shas=evidence,
        )
        is expected
    )


@pytest.mark.parametrize(
    "invalid_sha",
    ["a" * 39, "a" * 41, "g" * 40, " " + "a" * 39, "a" * 39 + " ", "a" * 39 + "\n", "é" + "a" * 39],
    ids=("short", "long", "non-hex", "leading-space", "trailing-space", "newline", "non-ascii"),
)
@pytest.mark.parametrize("location", ["dispatch", "current", "evidence"])
def test_rejects_invalid_sha_at_every_identity_location(invalid_sha: str, location: str) -> None:
    """Every supplied identity must be exactly forty ASCII hexadecimal characters."""
    dispatch, current, evidence = _DISPATCH, _CURRENT, []
    if location == "dispatch":
        dispatch = invalid_sha
    elif location == "current":
        current = invalid_sha
    else:
        evidence = [invalid_sha]
    assert (
        classify_writer_outcome(
            dispatch_head_sha=dispatch,
            current_head_sha=current,
            session_finished=True,
            evidence_head_shas=evidence,
        )
        is WriterOutcome.UNKNOWN
    )


def test_unfinished_session_is_unknown() -> None:
    """An unfinished session is unknown even when its heads are otherwise valid."""
    assert (
        classify_writer_outcome(
            dispatch_head_sha=_DISPATCH,
            current_head_sha=_DISPATCH,
            session_finished=False,
            evidence_head_shas=[],
        )
        is WriterOutcome.UNKNOWN
    )


def test_invalid_late_evidence_is_unknown_even_after_an_earlier_match() -> None:
    """A late invalid evidence SHA cannot be hidden by an earlier matching identity."""
    seen: list[str] = []

    def evidence():
        for sha in (_CURRENT.upper(), "invalid"):
            seen.append(sha)
            yield sha

    assert (
        classify_writer_outcome(
            dispatch_head_sha=_DISPATCH,
            current_head_sha=_CURRENT,
            session_finished=True,
            evidence_head_shas=evidence(),
        )
        is WriterOutcome.UNKNOWN
    )
    assert seen == [_CURRENT.upper(), "invalid"]


def test_invalid_evidence_precedes_unchanged_head_outcome() -> None:
    """Invalid evidence keeps an unchanged-head result unknown."""
    assert (
        classify_writer_outcome(
            dispatch_head_sha=_DISPATCH,
            current_head_sha=_DISPATCH.upper(),
            session_finished=True,
            evidence_head_shas=["x" * 40],
        )
        is WriterOutcome.UNKNOWN
    )


def test_normalizes_heads_and_evidence_before_comparison() -> None:
    """Mixed-case equal heads and evidence membership compare as the same SHA."""
    assert (
        classify_writer_outcome(
            dispatch_head_sha=_DISPATCH.upper(),
            current_head_sha=_CURRENT.upper(),
            session_finished=True,
            evidence_head_shas=[_CURRENT],
        )
        is WriterOutcome.PUSHED_WITH_EVIDENCE
    )
    assert (
        classify_writer_outcome(
            dispatch_head_sha=_DISPATCH,
            current_head_sha=_DISPATCH.upper(),
            session_finished=True,
            evidence_head_shas=[],
        )
        is WriterOutcome.NO_PUSH
    )
