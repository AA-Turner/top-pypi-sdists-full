"""Parity: UnifiedResponse (dataclass) vs UnifiedResponseModel (pydantic).

Phase 1b.2 of agent-engine-extraction. The dataclass is still authoritative;
these tests are what has to stay true before the twin can be shadowed on real
traffic, and then flipped.

The corpus behind the numbers quoted here is chat.request_snapshot's
response_payload column — 5,473 rows, which is UnifiedResponse.to_dict() as it
actually reached production. See config/models/response.py for the breakdown.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import pytest

from matrx_ai.config.finish_reason import FinishReason
from matrx_ai.config.models.response import UnifiedResponseModel
from matrx_ai.config.unified_config import UnifiedResponse


@dataclass
class _Usage:
    """Stand-in for TokenUsage: a dataclass with a to_dict, like the real one's
    siblings. TokenUsage itself has NO to_dict — asserted below."""

    input_tokens: int = 1
    output_tokens: int = 2

    def to_dict(self) -> dict:
        return {"input_tokens": self.input_tokens, "output_tokens": self.output_tokens}


class _Msg:
    def __init__(self, text: str) -> None:
        self.text = text

    def to_dict(self) -> dict:
        return {"role": "assistant", "text": self.text}


def _both(**kwargs):
    return UnifiedResponse(**kwargs), UnifiedResponseModel(**kwargs)


# ── the field set itself ──────────────────────────────────────────────────────


def test_the_two_shapes_declare_exactly_the_same_fields_in_the_same_order():
    import dataclasses

    old = [f.name for f in dataclasses.fields(UnifiedResponse)]
    new = list(UnifiedResponseModel.model_fields)
    # Order matters: to_dict() walks __dict__, so it is the key order of every
    # persisted snapshot row.
    assert old == new


def test_messages_is_required_on_both():
    with pytest.raises(TypeError):
        UnifiedResponse()
    with pytest.raises(Exception):
        UnifiedResponseModel()


# ── to_dict: the None-drop is the encoding, not an optimisation ───────────────


@pytest.mark.parametrize(
    "kwargs",
    [
        # The five structural cases the corpus actually contains, in order of
        # frequency: 4,523 / 691 / 245 / 12 / 2.
        {"messages": [_Msg("a")], "finish_reason": "stop", "raw_response": {"id": "r"}, "usage": _Usage()},
        {"messages": [_Msg("a")], "finish_reason": "stop", "stop_reason": "stop", "raw_response": {"id": "r"}, "usage": _Usage()},
        {"messages": [_Msg("a")], "usage": _Usage()},
        {"messages": [_Msg("a")], "finish_reason": "tool_calls", "stop_reason": "tool_calls", "usage": _Usage()},
        {"messages": [_Msg("a")], "finish_reason": "stop", "stop_reason": "stop"},
    ],
)
def test_to_dict_is_identical_across_the_five_corpus_cases(kwargs):
    old, new = _both(**kwargs)
    assert old.to_dict() == new.to_dict()
    # And identical once serialised — key order included.
    assert json.dumps(old.to_dict(), default=str) == json.dumps(new.to_dict(), default=str)


def test_none_is_dropped_but_an_empty_dict_is_kept():
    # 705 of 5,473 rows carry stop_reason; the other 4,768 OMIT the key rather
    # than storing null. metadata, by contrast, is present as {} in all 5,473 —
    # so this is exclude_none, never exclude_defaults.
    old, new = _both(messages=[_Msg("a")])
    for d in (old.to_dict(), new.to_dict()):
        assert "stop_reason" not in d
        assert "finish_reason" not in d
        assert "usage" not in d
        assert d["metadata"] == {}


def test_the_list_branch_quirk_is_reproduced_not_quietly_fixed():
    # to_dict tests only value[0]. A list whose first element has no to_dict
    # passes through RAW even though later elements have one. That is the
    # dataclass's behaviour; the twin must not silently improve on it, because
    # a shadow-compare would then report a divergence that is really a fix.
    mixed = ["plain", _Msg("b")]
    old, new = _both(messages=mixed)
    assert old.to_dict()["messages"] == new.to_dict()["messages"] == mixed


def test_empty_message_list_survives_as_an_empty_list():
    # executor.py builds UnifiedResponse(messages=[]) on eight interrupt and
    # synthetic paths. None of them reach a snapshot, so the corpus cannot
    # speak for them — the code does.
    old, new = _both(messages=[])
    assert old.to_dict()["messages"] == new.to_dict()["messages"] == []


# ── forcing functions: the two declared types that are FALSE ──────────────────


def test_raw_response_holds_provider_sdk_objects_not_dicts():
    """UnifiedResponse declares ``raw_response: dict[str, Any] | None``.

    from_openai takes an OpenAIResponse; groq/cerebras/together take Any; each
    passes that SDK object straight through. A literal port of the declaration
    rejects nearly every real provider response. This test fails the moment
    someone narrows the twin's annotation to dict.
    """

    class SdkResponse:  # not a dict, not a mapping, not a pydantic model
        id = "resp_123"

    sdk = SdkResponse()
    old, new = _both(messages=[_Msg("a")], raw_response=sdk)
    assert old.raw_response is sdk
    assert new.raw_response is sdk, "the twin must accept an SDK object verbatim"

    # And prove the narrowed version really would have rejected it.
    from typing import Any as _Any

    from pydantic import BaseModel, ConfigDict

    class Narrowed(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
        raw_response: dict[str, _Any] | None = None

    with pytest.raises(Exception):
        Narrowed(raw_response=sdk)


def test_a_str_enum_finish_reason_survives_every_consumer_it_meets():
    """Providers pass FinishReason (a StrEnum), not str.

    Pydantic silently downgrades it to a plain str on a ``str | None`` field.
    That is SAFE here — but only because of two facts that a future change
    could break, so both are pinned:
      1. StrEnum.__str__ is str.__str__, so executor.py's six str(...) call
         sites format identically.
      2. recovery_logic.handle_finish_reason re-parses through
         FinishReason(...), and isinstance(FinishReason.X, str) is already True,
         so it took that branch even before the migration.
    Turn FinishReason into a plain Enum and this test fails loudly.
    """
    old, new = _both(messages=[_Msg("a")], finish_reason=FinishReason.TOOL_CALLS)

    assert isinstance(FinishReason.TOOL_CALLS, str), "FinishReason must stay a StrEnum"
    assert str(old.finish_reason) == str(new.finish_reason) == "tool_calls"
    assert old.finish_reason == new.finish_reason == "tool_calls"
    assert FinishReason(old.finish_reason) is FinishReason(new.finish_reason)
    # The persisted form is what actually has to match, and it does.
    assert old.to_dict()["finish_reason"] == new.to_dict()["finish_reason"]
    # Every finish_reason the corpus has ever held is a valid member.
    for observed in ("stop", "tool_calls", "max_tokens"):
        assert FinishReason(observed)


def test_token_usage_still_has_no_to_dict():
    """to_dict()'s ``hasattr(value, "to_dict")`` branch decides how usage is
    serialised. TokenUsage has none, so usage falls to the else branch and is
    stored as the object itself — which is why the snapshot writer, not this
    method, is what turns it into JSON. Give TokenUsage a to_dict and the
    persisted shape changes; this test is the tripwire."""
    from matrx_ai.config.usage_config import TokenUsage

    assert not hasattr(TokenUsage, "to_dict")


# ── construction-time behaviour ───────────────────────────────────────────────


def test_missing_usage_warns_on_both(caplog):
    # Fired twice in production (2 rows with no usage key). It is the only
    # signal that a paid call recorded no cost. vcprint routes through logging,
    # so this reads the log rather than stdout.
    with caplog.at_level("WARNING"):
        UnifiedResponse(messages=[_Msg("a")])
        old = [r for r in caplog.records if "missing usage data" in r.getMessage()]
        caplog.clear()
        UnifiedResponseModel(messages=[_Msg("a")])
        new = [r for r in caplog.records if "missing usage data" in r.getMessage()]

    assert len(old) == len(new) == 1
    assert old[0].getMessage() == new[0].getMessage()
    assert old[0].levelno == new[0].levelno == 30


def test_usage_present_warns_on_neither(caplog):
    with caplog.at_level("ERROR"):
        UnifiedResponse(messages=[_Msg("a")], usage=_Usage())
        UnifiedResponseModel(messages=[_Msg("a")], usage=_Usage())
    assert not [r for r in caplog.records if "missing usage data" in r.getMessage()]


def test_both_refuse_an_unknown_field():
    # The dataclass raises TypeError; the model raises ValidationError. Both
    # refuse, which is what parity means here — extra="forbid" is the faithful
    # port on this type, not a tightening.
    with pytest.raises(TypeError):
        UnifiedResponse(messages=[], nonsense=1)
    with pytest.raises(Exception):
        UnifiedResponseModel(messages=[], nonsense=1)


def test_usage_can_still_be_assigned_after_construction():
    # providers/anthropic/anthropic_api.py:253 and :311 do exactly this once
    # the accumulated streaming usage is known.
    usage = _Usage()
    for obj in (UnifiedResponse(messages=[_Msg("a")], usage=_Usage()),
                UnifiedResponseModel(messages=[_Msg("a")], usage=_Usage())):
        obj.usage = usage
        assert obj.usage is usage


# ── the reason the twin exists at all ─────────────────────────────────────────


def test_model_emits_json_schema_for_the_typescript_twin():
    schema = UnifiedResponseModel.model_json_schema()
    assert set(schema["properties"]) == set(UnifiedResponseModel.model_fields)
    assert schema["required"] == ["messages"]
    # The staged fields emit NO type constraint, which is the honest projection
    # (TypeScript `any`) until their own types are migrated. When usage or
    # raw_response is narrowed, this is what tells the TypeScript generator's
    # owner that the emitted shape changed.
    for staged in ("usage", "raw_response"):
        prop = schema["properties"][staged]
        assert "type" not in prop and "$ref" not in prop and "anyOf" not in prop, (
            f"{staged} gained a type constraint: {prop}"
        )

    # The fields the corpus DID let us type are typed, and nullable.
    for typed in ("stop_reason", "finish_reason"):
        assert schema["properties"][typed]["anyOf"] == [{"type": "string"}, {"type": "null"}]
    assert schema["properties"]["metadata"]["type"] == "object"
    assert schema["properties"]["messages"]["type"] == "array"
