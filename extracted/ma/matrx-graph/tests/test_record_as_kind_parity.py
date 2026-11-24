"""B2 record-as-kind — the pure half, held byte-identical with its TypeScript twin.

K-kinds-connection §7 B2 / §8 U1 (common-docs ``systems/data/custom-data/projects/data-for-every-client/discovery/
K-kinds-connection.md``). A record id becomes the kind value it stands for: a row of an OUTPUT
table rebuilds its registry kind (``value_from_record``), any other row is ``table:<uuid>``.
What the store answers is the reader's; what is decided from it is
``matrx_graph.kind_fields.record_kind_value`` / ``output_kind_of`` / ``child_relations`` and
``@ai-matrx/records`` ``src/kind-fields.ts``. Both must equal the golden
``fixtures/record_as_kind_golden.json``, which this module owns (an exact copy lives in
``apps/shared/records/src/__tests__/fixtures``; ``scripts/check-matrx-graph-snapshots.mjs`` refuses
drift).

The golden's data is RANDOM GENERIC (seeded words, numbers, dates) — nothing names a company,
feature or industry. Regenerate: ``REGEN_RECORD_AS_KIND_GOLDEN=1 uv run pytest <this file>``.
"""

from __future__ import annotations

import json
import os
import random
import uuid
from pathlib import Path
from typing import Any

import pytest

from matrx_graph.kind_fields import (
    PLATFORM_KEYS,
    child_relations,
    declarations_for,
    fields_for_kind,
    output_kind_of,
    record_kind_value,
    record_values_for,
)

GOLDEN = Path(__file__).parent / "fixtures" / "record_as_kind_golden.json"

_WORDS = ["amber", "birch", "cobalt", "delta", "ember", "fjord", "garnet", "harbor", "indigo", "juniper"]


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _relations(case: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "key": r.key,
            "kind_key": r.kind_key,
            "child_kind": r.child_kind,
            "target_table_id": r.target_table_id,
            "many": r.many,
        }
        for r in child_relations(case["facts"]["fields"])
    ]


def _derive(case: dict[str, Any]) -> dict[str, Any]:
    kind = output_kind_of(case["table_document"])
    children = [(c[0], c[1], c[2]) for c in case["children"]]
    return {
        "kind": kind,
        "relations": _relations(case),
        "value": record_kind_value(
            case["facts"], case["document"], kind=kind, children=children, withheld=case["withheld"]
        ),
    }


# ---------------------------------------------------------------------------- the generator


def _uuid(rng: random.Random) -> str:
    return str(uuid.UUID(int=rng.getrandbits(128), version=4))


def _phrase(rng: random.Random, n: int = 3) -> str:
    return " ".join(rng.choice(_WORDS) for _ in range(n))


def _child_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "__kind": {"type": "string"},
            "heading": {"type": "string"},
            "count": {"type": "integer"},
            "done": {"type": "boolean"},
        },
    }


def _parent_schema(rng: random.Random) -> dict[str, Any]:
    props: dict[str, Any] = {
        "__kind": {"type": "string"},
        "title": {"type": "string"},
        "noteText": {"type": "string", "maxLength": 4000},
        "level": {"type": "string", "enum": ["low", "mid", "high"]},
        "tags": {"type": "array", "items": {"type": "string", "enum": _WORDS[:5]}},
        "amount": {"type": "number", "x-matrx-unit": "units"},
        "ratio": {"type": "number", "x-matrx-unit": "%"},
        "due": {"type": "string", "format": "date"},
        "flag": {"type": "boolean"},
        "extra": {"type": "object"},
        "items": {"type": "array", "items": {"type": "object"}},
        "lead": {"type": "object"},
    }
    keys = list(props)
    rng.shuffle(keys)
    return {"type": "object", "properties": {k: props[k] for k in keys}}


def _sample_value(rng: random.Random, kind: str, child: str, n_items: int, with_lead: bool) -> dict[str, Any]:
    value: dict[str, Any] = {
        "__kind": kind,
        "title": _phrase(rng).title(),
        "noteText": _phrase(rng, 8),
        "level": rng.choice(["low", "mid", "high"]),
        "tags": rng.sample(_WORDS[:5], rng.randint(0, 3)),
        "amount": round(rng.uniform(0, 900), 2),
        "ratio": rng.randint(0, 100),
        "due": f"2026-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
        "flag": rng.random() < 0.5,
        "extra": {"a": rng.randint(0, 9), "b": [_phrase(rng, 1), None]},
        "items": [
            {"__kind": child, "heading": _phrase(rng, 2), "count": rng.randint(0, 50), "done": rng.random() < 0.5}
            for _ in range(n_items)
        ],
    }
    if with_lead:
        value["lead"] = {"__kind": child, "heading": _phrase(rng, 2), "count": rng.randint(0, 9), "done": True}
    return value


def _output_case(rng: random.Random, n: int) -> dict[str, Any]:
    kind = f"sample_{rng.choice(_WORDS)}_{n}"
    child = f"part_{rng.choice(_WORDS)}_{n}"
    table_id, child_table = _uuid(rng), _uuid(rng)
    edges = [{"field_name": "items", "child_kind": child, "position": 0}, {"field_name": "lead", "child_kind": child, "position": 1}]
    kind_fields = fields_for_kind(_parent_schema(rng), edges, kind=kind)
    fields = []
    for d in declarations_for(kind_fields, {child: child_table}, self_table_id=table_id):
        fields.append({**d, "id": _uuid(rng), "version": 1})
    value = _sample_value(rng, kind, child, rng.randint(0, 4), rng.random() < 0.6)
    values, children = record_values_for(value, fields)
    document = dict(values)
    by_key = {f["key"]: f for f in fields}
    for key, _pos, _child in children:
        if (by_key[key].get("config") or {}).get("kind_many"):
            document.setdefault(key, []).append(_uuid(rng))
        else:
            document[key] = _uuid(rng)
    # The platform Fields the lander writes beside the kind's own.
    document.update(
        {
            "output_state": "draft",
            "output_kept": False,
            "output_chain": _uuid(rng),
            "output_generation": rng.randint(1, 4),
            "output_reason": "first",
        }
    )
    withheld = []
    if rng.random() < 0.4:
        masked = rng.choice([k for k in ("title", "level", "amount") if by_key.get(k)])
        withheld = [masked]
        document[masked] = None
    document["_hidden"] = {k: {"reason": "masked for this viewer"} for k in withheld}
    return {
        "name": f"output table #{n}",
        "facts": {"table_id": table_id, "organization_id": _uuid(rng), "fields": fields},
        "table_document": {"kept_for": "agent_output", "kind": kind, "name": "outputs"},
        "document": document,
        "children": [[k, p, c] for k, p, c in children],
        "withheld": withheld,
    }


def _ordinary_case(rng: random.Random, n: int) -> dict[str, Any]:
    table_id = _uuid(rng)
    fields = [
        {"key": "name", "type": "text", "id": _uuid(rng), "version": 1},
        {"key": "size", "type": "number", "id": _uuid(rng), "version": 2},
        {"key": "stage", "type": "list", "id": _uuid(rng), "version": 1, "config": {"options_table_id": _uuid(rng)}},
        {"key": "owner", "type": "relation", "id": _uuid(rng), "version": 1, "relation_target": _uuid(rng)},
    ]
    document: dict[str, Any] = {
        "name": _phrase(rng).title(),
        "size": rng.randint(1, 500),
        "stage": rng.choice(["open", "closed"]),
        "owner": _uuid(rng),
        "_hidden": {},
    }
    if rng.random() < 0.5:
        document["free_note"] = _phrase(rng, 5)
    withheld = ["size"] if rng.random() < 0.4 else []
    for k in withheld:
        document[k] = None
        document["_hidden"][k] = {"reason": "masked for this viewer"}
    table_document = rng.choice(
        [{"name": "a table"}, {"kept_for": "something_else", "kind": "unused"}, {"kept_for": "agent_output"}, None]
    )
    return {
        "name": f"ordinary table #{n}",
        "facts": {"table_id": table_id, "organization_id": _uuid(rng), "fields": fields},
        "table_document": table_document,
        "document": document,
        "children": [],
        "withheld": withheld,
    }


def _build_golden() -> dict[str, Any]:
    rng = random.Random(20261101)
    cases = [_output_case(rng, n) for n in range(6)] + [_ordinary_case(rng, n) for n in range(6)]
    for case in cases:
        case["expected"] = _derive(case)
    return {"cases": cases}


# ---------------------------------------------------------------------------- the tests


@pytest.fixture(scope="module")
def golden() -> dict[str, Any]:
    if os.environ.get("REGEN_RECORD_AS_KIND_GOLDEN") == "1":
        GOLDEN.write_text(json.dumps(_build_golden(), indent=2, sort_keys=True) + "\n")
    return json.loads(GOLDEN.read_text())


def test_the_golden_has_both_kinds_of_row(golden: dict[str, Any]) -> None:
    kinds = [c["expected"]["kind"] for c in golden["cases"]]
    assert sum(k is not None for k in kinds) >= 5 and sum(k is None for k in kinds) >= 5
    assert any(c["children"] for c in golden["cases"]), "no case exercises contained records"
    assert any(c["withheld"] for c in golden["cases"]), "no case exercises a masked field"


def test_python_derives_every_golden_case(golden: dict[str, Any]) -> None:
    for case in golden["cases"]:
        assert _canonical(_derive(case)) == _canonical(case["expected"]), case["name"]


def test_an_output_row_rebuilds_its_registry_kind_without_bookkeeping(golden: dict[str, Any]) -> None:
    for case in golden["cases"]:
        value = case["expected"]["value"]
        if case["expected"]["kind"]:
            assert value["__kind"] == case["expected"]["kind"]
            assert not set(value) & set(PLATFORM_KEYS), case["name"]
            for rel in case["expected"]["relations"]:
                assert rel["key"] not in value, f"{case['name']}: a relation id leaked as a value"
        else:
            assert value["__kind"] == f"table:{case['facts']['table_id']}"
        assert not any(k.startswith("_") and k != "__kind" for k in value), case["name"]


def test_a_masked_field_is_never_shown(golden: dict[str, Any]) -> None:
    for case in golden["cases"]:
        for key in case["withheld"]:
            field = next((f for f in case["facts"]["fields"] if f["key"] == key), {})
            name = (field.get("config") or {}).get("kind_key") or key
            assert name not in case["expected"]["value"], f"{case['name']}: {key} shown"


def test_the_golden_is_current() -> None:
    """The generator still produces the committed golden (a changed derivation is regenerated, reviewed)."""
    assert _canonical(_build_golden()) == _canonical(json.loads(GOLDEN.read_text()))
