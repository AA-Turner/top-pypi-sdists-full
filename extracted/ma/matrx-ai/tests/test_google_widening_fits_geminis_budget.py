"""OUR WIDENING MUST NEVER TURN A REQUEST GEMINI ACCEPTS INTO ONE IT REFUSES.

Arman, 2026-09-27: each provider's translator takes ANY shape we hold and makes it
safe for that exact API, and a provider refusing our shape is OUR translator's bug.

The defect (SCHEMA-TRANSLATION-VERIFY.md, **F1**): expressing an optional field as
required-and-nullable is lossless for the contract, and at the root of an object
Gemini does not charge for it — 80 of them are accepted. Inside a BOUNDED array it
is not free: Gemini unrolls ``maxItems: n`` and compiles the item schema n times,
so each widening there costs n, and past its ceiling it answers

    400 The specified schema produces a constraint that has too many states for
        serving.

Measured live against ``gemini-2.5-flash`` on 2026-09-28 on the live tool schema
``data_patterns`` (``fields: {maxItems: 40}``): the forced wire and the wire with
ONE widened item field are ACCEPTED (200); the wire with both widened — which is
what the translator built unconditionally — is REFUSED. ``AnthropicTranslator``
has fitted its widening inside a measured ceiling since 2026-09-27; the Google
translator had no measure and no fallback.

Gemini's rule is restated here FROM THE REFUSAL, by counting nullable unions under
a bounded array in the finished wire — never by calling the budget under test.
Every check fails on the pre-fix tree (``git show HEAD:<path> > <path>``).
"""

from __future__ import annotations

import contextlib
import io
from typing import Any

import pytest

#: The F1 shape: a bounded array whose items carry two optional fields, wrapped in
#: a root that also has optional fields (which Gemini charges nothing for).
F1_SHAPE: dict[str, Any] = {
    "type": "object",
    "required": ["action"],
    "properties": {
        "action": {"type": "string"},
        "domain": {"type": "string"},
        "name": {"type": "string"},
        "fields": {
            "type": "array",
            "maxItems": 40,
            "items": {
                "type": "object",
                "required": ["name", "selector"],
                "additionalProperties": False,
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "selector": {"type": "string", "minLength": 1},
                    "attr": {"type": "string"},
                    "is_list": {"type": "boolean"},
                },
            },
        },
    },
}

#: The same items under an UNBOUNDED array: a loop in Gemini's constraint, not an
#: unrolled sequence, and measured cheap — so nothing here may be forced.
UNBOUNDED_SHAPE: dict[str, Any] = {
    "type": "object",
    "required": ["action"],
    "properties": {
        "action": {"type": "string"},
        "fields": {
            "type": "array",
            "items": F1_SHAPE["properties"]["fields"]["items"],
        },
    },
}


def _wire(schema: dict[str, Any]) -> dict[str, Any]:
    from matrx_ai.providers.google.translator import GoogleTranslator

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        wire = GoogleTranslator._build_google_response_schema(
            {"type": "json_schema", "name": "f1_probe", "schema": schema}
        )
    assert isinstance(wire, dict), "the translator produced no wire schema at all"
    return wire


def _nullable_unions_under_bounded_arrays(node: Any, _multiple: int = 1) -> int:
    """How many states Gemini pays for our widening: every ``anyOf`` carrying a
    ``{"type": "null"}`` branch, counted ONCE PER unrolled element of every bounded
    array it sits inside. Restated from Gemini's refusal, independent of our own
    budget code."""
    if isinstance(node, list):
        return sum(_nullable_unions_under_bounded_arrays(item, _multiple) for item in node)
    if not isinstance(node, dict):
        return 0
    total = 0
    branches = node.get("anyOf")
    if isinstance(branches, list) and any(
        isinstance(b, dict) and b.get("type") == "null" for b in branches
    ):
        total += _multiple if _multiple > 1 else 0
    for key, value in node.items():
        if key in ("required", "enum", "const", "default", "examples", "description"):
            continue
        if key == "items":
            raw_max = node.get("maxItems")
            inner = _multiple * raw_max if isinstance(raw_max, int) and raw_max > 0 else _multiple
            total += _nullable_unions_under_bounded_arrays(value, inner)
        elif key in ("properties", "$defs", "definitions") and isinstance(value, dict):
            for sub in value.values():
                total += _nullable_unions_under_bounded_arrays(sub, _multiple)
        else:
            total += _nullable_unions_under_bounded_arrays(value, _multiple)
    return total


def _item_properties(wire: dict[str, Any]) -> dict[str, Any]:
    """`fields`'s item properties, wherever the widening put the array node."""
    node = wire["properties"]["fields"]
    if "anyOf" in node:
        node = next(b for b in node["anyOf"] if isinstance(b, dict) and b.get("type") == "array")
    return node["items"]["properties"]


def _is_nullable_union(node: Any) -> bool:
    branches = node.get("anyOf") if isinstance(node, dict) else None
    return isinstance(branches, list) and any(
        isinstance(b, dict) and b.get("type") == "null" for b in branches
    )


def test_the_widening_inside_a_bounded_array_stays_inside_geminis_measured_budget() -> None:
    from matrx_ai.providers.google.translator import GoogleTranslator

    wire = _wire(F1_SHAPE)
    spend = _nullable_unions_under_bounded_arrays(wire)
    budget = GoogleTranslator.GEMINI_UNROLLED_WIDENING_BUDGET
    assert spend <= budget, (
        "the Google translator widened optional fields inside a `maxItems: 40` array past "
        f"Gemini's measured budget ({spend} > {budget}) — this is the live 400 "
        '"too many states for serving" that our own transformation caused (F1)'
    )
    # And it did not simply give up on widening: the cheap ones still happened.
    assert spend > 0, "nothing was widened inside the array at all — that is over-correction"


def test_the_field_it_could_not_widen_is_named_not_dropped_quietly() -> None:
    """Law 4: a compromise announces itself with the field it cost."""
    import matrx_ai.providers.structured_output_findings as findings

    token = findings.begin_translation_findings()
    try:
        wire = _wire(F1_SHAPE)
        pending = findings._PENDING.get() or []
    finally:
        findings.end_translation_findings(token)

    forced = [
        name for name, node in _item_properties(wire).items() if not _is_nullable_union(node)
    ]
    # `name` and `selector` were required by the author; the forced one is an
    # OPTIONAL field the translator could not afford to widen.
    optional_forced = [n for n in forced if n in ("attr", "is_list")]
    assert optional_forced, "no optional item field was forced, so nothing to report"
    narrowed = [note for item in pending for note in item["narrowed"]]
    assert narrowed, (
        "an optional field the author may omit is now REQUIRED on the wire and the "
        "translator recorded nothing — a silent narrowing of the contract"
    )
    assert any(name in note for note in narrowed for name in optional_forced), (
        f"the narrowing note does not name the field it cost: {narrowed} vs {optional_forced}"
    )


def test_widening_at_the_root_is_untouched_because_gemini_does_not_charge_for_it() -> None:
    """Measured: 80 nullable-union properties at the root of a flat object are
    accepted. So the meter must cost nothing there — fixing F1 by widening less
    everywhere would trade one defect for a worse one."""
    wire = _wire(F1_SHAPE)
    for name in ("domain", "name"):
        assert _is_nullable_union(wire["properties"][name]), (
            f"root optional field {name!r} was FORCED although Gemini charges nothing for "
            "widening it — the meter is leaking outside bounded arrays"
        )


def test_an_unbounded_array_keeps_every_optional_item_field_nullable() -> None:
    """An unbounded array is a LOOP in Gemini's constraint, measured cheap: 4
    nullable item fields with no ``maxItems`` are accepted where ``maxItems: 100``
    is refused. Nothing under one may be forced."""
    wire = _wire(UNBOUNDED_SHAPE)
    for name in ("attr", "is_list"):
        assert _is_nullable_union(_item_properties(wire)[name]), (
            f"optional item field {name!r} was forced under an UNBOUNDED array, where "
            "Gemini pays for it once"
        )


def test_the_wire_still_enforces_the_contract_it_was_given() -> None:
    """The cure must not be a looser contract: every object still closed, every
    property still listed in ``required``, and every declared constraint still on
    the wire."""
    import json

    wire = _wire(F1_SHAPE)

    def walk(node: Any, path: str = "$") -> list[str]:
        problems: list[str] = []
        if isinstance(node, dict):
            if isinstance(node.get("properties"), dict):
                extra = node.get("additionalProperties")
                if extra is not False and not isinstance(extra, dict):
                    problems.append(f"{path} is not closed")
                missing = set(node["properties"]) - set(node.get("required") or ())
                if missing:
                    problems.append(f"{path} is not all-required: {sorted(missing)}")
            for key, value in node.items():
                problems += walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                problems += walk(value, f"{path}[{index}]")
        return problems

    assert walk(wire) == [], walk(wire)
    text = json.dumps(wire)
    for keyword in ("maxItems", "minLength"):
        assert keyword in text, f"the declared {keyword} constraint was dropped from the wire"


def test_no_other_provider_pays_for_geminis_array_rule() -> None:
    """``unroll_budget`` is Google's lever and nobody else's: an unmetered budget
    behaves exactly as before, so Anthropic's own fitted search is untouched."""
    from matrx_ai.schema.rules import WideningBudget

    unmetered = WideningBudget()
    assert unmetered.allow({"type": "string"}, 4_000) is True
    metered = WideningBudget(unroll_budget=40)
    assert metered.allow({"type": "string"}, 40) is True
    assert metered.allow({"type": "string"}, 40) is False, "the budget did not stop spending"
    assert metered.allow({"type": "string"}) is True, "an unmultiplied widening must stay free"


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
