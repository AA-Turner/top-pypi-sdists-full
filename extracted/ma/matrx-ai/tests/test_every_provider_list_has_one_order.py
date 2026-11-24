"""THE ONE ORDER (static seal P0.2, D16): every platform-built list that reaches a provider comes out
in one platform-guaranteed order, whatever path built it.

Live 2026-11-12: tool declarations reloaded from the jsonb ledger came back with different key order
on turn 2 and the provider re-wrote the whole conversation. These guards send the SAME input down
every path a turn can take and require byte-identical output:

* fresh, in memory (this worker sent the last turn);
* reloaded from storage (the record round-tripped through a jsonb column: object keys re-collated);
* a record written before P0.2 (append order, no sent JSON text);
* another worker with an empty in-process cache and no record;
* a cache hit (the same send again);
* no conversation at all (untracked);
* the producers handing the list over in any order.

Plus the static guard: nothing outside the one boundary builds a provider ``tools`` array.
"""

from __future__ import annotations

import itertools
import json
import re
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.config.canonical_order import canonical_bytes, canonical_json
from matrx_ai.config.message_config import MessageList
from matrx_ai.tools import declaration_ledger

PROVIDER = "anthropic"


def _jsonb(value: Any) -> Any:
    """What a jsonb column hands back: every object's keys by length, then bytewise."""
    if isinstance(value, list):
        return [_jsonb(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonb(value[k]) for k in sorted(value, key=lambda k: (len(k.encode()), k.encode()))}
    return value


def _decl(name: str) -> dict[str, Any]:
    # Keys in an author's order that a jsonb round trip changes (``type`` / ``required`` /
    # ``properties`` / ``description``), one property so only the KEYWORD order is at stake.
    return {
        "name": name,
        "description": f"{name} does one thing",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"description": "what to look for", "type": "string"}},
            "required": ["query"],
            "additionalProperties": False,
        },
    }


def _name_of(decl: dict[str, Any]) -> str | None:
    name = decl.get("name")
    return name if isinstance(name, str) else None


def _send(conversation_id: str | None, decls: list[dict[str, Any]]) -> bytes:
    out = declaration_ledger.stabilize_declarations(
        PROVIDER, [json.loads(json.dumps(d)) for d in decls], name_of=_name_of, conversation_id=conversation_id
    ).declarations
    # The SDK serializes in dict order: these are the bytes the provider receives.
    return json.dumps(out, ensure_ascii=False).encode()


@pytest.fixture(autouse=True)
def _clean_ledger():
    declaration_ledger.reset_for_tests()
    yield
    declaration_ledger.reset_for_tests()


NAMES = ("search_web", "apply_surface_write", "memory", "context")


def test_a_tools_array_is_the_same_bytes_on_every_path():
    decls = [_decl(n) for n in NAMES]
    conv = str(uuid4())

    fresh = _send(conv, decls)
    assert [d["name"] for d in json.loads(fresh)] == sorted(NAMES)

    # A cache hit: this worker sends again.
    assert _send(conv, list(reversed(decls))) == fresh

    # Reloaded from storage: the record round-trips through jsonb (the ``wire`` text survives).
    record = _jsonb(declaration_ledger.export_record(conv))
    declaration_ledger.forget_conversation(conv)
    assert declaration_ledger.hydrate_from_record(conv, record)
    assert _send(conv, decls[1:] + decls[:1]) == fresh

    # A record written before P0.2: append order, the declaration jsonb-reordered, no sent text.
    legacy = {
        PROVIDER: {
            "seq": 1,
            "tools": [{"name": d["name"], "declaration": _jsonb(d)} for d in decls],
        }
    }
    legacy_conv = str(uuid4())
    assert declaration_ledger.hydrate_from_record(legacy_conv, legacy)
    assert _send(legacy_conv, decls) == fresh

    # Another worker: empty in-process cache, no record reached the row.
    other = str(uuid4())
    assert _send(other, list(reversed(decls))) == fresh

    # No conversation at all: never tracked, still the one order.
    assert _send(None, decls[2:] + decls[:2]) == fresh


@pytest.mark.parametrize("order", list(itertools.permutations(range(len(NAMES)))))
def test_the_producers_hand_over_order_never_reaches_the_wire(order):
    decls = [_decl(NAMES[i]) for i in order]
    baseline = _send(str(uuid4()), [_decl(n) for n in NAMES])
    assert _send(str(uuid4()), decls) == baseline
    assert _send(None, decls) == baseline


def test_a_declarations_keywords_are_canonical_and_its_properties_keep_the_authors_order():
    authored = {
        "input_schema": {
            "required": ["topic"],
            "properties": {
                "topic": {"type": "string", "description": "first, as the author wrote it"},
                "id": {"description": "second", "enum": ["b", "a"], "type": "string"},
            },
            "type": "object",
        },
        "description": "d",
        "name": "t",
    }
    out = canonical_json(authored)
    assert list(out) == ["name", "description", "input_schema"]
    assert list(out["input_schema"]) == ["type", "properties", "required"]
    # The model writes arguments in ``properties`` order: never re-sorted.
    assert list(out["input_schema"]["properties"]) == ["topic", "id"]
    assert list(out["input_schema"]["properties"]["id"]) == ["type", "description", "enum"]
    # Data is the author's literal value: the enum keeps its order.
    assert out["input_schema"]["properties"]["id"]["enum"] == ["b", "a"]
    # A storage round trip changes nothing once canonical, and canonical is idempotent.
    assert canonical_bytes(_jsonb(authored)) != canonical_bytes(authored)  # only the properties' order differs
    reordered = _jsonb(authored)
    reordered["input_schema"]["properties"] = authored["input_schema"]["properties"]
    assert canonical_bytes(reordered) == canonical_bytes(authored)
    assert canonical_json(out) == out and canonical_bytes(out) == canonical_bytes(authored)


def test_turn_context_slots_render_in_one_order_whoever_attaches_first():
    first, second = MessageList(), MessageList()
    for slot, text in (("skills", "S"), ("active_context", "C"), ("helpers", "H"), ("attachments", "A")):
        first.attach_turn_context(text, slot=slot)
        first.attach_tail_context(text, slot=slot)
    for slot, text in (("helpers", "H"), ("attachments", "A"), ("skills", "S"), ("active_context", "C")):
        second.attach_turn_context(text, slot=slot)
        second.attach_tail_context(text, slot=slot)
    assert first.render_turn_context() == second.render_turn_context()
    assert first.render_tail_context() == second.render_tail_context()


# ── The static guard: nothing outside the one boundary builds a provider ``tools`` array ──────────

_PACKAGE = Path(__file__).resolve().parents[1] / "matrx_ai"

#: Where a provider declaration may be formatted. Everything else that reaches a provider gets its
#: tools from ``BaseTranslator.build_provider_tools`` (the ledger, THE ONE ORDER).
_ALLOWED = {
    "providers/base_translator.py",  # build_provider_tools: the one boundary
    "tools/registry.py",  # get_provider_tools: called only by the boundary
    "tools/models.py",  # the formatters themselves
    "config/context_preflight.py",  # a token ESTIMATE; never sent
}
_FORMATTERS = re.compile(r"\.(get_provider_tools|get_provider_format)\(")


def test_no_provider_tools_array_is_built_outside_the_one_boundary():
    offenders = []
    for path in sorted(_PACKAGE.rglob("*.py")):
        rel = path.relative_to(_PACKAGE).as_posix()
        if "/tests/" in f"/{rel}" or rel in _ALLOWED:
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if _FORMATTERS.search(line) and not line.lstrip().startswith("#"):
                offenders.append(f"{rel}:{lineno}: {line.strip()}")
    assert not offenders, (
        "A provider tools array is built outside BaseTranslator.build_provider_tools, so it skips THE ONE "
        "ORDER (matrx_ai/config/canonical_order.py, static seal P0.2). Route it through the boundary:\n"
        + "\n".join(offenders)
    )


def test_the_boundary_hands_every_declaration_through_the_one_order():
    """The static half of the forcing function: the ledger's outputs pass ``canonical_json`` and its
    order is sorted, on the tracked and the untracked path. A refactor that drops either fails here
    even before a behavioural test notices."""
    source = (_PACKAGE / "tools" / "declaration_ledger.py").read_text(encoding="utf-8")
    assert "out = [_canonical_or_copy(ledger.declarations[name]) for name in ledger.order]" in source
    assert "        return canonical_json(decl)\n" in source  # the one order, with the pre-P0.2 copy only on failure
    assert "ledger.order.sort(key=lambda name: order_key(name, ledger.authored))" in source
    assert "canonical_tool_array(declarations, name_of=name_of, authored=authored)" in source
    base = (_PACKAGE / "providers" / "base_translator.py").read_text(encoding="utf-8")
    assert "return stabilize_declarations(" in base
    assert "authored=authored_wire_names(config)," in base
