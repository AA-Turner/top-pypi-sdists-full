"""One bad element must not lose a paid list answer (research L6e, 2026-11-07): a 25-source authority answer
with one wrong ``__kind`` and one missing ``id`` failed the whole batch. ``set_aside_invalid_list_elements`` keeps
the valid elements and reports each removed one; anything that is not an element-level fault changes nothing.

The real JSON-Schema validator runs; only the kind catalog lookup is replaced by a fixed schema.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph import kinds
from matrx_graph.executor.schema_validation import validate_instance_checked

SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["rankings"],
    "properties": {
        "rankings": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id", "authority_score"],
                "properties": {
                    "__kind": {"const": "source_authority_ranking"},
                    "id": {"type": "string"},
                    "authority_score": {"type": "integer"},
                },
            },
        },
        "note": {"type": "string"},
    },
}


@pytest.fixture(autouse=True)
def _schema(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _check(value: Any, slug: str) -> kinds.KindCheck:
        errors, checked = validate_instance_checked(SCHEMA, value)
        return kinds.KindCheck(checked=checked, errors=errors)

    monkeypatch.setattr(kinds, "check_against_kind", _check)


def _ok(i: int) -> dict[str, Any]:
    return {"__kind": "source_authority_ranking", "id": f"s{i}", "authority_score": i}


@pytest.mark.asyncio
async def test_the_valid_elements_land_and_each_bad_one_is_reported() -> None:
    rankings = [_ok(i) for i in range(25)]
    rankings[19] = {**_ok(19), "__kind": "authority_ranking"}
    rankings[22] = {"__kind": "source_authority_ranking", "authority_score": 5}
    cleaned, aside = await kinds.set_aside_invalid_list_elements({"rankings": rankings}, "k")
    assert [r["id"] for r in cleaned["rankings"]] == [f"s{i}" for i in range(25) if i not in (19, 22)]
    assert [(a.field, a.index, a.element_id) for a in aside] == [("rankings", 19, "s19"), ("rankings", 22, None)]
    assert "__kind" in aside[0].errors[0] and "'id' is a required property" in aside[1].errors[0]


@pytest.mark.asyncio
async def test_a_valid_answer_is_untouched() -> None:
    value = {"rankings": [_ok(1)]}
    assert await kinds.set_aside_invalid_list_elements(value, "k") == (value, [])


@pytest.mark.asyncio
async def test_an_error_outside_a_list_element_sets_nothing_aside() -> None:
    value = {"rankings": [_ok(1), {"id": 2}], "note": 7}
    cleaned, aside = await kinds.set_aside_invalid_list_elements(value, "k")
    assert cleaned is value and aside == []


@pytest.mark.asyncio
async def test_an_answer_still_wrong_once_cleaned_sets_nothing_aside() -> None:
    """Every element wrong: the empty list breaks minItems, so the whole answer fails as before."""
    value = {"rankings": [{"id": 1}, {"id": 2}]}
    cleaned, aside = await kinds.set_aside_invalid_list_elements(value, "k")
    assert cleaned is value and aside == []


@pytest.mark.asyncio
async def test_an_unchecked_kind_sets_nothing_aside(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _skip(value: Any, slug: str) -> kinds.KindCheck:
        return kinds.KindCheck(checked=False, degraded_reason=kinds.KindDegradedReason.KIND_NOT_REGISTERED)

    monkeypatch.setattr(kinds, "check_against_kind", _skip)
    value = {"rankings": [{"id": 1}]}
    assert await kinds.set_aside_invalid_list_elements(value, "k") == (value, [])
