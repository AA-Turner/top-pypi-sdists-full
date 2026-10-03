"""Guard: a record kind's DEFAULT binding is exactly the registered kind on every provider wire.

THE FAILURE. KINDS-GLUE wave 2 (aidream ad4414a311) bound every ``record`` kind with two more
optional root keys, ``_replaces`` and ``_new``, on every run. Strict providers list every
property in ``required`` and widen an optional one to nullable only within a budget; past it the
field is FORCED non-null. Measured over the 24 live record kinds on 2026-10-02, Anthropic
(0 and 1 tools) went over that budget for five of them:

* ``flashcard_set``, ``quiz_set`` — ``_replaces`` and ``_new`` forced: the model had to invent a
  uuid and a boolean on every call;
* ``q_and_a_set``, ``diagram_spec`` — the keys forced AND real Fields lost their nullability;
* ``decision_tree`` — the keys stayed nullable and seven to eight real Fields were forced instead.

OpenAI and Google wires were unchanged apart from the two nullable keys.

THE RULE. The keys reach a model only when the run can act on them
(``response_format_for_kind(..., control_keys=True)``, wave 2's router). So the default binding
of every live record kind must translate, on OpenAI, Anthropic (0 and 1 tools) and Google, to
the SAME wire, with the SAME narrowing notes, as the registered schema itself — no key, no
forced Field, no lint change.

The schemas are the live registry's record kinds (``fixtures/live_record_kind_schemas.json``,
read 2026-10-02); only ``get_kind`` is injected, every translator is production code.

Plant that must turn this red (``plant.py``, this file as CMD): default ``control_keys`` to
``True`` in ``matrx_ai.kinds.response_format_for_kind``.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator

FIXTURE = Path(__file__).parent / "fixtures" / "live_record_kind_schemas.json"
SCHEMAS: dict[str, dict[str, Any]] = json.loads(FIXTURE.read_text())
CONTROL_KEYS = ("_replaces", "_new", "_record_id", "_records")
#: The kinds the 2026-10-02 measurement found broken — the fixture must keep them.
MEASURED_BROKEN = ("decision_tree", "diagram_spec", "flashcard_set", "q_and_a_set", "quiz_set")


def _wires(schema: dict[str, Any], slug: str) -> dict[str, Any]:
    response_format = {
        "type": "json_schema",
        "json_schema": {"name": slug, "schema": schema, "strict": True},
    }
    out: dict[str, Any] = {}
    out["openai"] = OpenAITranslator.translate_output_schema(copy.deepcopy(schema))[:2]
    for tools in (0, 1):
        out[f"anthropic/{tools}-tools"] = AnthropicTranslator.translate_output_schema(
            copy.deepcopy(schema), tool_count=tools
        )[:2]
    out["google"] = (
        GoogleTranslator._fit_google_wire_schema(copy.deepcopy(schema), response_format),
        [],
    )
    return out


def _mentions_control_key(node: Any) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        props = node.get("properties")
        if isinstance(props, dict):
            found += [k for k in props if k in CONTROL_KEYS]
        for value in node.values():
            found += _mentions_control_key(value)
    elif isinstance(node, list):
        for value in node:
            found += _mentions_control_key(value)
    return found


@pytest.fixture
def kinds_mod(monkeypatch):
    from matrx_graph.kinds import KindEntry

    import matrx_ai.kinds as kinds

    async def fake_get_kind(slug: str):
        schema = SCHEMAS.get(slug)
        if schema is None:
            return None
        return KindEntry(slug=slug, version=1, json_schema=schema, disposition="record")

    monkeypatch.setattr(kinds, "get_kind", fake_get_kind)
    return kinds


def test_the_fixture_still_holds_the_kinds_that_broke():
    assert set(MEASURED_BROKEN) <= set(SCHEMAS), sorted(set(MEASURED_BROKEN) - set(SCHEMAS))
    assert len(SCHEMAS) >= 20


@pytest.mark.parametrize("slug", sorted(SCHEMAS))
async def test_the_default_binding_is_the_registered_kind_on_every_wire(kinds_mod, slug):
    from matrx_ai.schema.lint import lint_output_schema

    registered = SCHEMAS[slug]
    bound = await kinds_mod.response_format_for_kind(slug)
    reg_report = lint_output_schema(registered)
    reg_ok = reg_report.portable_schema is not None or reg_report.ok
    if bound is None:
        assert not reg_ok, f"{slug}: the registered kind lints clean but the binding was refused"
        return
    assert reg_ok, f"{slug}: bound although the registered kind is not provider-portable"
    schema = bound.model_dump(mode="json", by_alias=True, exclude_none=True)["json_schema"][
        "schema"
    ]
    assert not _mentions_control_key(schema), (
        f"{slug}: the default binding carries control keys {_mentions_control_key(schema)}"
    )

    # The registered kind exactly as the binder would carry it with no control keys: `__kind`
    # first, through the same envelope model (its round-trip is not this guard's business).
    from matrx_ai.config.response_format import OutputSchemaEnvelope

    as_registered = OutputSchemaEnvelope.model_validate(
        {"name": slug, "schema": kinds_mod.discriminator_first(registered, slug), "strict": True}
    ).model_dump(mode="json", by_alias=True, exclude_none=True)["schema"]
    expected = _wires(as_registered, slug)
    actual = _wires(schema, slug)
    for provider, (wire, notes) in actual.items():
        want_wire, want_notes = expected[provider]
        assert not _mentions_control_key(wire), (
            f"{slug} on {provider}: control keys reached the wire: {_mentions_control_key(wire)}"
        )
        new_notes = [n for n in notes if n not in want_notes]
        assert not new_notes, f"{slug} on {provider}: the binding forced more than the kind: {new_notes}"
        assert json.dumps(wire, sort_keys=True) == json.dumps(want_wire, sort_keys=True), (
            f"{slug} on {provider}: the wire differs from the registered kind's"
        )
