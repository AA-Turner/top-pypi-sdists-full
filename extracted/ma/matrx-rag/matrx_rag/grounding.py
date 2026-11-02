"""Faithfulness / grounding verification — frontier model as judge.

Workflow:

    user_query
       ↓ (some agent generates an answer using retrieved chunks)
    answer_text + retrieved_chunks
       ↓ verify_grounded()
    list[ClaimVerdict]
       (each claim → supported / unsupported / partial,
        with the chunk_ids that support it)

How the model is reached
------------------------
Through the host-injected ``llm_provider`` seam (``matrx_rag._ext``) — NEVER a
provider SDK. matrx-rag is provider-agnostic and standalone-first: aidream
injects a matrx-ai-backed provider (full model catalog, cost tracking, and the
sampling-param policy that keeps adaptive models from 400ing); a standalone
install falls back to the default OpenAI provider; matrx-local swaps in a local
llama-server. The judge just asks for a model and a temperature and lets the
provider decide what is legal on that route.

``DEFAULT_JUDGE_MODEL`` is a frontier model that scores well on entailment / NLI;
any ``judge_model`` the injected provider can route is valid.

The verifier runs in two passes so we can prompt-cache aggressively:

  1. **Claim extraction** — one small call: split the answer into
     atomic, declarative claims. Cheap, deterministic enough at temp=0.
  2. **Per-claim judging** — one call that judges ALL claims against the
     retrieved chunks in one shot, so the chunk text is paid for once.
     STREAMED: each verdict object is parsed and reported the moment its
     tokens complete, so progress is real rather than an end-of-call burst.

Output shape::

    {
      "claims": [
        {
          "claim": "Patient was prescribed gabapentin 300mg TID.",
          "verdict": "supported",     # supported | partial | unsupported
          "confidence": 0.92,
          "supporting_chunk_ids": ["..."],
          "reasoning": "..."
        },
        ...
      ],
      "overall_faithfulness": 0.85,    # mean confidence of supported claims
      "judge_model": "claude-...",
      "latency_ms": 1234
    }
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_rag._ext import get_llm_provider

logger = logging.getLogger(__name__)

DEFAULT_JUDGE_MODEL = "claude-haiku-4-5"


# Sampling params: the judge asks for ``temperature=0`` (determinism is what a
# fact-checker wants) and the PROVIDER decides whether that key survives. The
# host-injected provider routes through a real model catalog and drops
# temperature/top_p/top_k for api_classes that reject them — the adaptive
# Anthropic models (claude 4.6+ / the claude-5 family) hard-400 on ANY sampling
# param. So we get determinism where it's available and safety where it isn't,
# with NO per-model branching here.
#
# This module used to hold a raw ``AsyncAnthropic`` client and hand-manage that
# policy itself (plus a dead ``_sampling_kwargs`` probe). Both are gone: every
# call now goes through the ``llm_provider`` seam. Do not reintroduce a provider
# SDK here — matrx-rag must stay provider-agnostic, and the funnel owns policy.

# "unchecked" is NOT a judgment about the answer: it means the judge never
# ruled on this claim (its output was cut off or incomplete, even after a
# batched retry). It must never be scored or shown as "unsupported".
Verdict = Literal["supported", "partial", "unsupported", "unchecked"]


@dataclass
class ClaimVerdict:
    claim: str
    verdict: Verdict
    confidence: float
    supporting_chunk_ids: list[str] = field(default_factory=list)
    reasoning: str = ""


class JudgeUnavailableError(RuntimeError):
    """The judge could not be RUN — a config/provider/timeout failure.

    Emphatically NOT a verdict. "We could not check this answer" and "this answer
    is unsupported" are different facts, and collapsing them is dangerous: a
    misconfigured provider would otherwise score every answer 0.0 faithfulness,
    which reads as "the model hallucinated" when it actually means "the judge
    never ran". Callers must branch on ``FaithfulnessReport.error``.
    """


@dataclass
class FaithfulnessReport:
    claims: list[ClaimVerdict]
    overall_faithfulness: float
    judge_model: str
    latency_ms: int
    # Set when the judge could not run at all (see JudgeUnavailableError).
    # When this is non-None, ``overall_faithfulness`` is MEANINGLESS — it is 0.0
    # because nothing was verified, not because the answer was unsupported.
    error: str | None = None
    # Claims the judge never ruled on (verdict == "unchecked"). They are left
    # out of ``overall_faithfulness``; a caller showing a score must also show
    # this count so a partial check never reads as a complete one.
    unchecked_claims: int = 0


# Per-claim progress seams. The judge is ONE model call that emits a JSON
# array of verdict objects; streaming that call and parsing each object as
# its tokens complete gives REAL incremental per-claim progress (never fake
# end-of-call bursts). Callbacks are best-effort: a callback failure must
# never fail the (paid) verification call.
OnClaims = Callable[[list[str]], Awaitable[None]]
OnVerdict = Callable[[int, ClaimVerdict], Awaitable[None]]


class _JsonArrayObjectScanner:
    """Incrementally extracts completed top-level ``{...}`` objects from a
    streaming JSON array (``[{...}, {...}, ...]``). String/escape aware;
    tolerates leading markdown fences and prose before the array."""

    def __init__(self) -> None:
        self._buf = ""
        self._pos = 0
        self._depth = 0
        self._in_string = False
        self._escape = False
        self._obj_start = -1

    def feed(self, text: str) -> list[dict[str, Any]]:
        self._buf += text
        out: list[dict[str, Any]] = []
        while self._pos < len(self._buf):
            ch = self._buf[self._pos]
            if self._in_string:
                if self._escape:
                    self._escape = False
                elif ch == "\\":
                    self._escape = True
                elif ch == '"':
                    self._in_string = False
            elif ch == '"':
                self._in_string = True
            elif ch == "{":
                if self._depth == 0:
                    self._obj_start = self._pos
                self._depth += 1
            elif ch == "}":
                self._depth -= 1
                if self._depth == 0 and self._obj_start >= 0:
                    raw = self._buf[self._obj_start : self._pos + 1]
                    self._obj_start = -1
                    try:
                        parsed = json.loads(raw)
                        if isinstance(parsed, dict):
                            out.append(parsed)
                    except json.JSONDecodeError:
                        pass  # malformed object — the final full parse decides
                elif self._depth < 0:
                    self._depth = 0
            self._pos += 1
        return out


def _verdict_from_item(claim: str, item: dict[str, Any]) -> ClaimVerdict:
    verdict_raw = str(item.get("verdict", "unsupported")).lower().strip()
    if verdict_raw not in ("supported", "partial", "unsupported"):
        verdict_raw = "unsupported"
    return ClaimVerdict(
        claim=claim,
        verdict=verdict_raw,  # type: ignore[arg-type]
        confidence=float(item.get("confidence", 0.0) or 0.0),
        supporting_chunk_ids=[str(x) for x in (item.get("supporting_chunk_ids") or [])],
        reasoning=str(item.get("reasoning", ""))[:500],
    )



# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------


# The passages and claims are the DATA of one run, so they ride the user turn,
# never the system prompt (THE SYSTEM-PROMPT LAW) — as the two values alone, no
# code-written wording around them (THE USER-INPUT LAW). In aidream the
# ``rag.grounding_judge`` mandate's Holder authors that turn itself from the
# same two values by name (``offered``). The package sends no instructions: the host
# provider owns them per ``purpose`` (``grounding_claim_extract`` / ``grounding_judge``).


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _strip_json_fence(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[1] if "\n" in s else s
        if s.endswith("```"):
            s = s.rsplit("```", 1)[0]
    return s.strip()


def _format_passages(retrieved: list[dict]) -> str:
    lines = []
    for r in retrieved:
        cid = r.get("chunk_id") or r.get("id") or "?"
        text = (r.get("content_text") or r.get("snippet") or "").strip()
        # Cap each passage to 1500 chars so the judge prompt stays sane.
        if len(text) > 1500:
            text = text[:1500] + "…"
        lines.append(f"[chunk_id={cid}]\n{text}")
    return "\n\n---\n\n".join(lines)


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------


async def extract_claims(
    answer: str,
    *,
    judge_model: str | None = None,
    judge_offering_id: str | None = None,
    timeout: float = 30.0,
) -> list[str]:
    """Run pass 1 — split ``answer`` into atomic factual claims.

    Returns at most ~50 claims. Raises :class:`JudgeUnavailableError` when
    extraction could not run or returned something unreadable — it used to
    fall back to "the whole answer is one claim" with a warning log, which
    turned a failed check into a plausible-looking verdict.
    """
    if not answer.strip():
        return []
    model = judge_model or DEFAULT_JUDGE_MODEL
    provider = get_llm_provider()
    from matrx_rag._ext import provider_call_kwargs

    try:
        raw = await asyncio.wait_for(
            provider.chat(
                [
                    {"role": "user", "content": answer},
                ],
                model=model,
                # The provider drops temperature for routes that reject it.
                temperature=0,
                max_tokens=2000,
                purpose="grounding_claim_extract",
                # The answer BY NAME, so a workflow Holder gets it as an input.
                **provider_call_kwargs(
                    provider.chat, {"answer": answer}, offering_id=judge_offering_id
                ),
            ),
            timeout=timeout,
        )
    except TimeoutError as exc:
        raise JudgeUnavailableError(f"Claim extraction timed out after {timeout}s") from exc
    except Exception as exc:  # noqa: BLE001 — every cause is one refusal, named
        raise JudgeUnavailableError(f"Claim extraction failed: {exc}") from exc
    raw = _strip_json_fence((raw or "").strip())
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise JudgeUnavailableError("Claim extraction returned text that is not JSON") from exc
    if not isinstance(parsed, list):
        raise JudgeUnavailableError("Claim extraction returned JSON that is not a list")
    return [str(c).strip() for c in parsed if str(c).strip()]


async def _judge_pass(
    claims: list[str],
    retrieved: list[dict],
    *,
    judge_model: str | None = None,
    judge_offering_id: str | None = None,
    timeout: float = 60.0,
    on_verdict: OnVerdict | None = None,
) -> list[ClaimVerdict | None]:
    """One judge call over ``claims``. Returns one entry per claim; ``None`` means
    the judge did not rule on that claim (output cut off or incomplete).

    Run pass 2 — judge every claim against the retrieved chunks in one
    Claude call. ``retrieved`` is a list of dicts with at least
    ``chunk_id`` and ``content_text`` (or ``snippet``).

    The judge call is STREAMED: as each verdict object completes on the
    wire, ``on_verdict(claim_index, provisional_verdict)`` fires (0-based
    index into ``claims``). The returned list — rebuilt from the full
    response exactly as before — remains the authoritative result.
    """
    if not claims:
        return []
    if not retrieved:
        # No passages at all → all claims unsupported.
        return [
            ClaimVerdict(
                claim=c,
                verdict="unsupported",
                confidence=1.0,
                supporting_chunk_ids=[],
                reasoning="No retrieved passages available.",
            )
            for c in claims
        ]
    model = judge_model or DEFAULT_JUDGE_MODEL
    provider = get_llm_provider()
    passages_text = _format_passages(retrieved)
    claims_text = "\n".join(f"{i+1}. {c}" for i, c in enumerate(claims))
    # The same two values BY NAME, so a Holder authors its own turn from them.
    offered = {"passages": passages_text, "claims": claims_text}
    from matrx_rag._ext import provider_call_kwargs
    # No composed turn: the Holder authors the user turn from ``offered`` (the
    # host's ``_authored_user_turn``). The package sends the values, never text.
    messages: list[dict[str, Any]] = []

    # Per-claim progress is REAL: the judge emits a JSON array of verdict
    # objects, and the scanner hands each one to ``on_verdict`` the moment its
    # tokens complete — never a fake end-of-call burst. That needs a streaming
    # provider; one that only implements ``chat`` degrades to a single batch
    # (see below), which is honest but coarser.
    scanner = _JsonArrayObjectScanner()
    seen = 0
    reported: set[int] = set()  # never fire on_verdict twice for one claim

    async def _emit(item: dict[str, Any]) -> None:
        nonlocal seen
        if on_verdict is None:
            return
        # EVERYTHING here is best-effort. This runs inside the provider's
        # streaming loop, so an exception escaping it aborts the (already PAID)
        # judge call — a model emitting `"claim_index": null` or `"1."` must not
        # cost us the whole verification. That means the int() coercion belongs
        # INSIDE the try, not outside it.
        try:
            idx = int(item.get("claim_index", seen + 1)) - 1
            seen += 1
            if not (0 <= idx < len(claims)):
                return
            if idx in reported:  # a model that repeats a claim_index
                return
            reported.add(idx)
            await on_verdict(idx, _verdict_from_item(claims[idx], item))
        except Exception:
            logger.warning(
                "rag.grounding: on_verdict callback failed (best-effort)",
                exc_info=True,
            )

    async def _on_delta(text: str) -> None:
        if on_verdict is None:
            return
        for item in scanner.feed(text):
            await _emit(item)

    chat_stream = getattr(provider, "chat_stream", None)

    async def _run_judge() -> str:
        if chat_stream is not None:
            return await chat_stream(
                messages,
                model=model,
                on_delta=_on_delta,
                # The provider drops temperature for routes that reject it.
                temperature=0,
                max_tokens=4000,
                purpose="grounding_judge",
                **provider_call_kwargs(chat_stream, offered, offering_id=judge_offering_id),
            )
        # Degrade: no streaming on this provider. Run the call, then feed the
        # whole response through the SAME scanner so on_verdict still fires per
        # claim — just all at once, once the call returns.
        text = await provider.chat(
            messages,
            model=model,
            temperature=0,
            max_tokens=4000,
            purpose="grounding_judge",
            **provider_call_kwargs(provider.chat, offered, offering_id=judge_offering_id),
        )
        await _on_delta(text or "")
        return text or ""

    # A judge that could not RUN is not evidence the answer is wrong. Raise so
    # the caller can report "not verified" instead of silently scoring every
    # claim `unsupported` (which reads as "the model hallucinated" and is exactly
    # how a misconfigured provider gets mistaken for a bad answer).
    try:
        raw = await asyncio.wait_for(_run_judge(), timeout=timeout)
    except TimeoutError as exc:
        raise JudgeUnavailableError(f"Judge timed out after {timeout}s") from exc
    except JudgeUnavailableError:
        raise
    except Exception as exc:
        raise JudgeUnavailableError(f"Judge call failed: {exc}") from exc
    raw = _strip_json_fence((raw or "").strip())
    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, list):
            raise ValueError("judge output is not a list")
    except (json.JSONDecodeError, ValueError) as exc:
        # Most often the 4000-token output cap cut the array mid-object. That is
        # "the judge did not finish", NOT "every claim is unsupported": keep the
        # objects that did complete and leave the rest unjudged (None).
        logger.warning("rag.grounding.judge_claims parse (incomplete output): %s", exc)
        parsed = _JsonArrayObjectScanner().feed(raw)
    # A model may emit `"claim_index": null` / `"1."` / omit it entirely. Never
    # let that crash the (already PAID) verification — fall back to the object's
    # position in the array, which is what `claim_index` is supposed to mirror.
    def _index_of(item: dict[str, Any], position: int) -> int:
        try:
            return int(item["claim_index"]) - 1
        except (KeyError, TypeError, ValueError):
            return position

    by_index = {
        _index_of(item, i): item for i, item in enumerate(parsed) if isinstance(item, dict)
    }
    return [
        _verdict_from_item(claim, by_index[i]) if i in by_index else None
        for i, claim in enumerate(claims)
    ]


def _retry_batch_size(total: int, unruled: int) -> int:
    """How many unruled claims one retry call carries — derived, never tuned.

    The whole-list pass already measured what fits under the judge's output
    cap: it finished ``total - unruled`` verdicts before being cut off, so a
    retry of that many fits too. When it finished none, halve the remainder.
    """
    finished = total - unruled
    return finished if finished > 0 else max(1, unruled // 2)


def _unchecked(claim: str, why: str) -> ClaimVerdict:
    return ClaimVerdict(
        claim=claim,
        verdict="unchecked",
        confidence=0.0,
        reasoning=f"NOT VERIFIED (could not check) — {why}",
    )


async def judge_claims(
    claims: list[str],
    retrieved: list[dict],
    *,
    judge_model: str | None = None,
    judge_offering_id: str | None = None,
    timeout: float = 60.0,
    on_verdict: OnVerdict | None = None,
) -> list[ClaimVerdict]:
    """Judge every claim against the retrieved chunks.

    One streamed call first. If its answer is cut off or incomplete (the output
    cap can truncate a long claim list), the claims it never ruled on are retried
    in batches as large as the first pass managed to finish (see
    ``_retry_batch_size``). Claims still unruled come back with
    verdict ``"unchecked"`` ("couldn't check") — never ``"unsupported"``.
    """
    results = await _judge_pass(
        claims,
        retrieved,
        judge_model=judge_model,
        judge_offering_id=judge_offering_id,
        timeout=timeout,
        on_verdict=on_verdict,
    )
    missing = [i for i, v in enumerate(results) if v is None]
    batch_size = _retry_batch_size(len(claims), len(missing))
    if missing:
        logger.warning(
            "rag.grounding: judge left %d of %d claims unruled; retrying in batches of %d",
            len(missing),
            len(claims),
            batch_size,
        )
    for at in range(0, len(missing), batch_size):
        chunk = missing[at : at + batch_size]

        async def _remap(local: int, verdict: ClaimVerdict, _chunk: list[int] = chunk) -> None:
            if on_verdict is not None:
                await on_verdict(_chunk[local], verdict)

        try:
            batch = await _judge_pass(
                [claims[i] for i in chunk],
                retrieved,
                judge_model=judge_model,
                judge_offering_id=judge_offering_id,
                timeout=timeout,
                on_verdict=_remap if on_verdict is not None else None,
            )
        except JudgeUnavailableError as exc:
            logger.error("rag.grounding: batched retry could not run: %s", exc)
            continue
        for local, verdict in enumerate(batch):
            if verdict is not None:
                results[chunk[local]] = verdict
    return [
        v if v is not None else _unchecked(claims[i], "the judge's answer was cut off or incomplete")
        for i, v in enumerate(results)
    ]


async def _reported_model(requested: str | None, fallback: str) -> str:
    """The model that ACTUALLY judges. A host provider whose calls are held by
    a mandate names its Holder's model (``resolved_model``); reporting the
    package default instead would name a model that never ran."""
    provider = get_llm_provider()
    resolve = getattr(provider, "resolved_model", None)
    if callable(resolve):
        try:
            return str(await resolve("grounding_judge", requested))
        except Exception as exc:  # noqa: BLE001 — reporting must not fail the check
            logger.error("rag.grounding: could not name the judging model: %s", exc)
    return requested or fallback


async def _record_unavailable(exc: BaseException, *, stage: str) -> None:
    """A check that could not run is recorded durably, never only logged."""
    try:
        from matrx_utils import capture_error

        await capture_error(exc, kind="rag_grounding_unavailable", context={"stage": stage})
    except Exception as capture_exc:  # noqa: BLE001 — the error log already fired
        logger.error("rag.grounding: could not record the unavailable check: %s", capture_exc)


async def verify_grounded(
    *,
    answer: str,
    retrieved: list[dict],
    judge_model: str | None = None,
    judge_offering_id: str | None = None,
    on_claims: OnClaims | None = None,
    on_verdict: OnVerdict | None = None,
) -> FaithfulnessReport:
    """End-to-end: extract claims from ``answer`` and judge each against
    ``retrieved``. Returns a ``FaithfulnessReport`` with the verdicts
    and an overall score.

    Progress seams: ``on_claims(claims)`` fires once after pass 1 (claim
    extraction); ``on_verdict(index, verdict)`` fires per claim as the
    streamed judge settles it. Callback failures are logged, never raised.
    """
    started = time.perf_counter()
    model = judge_model or DEFAULT_JUDGE_MODEL
    # A class belongs to the model the CALLER chose; with no judge_model of the
    # caller's own it has nothing to belong to (the host announces the drop).
    judge_class = judge_offering_id if judge_model else None
    if judge_offering_id and not judge_model:
        logger.warning(
            "rag.grounding: judge_offering_id %s given without a judge_model — dropped; "
            "the judge runs its default model's preferred class.",
            judge_offering_id,
        )

    reported_model = await _reported_model(judge_model, model)
    try:
        claims = await extract_claims(answer, judge_model=model, judge_offering_id=judge_class)
    except JudgeUnavailableError as exc:
        await _record_unavailable(exc, stage="claim_extract")
        return FaithfulnessReport(
            claims=[],
            overall_faithfulness=0.0,
            judge_model=reported_model,
            latency_ms=int((time.perf_counter() - started) * 1000),
            error=str(exc),
        )
    if on_claims is not None:
        try:
            await on_claims(claims)
        except Exception:
            logger.warning(
                "rag.grounding: on_claims callback failed (best-effort)", exc_info=True
            )
    try:
        verdicts = await judge_claims(
            claims,
            retrieved,
            judge_model=model,
            judge_offering_id=judge_class,
            on_verdict=on_verdict,
        )
    except JudgeUnavailableError as exc:
        # The judge never ran. Report that as its own fact — do NOT let it look
        # like the answer failed verification.
        logger.error("rag.grounding: verification UNAVAILABLE (judge did not run) — %s", exc)
        await _record_unavailable(exc, stage="judge")
        return FaithfulnessReport(
            claims=[
                _unchecked(c, f"the judge could not run: {exc}")
                for c in claims
            ],
            unchecked_claims=len(claims),
            overall_faithfulness=0.0,
            judge_model=reported_model,
            latency_ms=int((time.perf_counter() - started) * 1000),
            error=str(exc),
        )

    # Overall faithfulness: mean of confidence over claims that scored
    # "supported", weighted down by the proportion of unsupported claims.
    # Unchecked claims are left out of the score (they were never judged).
    checked = [v for v in verdicts if v.verdict != "unchecked"]
    unchecked_n = len(verdicts) - len(checked)
    if checked:
        supported = [v for v in checked if v.verdict == "supported"]
        partial = [v for v in checked if v.verdict == "partial"]
        sup_score = sum(v.confidence for v in supported) / max(1, len(checked))
        part_score = 0.5 * sum(v.confidence for v in partial) / max(1, len(checked))
        overall = round(sup_score + part_score, 4)
    else:
        overall = 0.0
    if verdicts and not checked:
        # Nothing was judged at all: the check did not run. Say so.
        err = "The judge's answer was cut off and no claim could be checked, even in batches."
        await _record_unavailable(JudgeUnavailableError(err), stage="judge_incomplete")
        return FaithfulnessReport(
            claims=verdicts,
            overall_faithfulness=0.0,
            judge_model=reported_model,
            latency_ms=int((time.perf_counter() - started) * 1000),
            error=err,
            unchecked_claims=unchecked_n,
        )
    return FaithfulnessReport(
        claims=verdicts,
        overall_faithfulness=overall,
        judge_model=reported_model,
        latency_ms=int((time.perf_counter() - started) * 1000),
        unchecked_claims=unchecked_n,
    )


__all__ = [
    "ClaimVerdict",
    "FaithfulnessReport",
    "JudgeUnavailableError",
    "OnClaims",
    "OnVerdict",
    "extract_claims",
    "judge_claims",
    "verify_grounded",
]
