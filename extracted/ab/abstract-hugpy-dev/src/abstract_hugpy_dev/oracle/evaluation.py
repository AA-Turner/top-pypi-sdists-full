"""Oracle evaluator kernel (k92): capability-aware judge rubrics on the Scorecard.

Generalizes the movie keyframe judge (``video_intel/runners/movie.py``:
``_score_keyframe`` / ``parse_vision_verdict``) into the oracle: the SAME
``VERDICT=YES|NO; SCORE=0-100; WHY=<one sentence>`` discipline, the SAME
tolerant parse, and the SAME degradation — a judge that raises, times out or
returns garbage yields an UNSCORED/UNAVAILABLE ``JudgeResult`` and NEVER flips
``hard_pass`` (movie: "unscored, keep"). The parser is a lift, not an import:
oracle must not grow a video_intel runtime dependency, so movie.py keeps its
own copy untouched (a later task may re-point it here).

Rubrics are per-capability defaults (``RUBRICS``):

  image.generate / image.transform -> VLM "does this image satisfy the prompt"
                                      (kind=intent, judge via image.understand)
  text.summarize                   -> LLM faithfulness quick-check
                                      (kind=semantic, judge via text.chat)
  everything analytic              -> NO judge (embed/similarity/detect/
                                      classify/depth/segment/transcribe/
                                      understand/chat/keywords/extract/fetch)

The judge MODEL is resolved through the oracle's own router over the k90
catalog (``resolve_route`` on the judge capability) — never hardcoded. The
pass bar is per-quality (``THRESHOLDS``: preview 40 / balanced 60 / best 75);
a judged score under it fails the card with ``RepairCode.INTENT_MISMATCH``
(the repair controller in repair.py maps that to one bounded retry).

Provider seams (``_resolve_judge_route`` / ``_judge_dispatch``) are
module-level and lazy so tests monkeypatch them and no worker/GPU is touched.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, replace
from typing import Any

from .contracts import (
    CheckKind,
    ExecutionReceipt,
    GoalSpec,
    JudgeResult,
    QualityProfile,
    RepairCode,
    Scorecard,
)
from .router import RouteDecision

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Rubrics — which capabilities get judged, and how.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Rubric:
    """One default judge rubric: what evidence axis it produces (``kind``),
    which catalog capability serves the judge, and whether the judged evidence
    is a produced image file or produced text."""
    name: str
    kind: CheckKind
    judge_capability: str
    judged_artifact: str    # "image" | "text"


RUBRICS: dict[str, Rubric] = {
    "image.generate":  Rubric("image_intent", CheckKind.INTENT,
                              "image.understand", "image"),
    "image.transform": Rubric("image_intent", CheckKind.INTENT,
                              "image.understand", "image"),
    "text.summarize":  Rubric("summary_faithfulness", CheckKind.SEMANTIC,
                              "text.chat", "text"),
}

# The capabilities POST /oracle/route evaluates by default (deliverable 3).
DEFAULT_EVALUATED: frozenset[str] = frozenset(RUBRICS)

# Judged-score pass bar per quality profile.
THRESHOLDS: dict[QualityProfile, int] = {
    QualityProfile.PREVIEW:  40,
    QualityProfile.BALANCED: 60,
    QualityProfile.BEST:     75,
}

_JUDGE_REPLY_FORMAT = ("Reply exactly: VERDICT=YES|NO; SCORE=0-100; "
                       "WHY=<one sentence>.")
_MAX_SOURCE_CHARS = 4000
_MAX_SUMMARY_CHARS = 2000
_ERROR_TAIL = 300


# ---------------------------------------------------------------------------
# Verdict parsing — lifted from movie.parse_vision_verdict (same tolerance).
# ---------------------------------------------------------------------------


def parse_judge_verdict(text: str) -> dict:
    """Parse a judge reply into ``{"verdict","score","why"}``. Tolerant of
    model drift exactly like the movie parser: field forms win, a bare YES/NO
    word is the fallback, garbage yields verdict=None/score=None (which the
    evaluator treats as "unscored, keep"). Returns DATA only — never raises."""
    t = text or ""
    verdict = None
    m = re.search(r"VERDICT\s*[=:]\s*(YES|NO)", t, re.I)
    if m:
        verdict = m.group(1).upper()

    score = None
    m = re.search(r"SCORE\s*[=:]\s*(\d{1,3})", t, re.I)
    if m:
        score = max(0, min(100, int(m.group(1))))

    why = ""
    m = re.search(r"WHY\s*[=:]\s*(.+)", t, re.I | re.S)
    if m:
        why = m.group(1).strip().splitlines()[0].strip().rstrip(".").strip()

    if verdict is None:
        if re.search(r"\bYES\b", t, re.I):
            verdict = "YES"
        elif re.search(r"\bNO\b", t, re.I):
            verdict = "NO"

    return {"verdict": verdict, "score": score, "why": why}


def _reply_text(res: Any) -> str:
    """Best-effort reply text from a dispatch result (movie._vision_text)."""
    txt = getattr(res, "text", None)
    if txt:
        return txt
    if isinstance(res, dict):
        return str(res.get("text") or res.get("content") or res)
    for attr in ("model_dump", "to_dict", "dict"):
        fn = getattr(res, attr, None)
        if callable(fn):
            try:
                d = fn()
            except TypeError:
                continue
            if isinstance(d, dict) and d.get("text"):
                return d["text"]
    return str(res)


# ---------------------------------------------------------------------------
# Provider seams — lazy, monkeypatchable.
# ---------------------------------------------------------------------------


def _resolve_judge_route(judge_capability: str) -> RouteDecision | None:
    """The judge's own route through the k90 catalog — the SAME resolution the
    judged execution used (eligibility gates, default-model policy), so the
    judge model is chosen, never hardcoded. None when resolution itself dies."""
    from . import router
    try:
        goal = GoalSpec(objective=f"judge via {judge_capability}",
                        raw_prompt=f"judge via {judge_capability}",
                        capability=judge_capability)
        return router.resolve_route(goal)
    except Exception as exc:  # noqa: BLE001 — an unresolvable judge degrades
        logger.info("oracle judge: route resolution failed (%s: %s)",
                    type(exc).__name__, exc)
        return None


def _judge_dispatch(task: str, body: dict[str, Any]) -> Any:
    """The judge call through the same inference front door the runtime uses
    (normalize + execute_prompt). Kept as a SEPARATE seam from the runtime's
    so tests drive the judged execution and the judge independently."""
    from . import runtime
    return runtime._dispatch(runtime._normalized_kwargs(task, body))


# ---------------------------------------------------------------------------
# Rubric prompt + evidence selection.
# ---------------------------------------------------------------------------


def _judged_image(artifacts: list[dict[str, Any]]) -> str | None:
    import os
    for art in artifacts:
        if art.get("kind") == "image" and os.path.isfile(art.get("uri", "")):
            return art["uri"]
    return None


def _judged_text(artifacts: list[dict[str, Any]]) -> str | None:
    for art in artifacts:
        text = str(art.get("text") or "").strip()
        if text:
            return text
    return None


def _rubric_body(rubric: Rubric, goal: GoalSpec,
                 artifacts: list[dict[str, Any]]) -> dict[str, Any] | None:
    """The pre-normalization judge request, or None when the artifacts carry
    nothing this rubric can judge (nothing to judge is not a judge failure —
    the technical checks already own that diagnosis)."""
    from abstract_hugpy_dev.utils.no_think import with_no_think

    if rubric.judged_artifact == "image":
        uri = _judged_image(artifacts)
        if uri is None:
            return None
        prompt = (f"GOAL: {goal.objective}.\n"
                  f"Does the image achieve this goal? {_JUDGE_REPLY_FORMAT}")
        return {"file": uri, "prompt": with_no_think(prompt),
                "max_new_tokens": 80}

    summary = _judged_text(artifacts)
    if summary is None:
        return None
    texts = [i.ref for i in goal.inputs if i.kind.value == "text"]
    source = "\n\n".join(texts) if texts else goal.raw_prompt
    prompt = (f"SOURCE:\n{source[:_MAX_SOURCE_CHARS]}\n\n"
              f"SUMMARY:\n{summary[:_MAX_SUMMARY_CHARS]}\n\n"
              "Is the summary faithful to the source (no invented claims) and "
              f"does it cover the main points? {_JUDGE_REPLY_FORMAT}")
    return {"prompt": with_no_think(prompt), "max_new_tokens": 80}


# ---------------------------------------------------------------------------
# The kernel.
# ---------------------------------------------------------------------------


def _unavailable(rubric: Rubric, model: str | None, detail: str) -> JudgeResult:
    return JudgeResult(
        judge=f"{rubric.name}:{model or rubric.judge_capability}",
        verdict="unavailable", score=None, rationale=detail[-_ERROR_TAIL:])


def run_judge(rubric: Rubric, goal: GoalSpec,
              artifacts: list[dict[str, Any]]) -> JudgeResult | None:
    """One judge pass under ``rubric``. None when nothing is judgeable;
    otherwise ALWAYS a JudgeResult — judge faults become the honest
    ``verdict="unavailable"`` entry (movie: plane raise -> unscored, keep)."""
    body = _rubric_body(rubric, goal, artifacts)
    if body is None:
        return None

    judge_route = _resolve_judge_route(rubric.judge_capability)
    if judge_route is None or judge_route.execution != "execute":
        reasons = "; ".join(judge_route.reasons) if judge_route else \
            "judge route resolution raised"
        return _unavailable(
            rubric, None,
            f"no eligible judge for {rubric.judge_capability}: {reasons}")

    model_id = judge_route.model_id
    if model_id:
        body["model_key"] = model_id
    judge_name = f"{rubric.name}:{model_id or rubric.judge_capability}"

    try:
        res = _judge_dispatch(judge_route.task or "", body)
    except Exception as exc:  # noqa: BLE001 — judge fault degrades, never fails the route
        logger.info("oracle judge %s raised (%s: %s); degrading to unavailable",
                    judge_name, type(exc).__name__, exc)
        return _unavailable(rubric, model_id, f"{type(exc).__name__}: {exc}")
    if not getattr(res, "ok", True) or (isinstance(res, dict)
                                        and res.get("ok") is False):
        err = getattr(res, "error", None) or \
            (res.get("error") if isinstance(res, dict) else None)
        return _unavailable(rubric, model_id, f"judge not-ok: {err}")

    from abstract_hugpy_dev.utils.no_think import strip_think
    raw = _reply_text(res)
    scored, _reasoning = strip_think(raw)   # parse the prose, never the monologue
    parsed = parse_judge_verdict(scored)
    return JudgeResult(
        judge=judge_name,
        verdict=parsed["verdict"] or "unscored",
        score=float(parsed["score"]) if parsed["score"] is not None else None,
        rationale=parsed["why"] or raw.strip()[:_ERROR_TAIL])


def evaluate(goal: GoalSpec, route: RouteDecision,
             artifacts: list[dict[str, Any]], receipt: ExecutionReceipt,
             scorecard: Scorecard) -> Scorecard:
    """The k92 kernel: fill ``judge_results`` on ``scorecard`` per the
    capability's default rubric and update hard_pass/diagnosis/repair_code
    when the judged score misses the quality bar. Analytic capabilities (no
    rubric), failed executions and unjudgeable artifacts return the card
    unchanged; an unavailable/unscored judge is recorded WITHOUT touching
    ``hard_pass`` (the fleet's vision plane being down must not fail routes)."""
    rubric = RUBRICS.get(route.capability)
    if rubric is None or receipt.failure is not None:
        return scorecard

    result = run_judge(rubric, goal, artifacts)
    if result is None:
        return scorecard

    judge_results = scorecard.judge_results + (result,)
    if result.verdict in ("unavailable", "unscored"):
        return replace(scorecard, judge_results=judge_results)

    threshold = THRESHOLDS[goal.quality]
    failing = (result.score is not None and result.score < threshold) or \
              (result.score is None and result.verdict == "NO")
    if not failing:
        disagreements = scorecard.disagreements
        if result.verdict == "NO":     # score cleared the bar but verdict says NO
            disagreements = disagreements + (
                f"{result.judge}: verdict NO but score {result.score:g} >= "
                f"threshold {threshold} — score wins (movie semantics)",)
        return replace(scorecard, judge_results=judge_results,
                       disagreements=disagreements)

    scored = f"score {result.score:g}" if result.score is not None else "no score"
    diagnosis = (f"{rubric.name} judge failed the artifact ({scored}, "
                 f"verdict {result.verdict}, threshold {threshold} "
                 f"for quality={goal.quality.value})"
                 + (f": {result.rationale}" if result.rationale else ""))
    if scorecard.diagnosis:
        diagnosis = f"{scorecard.diagnosis}; {diagnosis}"
    return replace(
        scorecard,
        hard_pass=False,
        judge_results=judge_results,
        diagnosis=diagnosis,
        repair_code=scorecard.repair_code or RepairCode.INTENT_MISMATCH,
        recommended_repair=scorecard.recommended_repair or
            "regenerate with a bumped seed (bounded repair — see oracle/repair.py)")


__all__ = ["RUBRICS", "Rubric", "DEFAULT_EVALUATED", "THRESHOLDS",
           "parse_judge_verdict", "run_judge", "evaluate"]
