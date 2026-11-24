"""A ``__kind`` the declared schema PINS to one value is restored at the seam.

Live record, ``structured_output.answer_off_contract``, 2026-11-07..10: 13 of the
16 events for the source-authority ranking agent (Gemini Flash, Search grounding,
so the schema travels as a JSON text contract, not constrained decoding) were ONE
item of ~25 whose ``__kind`` slot held the item's own ``id`` UUID (once
``"source_authority_magic"``). Every consumer received the slip and the kind
validator rejected the whole answer. The slot carries no information from the
model — exactly one value is legal there — so it is restored before any consumer
reads the answer, and the slip is still RECORDED (``was_recovered=True``).

What it must never do: touch any other field, guess a branch of a real union, or
hide an item that also lost its ``id`` (that answer stays off contract).
"""

from __future__ import annotations

import asyncio
import contextlib
import io
import json
from types import SimpleNamespace
from typing import Any

import pytest

ITEM_ID = "a10ef9c4-db74-4755-a7cc-1464d15faa89"

SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["__kind", "rankings"],
    "properties": {
        "__kind": {"type": "string", "const": "source_authority_rankings"},
        "rankings": {"type": "array", "items": {"$ref": "#/$defs/Ranking"}},
    },
    "$defs": {
        "Ranking": {
            "type": "object",
            "additionalProperties": False,
            "required": ["__kind", "id", "authority_score", "tier", "reasoning"],
            "properties": {
                "__kind": {"type": "string", "const": "source_authority_ranking"},
                "id": {"type": "string"},
                "authority_score": {"type": "integer"},
                "tier": {"type": "string", "enum": ["high", "medium", "low"]},
                "reasoning": {"type": "string"},
            },
        }
    },
}


def _ranking(index: int) -> dict[str, Any]:
    return {
        "__kind": "source_authority_ranking",
        "id": f"00000000-0000-4000-8000-{index:012d}",
        "authority_score": 60 + index,
        "tier": "medium",
        "reasoning": f"A peer-reviewed source on the topic (example {index}).",
    }


def _grounded_answer(slipped: dict[str, Any]) -> str:
    """The grounded text-contract shape: a digest, then one fenced json object,
    with the slip at item 19 as captured live (content scrubbed)."""
    rankings = [_ranking(i) for i in range(25)]
    rankings[19] = slipped
    payload = {"__kind": "source_authority_rankings", "rankings": rankings}
    return (
        "# GROUNDED RESEARCH DIGEST\n\nThe searched literature on the example topic spans "
        "trials and cohort studies (https://example.com/a).\n\n```json\n"
        + json.dumps(payload, indent=2)
        + "\n```"
    )


def _run_seam(answer_text: str, schema: dict[str, Any], monkeypatch: pytest.MonkeyPatch):
    import matrx_ai.providers.structured_output_findings as findings
    from matrx_ai.config import Role, UnifiedMessage, UnifiedResponse
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.providers.unified_client import UnifiedAIClient
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        mark_enforcement_dropped,
        release_declared_output_contract,
    )

    recorded: list[tuple[str, dict[str, Any]]] = []

    async def capture(key: str, **kwargs: Any) -> None:
        recorded.append((key, kwargs))

    monkeypatch.setattr(findings, "record_structured_output_finding", capture)

    async def dispatch() -> Any:
        return UnifiedResponse(
            messages=[UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text=answer_text)])],
            usage=None,
            finish_reason="stop",
        )

    async def run() -> str:
        token = bind_declared_output_contract(
            {"type": "json_schema", "json_schema": {"name": "SourceAuthorityOutput", "schema": schema}}
        )
        mark_enforcement_dropped("Google Search grounding: schema sent as a JSON text contract")
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                result = await UnifiedAIClient._dispatch_with_billing_net(
                    dispatch,
                    profile=SimpleNamespace(
                        vendor="google",
                        model_name="gemini-3.8-flash",
                        endpoint_id="test",
                        base_url=None,
                        offering_metadata={},
                    ),
                )
            return result.messages[0].get_output()
        finally:
            release_declared_output_contract(token)

    text = asyncio.run(run())
    off = [kw for key, kw in recorded if key == "structured_output.answer_off_contract"]
    return text, off


def _fenced(text: str) -> dict[str, Any]:
    body = text.split("```json", 1)[1].split("```", 1)[0]
    return json.loads(body)


@pytest.mark.parametrize(
    "slipped_kind", [ITEM_ID, "source_authority_magic"], ids=["id-in-kind-slot", "garbled-const"]
)
def test_a_slipped_pinned_kind_reaches_consumers_restored_and_is_recorded_recovered(
    slipped_kind: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    slipped = {**_ranking(19), "__kind": slipped_kind, "id": ITEM_ID}
    text, off = _run_seam(_grounded_answer(slipped), SCHEMA, monkeypatch)

    item = _fenced(text)["rankings"][19]
    assert item["__kind"] == "source_authority_ranking"
    assert item["id"] == ITEM_ID  # nothing else touched
    assert text.startswith("# GROUNDED RESEARCH DIGEST")
    assert len(off) == 1 and off[0]["was_recovered"] is True
    assert "$.rankings.19.__kind" in off[0]["detail"]["failures"][0]


def test_an_item_that_also_lost_its_id_stays_off_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    slipped = {k: v for k, v in _ranking(19).items() if k != "id"}
    slipped["__kind"] = ITEM_ID  # live shape: the id went into the kind slot
    text, off = _run_seam(_grounded_answer(slipped), SCHEMA, monkeypatch)

    assert "id" not in _fenced(text)["rankings"][19]
    assert len(off) == 1 and off[0]["was_recovered"] is False
    assert off[0]["detail"]["failures"] == ["$.rankings.19: 'id' is a required property"]
    assert off[0]["detail"]["kinds_restored"]


def test_a_real_union_is_never_guessed() -> None:
    from matrx_ai.schema.rules import restore_declared_kinds

    union = {
        "type": "object",
        "properties": {
            "block": {
                "anyOf": [
                    {"type": "object", "properties": {"__kind": {"const": "a"}}, "required": ["__kind"]},
                    {"type": "object", "properties": {"__kind": {"const": "b"}}, "required": ["__kind"]},
                ]
            },
            "maybe": {
                "anyOf": [
                    {"type": "object", "properties": {"__kind": {"const": "c"}}, "required": ["__kind"]},
                    {"type": "null"},
                ]
            },
        },
    }
    answer = {"block": {"__kind": "zzz"}, "maybe": {"__kind": "zzz"}}
    restored, notes = restore_declared_kinds(answer, union)
    assert restored["block"] == {"__kind": "zzz"}  # two real branches: untouched
    assert restored["maybe"] == {"__kind": "c"}  # nullable union: one real branch
    assert notes == ["$.maybe.__kind: 'zzz' restored to the declared 'c'"]


def test_an_on_contract_answer_is_left_byte_for_byte(monkeypatch: pytest.MonkeyPatch) -> None:
    answer = _grounded_answer(_ranking(19))
    text, off = _run_seam(answer, SCHEMA, monkeypatch)
    assert text == answer
    assert off == []
