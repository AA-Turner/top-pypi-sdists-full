"""The pick contract's model and its three functions, against the fixture TypeScript reads too.

Contract: common-docs/systems/data/scopes-context/projects/any-table-context/CONTRACT.md §1, §2, step 2.
The fixture is the one source of cases for both twins; a case changed here changes the TS twin's.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from matrx_connect.context.context_picks import (
    ContextPick,
    LegacySelection,
    canonical_picks,
    fold_legacy_selection,
    legacy_selection,
)

_FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "context_picks_cases.json").read_text())
CASES = _FIXTURE["cases"]
REFUSED = _FIXTURE["refused"]


def _json(picks: list[ContextPick]) -> list[dict]:
    return [p.model_dump(mode="json") for p in picks]


def _legacy_json(legacy: LegacySelection) -> dict:
    return {
        "scope_ids": legacy.scope_ids,
        "active_scope_type_ids": legacy.active_scope_type_ids,
        "built_in": _json(legacy.built_in),
    }


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_each_case_folds_to_its_recorded_canonical_picks(case: dict) -> None:
    picks = fold_legacy_selection(case["scope_ids"], case["active_scope_type_ids"], case["picks"])
    assert _json(picks) == case["canonical"]


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_each_case_reads_back_to_its_recorded_legacy_fields(case: dict) -> None:
    canonical = [ContextPick.model_validate(p) for p in case["canonical"]]
    assert _legacy_json(legacy_selection(canonical)) == case["legacy"]


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_canonical_is_a_fixed_point(case: dict) -> None:
    once = canonical_picks(case["canonical"])
    assert _json(canonical_picks(once)) == _json(once) == case["canonical"]


def test_a_legacy_body_round_trips_identically() -> None:
    round_trips = [c for c in CASES if c["round_trip"]]
    assert round_trips, "the fixture lost its round-trip cases"
    for case in round_trips:
        back = legacy_selection(
            fold_legacy_selection(case["scope_ids"], case["active_scope_type_ids"])
        )
        assert (back.scope_ids, back.active_scope_type_ids) == (
            case["scope_ids"],
            case["active_scope_type_ids"],
        )


def test_a_built_in_pick_never_lands_in_the_old_scope_ids() -> None:
    seen = 0
    for case in CASES:
        canonical = [ContextPick.model_validate(p) for p in case["canonical"]]
        legacy = legacy_selection(canonical)
        built_in_ids = {
            str(r) for p in canonical if (p.table or "").startswith("entity:") for r in p.record_ids
        }
        seen += len(built_in_ids)
        assert not built_in_ids & set(legacy.scope_ids), case["name"]
        assert all((p.table or "").startswith("entity:") for p in legacy.built_in), case["name"]
    assert seen, "the fixture lost its built-in record picks"


def test_a_folded_pick_is_absorbed_by_a_filled_one_whichever_comes_first() -> None:
    case = next(c for c in CASES if c["name"].startswith("a folded pick is absorbed"))
    folded_first = canonical_picks(
        fold_legacy_selection(case["scope_ids"], case["active_scope_type_ids"])
        + [ContextPick.model_validate(p) for p in case["picks"]]
    )
    assert {json.dumps(p, sort_keys=True) for p in _json(folded_first)} == {
        json.dumps(p, sort_keys=True) for p in case["canonical"]
    }


@pytest.mark.parametrize("case", REFUSED, ids=[c["name"] for c in REFUSED])
def test_a_malformed_pick_is_refused(case: dict) -> None:
    with pytest.raises(ValidationError):
        ContextPick.model_validate(case["pick"])


def test_a_malformed_legacy_id_is_skipped_never_raised() -> None:
    assert fold_legacy_selection(["nope", None, 7], ["Clients"]) == []  # type: ignore[list-item]
    assert fold_legacy_selection(None, None, None) == []


def test_a_pick_is_frozen() -> None:
    pick = ContextPick.model_validate({"organization_id": None, "table": "entity:party"})
    with pytest.raises(ValidationError):
        pick.table = "entity:task"  # type: ignore[misc]


@pytest.mark.parametrize(
    "pick",
    [
        {"organization_id": "0a000000-0000-4000-8000-000000000001", "table": None, "fields": ["a"]},
        {"organization_id": None, "table": None},
        {
            "organization_id": "0a000000-0000-4000-8000-000000000001",
            "table": None,
            "record_ids": ["1e000000-0000-4000-8000-000000000001"],
        },
    ],
    ids=[
        "an organization with no table",
        "nothing at all",
        "a legacy record id with an organization",
    ],
)
def test_a_tableless_pick_is_only_a_folded_record_pick(pick: dict) -> None:
    """table=None means "folded from legacy scope_ids": no organization, at least one record. Anything
    else would be dropped silently by canonical_picks, so the model refuses it."""
    with pytest.raises(ValidationError):
        ContextPick.model_validate(pick)


def test_every_folded_record_pick_merges_into_one_in_first_seen_place() -> None:
    a, b, c = (f"1e000000-0000-4000-8000-00000000000{i}" for i in (1, 2, 3))
    table = "7a000000-0000-4000-8000-000000000001"
    org = "0a000000-0000-4000-8000-000000000001"
    picks = canonical_picks(
        [
            {"organization_id": None, "table": None, "record_ids": [a]},
            {"organization_id": org, "table": table},
            {"organization_id": None, "table": None, "record_ids": [b, a]},
            {"organization_id": None, "table": None, "record_ids": [c], "fields": ["f"]},
        ]
    )
    assert _json(picks) == [
        {
            "organization_id": None,
            "table": None,
            "view": None,
            "record_ids": [a, b, c],
            "fields": ["f"],
        },
        {"organization_id": org, "table": table, "view": None, "record_ids": [], "fields": []},
    ]
