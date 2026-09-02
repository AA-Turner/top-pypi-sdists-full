"""S1 for Retirement Ledger rows 2 and 3 — UnifiedMessage and UnifiedResponse.

The content twins (rows 4 and 5) reached S1 by replaying stored BLOCKS through
the ONE deserializer. These two cannot advance that way and the difference is
the point: `UnifiedMessage` and `UnifiedResponse` are CONSTRUCTED — a message
from a stored row or an API dict, a response by eleven provider translators —
so their corpus is the row shape and the emitted shape, not a stored block.

  * `UnifiedMessage` — all 19 distinct (role, status, has_metadata,
    is_visible_to_model) combinations in `chat.message`, 102,461 rows
    (fixtures/message_shapes.json). Replayed through `from_dict`, the
    deserialization funnel.
  * `UnifiedResponse` — the five structural cases in
    `chat.request_snapshot.response_payload`, 5,473 rows (CORPUS.md §3b).
    Compared on `to_dict()`, because that IS the persisted artifact.

Both fixtures carry shapes and never values, per CORPUS.md §7.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib

import pytest

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.models.message import UnifiedMessageModel
from matrx_ai.config.models.response import UnifiedResponseModel
from matrx_ai.config.unified_config import UnifiedResponse

MSG = json.loads(
    (pathlib.Path(__file__).parent / "fixtures" / "message_shapes.json").read_text()
)


def _msg_id(case: dict) -> str:
    return f"{case['role']}/{case['status']}/meta={int(case['has_metadata'])}/vis={int(case['is_visible_to_model'])}"


@pytest.mark.parametrize("case", MSG["cases"], ids=_msg_id)
def test_every_stored_message_shape_round_trips_into_the_twin(case):
    row = {
        "role": case["role"],
        "content": [{"type": "text", "text": "x"}],
        "id": "m-1",
        # ISO-8601 STRING — the Phase 1a finding. 11,259 of 11,259 stored
        # timestamps are strings against a declared `int | None`.
        "timestamp": "2026-08-24T00:00:00+00:00",
        "status": case["status"],
        "metadata": {"k": "v"} if case["has_metadata"] else {},
        "position": 3,
    }
    old = UnifiedMessage.from_dict(row)
    values = {f.name: getattr(old, f.name) for f in dataclasses.fields(old)}
    new = UnifiedMessageModel(**values)

    for name, expected in values.items():
        assert getattr(new, name) == expected, name
        assert type(getattr(new, name)) is type(expected), (
            f"{name} changed TYPE: {type(expected).__name__} -> "
            f"{type(getattr(new, name)).__name__}"
        )


def test_from_dict_ignores_is_visible_to_model_and_that_is_recorded():
    """`from_cx_message` reads is_visible_to_model; `from_dict` does not, so an
    API caller cannot set it and always gets the default. 346 stored rows have
    it False. Not a defect of the twin — an asymmetry between the two
    constructors that the flip must not silently change, so it is pinned."""
    row = {"role": "assistant", "content": [], "is_visible_to_model": False}
    assert UnifiedMessage.from_dict(row).is_visible_to_model is True
    assert UnifiedMessageModel(role="assistant", is_visible_to_model=False).is_visible_to_model is False


def test_the_message_fixture_covers_what_it_claims():
    assert MSG["_distinct_cases"] == len(MSG["cases"]) == 19
    assert MSG["_total_rows"] == sum(c["rows"] for c in MSG["cases"])
    assert {c["role"] for c in MSG["cases"]} == set(MSG["_invariants"]["roles"])
    assert {c["status"] for c in MSG["cases"]} == set(MSG["_invariants"]["statuses"])


# ── UnifiedResponse: the five structural cases, compared on to_dict() ─────────

class _Usage:
    def to_dict(self) -> dict:
        return {"input_tokens": 1, "output_tokens": 2}


class _Msg:
    def to_dict(self) -> dict:
        return {"role": "assistant", "text": "x"}


# (finish_reason, stop_reason, raw_response, usage) exactly as CORPUS.md §3b
# found them, with the block counts behind each.
RESPONSE_CASES = [
    ("stop", None, {"id": "r"}, True, 4523),
    ("stop", "stop", {"id": "r"}, True, 691),
    (None, None, None, True, 245),
    ("tool_calls", "tool_calls", None, True, 12),
    ("stop", "stop", None, False, 2),
]


@pytest.mark.parametrize(
    "finish,stop,raw,has_usage,rows", RESPONSE_CASES,
    ids=[f"finish={f}/stop={s}/raw={bool(r)}/usage={u}[{n}]" for f, s, r, u, n in RESPONSE_CASES],
)
def test_every_response_shape_serialises_identically(finish, stop, raw, has_usage, rows):
    kwargs = {"messages": [_Msg()]}
    if finish is not None:
        kwargs["finish_reason"] = finish
    if stop is not None:
        kwargs["stop_reason"] = stop
    if raw is not None:
        kwargs["raw_response"] = raw
    if has_usage:
        kwargs["usage"] = _Usage()

    old = UnifiedResponse(**kwargs)
    new = UnifiedResponseModel(**kwargs)

    assert old.to_dict() == new.to_dict()
    # Key ORDER too — to_dict walks __dict__, so this is the persisted key order.
    assert list(old.to_dict()) == list(new.to_dict())
    assert json.dumps(old.to_dict(), default=str) == json.dumps(new.to_dict(), default=str)


def test_the_response_cases_account_for_the_measured_corpus():
    assert sum(n for *_, n in RESPONSE_CASES) == 5473
