"""Every check proven able to fail (Agent Evaluation PLAN §2.4, CONTRACT v2 §2.7).

A mutation is applied to a COPY of the resolved observed/expected values and the op is
re-run. A check whose mutation does not flip to ``fail`` cannot fail, and a pass it
produces never counts (``compute_verdict`` treats it as unproven). No AI call, no I/O.
"""

from __future__ import annotations

import hashlib
import re
from decimal import Decimal
from typing import Any

from matrx_ai.checks.engine import (
    Missing,
    _resolved_turns,
    compare,
    parity_outcome,
    parity_values,
    to_text,
)
from matrx_ai.checks.models import OP_KIND, Bindings, Check, Evidence, FailProof

__all__ = ["mutate", "prove_can_fail", "prove_parity_can_fail"]

_CENT_UNIT = Decimal("0.0001")


def _decoy(seed: str) -> str:
    return "DECOY-" + hashlib.sha256(seed.encode()).hexdigest()[:12].upper()


def _unit(observed: Any, expected: Any) -> Decimal:
    """One unit: 1 for whole numbers on both sides, else a 0.0001 (cents) step."""
    try:
        o, e = Decimal(str(observed)), Decimal(str(expected))
    except Exception:  # noqa: BLE001
        return Decimal(1)
    if o == o.to_integral_value() and e == e.to_integral_value() and not isinstance(observed, Decimal):
        return Decimal(1)
    return _CENT_UNIT


def _literal_from_pattern(pattern: str) -> str | None:
    """A string the pattern matches, when one can be read off it (used for not_matches)."""
    candidate = pattern
    for cls, sample in ((r"\d", "7"), (r"\w", "a"), (r"\s", " "), (r"\S", "a"), (r"\D", "a"), (r"\W", "-")):
        candidate = candidate.replace(cls, sample)
    candidate = re.sub(r"\{\d+(,\d*)?\}|(?<!\\)[+*?]", "", candidate)
    candidate = re.sub(r"(?<!\\)\.", "a", candidate)
    candidate = re.sub(r"\\(.)", r"\1", candidate)
    candidate = re.sub(r"[\^\$]", "", candidate)
    try:
        return candidate if re.search(pattern, candidate) else None
    except re.error:
        return None


def mutate(op: str, observed: Any, expected: Any, *, count_op: str | None, seed: str) -> tuple[Any, Any, str] | None:
    """Return ``(observed', expected', description)``, or ``None`` when no mutation applies."""
    kind = OP_KIND[op]
    if kind == "positive":
        decoy = _decoy(seed)
        if op in ("in", "routes_in"):
            return observed, [decoy], "expected list replaced by a decoy"
        if op == "matches":
            return observed, re.escape(decoy), "pattern replaced by a decoy"
        return observed, decoy, "expected replaced by a decoy marker"
    if kind == "negative":
        if op == "ne":
            return expected, expected, "observed set to the forbidden value"
        if op == "not_matches":
            lit = _literal_from_pattern(to_text(expected))
            if lit is None:
                return None
            return f"{to_text(observed)} {lit}", expected, "a matching value injected into the observed copy"
        needles = expected if isinstance(expected, list) else [expected]
        injected = "\n".join([to_text(observed), *[to_text(n) for n in needles]])
        return injected, expected, "forbidden value injected into the observed copy"
    if kind == "presence":
        if op == "empty":
            return "x", expected, "observed filled"
        if op in ("matches_schema", "conforms"):
            return "∅not-an-object", expected, "observed replaced by a schema-breaking value"
        return None, expected, "observed blanked"
    if kind == "bound":
        if op == "count":
            target = int(Decimal(str(expected)))
            cop = count_op or "eq"
            n = target - 1 if cop == "gte" else target + 1
            if n < 0:
                return None
            return ["x"] * n, expected, f"count moved to {n}"
        step = _unit(observed, expected)
        exp = Decimal(str(expected))
        moved = exp - step if op == "gte" else exp + step
        return moved, expected, f"observed moved one unit ({step}) past {exp}"
    return None


def prove_can_fail(check: Check, evidence: Evidence, bindings: Bindings) -> FailProof:
    """Mutate each resolved turn; the check can fail only if every turn's mutation fails."""
    resolved = [e for e in _resolved_turns(check, evidence, bindings) if not isinstance(e[1], Missing)]
    if not resolved:
        return FailProof(can_fail=False, mutation="nothing resolved to mutate", outcome_after="undecided")
    descriptions: list[str] = []
    for ti, observed, expected, _label, _sens in resolved:
        m = mutate(check.op, observed, expected, count_op=check.count_op, seed=f"{check.id}:{ti}")
        if m is None:
            return FailProof(can_fail=False, mutation=f"no mutation applies to {check.op}", outcome_after="pass")
        obs2, exp2, desc = m
        descriptions.append(desc)
        try:
            ok, _ = compare(check.op, obs2, exp2, count_op=check.count_op)
        except Missing:
            return FailProof(can_fail=False, mutation=desc, outcome_after="undecided")
        if ok:
            return FailProof(can_fail=False, mutation=desc, outcome_after="pass")
    return FailProof(can_fail=True, mutation=descriptions[0], outcome_after="fail")


def prove_parity_can_fail(check: Check, evidence_by_door: dict[str, Evidence], bindings: Bindings) -> FailProof:
    try:
        values = parity_values(check, evidence_by_door, bindings)
    except Missing as miss:
        return FailProof(can_fail=False, mutation=miss.reason, outcome_after=miss.outcome)
    if len(values) < 2:
        return FailProof(can_fail=False, mutation="fewer than two doors", outcome_after="undecided")
    door = sorted(values)[-1]
    mutated = dict(values)
    mutated[door] = _perturb(values[door])
    outcome, _ = parity_outcome(mutated)
    return FailProof(
        can_fail=outcome == "fail", mutation=f"{door} perturbed by one character", outcome_after=outcome
    )


def _perturb(value: Any) -> Any:
    if isinstance(value, str):
        return value + "⁣"
    if isinstance(value, dict):
        return {**value, "⁣": 1}
    if isinstance(value, list):
        return [*value, "⁣"]
    return to_text(value) + "⁣"
