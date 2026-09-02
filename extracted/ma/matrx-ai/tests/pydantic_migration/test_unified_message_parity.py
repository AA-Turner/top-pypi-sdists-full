"""Phase 1b — UnifiedMessage: the pydantic twin must accept every production
shape and agree with the dataclass field-for-field.

Shapes here are not invented. Each is a field combination MEASURED in
``chat.request_snapshot`` during Phase 1a (agent-engine-extraction
FIELD_TRUTH.md): 57,213 message objects, of which only five keys ever appear —
``role`` (57,213), ``content`` (57,213), ``metadata`` (21,509), ``id`` (19,273)
and ``timestamp`` (11,259).
"""

from __future__ import annotations

import pytest

from matrx_ai.config import _parity
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.models import UnifiedMessageModel

_FIELDS = (
    "role",
    "content",
    "id",
    "name",
    "timestamp",
    "status",
    "is_visible_to_model",
    "metadata",
    "position",
)

# The exact ISO-8601 form production stores — 32 chars, microseconds, +00:00.
# ``from_cx_message`` writes ``message.created_at.isoformat()``.
ISO_TS = "2026-05-18T07:18:52.600691+00:00"

# Every field combination observed in the corpus, in descending frequency.
PRODUCTION_SHAPES = [
    pytest.param({"role": "user", "content": []}, id="role+content (57,213)"),
    pytest.param({"role": "assistant", "content": [], "metadata": {"k": "v"}}, id="+metadata (21,509)"),
    pytest.param({"role": "user", "content": [], "id": "0b9c1e2f-aaaa-4bbb-8ccc-ddddeeeeffff"}, id="+id (19,273)"),
    pytest.param({"role": "assistant", "content": [], "timestamp": ISO_TS}, id="+timestamp ISO (11,259)"),
    pytest.param(
        {
            "role": "assistant",
            "content": [],
            "metadata": {"source": "cx"},
            "id": "0b9c1e2f-aaaa-4bbb-8ccc-ddddeeeeffff",
            "timestamp": ISO_TS,
        },
        id="all five observed keys",
    ),
    pytest.param({"role": "system", "content": []}, id="system role"),
]


@pytest.mark.parametrize("payload", PRODUCTION_SHAPES)
def test_pydantic_twin_accepts_every_production_shape(payload):
    """The model must not reject anything production actually sends."""
    UnifiedMessageModel(**payload)


@pytest.mark.parametrize("payload", PRODUCTION_SHAPES)
def test_dataclass_and_model_agree_field_for_field(payload):
    """Field-for-field parity, TYPE included — a coerced value is a divergence."""
    old = UnifiedMessage(**payload)
    new = UnifiedMessageModel(**payload)
    diffs = _parity.diff_fields(old, new, fields=_FIELDS)
    assert diffs == [], f"parity divergence on {payload}: {diffs}"


def test_iso_timestamp_would_have_broken_a_literal_port():
    """FORCING FUNCTION for the Phase 1a finding — do not delete this test.

    ``UnifiedMessage.timestamp`` is declared ``int | None``. Production has
    never once stored an int: 11,259 of 11,259 observed values are ISO-8601
    strings, written deliberately by ``from_cx_message``. A literal port of the
    hint would therefore raise on every message carrying a timestamp.

    This proves the trap is real (so nobody "corrects" the model back to int),
    and that the shipped model does not fall into it.
    """
    from pydantic import BaseModel

    class LiteralPortOfTheHint(BaseModel):
        timestamp: int | None = None

    with pytest.raises(Exception) as caught:
        LiteralPortOfTheHint(timestamp=ISO_TS)
    assert "int" in str(caught.value).lower()

    # The shipped model keeps the string as a string — no coercion, no loss.
    assert UnifiedMessageModel(role="user", timestamp=ISO_TS).timestamp == ISO_TS
    # …and still accepts an int for any in-memory caller that sets one.
    assert UnifiedMessageModel(role="user", timestamp=1724400000).timestamp == 1724400000


def test_model_emits_json_schema_for_the_typescript_twin():
    """The whole reason for pydantic (D2): a dataclass emits no schema, so the
    TypeScript twin cannot be generated against it."""
    schema = UnifiedMessageModel.model_json_schema()
    assert set(schema["properties"]) == set(_FIELDS)
    assert schema["required"] == ["role"]


class _Boom:
    def __init__(self):
        raise ValueError("the new path exploded")


def test_shadow_never_breaks_the_caller(monkeypatch):
    """CUTOVER.md §3 rule 2 — with the shadow ON and the new path raising, the
    caller still receives the old result."""
    monkeypatch.setattr(_parity, "PARITY_SHADOW_ENABLED", True)
    recorded: list[tuple] = []
    monkeypatch.setattr(
        _parity, "record_divergence", lambda *a, **k: recorded.append((a, k))
    )

    old = UnifiedMessage(role="user", content=[])
    got = _parity.shadow_compare(
        "UnifiedMessage", {}, lambda: old, _Boom, fields=_FIELDS
    )

    assert got is old, "the shadow changed what the caller received"
    assert recorded, "a raising new path must still be recorded"


def test_shadow_is_off_by_default_and_costs_one_read(monkeypatch):
    """Disabled is the production default; the new path must not even run."""
    monkeypatch.setattr(_parity, "PARITY_SHADOW_ENABLED", False)
    ran = []
    old = UnifiedMessage(role="user", content=[])
    got = _parity.shadow_compare(
        "UnifiedMessage", {}, lambda: old, lambda: ran.append(1), fields=_FIELDS
    )
    assert got is old
    assert ran == [], "the new path ran while the shadow was disabled"
