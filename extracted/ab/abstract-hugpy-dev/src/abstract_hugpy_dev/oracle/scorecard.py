"""Oracle scorecard builder (k91): deterministic technical checks, every response.

Operator ruling (KEEPER-ASSESSMENT Decision, 2026-08-05): the Scorecard is
load-bearing from day one. This module builds it from evidence OUTSIDE the
generator — the receipt's failure class and cheap direct inspection of the
produced artifacts. Checks implemented here:

  execution         — the receipt carries no failure class (TIMEOUT /
                      WORKER_UNAVAILABLE / RUNNER_ERROR surface here)
  empty_output      — >=1 artifact with substance (text: non-blank; inline
                      data: truthy; file: exists and >0 bytes)
  format            — every artifact kind is one the capability declares in
                      ``produces`` (catalog IO table)
  decode            — file artifacts are readable; images additionally open
                      via PIL with nonzero dimensions (size-only when PIL is
                      not installed — the degradation is named in the check)

``hard_pass`` is the conjunction. ``judge_results`` is PRESENT AND EMPTY on
every card built here — that tuple is the k92 seam: the evaluator kernel
(judges, heterogeneous evidence, repair loop) fills it; k91 deliberately does
not. ``build_gap_scorecard`` / ``build_deferred_scorecard`` cover the two
non-executed response shapes so the scorecard is mandatory on EVERY response.
"""

from __future__ import annotations

import os
from typing import Any

from .contracts import (
    ArtifactKind,
    Check,
    CheckKind,
    ExecutionReceipt,
    FailureClass,
    GoalSpec,
    RepairCode,
    Scorecard,
)
from .router import RouteDecision

# Receipt failure class -> the repair code named on the card. RUNNER_ERROR /
# REFUSED / CANCELLED / UNKNOWN have no regeneration verb in RepairCode — they
# fail the card with a diagnosis and no repair_code (k92 may widen this).
_FAILURE_REPAIR: dict[FailureClass, RepairCode] = {
    FailureClass.TIMEOUT:            RepairCode.TIMEOUT,
    FailureClass.WORKER_UNAVAILABLE: RepairCode.WORKER_UNAVAILABLE,
    FailureClass.DECODE_FAILED:      RepairCode.DECODE_FAILED,
    FailureClass.EMPTY_OUTPUT:       RepairCode.EMPTY_OUTPUT,
    FailureClass.FORMAT_MISMATCH:    RepairCode.FORMAT_MISMATCH,
    FailureClass.CAPABILITY_GAP:     RepairCode.CAPABILITY_GAP,
}


def _has_substance(art: dict[str, Any]) -> bool:
    if "text" in art:
        return bool(str(art["text"]).strip())
    if "data" in art:
        return bool(art["data"])
    uri = art.get("uri", "")
    try:
        return os.path.isfile(uri) and os.path.getsize(uri) > 0
    except OSError:
        return False


def _decode_file(art: dict[str, Any]) -> tuple[bool, str]:
    """(readable, detail) for a file-backed artifact. Images get a real decode
    via PIL when available; everything else is open-and-read-a-byte."""
    uri = art.get("uri", "")
    if not os.path.isfile(uri):
        return False, f"file missing: {uri}"
    try:
        with open(uri, "rb") as fh:
            if not fh.read(1):
                return False, f"zero-byte file: {uri}"
    except OSError as exc:
        return False, f"unreadable ({exc}): {uri}"
    if art.get("kind") == ArtifactKind.IMAGE.value:
        try:
            from PIL import Image  # optional dep — degrade, don't require
        except ImportError:
            return True, "readable (PIL unavailable — size-only image check)"
        try:
            with Image.open(uri) as img:
                w, h = img.size
            if w <= 0 or h <= 0:
                return False, f"image decodes to zero dimensions: {uri}"
            return True, f"image decodes ({w}x{h})"
        except Exception as exc:  # noqa: BLE001 — undecodable is the finding
            return False, f"image undecodable ({type(exc).__name__}: {exc})"
    return True, "readable"


def build_technical_scorecard(goal: GoalSpec, route: RouteDecision,
                              artifacts: list[dict[str, Any]],
                              receipt: ExecutionReceipt) -> Scorecard:
    """The mandatory deterministic card for an executed route."""
    checks: list[Check] = []
    repair: RepairCode | None = None
    diagnoses: list[str] = []

    exec_ok = receipt.failure is None
    checks.append(Check(
        name="execution", kind=CheckKind.TECHNICAL,
        value="ok" if exec_ok else receipt.failure.value, threshold=None,
        passed=exec_ok,
        detail="" if exec_ok else "; ".join(receipt.log_excerpt)[:500]))
    if not exec_ok:
        repair = _FAILURE_REPAIR.get(receipt.failure)
        diagnoses.append(f"execution failed: {receipt.failure.value}")

    substantive = [a for a in artifacts if _has_substance(a)]
    empty_ok = bool(substantive)
    checks.append(Check(
        name="empty_output", kind=CheckKind.TECHNICAL,
        value=len(substantive), threshold=1, passed=empty_ok,
        detail=(f"{len(substantive)}/{len(artifacts)} artifacts carry substance"
                if artifacts else "no artifacts produced")))
    if not empty_ok:
        repair = repair or RepairCode.EMPTY_OUTPUT
        diagnoses.append("no substantive artifact (blank/zero-byte output)")

    declared = {k.value for k in route.produces}
    observed = [a.get("kind", "?") for a in artifacts]
    fmt_ok = all(k in declared for k in observed) if declared else True
    checks.append(Check(
        name="format", kind=CheckKind.TECHNICAL,
        value=",".join(sorted(set(observed))) or "(none)",
        threshold=",".join(sorted(declared)), passed=fmt_ok,
        detail="artifact kinds vs the capability's declared produces"))
    if not fmt_ok:
        repair = repair or RepairCode.FORMAT_MISMATCH
        diagnoses.append(
            f"produced kind(s) {sorted(set(observed) - declared)} not in "
            f"{route.capability}'s declared produces")

    file_arts = [a for a in artifacts if "text" not in a and "data" not in a]
    decode_details: list[str] = []
    decode_ok = True
    for art in file_arts:
        ok, detail = _decode_file(art)
        decode_ok = decode_ok and ok
        decode_details.append(detail)
    checks.append(Check(
        name="decode", kind=CheckKind.TECHNICAL,
        value=len(file_arts), threshold=None, passed=decode_ok,
        detail="; ".join(decode_details) or "no file-backed artifacts"))
    if not decode_ok:
        repair = repair or RepairCode.DECODE_FAILED
        diagnoses.append("a produced file is missing/unreadable/undecodable")

    hard_pass = all(c.passed for c in checks)
    return Scorecard(
        hard_pass=hard_pass,
        checks=tuple(checks),
        judge_results=(),   # k92 seam: the evaluator kernel fills this
        confidence=1.0,     # deterministic checks — no judge disagreement yet
        diagnosis="; ".join(diagnoses) or None,
        repair_code=None if hard_pass else repair,
        recommended_repair=None if hard_pass else (
            "re-route or regenerate per repair_code (bounded repair loop "
            "lands in k92)"))


def build_gap_scorecard(route: RouteDecision) -> Scorecard:
    """The card for a CAPABILITY_GAP response — nothing executed; the catalog's
    eligibility reasons are the evidence."""
    return Scorecard(
        hard_pass=False,
        checks=(Check(
            name="route.eligibility", kind=CheckKind.TECHNICAL,
            value="capability_gap", threshold=None, passed=False,
            detail="; ".join(route.reasons) or route.capability),),
        judge_results=(),   # k92 seam
        diagnosis=f"no eligible route for {route.capability!r}",
        repair_code=RepairCode.CAPABILITY_GAP,
        recommended_repair=("register/unblock a model serving this capability, "
                            "or pick one from GET /oracle/capabilities"))


def build_deferred_scorecard(route: RouteDecision) -> Scorecard:
    """The card for a deferred (video.*) response: routing succeeded, execution
    did not happen here — hard_pass must not claim it did."""
    return Scorecard(
        hard_pass=False,
        checks=(Check(
            name="execution.deferred", kind=CheckKind.TECHNICAL,
            value="deferred", threshold=None, passed=False,
            detail=(f"routed to {route.model_id or 'the studio router'}; "
                    "video capabilities execute through the studio job "
                    "pipeline, not POST /oracle/route")),),
        judge_results=(),   # k92 seam
        diagnosis="video execution is deferred by k91 scope",
        recommended_repair=None)


__all__ = ["build_technical_scorecard", "build_gap_scorecard",
           "build_deferred_scorecard"]
