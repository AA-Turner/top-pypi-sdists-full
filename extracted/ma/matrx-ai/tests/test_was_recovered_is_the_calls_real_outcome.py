"""``was_recovered`` ON A STRUCTURED-OUTPUT FINDING IS A MEASUREMENT, NEVER A DEFAULT.

Arman's rule: nothing fails silently and a log NEVER lies. A finding that says
``was_recovered = true`` is telling a reader "the compromise this row describes
worked out" — so it may only be written once that is a fact.

The defect these checks exist for (SCHEMA-TRANSLATION-VERIFY.md, **F2**): every
translation-time write in ``flush_translation_findings`` passed no
``was_recovered`` at all and took ``record_structured_output_finding``'s default
``True``. All 279 live translation findings in ``ops.ops_issue_event`` read
``was_recovered = true``, including on requests whose answer was then recorded
OFF CONTRACT. The gate half read only whether the CALL returned, so a served
call whose answer missed the contract also read "recovered".

Every check below fails on the pre-fix tree (``git show HEAD:<path> > <path>``):
the first two because ``flush_translation_findings`` has no
``answer_off_contract`` parameter, the third because the seam never told it what
the answer check found, and the last because the truth table did not exist.
"""

from __future__ import annotations

import asyncio
import contextlib
import io
from types import SimpleNamespace
from typing import Any

import pytest

DECLARED: dict[str, Any] = {
    "type": "object",
    "required": ["verdict", "score"],
    "additionalProperties": False,
    "properties": {"verdict": {"type": "string"}, "score": {"type": "integer"}},
}

#: What a model answers when it missed the contract: `score` is not an integer.
OFF_CONTRACT_ANSWER = '```json\n{"verdict": "ok", "score": "high"}\n```'
ON_CONTRACT_ANSWER = '```json\n{"verdict": "ok", "score": 7}\n```'


@contextlib.contextmanager
def _capture_findings():
    """Every finding the code under test writes, with its kwargs — captured at
    ``record_structured_output_finding``, the one function all of them reach."""
    import matrx_ai.providers.structured_output_findings as findings

    recorded: list[tuple[str, dict[str, Any]]] = []
    original = findings.record_structured_output_finding

    async def capture(key: str, **kwargs: Any) -> None:
        recorded.append((key, kwargs))

    findings.record_structured_output_finding = capture  # type: ignore[assignment]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            yield recorded
    finally:
        findings.record_structured_output_finding = original  # type: ignore[assignment]


def _flush(*, succeeded: bool | None, answer_off_contract: bool | None) -> dict[str, Any]:
    """Buffer one real translator note, flush it the way the dispatch seam does,
    and return the kwargs the finding was written with."""
    import matrx_ai.providers.structured_output_findings as findings

    async def drive() -> list[tuple[str, dict[str, Any]]]:
        with _capture_findings() as recorded:
            # Isolation only: other suites in this process may have left a held
            # gate finding in this task's ContextVar (production rescues those on
            # the next call's `open_gate_findings`); this check is about the
            # translation half.
            findings._GATE_PENDING.set(None)
            token = findings.begin_translation_findings()
            try:
                findings.note_translation(
                    "anthropic",
                    relaxed=["additionalProperties:false could not be sent"],
                    response_format={"type": "json_schema", "name": "verdict", "schema": DECLARED},
                )
                await findings.flush_translation_findings(
                    model="claude-sonnet-5",
                    succeeded=succeeded,
                    answer_off_contract=answer_off_contract,
                )
            finally:
                findings.end_translation_findings(token)
            return list(recorded)

    recorded = asyncio.run(drive())
    assert len(recorded) == 1, f"expected exactly one finding, got {[k for k, _ in recorded]}"
    return recorded[0][1]


def test_a_translation_finding_never_claims_a_recovery_nobody_measured() -> None:
    """The four outcomes a translation finding can have, each written as the
    truth. Before the fix all four wrote ``True``."""
    served_on_contract = _flush(succeeded=True, answer_off_contract=False)
    assert served_on_contract["was_recovered"] is True, served_on_contract
    assert "ON CONTRACT" in served_on_contract["detail"]["outcome"]

    served_off_contract = _flush(succeeded=True, answer_off_contract=True)
    assert served_off_contract["was_recovered"] is False, (
        "the call returned and its answer MISSED the declared contract, and the row "
        f"still claims a recovery: {served_off_contract}"
    )
    assert "OFF CONTRACT" in served_off_contract["detail"]["outcome"]

    failed = _flush(succeeded=False, answer_off_contract=None)
    assert failed["was_recovered"] is False, failed
    assert "FAILED" in failed["detail"]["outcome"]

    build_only = _flush(succeeded=None, answer_off_contract=None)
    assert build_only["was_recovered"] is False, (
        f"a build-only translate asserted an outcome it cannot know: {build_only}"
    )
    assert "not known" in build_only["detail"]["outcome"]


def test_no_contract_bound_is_not_the_same_claim_as_an_answer_that_passed() -> None:
    """A served call with no bound contract IS recovered — nothing was
    compromised that an answer could contradict — but the row must say that no
    answer was judged, rather than implying one passed."""
    no_contract = _flush(succeeded=True, answer_off_contract=None)
    assert no_contract["was_recovered"] is True, no_contract
    outcome = no_contract["detail"]["outcome"]
    assert "no output contract was bound" in outcome, outcome
    assert "ON CONTRACT" not in outcome, (
        f"a call that judged no answer claims its answer was on contract: {outcome}"
    )


def test_the_dispatch_seam_feeds_the_real_answer_verdict_into_the_findings() -> None:
    """END TO END through the production seam. A translator compromises the
    schema, the provider serves the call, the answer misses the contract — and the
    finding the seam writes says NOT recovered.

    This is the check that proves the WIRING, not just the truth table: before the
    fix the seam knew the answer was off contract (it had just recorded an
    ``answer_off_contract`` finding for it) and still wrote the translation
    finding as recovered.
    """
    import matrx_ai.providers.structured_output_findings as findings
    from matrx_ai.providers.unified_client import UnifiedAIClient
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        release_declared_output_contract,
    )
    from matrx_ai.config import Role, UnifiedMessage, UnifiedResponse

    profile = SimpleNamespace(vendor="anthropic", model_name="claude-sonnet-5", client_attr="anthropic")

    def run(answer: str) -> list[tuple[str, dict[str, Any]]]:
        async def dispatch() -> UnifiedResponse:
            # A real translator note, made where a translator makes it: inside the
            # call, with the seam's buffer open.
            findings.note_translation(
                "anthropic",
                relaxed=["additionalProperties:false could not be sent"],
                response_format={"type": "json_schema", "name": "verdict", "schema": DECLARED},
            )
            return UnifiedResponse(
                messages=[UnifiedMessage(role=Role.ASSISTANT, content=answer)],
                usage=None,
                finish_reason="stop",
            )

        async def drive() -> list[tuple[str, dict[str, Any]]]:
            with _capture_findings() as recorded:
                token = bind_declared_output_contract(
                    {"type": "json_schema", "name": "verdict", "schema": DECLARED}
                )
                try:
                    await UnifiedAIClient._dispatch_with_billing_net(dispatch, profile=profile)
                finally:
                    release_declared_output_contract(token)
                return list(recorded)

        return asyncio.run(drive())

    off = run(OFF_CONTRACT_ANSWER)
    keys = [k for k, _ in off]
    assert any(k.endswith("answer_off_contract") for k in keys), (
        f"the seam did not judge the answer at all: {keys}"
    )
    relaxed = [kw for k, kw in off if k.endswith(".relaxed")]
    assert relaxed, f"the translator's compromise was not recorded: {keys}"
    assert relaxed[0]["was_recovered"] is False, (
        "the seam recorded the answer as OFF CONTRACT and the translation finding on "
        f"the very same call as recovered: {relaxed[0]}"
    )

    good = run(ON_CONTRACT_ANSWER)
    relaxed = [kw for k, kw in good if k.endswith(".relaxed")]
    assert relaxed and relaxed[0]["was_recovered"] is True, relaxed
    assert not [k for k, _ in good if k.endswith("answer_off_contract")]


def test_the_outcome_decision_lives_in_one_place() -> None:
    """One function decides ``was_recovered`` for every structured-output finding,
    so a new writer cannot re-introduce the default. Its truth table, restated
    here from the RULE rather than by calling it twice."""
    from matrx_ai.providers.structured_output_findings import translation_outcome

    assert translation_outcome(True, False)[0] is True
    assert translation_outcome(True, None)[0] is True
    assert translation_outcome(True, True)[0] is False
    assert translation_outcome(False, None)[0] is False
    assert translation_outcome(False, False)[0] is False
    assert translation_outcome(None, None)[0] is False
    for succeeded in (True, False, None):
        for off in (True, False, None):
            sentence = translation_outcome(succeeded, off)[1]
            assert sentence and sentence[0].islower(), sentence


def test_no_finding_writer_hardcodes_recovery_before_the_call_runs() -> None:
    """THE CENSUS, so this is fixed as a class. A ``was_recovered=True`` literal is
    only honest where the provider call has already returned — which, across
    ``matrx-ai``'s structured-output writers, is exactly one place: Anthropic's
    grammar ladder, after ``send(payload)`` returned. Anywhere else a literal
    ``True`` is a claim made too early; the value is held (``None``) and the
    dispatch seam writes it.
    """
    import ast
    import pathlib

    root = pathlib.Path(__file__).resolve().parents[1] / "matrx_ai"
    writers = ("record_structured_output_finding", "record_structured_output_finding_sync")
    offenders: list[str] = []
    for path in sorted(root.rglob("*.py")):
        text = path.read_text()
        if "record_structured_output_finding" not in text:
            continue
        for node in ast.walk(ast.parse(text)):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.id if isinstance(node.func, ast.Name) else None
            if name not in writers:
                continue
            for kw in node.keywords:
                if kw.arg == "was_recovered" and isinstance(kw.value, ast.Constant):
                    if kw.value.value is True:
                        offenders.append(f"{path.relative_to(root)}:{node.lineno}")
    assert offenders == ["providers/anthropic/anthropic_api.py:418"], (
        "a structured-output finding writer hardcodes was_recovered=True. Hold it with "
        f"was_recovered=None and let the dispatch seam write the real outcome: {offenders}"
    )


def test_the_ladders_recovery_says_which_recovery_it_means() -> None:
    """The one sanctioned ``True`` describes a recovery of the REQUEST, and the row
    says so — a reader must never read it as a verdict on the answer."""
    import pathlib

    text = (
        pathlib.Path(__file__).resolve().parents[1]
        / "matrx_ai/providers/anthropic/anthropic_api.py"
    ).read_text()
    assert "recovered_means" in text, (
        "the ladder claims a recovery without saying which one it measured"
    )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
