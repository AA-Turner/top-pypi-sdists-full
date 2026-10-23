"""The pure check engine (Agent Evaluation CONTRACT v2 §2, §3.1).

Reads observed values from ``Evidence``, binds expected values from ``Bindings``,
applies one op, proves the check can fail, and computes the verdict. Stdlib and
pydantic only (jsonschema lazily, for ``matches_schema``). It never imports the
fill or execution code: it must judge that code, so it cannot share it.
"""

from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from typing import Any

from matrx_ai.checks.models import (
    OP_KIND,
    Bindings,
    Check,
    CheckOutcome,
    CheckResult,
    Evidence,
    Expected,
    JudgeDecision,
    JudgeFact,
    Modifiers,
    ReadSpec,
    TurnEvidence,
    VerdictResult,
)

__all__ = [
    "Missing",
    "apply_modifiers",
    "compare",
    "compute_verdict",
    "evaluate_check",
    "evaluate_checks",
    "evaluate_parity",
    "fact_items",
    "judge_feed",
    "needs_judge",
    "read_path",
    "resolve_expected",
    "row_specs",
    "rows_key",
    "store_excerpts",
    "to_text",
]

_REPLY_SINKS = {"reply", "output", "stored", "conversation", "tool_calls"}
_REQUEST_SINKS = {"request", "preview"}


class Missing(Exception):
    """A value could not be read or bound. ``outcome`` says how the check reports it."""

    def __init__(self, reason: str, outcome: CheckOutcome = "undecided") -> None:
        super().__init__(reason)
        self.reason = reason
        self.outcome: CheckOutcome = outcome


# ── small value helpers ──────────────────────────────────────────────────────


def to_text(value: Any) -> str:
    """Flatten any value to text: strings joined by newlines, scalars stringified."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float | Decimal):
        return str(value)
    if isinstance(value, dict):
        return "\n".join(to_text(v) for v in value.values())
    if isinstance(value, list | tuple | set):
        return "\n".join(to_text(v) for v in value)
    if hasattr(value, "model_dump"):
        return to_text(value.model_dump(mode="json"))
    return str(value)


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list | tuple | dict | set):
        return len(value) == 0
    return False


def _jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, list | tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


def read_path(value: Any, path: str) -> Any:
    """Dotted path; numeric segments index lists. A miss anywhere is ``None``."""
    if not path:
        return value
    current = _jsonable(value)
    for segment in path.split("."):
        if current is None:
            return None
        if isinstance(current, dict):
            current = current.get(segment)
        elif isinstance(current, list):
            try:
                index = int(segment)
            except ValueError:
                return None
            current = current[index] if -len(current) <= index < len(current) else None
        else:
            return None
    return current


def _field_values(text: str, key: str) -> list[str]:
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:\s*(.*?)\s*$", re.MULTILINE)
    return pattern.findall(text)


def _kv_values(text: str) -> list[str]:
    return re.findall(r"^\s*[A-Za-z0-9_ ]+\s*:\s*(.*?)\s*$", text, re.MULTILINE)


def apply_modifiers(value: Any, mods: Modifiers, *, what: str) -> Any:
    """split → match → trim → lower, element-wise over lists."""
    if isinstance(value, list):
        return [apply_modifiers(v, mods, what=what) for v in value]
    if value is None:
        return None
    if mods.split is not None:
        parts = to_text(value).split(mods.split.sep)
        idx = mods.split.index
        if not -len(parts) <= idx < len(parts):
            raise Missing(f"{what}: split has no part {idx} ({len(parts)} parts)")
        value = parts[idx]
    if mods.match is not None:
        try:
            found = re.search(mods.match, to_text(value))
        except re.error as exc:
            raise Missing(f"{what}: bad pattern {mods.match!r}: {exc}") from exc
        if found is None:
            raise Missing(f"{what}: pattern {mods.match!r} did not match")
        value = found.group(1) if found.groups() else found.group(0)
    if mods.trim and isinstance(value, str):
        value = value.strip()
    if mods.lower and isinstance(value, str):
        value = value.lower()
    return value


# ── reading observed values ──────────────────────────────────────────────────


def rows_key(table: str, where: dict[str, Any]) -> str:
    return table + "?" + json.dumps(_jsonable(where), sort_keys=True, default=str)


def _turn_indexes(turn: int | str | None, evidence: Evidence) -> list[int]:
    count = len(evidence.turns)
    if turn == "each":
        return list(range(count))
    if turn is None:
        return [count - 1] if count else [0]
    return [int(turn) - 1]


def _turn(evidence: Evidence, index: int, what: str) -> TurnEvidence:
    if index < 0 or index >= len(evidence.turns):
        raise Missing(f"{what}: turn {index + 1} has no evidence")
    return evidence.turns[index]


def _resolve_where(read: ReadSpec, bindings: Bindings, evidence: Evidence | None, ti: int) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for col, raw in (read.where or {}).items():
        if isinstance(raw, Expected):
            out[col] = resolve_expected(raw, bindings, evidence, ti)[0]
        elif isinstance(raw, dict) and "from" in raw:
            out[col] = resolve_expected(Expected.model_validate(raw), bindings, evidence, ti)[0]
        else:
            out[col] = raw
    return out


def _read_sink(sink: str, read: ReadSpec, evidence: Evidence, bindings: Bindings, ti: int) -> Any:
    what = f"{sink}[{ti + 1}]"
    if sink == "reply":
        t = _turn(evidence, ti, what)
        if t.reply is None:
            raise Missing(f"{what}: no assistant reply")
        base: Any = t.reply
    elif sink == "output":
        t = _turn(evidence, ti, what)
        if t.output is None:
            raise Missing(f"{what}: no structured output")
        base = t.output
    elif sink in ("request", "preview"):
        t = _turn(evidence, ti, what)
        view = t.request if sink == "request" else t.preview
        if view is None:
            raise Missing(f"{what}: no {sink} snapshot")
        base = view.model_dump(mode="json")
    elif sink == "stored":
        t = _turn(evidence, ti, what)
        if t.stored_user_message is None and t.stored_messages is None:
            raise Missing(f"{what}: no stored messages")
        base = {"user_message": t.stored_user_message, "messages": t.stored_messages or []}
    elif sink == "conversation":
        if evidence.conversation_variables is None:
            raise Missing("conversation: no conversation variables")
        base = {"variables": evidence.conversation_variables}
    elif sink == "tool_calls":
        t = _turn(evidence, ti, what)
        if t.tool_calls is None:
            raise Missing(f"{what}: no tool-call record")
        calls = [c.model_dump(mode="json") for c in t.tool_calls if read.tool in (None, c.name)]
        if read.path:
            vals = [read_path(c, read.path) for c in calls]
            vals = [v for v in vals if v is not None]
            return vals[0] if len(vals) == 1 else vals
        return calls
    elif sink == "rows":
        if not read.table:
            raise Missing("rows: no table named")
        key = rows_key(read.table, _resolve_where(read, bindings, evidence, ti))
        if key not in evidence.rows:
            raise Missing(f"rows: {read.table} was not fetched for this filter")
        base = evidence.rows[key]
    elif sink == "usage":
        if evidence.usage is None:
            raise Missing("usage: no usage record")
        base = evidence.usage.model_dump()
    elif sink == "outcome":
        if evidence.outcome is None:
            raise Missing("outcome: no outcome")
        base = evidence.outcome.model_dump(mode="json")
    elif sink == "door":
        if evidence.door is None:
            raise Missing("door: unknown")
        base = evidence.door
    else:  # pragma: no cover - Literal guards it
        raise Missing(f"unknown sink {sink}")
    return read_path(base, read.path) if sink != "usage" else _usage_path(base, read.path)


def _usage_path(base: dict[str, Any], path: str) -> Any:
    return base if not path else base.get(path)


def read_observed(check: Check, evidence: Evidence, bindings: Bindings, ti: int) -> Any:
    read = check.read
    value = _read_sink(check.sink, read, evidence, bindings, ti)
    if read.field is not None:
        found = _field_values(to_text(value), read.field)
        value = found[-1] if found else None
    if read.line is not None:
        lines = to_text(value).splitlines()
        value = lines[read.line] if -len(lines) <= read.line < len(lines) else None
    if read.final is not None:
        vals = _kv_values(to_text(value))
        value = vals[-read.final] if 0 < read.final <= len(vals) else None
    return apply_modifiers(value, read, what=f"{check.sink} read")


# ── binding expected values ──────────────────────────────────────────────────


def _declared(bindings: Bindings, var: str) -> None:
    if bindings.declared_variables is not None and var not in bindings.declared_variables:
        raise Missing(f"variable {var!r} is not declared by this setup's agent", "not_applicable")


def _turn_binding(bindings: Bindings, n: int, what: str):  # noqa: ANN202
    if n < 1 or n > len(bindings.turns):
        raise Missing(f"{what}: the case has no turn {n}")
    return bindings.turns[n - 1]


def _input_value(path: str, bindings: Bindings, ti: int) -> Any:
    parts = path.split(".")
    head = parts[0]
    if head == "variables" and len(parts) >= 2:
        _declared(bindings, parts[1])
        if parts[1] not in bindings.variables:
            raise Missing(f"input.variables.{parts[1]} is not set by the case")
        return read_path(bindings.variables[parts[1]], ".".join(parts[2:]))
    if head == "user_text":
        return _turn_binding(bindings, ti + 1, "input.user_text").user_text
    if head == "context" and len(parts) >= 2:
        ctx = _turn_binding(bindings, ti + 1, "input.context").context
        if parts[1] not in ctx:
            raise Missing(f"input.context.{parts[1]} is not set for turn {ti + 1}")
        return read_path(ctx[parts[1]], ".".join(parts[2:]))
    if head == "turn" and len(parts) >= 3:
        try:
            n = int(parts[1])
        except ValueError as exc:
            raise Missing(f"input.{path}: turn must be a number") from exc
        tb = _turn_binding(bindings, n, f"input.{path}")
        sect = parts[2]
        rest = parts[3:]
        if sect == "user_text":
            return tb.user_text
        if sect in ("context", "variable_edits") and rest:
            pool = tb.context if sect == "context" else tb.variable_edits
            if sect == "variable_edits":
                _declared(bindings, rest[0])
            if rest[0] not in pool:
                raise Missing(f"input.{path} is not set")
            return read_path(pool[rest[0]], ".".join(rest[1:]))
        if sect == "fixture_edits" and rest:
            if rest[0] not in tb.fixture_edits:
                raise Missing(f"input.{path}: no fixture edit {rest[0]!r} on turn {n}")
            value = tb.fixture_edits[rest[0]]
            tail = rest[1:]
            if tail and tail[0] == "value":
                tail = tail[1:]
            return read_path(value, ".".join(tail))
    raise Missing(f"input.{path} is not a known input path")


def resolve_expected(
    expected: Expected, bindings: Bindings, evidence: Evidence | None, ti: int
) -> tuple[Any, str, bool]:
    """Return ``(value, source_label, sensitive)``; raise ``Missing`` when it cannot bind."""
    src = expected.from_
    sensitive = False
    if src == "literal":
        value: Any = expected.value
        label = "literal"
    elif src == "input":
        value = _input_value(expected.path or "", bindings, ti)
        label = f"input.{expected.path}"
    elif src == "marker":
        name = expected.name or ""
        if name not in bindings.markers:
            raise Missing(f"marker {name!r} was not minted for this result")
        value = bindings.markers[name]
        label = f"marker({name})"
    elif src == "pick_list":
        var = expected.var or ""
        _declared(bindings, var)
        part = expected.part or "label"
        items = bindings.pick_lists.get(var, {}).get(expected.at)
        if not items:
            raise Missing(f"pick_list({var}) has no {expected.at} item")
        if part == "label":
            value = items[0].label
        elif part == "hidden_text":
            value, sensitive = items[0].hidden_text, True
        elif part == "labels":
            value = [i.label for i in items]
        elif part == "hidden_texts":
            value, sensitive = [i.hidden_text for i in items], True
        else:
            raise Missing(f"pick_list part {part!r} is unknown")
        label = f"pick_list({var}).{part}@{expected.at}"
    elif src == "prompt_block":
        name = expected.name or ""
        part = expected.part or "content"
        if part == "name":
            value = name
        else:
            content = bindings.prompt_blocks.get(name, {}).get(expected.at)
            if content is None:
                raise Missing(f"prompt_block({name}) has no {expected.at} content")
            value, sensitive = content, True
        label = f"prompt_block({name}).{part}@{expected.at}"
    elif src == "default":
        var = expected.var or ""
        _declared(bindings, var)
        slot = bindings.defaults.get(var, {})
        if expected.at not in slot:
            raise Missing(f"default({var}) has no {expected.at} value")
        value = slot[expected.at]
        label = f"default({var})@{expected.at}"
    elif src == "observed":
        if evidence is None or expected.sink is None:
            raise Missing("observed: no evidence to read")
        probe = Check(id="_observed", sink=expected.sink, read=expected.read or ReadSpec(), op="exists")
        oti = (expected.turn - 1) if expected.turn else ti
        value = read_observed(probe, evidence, bindings, oti)
        sensitive = expected.sink in _REQUEST_SINKS
        label = f"observed({expected.sink}[{oti + 1}])"
    elif src == "run":
        field = expected.field or ""
        if field not in bindings.run:
            raise Missing(f"run.{field} is not known for this result")
        value = bindings.run[field]
        label = f"run.{field}"
    else:  # pragma: no cover
        raise Missing(f"unknown expected source {src}")
    value = apply_modifiers(value, expected, what=label)
    return value, label, sensitive


# ── ops ──────────────────────────────────────────────────────────────────────


def _dec(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise Missing(f"{value!r} is not a number") from exc


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return list(value) if isinstance(value, list | tuple | set) else [value]


def _equal(a: Any, b: Any) -> bool:
    if isinstance(a, int | float | Decimal) and isinstance(b, int | float | Decimal) and not isinstance(a, bool):
        return Decimal(str(a)) == Decimal(str(b))
    if isinstance(a, str) and isinstance(b, int | float | Decimal) and not isinstance(b, bool):
        try:
            return Decimal(a.strip()) == Decimal(str(b))
        except InvalidOperation:
            return False
    return _jsonable(a) == _jsonable(b)


def compare(op: str, observed: Any, expected: Any, *, count_op: str | None = None) -> tuple[bool, str]:
    """Apply one op. Returns ``(passed, reason)``; raises ``Missing`` when it cannot decide."""
    if op == "eq":
        ok = _equal(observed, expected)
        return ok, "equal" if ok else "not equal"
    if op == "ne":
        ok = not _equal(observed, expected)
        return ok, "differs" if ok else "equal"
    if op in ("contains", "not_contains"):
        hay = to_text(observed)
        needles = [to_text(n) for n in _as_list(expected)]
        if any(not n for n in needles) or not needles:
            raise Missing("expected value is empty; contains cannot decide")
        present = [n for n in needles if n in hay]
        if op == "contains":
            ok = len(present) == len(needles)
            return ok, "found" if ok else f"missing {[n for n in needles if n not in present][:3]}"
        ok = not present
        return ok, "absent" if ok else f"present {present[:3]}"
    if op in ("matches", "not_matches"):
        try:
            found = re.search(to_text(expected), to_text(observed))
        except re.error as exc:
            raise Missing(f"bad pattern: {exc}") from exc
        ok = (found is not None) == (op == "matches")
        return ok, "matched" if found else "no match"
    if op == "in":
        ok = any(_equal(observed, e) for e in _as_list(expected))
        return ok, "in the list" if ok else "not in the list"
    if op == "routes_in":
        allowed = {to_text(e) for e in _as_list(expected)}
        routes = (
            [r for r in re.split(r"[,\s]+", observed) if r] if isinstance(observed, str) else _as_list(observed)
        )
        bad = [to_text(r) for r in routes if to_text(r) not in allowed]
        return not bad, "every route allowed" if not bad else f"not allowed {bad[:3]}"
    if op == "not_leaks":
        hay = _norm(to_text(observed))
        leaks = [to_text(n) for n in _as_list(expected) if _norm(to_text(n)) and _norm(to_text(n)) in hay]
        if not [n for n in _as_list(expected) if _norm(to_text(n))]:
            raise Missing("expected value is empty; not leaks cannot decide")
        return not leaks, "no leak" if not leaks else "leaked"
    if op == "exists":
        ok = not _is_empty(observed)
        return ok, "present" if ok else "absent"
    if op == "empty":
        ok = _is_empty(observed)
        return ok, "empty" if ok else "not empty"
    if op == "matches_schema":
        try:
            import jsonschema  # lazy: optional dependency
        except ImportError as exc:  # pragma: no cover
            raise Missing("jsonschema is not installed") from exc
        if not isinstance(expected, dict):
            raise Missing("matches_schema needs a schema object")
        try:
            jsonschema.Draft202012Validator(expected).validate(_jsonable(observed))
        except jsonschema.ValidationError as exc:
            return False, f"schema: {exc.message[:200]}"
        except jsonschema.SchemaError as exc:
            raise Missing(f"bad schema: {exc.message[:200]}") from exc
        return True, "matches schema"
    if op == "conforms":
        keys = [to_text(k) for k in _as_list(expected)]
        if not isinstance(observed, dict):
            return False, "not an object"
        missing = [k for k in keys if observed.get(k) is None]
        return not missing, "has every key" if not missing else f"missing keys {missing[:5]}"
    if op in ("gte", "lte"):
        a, b = _dec(observed), _dec(expected)
        ok = a >= b if op == "gte" else a <= b
        return ok, f"{a} {'>=' if op == 'gte' else '<='} {b}: {'yes' if ok else 'no'}"
    if op == "count":
        n = len(observed) if isinstance(observed, list | tuple | dict | str) else (0 if observed is None else 1)
        target = int(_dec(expected))
        cop = count_op or "eq"
        ok = {"eq": n == target, "gte": n >= target, "lte": n <= target}[cop]
        return ok, f"count {n} {cop} {target}: {'yes' if ok else 'no'}"
    raise Missing(f"op {op} is not evaluated here")


# ── evaluation ───────────────────────────────────────────────────────────────


def _side(sink: str) -> str:
    if sink in _REPLY_SINKS:
        return "reply"
    if sink in _REQUEST_SINKS:
        return "request"
    return "other"


def _resolved_turns(check: Check, evidence: Evidence, bindings: Bindings):  # noqa: ANN202
    """Yield ``(ti, observed, expected, label, sensitive)`` or a ``Missing`` per turn."""
    out = []
    for ti in _turn_indexes(check.turn, evidence):
        try:
            observed = read_observed(check, evidence, bindings, ti)
            if check.expected is None:
                if OP_KIND[check.op] != "presence" or check.op in ("matches_schema", "conforms"):
                    raise Missing(f"op {check.op} needs an expected value")
                expected, label, sensitive = None, "", False
            else:
                expected, label, sensitive = resolve_expected(check.expected, bindings, evidence, ti)
            out.append((ti, observed, expected, label, sensitive or check.sink in _REQUEST_SINKS))
        except Missing as miss:
            out.append((ti, miss))
    return out


def evaluate_check(check: Check, evidence: Evidence, bindings: Bindings, *, prove: bool = True) -> CheckResult:
    if check.op == "same_across_doors":
        return _result(check, "undecided", reason="parity checks run through evaluate_parity")
    resolved = _resolved_turns(check, evidence, bindings)
    outcomes: list[CheckOutcome] = []
    first_obs: Any = None
    first_exp: Any = None
    label = ""
    sensitive = False
    reasons: list[str] = []
    for entry in resolved:
        if isinstance(entry[1], Missing):
            miss = entry[1]
            outcomes.append(miss.outcome)
            reasons.append(f"turn {entry[0] + 1}: {miss.reason}")
            continue
        ti, observed, expected, lbl, sens = entry
        label, sensitive = lbl, sensitive or sens
        try:
            ok, why = compare(check.op, observed, expected, count_op=check.count_op)
            outcomes.append("pass" if ok else "fail")
            reasons.append(f"turn {ti + 1}: {why}")
        except Missing as miss:
            outcomes.append(miss.outcome)
            reasons.append(f"turn {ti + 1}: {miss.reason}")
        if first_obs is None:
            first_obs, first_exp = observed, expected
        if outcomes[-1] == "fail":
            first_obs, first_exp = observed, expected
    if not outcomes:
        outcome: CheckOutcome = "undecided"
        reasons.append("no turn to read")
    elif "fail" in outcomes:
        outcome = "fail"
    elif "undecided" in outcomes:
        outcome = "undecided"
    elif all(o == "not_applicable" for o in outcomes):
        outcome = "not_applicable"
    elif "not_applicable" in outcomes:
        outcome = "undecided"
    else:
        outcome = "pass"
    result = _result(
        check,
        outcome,
        observed=_jsonable(first_obs),
        expected=_jsonable(first_exp),
        expected_source=label,
        reason="; ".join(reasons)[:1000],
        sensitive=sensitive,
    )
    if prove and outcome in ("pass", "fail"):
        from matrx_ai.checks.mutation import prove_can_fail

        proof = prove_can_fail(check, evidence, bindings)
        result = result.model_copy(update={"can_fail": proof.can_fail, "mutation": proof.mutation})
    return result


def _result(check: Check, outcome: CheckOutcome, **kw: Any) -> CheckResult:
    turn = check.turn if isinstance(check.turn, int) else None
    return CheckResult(
        id=check.id,
        title=check.title,
        proves=check.proves,
        required=check.required,
        sink=check.sink,
        outcome=outcome,
        side=_side(check.sink),  # type: ignore[arg-type]
        locator={"sink": check.sink, "turn": turn},
        **kw,
    )


def evaluate_checks(
    checks: list[Check], evidence: Evidence, bindings: Bindings, *, prove: bool = True
) -> list[CheckResult]:
    return [evaluate_check(c, evidence, bindings, prove=prove) for c in checks if c.op != "same_across_doors"]


def _strip(value: Any, ignore: list[str]) -> Any:
    if isinstance(value, dict):
        return {k: _strip(v, ignore) for k, v in value.items() if k not in ignore}
    if isinstance(value, list):
        return [_strip(v, ignore) for v in value]
    if isinstance(value, str):
        for pattern in ignore:
            try:
                value = re.sub(pattern, "", value)
            except re.error:
                continue
        return value
    return value


def parity_values(check: Check, evidence_by_door: dict[str, Evidence], bindings: Bindings) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for door, ev in sorted(evidence_by_door.items()):
        ti = _turn_indexes(check.turn, ev)[0]
        values[door] = _strip(_jsonable(read_observed(check, ev, bindings, ti)), check.ignore)
    return values


def parity_outcome(values: dict[str, Any]) -> tuple[CheckOutcome, str]:
    if len(values) < 2:
        return "undecided", f"parity needs two doors, have {len(values)}"
    items = list(values.items())
    base_door, base = items[0]
    differ = [d for d, v in items[1:] if v != base]
    if differ:
        return "fail", f"{', '.join(differ)} differ from {base_door}"
    return "pass", f"same across {', '.join(values)}"


def evaluate_parity(
    check: Check, evidence_by_door: dict[str, Evidence], bindings: Bindings, *, prove: bool = True
) -> CheckResult:
    try:
        values = parity_values(check, evidence_by_door, bindings)
    except Missing as miss:
        return _result(check, miss.outcome, reason=miss.reason)
    outcome, reason = parity_outcome(values)
    result = _result(
        check,
        outcome,
        observed={d: _digest(v) for d, v in values.items()},
        expected_source="same_across_doors",
        reason=reason,
        sensitive=check.sink in _REQUEST_SINKS,
    )
    if prove and outcome in ("pass", "fail"):
        from matrx_ai.checks.mutation import prove_parity_can_fail

        proof = prove_parity_can_fail(check, evidence_by_door, bindings)
        result = result.model_copy(update={"can_fail": proof.can_fail, "mutation": proof.mutation})
    return result


def _digest(value: Any) -> dict[str, Any]:
    text = json.dumps(value, sort_keys=True, default=str)
    return {"chars": len(text), "sha256": hashlib.sha256(text.encode()).hexdigest()[:16]}


def fact_items(facts: list[JudgeFact]) -> list[CheckResult]:
    """Judge facts are required items the checks cannot decide: undecided until judged."""
    return [
        CheckResult(
            id=f"fact:{f.id}",
            title=f.statement[:200],
            required=True,
            sink="reply",
            outcome="undecided",
            side="reply",
            expected_source="judge_fact",
            reason="decided by the judge",
        )
        for f in facts
    ]


# ── verdict ──────────────────────────────────────────────────────────────────


def _required(results: list[CheckResult]) -> list[CheckResult]:
    return [r for r in results if r.required and r.outcome != "not_applicable"]


def needs_judge(results: list[CheckResult], *, policy: str) -> bool:
    if policy == "off":
        return False
    if any(r.outcome == "fail" and r.format_failure for r in _required(results)):
        return False  # code already decided: the answer is not the declared output
    return any(r.outcome in ("fail", "undecided") for r in _required(results))


def judge_feed(results: list[CheckResult]) -> list[CheckResult]:
    return [r for r in _required(results) if r.side == "reply" and r.outcome in ("fail", "undecided")]


def compute_verdict(
    results: list[CheckResult],
    *,
    judge: JudgeDecision | None = None,
    blocked: bool = False,
    error: bool = False,
    precondition_failed: bool = False,
) -> VerdictResult:
    """CONTRACT v2 §2.6. A fail is never turned into a pass; nothing decided is never a pass."""
    if blocked:
        return VerdictResult(verdict="blocked", reason="a platform gate refused the run")
    if error:
        return VerdictResult(verdict="error", reason="the door failed after retries")
    if precondition_failed:
        return VerdictResult(verdict="inconclusive", reason="precondition failed; nothing was run")
    req = _required(results)
    usable = judge is not None and judge.fed_ok and not judge.advisory and judge.verdict != "judge_unfed"
    fails = [r for r in req if r.outcome == "fail"]
    if fails:
        if all(r.format_failure for r in fails):
            return VerdictResult(verdict="fail_format", reason=f"format: {fails[0].reason}"[:300], counted=True)
        if usable and judge is not None and judge.verdict == "format_only":
            return VerdictResult(verdict="fail_format", reason="judge: only the format is wrong", counted=True)
        return VerdictResult(verdict="fail", reason=f"failed: {', '.join(r.id for r in fails[:5])}", counted=True)
    if not req:
        return VerdictResult(verdict="inconclusive", reason="nothing decided: no required check applies")
    undecided = [r for r in req if r.outcome == "undecided"]
    unproven = [r for r in req if r.outcome == "pass" and r.can_fail is not True]
    if undecided:
        if not usable or judge is None:
            return VerdictResult(
                verdict="inconclusive", reason=f"undecided: {', '.join(r.id for r in undecided[:5])}"
            )
        if judge.verdict == "violated":
            return VerdictResult(verdict="fail", reason="judge: violated", counted=True)
        if judge.verdict == "format_only":
            return VerdictResult(verdict="fail_format", reason="judge: only the format is wrong", counted=True)
        if judge.verdict == "holds":
            if unproven:
                return VerdictResult(
                    verdict="inconclusive",
                    reason=f"cannot fail: {', '.join(r.id for r in unproven[:5])}",
                )
            return VerdictResult(verdict="pass_judged", reason="judge: holds", counted=True)
        return VerdictResult(verdict="inconclusive", reason=f"judge: {judge.verdict}")
    if unproven:
        return VerdictResult(
            verdict="inconclusive", reason=f"cannot fail: {', '.join(r.id for r in unproven[:5])}"
        )
    return VerdictResult(verdict="pass", reason=f"{len(req)} required checks passed", counted=True)


# ── storage excerpts ─────────────────────────────────────────────────────────


def _excerpt(value: Any, cap: int) -> tuple[Any, bool]:
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    if len(text) <= cap:
        return value, False
    return text[:cap], True


def _redact(value: Any) -> dict[str, Any]:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True, default=str)
    return {"redacted": True, "chars": len(text), "sha256": hashlib.sha256(text.encode()).hexdigest()}


def store_excerpts(results: list[CheckResult], *, cap: int = 2048) -> list[CheckResult]:
    """CONTRACT v2 §2.8: excerpts ≤ cap; hidden text, blocks and request sinks redacted."""
    out: list[CheckResult] = []
    for r in results:
        if r.sensitive:
            out.append(
                r.model_copy(
                    update={
                        "observed": None if r.observed is None else _redact(r.observed),
                        "expected": None if r.expected is None else _redact(r.expected),
                        "redacted": True,
                    }
                )
            )
            continue
        obs, t1 = _excerpt(r.observed, cap)
        exp, t2 = _excerpt(r.expected, cap)
        out.append(r.model_copy(update={"observed": obs, "expected": exp, "truncated": t1 or t2}))
    return out


def row_specs(checks: list[Check], bindings: Bindings, n_turns: int) -> list[dict[str, Any]]:
    """Every ``rows`` read the loaders must fetch: ``[{key, table, where, limit}]``."""
    specs: dict[str, dict[str, Any]] = {}
    for check in checks:
        if check.sink != "rows" or not check.read.table:
            continue
        indexes = list(range(n_turns)) if check.turn == "each" else [
            (n_turns - 1) if check.turn is None else int(check.turn) - 1
        ]
        for ti in indexes:
            try:
                where = _resolve_where(check.read, bindings, None, max(ti, 0))
            except Missing:
                continue
            key = rows_key(check.read.table, where)
            specs[key] = {"key": key, "table": check.read.table, "where": where, "limit": check.read.limit}
    return list(specs.values())
