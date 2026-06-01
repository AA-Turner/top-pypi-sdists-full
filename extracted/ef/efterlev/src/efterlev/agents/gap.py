"""Gap Agent — classify each baseline KSI as implemented / partial / not_implemented / NA.

The Gap Agent is v0's first agent. It consumes:

  - the baseline's list of `Indicator`s (the set of KSIs to classify), and
  - the set of `Evidence` records produced by `scan_terraform` so far,

and returns a `GapReport` with one `KsiClassification` per baseline KSI plus
a bucket of `UnmappedFinding`s for evidence records whose `ksis_evidenced=[]`
(per DECISIONS 2026-04-21 design call #1 — SC-28 lives here).

Trust boundary: evidence content is attacker-controllable at the input layer.
Every evidence record this agent shows the model goes through
`format_evidence_for_prompt` which XML-fences it (DECISIONS 2026-04-21
design call #3). The `validate_cited_ids` step below rejects any output that
cites an evidence id the model did not actually see in the prompt.

Every classification becomes a `Claim(claim_type="classification")` with
`derived_from=[evidence_ids]`, persisted into the active ProvenanceStore so
the Documentation Agent (Phase 3 downstream) can walk from a drafted
attestation back to the evidence that supported it.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from efterlev.agents.base import (
    Agent,
    format_evidence_for_prompt,
    new_fence_nonce,
    parse_evidence_fence_ids,
)
from efterlev.agents.gap_batching import (
    DEFAULT_BATCH_SIZE_KSIS,
    Batch,
    compute_unmapped_findings,
    fill_missing_classifications,
    plan_batches,
)

# Re-export the shared model classes so existing
# `from efterlev.agents.gap import GapReport, KsiClassification, ...`
# imports keep working. The classes were extracted to `gap_types.py`
# in v0.1.143 to break the circular dependency between gap.py and
# gap_batching.py.
from efterlev.agents.gap_types import (
    GapReport,
    GapStatus,
    KsiClassification,
    UnmappedFinding,
)
from efterlev.errors import AgentError, AgentValidatorRejectionError
from efterlev.llm import LLMClient
from efterlev.models import Claim, Evidence, Indicator, ScanSummary
from efterlev.provenance.context import get_active_store

__all__ = [
    "DEFAULT_BATCH_SIZE_KSIS",
    "Batch",
    "GapAgent",
    "GapAgentInput",
    "GapReport",
    "GapStatus",
    "KsiClassification",
    "UnmappedFinding",
    "compute_unmapped_findings",
    "fill_missing_classifications",
    "plan_batches",
]

# Substring of the message raised by `KsiClassification._positive_status_requires_evidence`
# — used to detect the rejection from outside pydantic. Keep in sync with the
# model_validator below. Narrow enough not to match other AgentError messages
# (`json.loads` failures, backend errors).
_EVIDENCE_CITATION_MARKER = "requires at least one evidence_id citation"

# Substring of the message raised by `Agent._invoke_llm` when `json.loads` fails
# on the LLM response. Used to detect the failure class from outside base.py and
# trigger a retry-with-feedback path (v0.1.140 / #345). Customer-visible Haiku
# failure 2026-05-16: attempt 1 was a fabricated-id rejection, attempt 2 produced
# malformed JSON (line 499 truncation); pre-v0.1.140 the JSON error bypassed
# retry and surfaced raw. Narrow enough not to match other AgentError messages.
_JSON_PARSE_MARKER = "LLM response was not valid JSON"

# Substrings emitted by Bedrock / Anthropic when the prompt exceeds the model's
# context window. Caught and translated to a user-actionable error rather than
# leaving the raw "bedrock completion failed: ... ValidationException..." string
# in the user's terminal (v0.1.142 / #347). Customer hit this 2026-05-16 with
# 660 evidence records → 207k-token prompt vs Bedrock's 200k cap.
_PROMPT_TOO_LONG_MARKERS = ("prompt is too long", "prompt too long")


class GapAgentInput(BaseModel):
    """Input to `GapAgent.run`."""

    # arbitrary_types_allowed=True so progress_callback (a Callable) can
    # ride on this pydantic model. Frozen so the model's other invariants
    # stay enforced; Callable is opaque to pydantic and isn't validated.
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    indicators: list[Indicator]
    evidence: list[Evidence]
    # Slim summary of the scan that produced `evidence`. When the scan was
    # HCL-mode against a module-composed codebase, the agent's prompt surfaces
    # this so narratives can reflect the coverage limitation ("findings
    # classified `not_implemented` may be coverage gaps, not real gaps").
    # None when the agent is invoked directly (e.g. unit tests) without a
    # prior scan in the active store. Priority 0 (2026-04-27).
    scan_summary: ScanSummary | None = None
    # v0.1.86: optional streaming-progress callback. CLI installs a
    # `GapProgressReporter` from `efterlev.agents.gap_progress` when
    # stderr is a TTY (regex-extracts KSI IDs from the streaming JSON
    # and prints `[gap] classifying KSI X/N: KSI-AAA-BBB`). None in CI
    # and tests so output stays uncluttered.
    progress_callback: Callable[[str], None] | None = Field(default=None, exclude=True)


class GapAgent(Agent):
    """LLM-backed KSI classifier, grounded in deterministic scanner evidence.

    Uses Opus 4.7 by default — the classifier makes judgment calls about
    ambiguous/missing-evidence cases and must resist borrowing evidence from
    unrelated KSIs. Those are Opus-grade reasoning requirements; cheaper
    models drift on the honesty discipline.
    """

    name = "gap_agent@0.1.0"
    system_prompt_path = "gap_prompt.md"
    output_model = GapReport
    default_model = "claude-opus-4-7"

    def _dry_run_stub_output(self) -> GapReport:
        """Empty `GapReport` for dry-run mode (no classifications, no findings).

        See `efterlev.agents.dry_run` for the dry-run mechanism. The
        empty `ksi_classifications` list means the agent's downstream
        loop iterates zero times — no Claim records to write, no
        per-KSI HTML rendering. The CLI ignores the agent's actual
        return value in dry-run mode and dumps the captured prompts
        from the session collector instead.
        """
        return GapReport(ksi_classifications=[], unmapped_findings=[])

    def __init__(
        self,
        *,
        client: LLMClient | None = None,
        model: str | None = None,
    ) -> None:
        super().__init__(client=client, model=model)

    def _invoke_with_validator_retry(
        self,
        *,
        user_message: str,
        max_tokens: int,
        nonce: str,
        on_chunk: Callable[[str], None] | None,
    ) -> tuple[GapReport, Any, str]:
        """Invoke the LLM and validate cited evidence IDs; retry with feedback
        on rejection; gracefully repair on final exhaustion. Returns the
        validated (or repaired) `(report, response, system_prompt)` tuple.

        Three rejection classes are retryable:

        - `AgentValidatorRejectionError` from `_validate_cited_ids` — the
          post-pydantic citation guard rejecting fabricated evidence IDs
          (v0.1.125 / #327, retry strengthened in v0.1.139 / #344).
        - `AgentError` from `_invoke_llm` whose message contains the
          KsiClassification model_validator marker
          (`"requires at least one evidence_id citation"`) — pydantic
          rejecting `status="partial"|"implemented"` with `evidence_ids=[]`.
          Surfaced 2026-05-16 (v0.1.138 / #343).
        - Either of the above on the final attempt — instead of raising,
          we strip fabricated citations and downgrade orphaned positive
          classifications to `not_implemented` with a marker in the
          rationale. The user gets a usable report plus a stderr summary
          of every repair (v0.1.139 / #344). Pure-retry was failing
          customers on Haiku runs where the LLM fabricated across multiple
          attempts (3 user-visible failures over v0.1.137-v0.1.138 testing).

        Retry budget: up to 3 LLM calls total. On retry, the prior attempt's
        fabricated IDs are appended to the user message as explicit "do not
        cite these — they don't exist" feedback so the next attempt has
        meaningfully different input. JSON-parse retries get a separate
        feedback block telling the LLM to emit valid JSON only. Backend
        failures and unrecognized `AgentError` subclasses propagate
        without retry.
        """
        max_attempts = 3
        rejected_ids_history: set[str] = set()
        json_parse_error_history: list[str] = []
        last_validator_error: AgentValidatorRejectionError | None = None
        last_pydantic_error: AgentError | None = None
        last_report: GapReport | None = None
        last_response: Any = None
        last_system_prompt: str | None = None

        for attempt in range(1, max_attempts + 1):
            current_user_message = (
                _user_message_with_feedback(
                    user_message,
                    rejected_ids=rejected_ids_history,
                    json_parse_errors=json_parse_error_history,
                )
                if attempt > 1
                else user_message
            )
            # Emit an immediate "calling LLM" line so the user sees
            # activity instantly — the stream-callback heartbeat only fires
            # after the first chunk arrives, which is a multi-second wait
            # on cold-start (v0.1.142 / #347).
            _emit_dispatch_line(attempt=attempt, max_attempts=max_attempts)
            try:
                report, response, system_prompt = self._invoke_llm(
                    user_message=current_user_message,
                    max_tokens=max_tokens,
                    on_chunk=on_chunk,
                )
            except AgentError as e:
                if _EVIDENCE_CITATION_MARKER in str(e):
                    last_pydantic_error = e
                    if attempt < max_attempts:
                        _emit_retry_banner(
                            "Model claimed a positive status without citing evidence",
                            attempt=attempt,
                            max_attempts=max_attempts,
                        )
                        _reset_progress(on_chunk, attempt + 1, max_attempts)
                        continue
                    # Final attempt also rejected by pydantic. No parsed report
                    # to repair — surface the error.
                    raise
                if _JSON_PARSE_MARKER in str(e):
                    json_parse_error_history.append(str(e))
                    if attempt < max_attempts:
                        _emit_retry_banner(
                            "Model response was malformed JSON",
                            attempt=attempt,
                            max_attempts=max_attempts,
                        )
                        _reset_progress(on_chunk, attempt + 1, max_attempts)
                        continue
                    raise
                # Prompt-too-long is a hard failure — translate the raw
                # provider error into actionable guidance the customer can
                # act on without reading the source (v0.1.142 / #347).
                if any(marker in str(e).lower() for marker in _PROMPT_TOO_LONG_MARKERS):
                    raise AgentError(_format_prompt_too_long_message(str(e))) from e
                # Non-retryable AgentError (backend failure, etc.) — bubble up.
                raise
            assert isinstance(report, GapReport)  # type narrowing
            fabricated = _compute_fabricated_ids(
                report,
                fenced_prompt=system_prompt + "\n" + current_user_message,
                nonce=nonce,
            )
            if not fabricated:
                return report, response, system_prompt
            # Validator rejection: remember everything we need to either retry
            # with feedback or gracefully repair on exhaustion.
            rejected_ids_history.update(fabricated)
            last_validator_error = AgentValidatorRejectionError(
                f"gap agent output cites evidence IDs not present in the prompt: "
                f"{sorted(fabricated)[:5]}. Prompt-injection guard refuses fabricated citations."
            )
            last_report = report
            last_response = response
            last_system_prompt = system_prompt
            if attempt < max_attempts:
                count = len(fabricated)
                phrase = "1 unknown evidence ID" if count == 1 else f"{count} unknown evidence IDs"
                _emit_retry_banner(
                    f"Model cited {phrase} (not present in scan findings)",
                    attempt=attempt,
                    max_attempts=max_attempts,
                )
                _reset_progress(on_chunk, attempt + 1, max_attempts)
                continue
            # Final attempt rejected. Graceful repair — strip the fabricated
            # citations rather than fail the whole run.
            repaired_report, repair_notes = _repair_fabricated_citations(
                report, fabricated=fabricated
            )
            sys.stderr.write(
                f"[gap] After {max_attempts} attempts, model still cited evidence that "
                f"doesn't exist. Auto-repairing affected classifications:\n"
            )
            for note in repair_notes:
                sys.stderr.write(f"        - {note}\n")
            return repaired_report, response, system_prompt

        # Unreachable — every path through the loop returns or raises.
        if last_validator_error is not None and last_report is not None:
            # Defensive fallback (should not hit; the attempt==max_attempts
            # branch above returns the repaired report). Repair anyway so
            # we never surface a fabricated-id error to the caller.
            assert last_response is not None
            assert last_system_prompt is not None
            fabricated_final = _compute_fabricated_ids(
                last_report,
                fenced_prompt=last_system_prompt + "\n" + user_message,
                nonce=nonce,
            )
            repaired, _ = _repair_fabricated_citations(last_report, fabricated=fabricated_final)
            return repaired, last_response, last_system_prompt
        assert last_pydantic_error is not None
        raise last_pydantic_error

    def run(self, input: GapAgentInput) -> GapReport:
        """Classify every indicator in `input.indicators` across N batched LLM calls.

        v0.1.143 / #348 — per-batch processing:

        - The work is split into batches of `DEFAULT_BATCH_SIZE_KSIS` (5)
          indicators each by `plan_batches`. Each batch carries ONLY the
          evidence whose `ksis_evidenced` overlaps with the batch's KSI ids
          (~10x prompt size reduction vs. the pre-v0.1.143 single call).
        - Each batch independently runs through `_invoke_with_validator_retry`,
          so the existing 3-attempt / feedback-on-retry / graceful-repair
          logic (v0.1.125 / v0.1.139 / v0.1.140) applies per batch. A
          failed batch does not abort other batches.
        - `compute_unmapped_findings` builds the UnmappedFinding list
          deterministically from evidence with `ksis_evidenced=[]` —
          no LLM token cost for that part of the report.
        - `fill_missing_classifications` is a safety net: any batch
          indicator the model omitted gets a `not_implemented` placeholder
          with an auto-repair marker.

        Per-claim provenance records carry their batch's `input_tokens`/
        `output_tokens` (the batch-call costs), so receipts.log aggregation
        in `shell/state.py` and `cost_summary` continue to work unchanged.
        """
        # One nonce per agent run; threaded through every fence and the
        # post-generation validator so content-authored strings can't forge
        # matching tags (DECISIONS 2026-04-22 Phase 2 post-review fixup F).
        # Same nonce across batches — each batch's prompt independently
        # carries its own subset of fences with this nonce.
        nonce = new_fence_nonce()
        # max_tokens default: 32768 on both backends.
        max_tokens = self._resolve_max_tokens(default_anthropic=32768, default_bedrock=32768)

        # Dry-run short-circuit: `_invoke_llm` returns an empty stub report
        # under dry-run, so per-batch processing would fire `fill_missing_classifications`
        # for every indicator in every batch and produce N*K spurious placeholder
        # classifications. Honor the dry-run path with a single call (the stub
        # captures the prompt, returns the empty report — same behavior as
        # pre-v0.1.143 dry-run, no batching artifacts).
        from efterlev.agents.dry_run import get_active_dry_run_session

        if get_active_dry_run_session() is not None:
            mapped, unmapped = _split_mapped_unmapped(input.evidence)
            user_message = _build_user_message(
                input.indicators,
                mapped,
                unmapped,
                nonce=nonce,
                scan_summary=input.scan_summary,
            )
            report, _response, _system_prompt = self._invoke_with_validator_retry(
                user_message=user_message,
                max_tokens=max_tokens,
                nonce=nonce,
                on_chunk=input.progress_callback,
            )
            return report

        batches = plan_batches(input.indicators, input.evidence)
        all_classifications: list[KsiClassification] = []
        record_ids: list[str] = []
        store = get_active_store()

        # Studio event spine (DECISIONS 2026-05-22, Phase 1): emit the agent's
        # reasoning as a typed stream so the Studio starfield can turn each
        # star to its verdict live. No-op when no bus is bound (the CLI path).
        from efterlev.events import (
            AgentFinished,
            AgentStarted,
            BatchStarted,
            KsiClassified,
            emit,
            get_active_bus,
        )

        _bus_active = get_active_bus() is not None
        if _bus_active:
            total_ksis = sum(len(b.indicators) for b in batches)
            emit(AgentStarted(agent=self.name, total_ksis=total_ksis))
        _verdict_counts: dict[str, int] = {}

        # v0.1.150 / #355: detect which backend the LLM client is so we can
        # surface it on the first batch dispatch line — users testing the
        # subscription backend asked "how do I know it's using my Max plan
        # and not the API?"
        backend_hint = _describe_backend(self.client)

        for batch in batches:
            # Surface batch progress so the user sees movement during long
            # multi-batch runs. Stream-callback heartbeat fills any gap
            # > 2s within a batch (per v0.1.142 dispatch line + v0.1.141
            # reset semantics).
            _emit_batch_dispatch_line(batch, backend_hint=backend_hint)
            if _bus_active:
                emit(
                    BatchStarted(
                        index=batch.index,
                        total=batch.total,
                        ksis=[ind.id for ind in batch.indicators],
                    )
                )
            # v0.1.155 / #360: capture per-batch wall-clock so cache hits
            # (~0.1s) vs real LLM calls (~30-90s) are visible at a glance —
            # the prior `[gap] done in T` line aggregated all batches into
            # one number that hid per-batch behavior.
            import time as _time

            batch_t0 = _time.perf_counter()

            user_message = _build_user_message(
                batch.indicators,
                batch.evidence,
                # Unmapped evidence handled deterministically post-batches —
                # don't waste tokens asking the LLM to enumerate it.
                unmapped_evidence=[],
                nonce=nonce,
                scan_summary=input.scan_summary,
            )

            batch_report, response, _system_prompt = self._invoke_with_validator_retry(
                user_message=user_message,
                max_tokens=max_tokens,
                nonce=nonce,
                on_chunk=input.progress_callback,
            )
            _emit_batch_completion_line(batch, elapsed=_time.perf_counter() - batch_t0)

            # Safety net: ensure every batch indicator got a classification.
            # Per-batch this surfaces immediately; pre-batching it was
            # invisible (1 missing out of 60 vs 1 out of 5).
            batch_report, fill_notes = fill_missing_classifications(batch_report, batch.indicators)
            if fill_notes:
                # v0.1.146 / #351: fill_notes now also covers dropped unknown
                # KSI ids in addition to omissions; use a more generic phrase.
                sys.stderr.write(
                    f"[gap] Batch {batch.index}/{batch.total}: "
                    f"{len(fill_notes)} correction(s) applied:\n"
                )
                for note in fill_notes:
                    sys.stderr.write(f"        - {note}\n")

            all_classifications.extend(batch_report.ksi_classifications)

            if _bus_active:
                for clf in batch_report.ksi_classifications:
                    _verdict_counts[clf.status] = _verdict_counts.get(clf.status, 0) + 1
                    emit(
                        KsiClassified(
                            ksi=clf.ksi_id,
                            status=clf.status,
                            evidence_count=len(clf.evidence_ids),
                            rationale=clf.rationale,
                        )
                    )

            # Persist one Claim per KSI classification, linking back to the
            # evidence IDs the model cited. `cited_evidence_ids` are already
            # in `sha256:<hex>` form (the fence id format) which matches
            # evidence record_ids exactly, so Claim.derived_from stores
            # them as-is — no prefix translation at the boundary.
            for clf in batch_report.ksi_classifications:
                claim = Claim.create(
                    claim_type="classification",
                    content={
                        "ksi_id": clf.ksi_id,
                        "status": clf.status,
                        "rationale": clf.rationale,
                    },
                    confidence="medium",
                    derived_from=list(clf.evidence_ids),
                    model=response.model,
                    prompt_hash=response.prompt_hash,
                )
                if store is not None:
                    record = store.write_record(
                        payload=claim.model_dump(mode="json"),
                        record_type="claim",
                        derived_from=list(clf.evidence_ids),
                        agent=self.name,
                        model=response.model,
                        prompt_hash=response.prompt_hash,
                        metadata={
                            "kind": "ksi_classification",
                            "ksi_id": clf.ksi_id,
                            # Per-batch token counts. The shell's
                            # cost-aggregation in receipts.log sums these
                            # across the whole run, so the user still sees
                            # one total cost figure.
                            "input_tokens": response.input_tokens,
                            "output_tokens": response.output_tokens,
                            "batch_index": batch.index,
                            "batch_total": batch.total,
                        },
                    )
                    record_ids.append(record.record_id)

        unmapped_findings = compute_unmapped_findings(input.evidence)

        if _bus_active:
            emit(AgentFinished(counts=dict(_verdict_counts)))

        return GapReport(
            ksi_classifications=all_classifications,
            unmapped_findings=unmapped_findings,
            claim_record_ids=record_ids,
        )


def _format_prompt_too_long_message(raw_error: str) -> str:
    """Translate a provider prompt-too-long error into actionable guidance.

    Bedrock raises:
      bedrock completion failed: An error occurred (ValidationException) ...
      The model returned the following errors: prompt is too long:
      207302 tokens > 200000 maximum

    That's enough information to compute three concrete workarounds:
      1. Switch backend (Anthropic API has 1M context vs Bedrock's 200k)
      2. Scan a smaller subdir (fewer evidence records → smaller prompt)
      3. Filter the baseline to a subset of KSIs (planned for a future
         release; mentioned in the error as the architectural fix)
    """
    return (
        "evidence prompt exceeded the model's context window.\n"
        f"  Provider reported: {raw_error.strip()}\n"
        "\n"
        "  This workspace has too much evidence for a single LLM call. "
        "Three things you can do right now:\n"
        "    1. Switch to the Anthropic API backend (1M context, "
        "vs Bedrock's 200k). Run `/setup` and choose Anthropic.\n"
        "    2. Scan a smaller subdirectory (e.g. one Terraform module at "
        "a time) so fewer evidence records are bundled into the prompt.\n"
        "    3. Wait for the per-KSI batching arc (planned) which will "
        "automatically chunk large workspaces into multiple calls.\n"
        "\n"
        "  If you switched recently and saw this fail, your previous scan's "
        "evidence is still in the workspace — re-run `/scan` after `/setup` "
        "to reset."
    )


def _describe_backend(client: Any) -> str | None:
    """Return a short user-facing string describing which backend `client`
    routes through, or None if it can't be identified (test stubs etc.).

    Duck-typed on class name to avoid importing every backend module here;
    the gap agent shouldn't grow a hard dependency on which clients exist.
    v0.1.150 / #355.
    """
    if client is None:
        return None
    # Unwrap the cache layer to find the real backend underneath.
    inner = getattr(client, "inner", client)
    name = type(inner).__name__
    if name == "ClaudeCodeClient":
        return "via Claude Code subscription (no per-call billing)"
    if name == "AnthropicClient":
        return "via Anthropic API (pay-per-token)"
    if name == "AnthropicBedrockClient":
        return "via AWS Bedrock (pay-per-token)"
    return None


def _emit_batch_dispatch_line(batch: Batch, *, backend_hint: str | None = None) -> None:
    """Print a per-batch starting line so the user sees movement across batches.

    Multi-batch runs (the v0.1.143 default) without this would show
    silence between batches — the stream-callback heartbeat only fires
    while a single LLM call is in flight. Suppressed when stderr isn't
    a TTY (matches `_emit_dispatch_line`).

    v0.1.150 / #355: only the FIRST batch gets a `backend_hint` appended
    (e.g. "via Claude Code subscription") so the user can confirm at a
    glance which backend is being used without cluttering every batch.
    """
    if not sys.stderr.isatty():
        return
    ksi_word = "KSI" if len(batch.indicators) == 1 else "KSIs"
    ev_word = "record" if len(batch.evidence) == 1 else "records"
    hint = f" — {backend_hint}" if backend_hint and batch.index == 1 else ""
    sys.stderr.write(
        f"[gap] Batch {batch.index}/{batch.total}: classifying "
        f"{len(batch.indicators)} {ksi_word} against {len(batch.evidence)} "
        f"evidence {ev_word}...{hint}\n"
    )


def _emit_batch_completion_line(batch: Batch, *, elapsed: float) -> None:
    """Print per-batch wall-clock after a batch finishes (v0.1.155 / #360).

    Cache hits drop the gap stage from ~50s/batch to ~0.1s/batch; before
    this line the only timing signal was the aggregate "[gap] done in T"
    at the very end, which hid which batches replayed from cache vs hit
    the LLM. Now each batch's elapsed prints on completion so the user
    sees the cache state in real time. TTY-suppressed like the other
    progress lines so piped output stays clean.
    """
    if not sys.stderr.isatty():
        return
    if elapsed < 60:
        rendered = f"{elapsed:.1f}s"
    else:
        minutes, sec = divmod(int(elapsed), 60)
        rendered = f"{minutes}m{sec:02d}s"
    sys.stderr.write(f"[gap] Batch {batch.index}/{batch.total} done in {rendered}\n")


def _emit_dispatch_line(*, attempt: int, max_attempts: int) -> None:
    """Print an immediate "starting" line BEFORE the LLM call (v0.1.142 / #347).

    The stream-callback heartbeat only fires once chunks start arriving,
    which is a multi-second wait on Bedrock cold-start (~10-30s before
    the first token). Without this line, the user types `/agent gap`
    and stares at silence wondering if it's hung. The line is suppressed
    when stderr isn't a TTY so test logs and piped output stay clean.

    v0.1.155 / #360: dropped the "typically 30-90s" duration claim that
    was misleading on cache hits — customer's gap stage dropped from
    1247s to 0.3s after the v0.1.153 cache fix, but the "30-90s" line
    still printed before every sub-millisecond batch. The per-batch
    completion line (`[gap] Batch N/M done in T`) now reveals timing
    accurately for both miss and hit.
    """
    if not sys.stderr.isatty():
        return
    if attempt == 1:
        sys.stderr.write("[gap] Starting analysis...\n")
    else:
        sys.stderr.write(f"[gap] Calling model again (attempt {attempt}/{max_attempts})...\n")


def _emit_retry_banner(reason: str, *, attempt: int, max_attempts: int) -> None:
    """Print a plain-language retry banner to stderr (v0.1.141 / #346).

    Replaces the prior format
    ("gap_agent: validator rejected attempt N (ExceptionClassName, ...);
    retrying with feedback (vX.Y.Z / #NNN)")
    with something a non-developer can read:

        [gap] Model cited an unknown evidence ID. Retrying with stricter
              instructions (attempt 2/3)...

    Consistent `[gap]` prefix matches the per-KSI progress lines so the
    user sees one continuous activity stream rather than a mix of
    technical and user-facing output.
    """
    next_attempt = attempt + 1
    sys.stderr.write(
        f"[gap] {reason}. Retrying with stricter instructions "
        f"(attempt {next_attempt}/{max_attempts})...\n"
    )


def _reset_progress(
    on_chunk: Callable[[str], None] | None, next_attempt: int, max_attempts: int
) -> None:
    """If `on_chunk` is a `GapProgressReporter`, reset it for the next attempt.

    Without this, attempt 2's identical 60 KSI IDs collide with attempt 1's
    dedup set and the user sees silence for the entire retry duration. The
    reset clears the seen set and installs a "Retry N/M" label that the
    heartbeat picks up until per-KSI lines start flowing again. Duck-typed:
    non-reporter callables (or None) are ignored, so the retry layer stays
    decoupled from `gap_progress.py`.
    """
    if on_chunk is None or not hasattr(on_chunk, "reset_for_next_attempt"):
        return
    on_chunk.reset_for_next_attempt(  # type: ignore[attr-defined]
        f"Retry {next_attempt}/{max_attempts} with stricter instructions"
    )


def _user_message_with_feedback(
    base_user_message: str,
    *,
    rejected_ids: set[str] | None = None,
    json_parse_errors: list[str] | None = None,
) -> str:
    """Append system-controlled feedback blocks describing prior-attempt failures.

    Two block types, appended in order when their corresponding history is
    non-empty:

      - CITATION REJECTION: lists evidence IDs the previous attempt cited
        that don't trace to any `<evidence_*>` fence. Tells the LLM not to
        re-cite them. Used on retry after a validator rejection.
      - JSON PARSE FAILURE: tells the LLM its previous response wasn't
        valid JSON and asks for ONLY a JSON object next time (no markdown
        fences, no prose, no truncation). Used on retry after `json.loads`
        raised inside `Agent._invoke_llm` (v0.1.140 / #345).

    Both blocks render *outside* the `<evidence_*>` fences — content-authored
    strings can't forge them because the sections are generated by
    Efterlev. With no failure history, returns the base message unchanged.
    """
    blocks: list[str] = []
    if rejected_ids:
        sorted_ids = sorted(rejected_ids)
        listed = "\n".join(f"  - {eid}" for eid in sorted_ids[:25])
        extra_count = len(sorted_ids) - 25
        overflow = f"\n  ... and {extra_count} more" if extra_count > 0 else ""
        blocks.append(
            "--- CITATION REJECTION FEEDBACK (auto-generated) ---\n"
            "Your previous attempt cited evidence IDs that do not exist in the "
            "<evidence_*> fences above. Those citations were rejected as "
            "fabricated. The following IDs MUST NOT appear in this attempt's "
            "`evidence_ids` arrays:\n"
            f"{listed}{overflow}\n\n"
            "Only cite `evidence_id` values that appear inside an `<evidence_*>` "
            'fence above (look for the `id="sha256:..."` attribute on each '
            "fence opener). If you cannot find a real evidence ID that supports "
            'a positive classification, set `status="not_implemented"` rather '
            "than fabricate one."
        )
    if json_parse_errors:
        latest = json_parse_errors[-1]
        # Truncate the captured error — sometimes it embeds the first 200 chars
        # of the bad response, which is helpful but bloats the prompt.
        latest_short = latest[:400] + ("..." if len(latest) > 400 else "")
        blocks.append(
            "--- JSON PARSE FAILURE FEEDBACK (auto-generated) ---\n"
            "Your previous response could not be parsed as JSON. The parser "
            f"reported: {latest_short}\n\n"
            "REQUIREMENTS for this attempt:\n"
            "  - Emit ONLY a single JSON object matching the schema "
            '(with "ksi_classifications" and "unmapped_findings" keys).\n'
            "  - Do NOT wrap the JSON in markdown fences (no ```json ... ```).\n"
            "  - Do NOT include explanatory prose, notes, or commentary "
            "outside the JSON.\n"
            "  - Ensure every opening brace, bracket, and quote has a "
            "matching close.\n"
            "  - Keep `rationale` strings concise (<200 chars each) to "
            "avoid hitting output limits.\n"
            "  - The response will be parsed by `json.loads`; anything not "
            "strictly valid JSON will fail."
        )
    if not blocks:
        return base_user_message
    return base_user_message + "\n\n" + "\n\n".join(blocks) + "\n"


def _split_mapped_unmapped(
    evidence: list[Evidence],
) -> tuple[list[Evidence], list[Evidence]]:
    """Bucket evidence by whether it carries any KSI attribution."""
    mapped: list[Evidence] = []
    unmapped: list[Evidence] = []
    for ev in evidence:
        if ev.ksis_evidenced:
            mapped.append(ev)
        else:
            unmapped.append(ev)
    return mapped, unmapped


def _build_user_message(
    indicators: list[Indicator],
    mapped_evidence: list[Evidence],
    unmapped_evidence: list[Evidence],
    *,
    nonce: str,
    scan_summary: ScanSummary | None = None,
) -> str:
    """Assemble the per-batch user message with fenced evidence blocks.

    v0.1.143 / #348: the unmapped section is omitted entirely when
    `unmapped_evidence` is empty (the batched-run default — unmapped
    findings are now computed deterministically post-batch, so no
    unmapped evidence is sent to the LLM). Saves tokens on every
    batch call.
    """
    ksi_lines: list[str] = []
    for ind in indicators:
        statement = ind.statement or "(no statement in FRMR)"
        ksi_lines.append(f"- {ind.id} — {ind.name}: {statement}")

    fenced_mapped = format_evidence_for_prompt(mapped_evidence, nonce=nonce)
    summary_block = _format_scan_summary_block(scan_summary)

    parts = [
        "Classify the following KSIs from the loaded FedRAMP 20x baseline.\n\n",
        summary_block,
        "## KSIs to classify\n\n",
        "\n".join(ksi_lines),
        "\n\n## Evidence attached to one or more KSIs\n\n",
        fenced_mapped,
    ]
    if unmapped_evidence:
        fenced_unmapped = format_evidence_for_prompt(unmapped_evidence, nonce=nonce)
        parts.append("\n\n## Evidence with no KSI attribution (unmapped)\n\n")
        parts.append(fenced_unmapped)
    parts.append(
        "\n\nReturn JSON matching the schema in the system prompt. "
        "No prose, no code fences, no commentary."
    )
    return "".join(parts)


def _format_scan_summary_block(scan_summary: ScanSummary | None) -> str:
    """When the scan was thin-evidence due to module composition, surface that
    fact to the model so its rationales can reflect the coverage limitation
    rather than treating thin evidence as a real implementation gap.

    Plan-mode scans (modules already expanded) and HCL-mode scans against
    resource-only codebases produce no block — the prompt stays focused on
    the evidence itself.
    """
    if scan_summary is None or not scan_summary.recommend_plan_json:
        return ""
    return (
        "## Scan coverage note\n\n"
        f"This scan was HCL-mode (parsed `.tf` files directly). The codebase "
        f"contains {scan_summary.module_calls} `module` calls alongside "
        f"{scan_summary.resources_parsed} root-level `resource` declarations, "
        f"and produced {scan_summary.evidence_count} evidence records. "
        "Detectors do not follow into upstream module sources, so resources "
        "defined inside those modules (typically EKS clusters, VPCs, IAM "
        "roles, KMS keys, security groups, CloudTrail) are invisible in this "
        "mode. Plan-JSON expansion would surface them.\n\n"
        "When classifying a KSI as `not_implemented` against this scan, "
        "explicitly note in your rationale that the absence may be a coverage "
        "gap rather than a real implementation gap, and suggest plan-JSON "
        "scanning if the KSI is one a Terraform-defined workload would "
        "typically address.\n\n"
    )


def _compute_fabricated_ids(report: GapReport, *, fenced_prompt: str, nonce: str) -> set[str]:
    """Return the set of cited evidence IDs that don't match any prompt fence.

    Computes `cited - fenced_ids`. Empty set means the report is clean.
    Non-empty means the LLM fabricated (or hallucinated, or got an ID
    wrong by a few characters — the validator treats all three the same
    because the design call is "cited evidence must trace to a record
    we put into the prompt"). Split out from `_validate_cited_ids` so
    the retry loop can use the set as feedback for the next attempt
    (v0.1.139 / #344) rather than discarding it via `raise`.
    """
    fenced_ids = parse_evidence_fence_ids(fenced_prompt, nonce=nonce)
    cited: set[str] = set()
    for clf in report.ksi_classifications:
        cited.update(clf.evidence_ids)
    for um in report.unmapped_findings:
        cited.add(um.evidence_id)
    return cited - fenced_ids


def _validate_cited_ids(report: GapReport, *, fenced_prompt: str, nonce: str) -> None:
    """Enforce design call #3: every cited id must correspond to a real fence.

    Thin wrapper over `_compute_fabricated_ids` that raises on non-empty
    fabricated set. Callers that want to *handle* fabricated citations
    (e.g. the graceful-repair fallback) should call `_compute_fabricated_ids`
    directly.
    """
    fabricated = _compute_fabricated_ids(report, fenced_prompt=fenced_prompt, nonce=nonce)
    if fabricated:
        raise AgentValidatorRejectionError(
            f"gap agent output cites evidence IDs not present in the prompt: "
            f"{sorted(fabricated)[:5]}. Prompt-injection guard refuses fabricated citations."
        )


def _repair_fabricated_citations(
    report: GapReport, *, fabricated: set[str]
) -> tuple[GapReport, list[str]]:
    """Strip fabricated citations from the report; downgrade orphaned positives.

    Per-classification logic:
      - Remove every `evidence_id` that's in `fabricated`.
      - If the classification was `status="implemented"|"partial"` and ends
        with **zero** valid `evidence_ids` after stripping, downgrade to
        `status="not_implemented"` and append a marker to the rationale so
        the user (and any downstream OSCAL/POA&M consumer) can see the
        auto-repair in the artifact rather than wondering why the agent
        contradicted itself. The downgrade is honest: a positive claim
        with no real evidence is functionally not_implemented from
        anyone reviewing the bundle.
      - Other statuses keep their (now-empty) citations — the validator
        only requires evidence for positive statuses.

    Drops any `UnmappedFinding` whose `evidence_id` is fabricated — those
    are bogus references that don't trace to a real scan record.

    Returns the repaired `GapReport` plus a list of human-readable repair
    notes (one per change) suitable for printing to stderr and recording
    in provenance.
    """
    notes: list[str] = []
    repaired_classifications: list[KsiClassification] = []
    for clf in report.ksi_classifications:
        clean_ids = [eid for eid in clf.evidence_ids if eid not in fabricated]
        stripped_count = len(clf.evidence_ids) - len(clean_ids)
        if stripped_count == 0:
            repaired_classifications.append(clf)
            continue
        if clf.status in ("implemented", "partial") and not clean_ids:
            cite_word = "citation" if stripped_count == 1 else "citations"
            notes.append(
                f"{clf.ksi_id}: downgraded '{clf.status}' to 'not_implemented' "
                f"(cited {stripped_count} {cite_word} that don't exist in scan findings)"
            )
            repaired_classifications.append(
                KsiClassification(
                    ksi_id=clf.ksi_id,
                    status="not_implemented",
                    rationale=(
                        clf.rationale + " [auto-repair: LLM cited fabricated evidence; downgraded "
                        "from positive status to honest not_implemented]"
                    ),
                    evidence_ids=[],
                )
            )
        else:
            if stripped_count == 1:
                phrase = "1 citation that doesn't exist"
            else:
                phrase = f"{stripped_count} citations that don't exist"
            notes.append(
                f"{clf.ksi_id}: removed {phrase} in scan findings (status '{clf.status}' unchanged)"
            )
            repaired_classifications.append(
                KsiClassification(
                    ksi_id=clf.ksi_id,
                    status=clf.status,
                    rationale=clf.rationale,
                    evidence_ids=clean_ids,
                )
            )

    repaired_unmapped = [um for um in report.unmapped_findings if um.evidence_id not in fabricated]
    if len(repaired_unmapped) != len(report.unmapped_findings):
        dropped = len(report.unmapped_findings) - len(repaired_unmapped)
        notes.append(f"unmapped_findings: dropped {dropped} entry with fabricated evidence_id")

    repaired_report = GapReport(
        ksi_classifications=repaired_classifications,
        unmapped_findings=repaired_unmapped,
        claim_record_ids=list(report.claim_record_ids),
    )
    return repaired_report, notes
