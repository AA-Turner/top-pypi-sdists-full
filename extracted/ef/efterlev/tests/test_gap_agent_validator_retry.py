"""Tests for the Gap Agent built-in retry on validator-rejection.

Three rejection classes are retryable:
  - AgentValidatorRejectionError (fabricated evidence IDs) — v0.1.125 / #327
  - AgentError carrying the "requires at least one evidence_id citation"
    marker (pydantic rejecting positive-status-without-evidence) —
    v0.1.138 / #343
  - Either of the above on the final attempt → graceful repair instead
    of raise (v0.1.139 / #344)

Retry budget: 3 LLM calls (was 2 through v0.1.138). On retry, the prior
attempt's fabricated IDs are appended to the user message as explicit
"do not cite these" feedback. On final exhaustion of the fabricated-ID
path, the report is repaired in place rather than raising — orphaned
positive classifications downgrade to not_implemented with a marker in
the rationale. End-customers don't see hard failures from stochastic
Haiku drift even when it persists across all 3 attempts.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from efterlev.agents import GapAgent, GapAgentInput
from efterlev.errors import AgentError, AgentValidatorRejectionError
from efterlev.llm.base import LLMMessage, LLMResponse
from efterlev.models import Indicator
from efterlev.provenance import ProvenanceStore, active_store


def _ind() -> Indicator:
    return Indicator(
        id="KSI-AFR-UCM",
        theme="AFR",
        name="Cryptographic Module Use",
        statement="...",
        controls=["SC-28(1)"],
    )


def _clean_response() -> str:
    """A GapReport JSON with no evidence_ids cited (passes validator trivially)."""
    return json.dumps(
        {
            "reasoning_summary": "Surveyed.",
            "ksi_classifications": [
                {
                    "ksi_id": "KSI-AFR-UCM",
                    "status": "evidence_layer_inapplicable",
                    "rationale": "no detector evidence",
                    "evidence_ids": [],
                }
            ],
            "unmapped_findings": [],
        }
    )


def _fabricated_response() -> str:
    """A GapReport JSON citing an evidence ID that doesn't exist in the prompt
    fences. Triggers AgentValidatorRejectionError from `_validate_cited_ids`.
    """
    return json.dumps(
        {
            "reasoning_summary": "Surveyed.",
            "ksi_classifications": [
                {
                    "ksi_id": "KSI-AFR-UCM",
                    "status": "implemented",
                    "rationale": "fabricated",
                    "evidence_ids": [
                        "sha256:0000000000000000000000000000000000000000000000000000000000000000"
                    ],
                }
            ],
            "unmapped_findings": [],
        }
    )


@dataclass
class SequencedStubLLMClient:
    """Stub LLM client that returns a different response on each call."""

    responses: list[str]
    model: str = "stub-haiku"
    call_count: int = 0
    last_prompt_hash: str = ""
    last_system: str = ""
    last_messages: list[LLMMessage] = field(default_factory=list)

    def complete(
        self,
        *,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int = 4096,
        on_chunk=None,
    ) -> LLMResponse:
        import hashlib

        idx = min(self.call_count, len(self.responses) - 1)
        text = self.responses[idx]
        self.last_system = system
        self.last_messages = list(messages)
        self.call_count += 1
        joined = system + "\n".join(m.content for m in messages)
        prompt_hash = hashlib.sha256(joined.encode("utf-8")).hexdigest()
        self.last_prompt_hash = prompt_hash
        return LLMResponse(text=text, model=self.model, prompt_hash=prompt_hash)


def _run_with_responses(responses: list[str]) -> tuple[GapAgent, SequencedStubLLMClient]:
    """Run GapAgent with a sequenced stub; return the agent + stub for assertions.
    Returns even when the agent raises (caller wraps in pytest.raises).
    """
    stub = SequencedStubLLMClient(responses=responses)
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        agent.run(GapAgentInput(indicators=[_ind()], evidence=[]))
    return agent, stub


def test_first_attempt_success_no_retry() -> None:
    """Validator passes on attempt 1 — single LLM call."""
    _, stub = _run_with_responses([_clean_response()])
    assert stub.call_count == 1


def test_validator_rejection_then_success_absorbed_by_retry(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Attempt 1 fabricates → rejected; attempt 2 clean → succeeds.
    Customer sees a successful run; stderr carries a diagnostic line.
    """
    _, stub = _run_with_responses([_fabricated_response(), _clean_response()])
    assert stub.call_count == 2
    err = capsys.readouterr().err
    # v0.1.141 / #346 reworded all retry banners to plain English with the
    # `[gap]` prefix that matches per-KSI progress lines.
    assert "[gap]" in err
    assert "unknown evidence ID" in err
    assert "attempt 2/3" in err
    # Technical exception names should NOT leak into user-facing stderr.
    assert "AgentValidatorRejectionError" not in err


def test_third_attempt_success_after_two_rejections(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """v0.1.139 / #344: retry budget is 3 LLM calls. Fabricated x 2 then
    clean -> succeeds without graceful-repair fallback. Pre-v0.1.139 this
    would have surfaced as a hard failure (cap was 2).
    """
    _, stub = _run_with_responses(
        [_fabricated_response(), _fabricated_response(), _clean_response()]
    )
    assert stub.call_count == 3
    err = capsys.readouterr().err
    assert "unknown evidence ID" in err
    assert "attempt 2/3" in err
    assert "attempt 3/3" in err
    # Graceful-repair banner must NOT fire when the third attempt is clean.
    assert "Auto-repairing" not in err


def test_three_rejections_trigger_graceful_repair(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """v0.1.139 / #344: all 3 attempts fabricate → graceful repair instead
    of raising. The orphaned positive-status classification downgrades to
    not_implemented and gets a marker in the rationale; stderr carries a
    repair summary listing every change.
    """
    stub = SequencedStubLLMClient(
        responses=[_fabricated_response(), _fabricated_response(), _fabricated_response()]
    )
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        # No exception — graceful repair turns the failure into a usable report.
        agent.run(GapAgentInput(indicators=[_ind()], evidence=[]))
    assert stub.call_count == 3
    err = capsys.readouterr().err
    assert "After 3 attempts" in err
    assert "Auto-repairing" in err
    # The _fabricated_response() fixture cites a sha256:000... id with status="implemented",
    # so the repair must downgrade it.
    assert "KSI-AFR-UCM" in err
    assert "downgraded" in err
    assert "'not_implemented'" in err


def test_retry_caps_at_three_attempts() -> None:
    """If 4 fabricated responses are queued, only 3 are consumed and the
    third triggers graceful repair. Cap protects against deterministic
    prompt / fixture issues consuming an unbounded retry budget.
    """
    stub = SequencedStubLLMClient(
        responses=[
            _fabricated_response(),
            _fabricated_response(),
            _fabricated_response(),
            _clean_response(),
        ]
    )
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        agent.run(GapAgentInput(indicators=[_ind()], evidence=[]))
    assert stub.call_count == 3, (
        "retry must cap at 3; the 4th queued response should never be consumed"
    )


def test_retry_user_message_includes_rejected_id_feedback() -> None:
    """v0.1.139 / #344: on retry, the prior attempt's fabricated IDs must
    appear in the user message so the LLM sees what NOT to cite. Without
    feedback, the same prompt asks the same model the same thing and the
    LLM is likely to make the same mistake.
    """
    stub = SequencedStubLLMClient(
        responses=[_fabricated_response(), _fabricated_response(), _clean_response()]
    )
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        agent.run(GapAgentInput(indicators=[_ind()], evidence=[]))
    last_msg = stub.last_messages[-1].content
    # The fabricated id from _fabricated_response (all zeros) must be in
    # the final user message as feedback against re-citing it.
    assert "CITATION REJECTION FEEDBACK" in last_msg
    assert "sha256:0000000000000000000000000000000000000000000000000000000000000000" in last_msg


def test_validator_rejection_is_subclass_of_agent_error() -> None:
    """`AgentValidatorRejectionError` extends `AgentError` so existing
    `except AgentError` callers still catch it.
    """
    assert issubclass(AgentValidatorRejectionError, AgentError)


def _positive_without_evidence_response() -> str:
    """A GapReport JSON with status='partial' and evidence_ids=[] — rejected
    by `KsiClassification._positive_status_requires_evidence` *inside*
    pydantic, before `_validate_cited_ids` runs. Surfaces as plain
    `AgentError` from `_invoke_llm` rather than `AgentValidatorRejectionError`.
    """
    return json.dumps(
        {
            "reasoning_summary": "Surveyed.",
            "ksi_classifications": [
                {
                    "ksi_id": "KSI-AFR-UCM",
                    "status": "partial",
                    "rationale": "evidence exists but coverage is incomplete",
                    "evidence_ids": [],
                }
            ],
            "unmapped_findings": [],
        }
    )


def test_pydantic_rejection_then_success_absorbed_by_retry(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """v0.1.138 / #343: Attempt 1 emits status=partial with no evidence —
    pydantic raises ValueError, base.py wraps as AgentError. The retry
    must recognize this specific case (marker substring in message) and
    retry, not bubble it up untreated like v0.1.137 did.
    """
    _, stub = _run_with_responses([_positive_without_evidence_response(), _clean_response()])
    assert stub.call_count == 2
    err = capsys.readouterr().err
    # v0.1.141 / #346 reworded all banners. "positive status without citing
    # evidence" is the user-facing wording for the pydantic model_validator
    # rejecting partial/implemented with empty evidence_ids.
    assert "positive status without citing evidence" in err
    assert "attempt 2/3" in err


def test_pydantic_rejection_on_all_three_attempts_surfaces_agent_error() -> None:
    """Three pydantic rejections in a row → the wrapped AgentError surfaces.
    The pydantic-rejection class is NOT eligible for graceful repair (we
    have no parsed report to repair — pydantic failed during construction).
    Deterministic prompt issues must not be masked by unbounded retry.
    """
    stub = SequencedStubLLMClient(
        responses=[
            _positive_without_evidence_response(),
            _positive_without_evidence_response(),
            _positive_without_evidence_response(),
        ]
    )
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        with pytest.raises(AgentError) as exc_info:
            agent.run(GapAgentInput(indicators=[_ind()], evidence=[]))
    assert "requires at least one evidence_id citation" in str(exc_info.value)
    assert stub.call_count == 3


# --- _repair_fabricated_citations unit tests ------------------------------
# These exercise the per-classification repair logic in isolation, separate
# from the retry-loop integration tests above.


def test_repair_strips_fabricated_ids_and_keeps_real_ones() -> None:
    """Mixed citation: real id stays, fabricated id is removed; status
    unchanged because at least one real citation remains."""
    from efterlev.agents.gap import GapReport, KsiClassification, _repair_fabricated_citations

    report = GapReport(
        ksi_classifications=[
            KsiClassification(
                ksi_id="KSI-A",
                status="implemented",
                rationale="seen via real evidence",
                evidence_ids=["sha256:real_one", "sha256:fabricated"],
            )
        ],
        unmapped_findings=[],
    )
    repaired, notes = _repair_fabricated_citations(report, fabricated={"sha256:fabricated"})
    assert repaired.ksi_classifications[0].status == "implemented"
    assert repaired.ksi_classifications[0].evidence_ids == ["sha256:real_one"]
    assert any("KSI-A" in n and "removed 1 citation" in n for n in notes)


def test_repair_downgrades_positive_with_only_fabricated_citations() -> None:
    """When stripping leaves a positive classification with zero citations,
    downgrade to not_implemented and append the auto-repair marker."""
    from efterlev.agents.gap import GapReport, KsiClassification, _repair_fabricated_citations

    report = GapReport(
        ksi_classifications=[
            KsiClassification(
                ksi_id="KSI-B",
                status="partial",
                rationale="claimed partial",
                evidence_ids=["sha256:fake1", "sha256:fake2"],
            )
        ],
        unmapped_findings=[],
    )
    repaired, notes = _repair_fabricated_citations(
        report, fabricated={"sha256:fake1", "sha256:fake2"}
    )
    assert repaired.ksi_classifications[0].status == "not_implemented"
    assert repaired.ksi_classifications[0].evidence_ids == []
    assert "[auto-repair:" in repaired.ksi_classifications[0].rationale
    assert any("KSI-B" in n and "downgraded" in n for n in notes)


def test_repair_leaves_clean_classifications_untouched() -> None:
    """A classification whose citations are all real must be returned
    byte-identical, including any other unrelated fabricated IDs in the
    overall set. Surgical: only fix what's broken."""
    from efterlev.agents.gap import GapReport, KsiClassification, _repair_fabricated_citations

    clean = KsiClassification(
        ksi_id="KSI-C", status="implemented", rationale="real", evidence_ids=["sha256:real"]
    )
    report = GapReport(
        ksi_classifications=[
            clean,
            KsiClassification(
                ksi_id="KSI-D",
                status="implemented",
                rationale="fabricated",
                evidence_ids=["sha256:fake"],
            ),
        ],
        unmapped_findings=[],
    )
    repaired, notes = _repair_fabricated_citations(report, fabricated={"sha256:fake"})
    # KSI-C is untouched; KSI-D is downgraded.
    assert repaired.ksi_classifications[0] == clean
    assert repaired.ksi_classifications[1].status == "not_implemented"
    assert all("KSI-C" not in n for n in notes)


def test_repair_drops_unmapped_findings_with_fabricated_evidence_id() -> None:
    """An UnmappedFinding referencing a fabricated evidence_id has no
    referent — drop it rather than emit it as 'evidence with unknown
    provenance.'"""
    from efterlev.agents.gap import (
        GapReport,
        KsiClassification,
        UnmappedFinding,
        _repair_fabricated_citations,
    )

    report = GapReport(
        ksi_classifications=[
            KsiClassification(
                ksi_id="KSI-E", status="not_implemented", rationale="r", evidence_ids=[]
            )
        ],
        unmapped_findings=[
            UnmappedFinding(evidence_id="sha256:real", controls=["AC-1"], note="real"),
            UnmappedFinding(evidence_id="sha256:fake", controls=["AC-2"], note="fake"),
        ],
    )
    repaired, notes = _repair_fabricated_citations(report, fabricated={"sha256:fake"})
    assert len(repaired.unmapped_findings) == 1
    assert repaired.unmapped_findings[0].evidence_id == "sha256:real"
    assert any("dropped 1" in n for n in notes)


# --- JSON-parse retry (v0.1.140 / #345) -----------------------------------


def _malformed_json_response() -> str:
    """A response that triggers `json.loads` failure. Mimics Haiku going off
    the rails mid-stream — opens a JSON object, never closes it. The base
    `Agent._invoke_llm` wraps the json.JSONDecodeError as AgentError with
    the marker substring "LLM response was not valid JSON" that the retry
    loop pattern-matches on.
    """
    return '{"ksi_classifications": [{"ksi_id": "KSI-AFR-UCM"'


def test_json_parse_failure_then_success_absorbed_by_retry(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """v0.1.140 / #345: attempt 1 returns malformed JSON → retried with
    JSON-specific feedback; attempt 2 clean → succeeds. Pre-v0.1.140 the
    JSON parse error bypassed the retry loop entirely and surfaced raw."""
    _, stub = _run_with_responses([_malformed_json_response(), _clean_response()])
    assert stub.call_count == 2
    err = capsys.readouterr().err
    assert "Model response was malformed JSON" in err
    assert "attempt 2/3" in err


def test_json_parse_failure_on_all_three_attempts_surfaces_agent_error() -> None:
    """Three JSON-parse failures in a row → AgentError surfaces. No
    graceful repair for this class — without a parsed report, there's
    nothing to repair. Deterministic prompt or fixture issues must not
    be masked by unbounded retry."""
    stub = SequencedStubLLMClient(
        responses=[
            _malformed_json_response(),
            _malformed_json_response(),
            _malformed_json_response(),
        ]
    )
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        with pytest.raises(AgentError) as exc_info:
            agent.run(GapAgentInput(indicators=[_ind()], evidence=[]))
    assert "not valid JSON" in str(exc_info.value)
    assert stub.call_count == 3


def test_json_parse_retry_includes_json_specific_feedback() -> None:
    """The retry user message must contain the JSON-PARSE-FAILURE-FEEDBACK
    block — without it, the next attempt has no idea what was wrong and
    is likely to repeat the same mistake."""
    stub = SequencedStubLLMClient(responses=[_malformed_json_response(), _clean_response()])
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        agent.run(GapAgentInput(indicators=[_ind()], evidence=[]))
    last_msg = stub.last_messages[-1].content
    assert "JSON PARSE FAILURE FEEDBACK" in last_msg
    assert "Emit ONLY a single JSON object" in last_msg
    assert "Do NOT wrap the JSON in markdown fences" in last_msg


def test_mixed_failure_modes_can_chain_within_three_attempts(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The exact customer pattern from v0.1.139 testing: attempt 1 was a
    fabricated-id rejection, attempt 2 was malformed JSON. v0.1.140 must
    handle the mix — both feedback blocks accumulate, attempt 3 has all
    context, and a clean response there succeeds.
    """
    _, stub = _run_with_responses(
        [_fabricated_response(), _malformed_json_response(), _clean_response()]
    )
    assert stub.call_count == 3
    last_msg = stub.last_messages[-1].content
    # Both feedback blocks should be present in the third attempt's prompt.
    assert "CITATION REJECTION FEEDBACK" in last_msg
    assert "JSON PARSE FAILURE FEEDBACK" in last_msg
    err = capsys.readouterr().err
    assert "unknown evidence ID" in err  # attempt 1 banner
    assert "Model response was malformed JSON" in err  # attempt 2 banner
    assert "attempt 2/3" in err
    assert "attempt 3/3" in err


# --- v0.1.142 / #347 UX follow-ups ---------------------------------------


def _make_fabricated_response_with_n_ids(n: int) -> str:
    """A GapReport JSON citing N fabricated evidence IDs across 1 classification."""
    return json.dumps(
        {
            "reasoning_summary": "Surveyed.",
            "ksi_classifications": [
                {
                    "ksi_id": "KSI-AFR-UCM",
                    "status": "partial",
                    "rationale": "fabricated",
                    "evidence_ids": [f"sha256:{i:064x}" for i in range(1, n + 1)],
                }
            ],
            "unmapped_findings": [],
        }
    )


def test_retry_banner_singular_grammar_for_one_fabricated_id(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """v0.1.142 / #347: customer hit "Model cited an unknown 5 evidence IDs"
    (un-fixable English). v0.1.142 reads "cited N unknown evidence IDs"
    with singular when N=1.
    """
    _run_with_responses([_make_fabricated_response_with_n_ids(1), _clean_response()])
    err = capsys.readouterr().err
    assert "cited 1 unknown evidence ID" in err
    assert "an unknown" not in err  # the v0.1.141 wording


def test_retry_banner_plural_grammar_for_many_fabricated_ids(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The N>1 case must read "cited N unknown evidence IDs" — not
    "cited an unknown N evidence IDs" (the v0.1.141 bug)."""
    _run_with_responses([_make_fabricated_response_with_n_ids(5), _clean_response()])
    err = capsys.readouterr().err
    assert "cited 5 unknown evidence IDs" in err
    assert "an unknown 5" not in err


def test_dispatch_line_emitted_before_each_attempt(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """v0.1.142 / #347: customer reported "no spinner after /agent gap"
    because the stream-callback heartbeat only fires once chunks arrive.
    v0.1.142 emits an immediate "Starting..." line for attempt 1 and
    "Calling model again..." for retries — before the LLM call.

    v0.1.155 / #360: dropped the misleading "typically 30-90s" suffix
    (was a flat lie on cache hits — customer's gap stage dropped from
    1247s to 0.3s after the cache fix, but the duration claim still
    printed). Per-batch completion line now reveals actual elapsed.
    """
    # Force stderr to be "a TTY" so the dispatch line emits.
    monkeypatch.setattr("sys.stderr.isatty", lambda: True)
    _run_with_responses([_fabricated_response(), _clean_response()])
    err = capsys.readouterr().err
    assert "[gap] Starting analysis" in err
    assert "30-90s" not in err  # v0.1.155: misleading duration claim removed
    assert "[gap] Calling model again (attempt 2/3" in err


def test_dispatch_line_suppressed_when_stderr_not_a_tty(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """In CI / piped output, the dispatch line should not appear — keeps
    logs clean. Same gating rule as `make_reporter_if_tty`."""
    monkeypatch.setattr("sys.stderr.isatty", lambda: False)
    _run_with_responses([_clean_response()])
    err = capsys.readouterr().err
    assert "Starting analysis" not in err
    assert "Calling model again" not in err


def test_prompt_too_long_translates_to_friendly_error() -> None:
    """v0.1.142 / #347: customer hit a raw
    "bedrock completion failed: ... prompt is too long: 207302 tokens > 200000 maximum"
    error during /report. v0.1.142 translates that into actionable guidance
    listing the three workarounds (Anthropic backend, smaller subdir,
    per-KSI batching planned)."""
    raw = "bedrock completion failed: prompt is too long: 207302 tokens > 200000 maximum"
    stub = SequencedStubLLMClient(responses=[raw])

    class _PromptTooLongStub(SequencedStubLLMClient):
        def complete(self, **_kwargs):  # type: ignore[no-untyped-def, override]
            self.call_count += 1
            raise AgentError(raw)

    stub = _PromptTooLongStub(responses=[])
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        with pytest.raises(AgentError) as exc_info:
            agent.run(GapAgentInput(indicators=[_ind()], evidence=[]))
    msg = str(exc_info.value)
    assert "exceeded the model's context window" in msg
    # The raw provider message is preserved so the user can correlate.
    assert "207302 tokens" in msg
    # Three concrete workarounds present.
    assert "Switch to the Anthropic API" in msg
    assert "smaller subdirectory" in msg
    assert "per-KSI batching" in msg


def test_repair_note_singular_for_one_citation() -> None:
    """v0.1.142 / #347: customer saw "removed 1 citation that don't exist"
    (singular noun, plural verb). v0.1.142 says "1 citation that doesn't
    exist" for the singular case."""
    from efterlev.agents.gap import GapReport, KsiClassification, _repair_fabricated_citations

    report = GapReport(
        ksi_classifications=[
            KsiClassification(
                ksi_id="KSI-A",
                status="implemented",
                rationale="seen",
                evidence_ids=["sha256:real", "sha256:fake"],
            )
        ],
        unmapped_findings=[],
    )
    _, notes = _repair_fabricated_citations(report, fabricated={"sha256:fake"})
    assert any("1 citation that doesn't exist" in n for n in notes)
    assert all("don't exist" not in n or "doesn't" in n for n in notes)


# --- v0.1.141 / #346 UX: friendlier diagnostics + retry-progress reset ----


def test_retry_banner_uses_plain_language_and_no_pr_numbers(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """v0.1.141 / #346: end-customers never see exception class names, PR
    numbers, or version refs in stderr diagnostics. Banner format is
    [gap] <reason in plain English>. Retrying with stricter instructions
    (attempt N/3)..."""
    _run_with_responses([_fabricated_response(), _clean_response()])
    err = capsys.readouterr().err
    assert "[gap]" in err
    # No technical leakage:
    for forbidden in [
        "AgentValidatorRejectionError",
        "AgentError",
        "ValidationError",
        "validator rejected",
        "model_validator",
        "v0.1.139",
        "v0.1.140",
        "v0.1.141",
        "#344",
        "#345",
        "#346",
    ]:
        assert forbidden not in err, f"user-facing stderr should not contain {forbidden!r}"


def test_retry_resets_gap_progress_reporter() -> None:
    """v0.1.141 / #346: when the retry layer calls `reset_for_next_attempt`
    on the GapProgressReporter, the reporter clears its dedup state and
    installs a "Retry N/3" label. Without this, the second attempt's
    identical KSI IDs collide with attempt 1's seen-set and the user
    sees silence for the entire retry."""
    from efterlev.agents.gap_progress import GapProgressReporter

    reporter = GapProgressReporter(total_ksis=60)
    # Simulate attempt 1 finished streaming all 60 KSIs.
    reporter.seen_ksi_ids = {f"KSI-X-{i:03d}" for i in range(60)}
    reporter.seen_ksi_count = 60

    reporter.reset_for_next_attempt("Retry 2/3 with stricter instructions")

    assert reporter.seen_ksi_ids == set()
    assert reporter.seen_ksi_count == 0
    assert reporter.attempt_label == "Retry 2/3 with stricter instructions"


def test_gap_progress_heartbeat_uses_attempt_label_after_reset(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """After reset, the heartbeat must use the attempt label (not the
    default "Analyzing KSIs..." text) until per-KSI lines start flowing
    again — so the user sees "Retry 2/3" during the retry's preamble."""
    from efterlev.agents.gap_progress import GapProgressReporter

    reporter = GapProgressReporter(total_ksis=60, stream=sys.stderr)
    reporter.reset_for_next_attempt("Retry 2/3 with stricter instructions")
    # Force the heartbeat to fire by pretending no heartbeat has happened
    # for longer than the throttle window.
    reporter.last_heartbeat_at = 0.0
    # Feed a chunk that contains no ksi_id pattern — heartbeat path.
    reporter('{"reasoning_summary": "still thinking through these KSIs..."}')
    err = capsys.readouterr().err
    assert "Retry 2/3 with stricter instructions" in err
    # Spinner frame should be present somewhere on the line.
    assert any(frame in err for frame in ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"))


def test_non_agent_exception_propagates_immediately() -> None:
    """A non-AgentError exception (e.g. backend RuntimeError, network hiccup)
    must propagate immediately without consuming retry budget. Only the
    three documented `AgentError` subclasses (citation rejection, pydantic
    rejection, JSON parse failure) are retryable; everything else bubbles
    up so deterministic non-LLM failures don't get masked.
    """
    from dataclasses import dataclass

    @dataclass
    class _RaisingClient:
        model: str = "stub-haiku"
        call_count: int = 0
        last_prompt_hash: str = ""
        last_system: str = ""
        last_messages: list = field(default_factory=list)

        def complete(self, **_kwargs) -> LLMResponse:  # type: ignore[no-untyped-def]
            self.call_count += 1
            raise RuntimeError("simulated backend failure (e.g. network timeout)")

    stub = _RaisingClient()
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        with pytest.raises(RuntimeError, match="simulated backend failure"):
            agent.run(GapAgentInput(indicators=[_ind()], evidence=[]))
    assert stub.call_count == 1, "non-AgentError exceptions must not be retried"
