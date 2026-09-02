"""Parity for `UnifiedConfig` — the last and largest contract type.

Phase 1b.2, Retirement Ledger row 9. 90 fields, 99 construction sites.

The twin was GENERATED from the dataclass rather than hand-written, because
FIELD_TRUTH §4d verified 56 of 57 declared types against 6,485 stored configs —
with the annotations trustworthy, hand-typing 90 fields adds transcription risk
and no information. This suite is what makes that safe: it asserts names, ORDER,
defaults and RESOLVED ANNOTATIONS field by field, so a generator bug fails here
rather than at a flip.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from matrx_ai.config.models.unified import UnifiedConfigModel
from matrx_ai.config.unified_config import UnifiedConfig

REQUIRED = {"model": "gpt-4o", "messages": []}
# Held as `Any` in the twin because the type they carry is not migrated — or,
# for MessageList, may never be a contract type. PLAN.md § The last three siblings.
STAGED = {"messages", "system_instruction"}


def test_same_fields_in_the_same_order():
    assert [f.name for f in dataclasses.fields(UnifiedConfig)] == list(UnifiedConfigModel.model_fields)


def test_field_count_is_ninety():
    assert len(UnifiedConfigModel.model_fields) == 90


def test_annotations_are_identical_except_the_staged_two():
    """The guard that replaces hand-transcription care. A `str | None` emitted
    as `str` would pass a names-and-defaults check and then reject a real null
    on 6,485 rows' worth of traffic."""
    old, new = typing.get_type_hints(UnifiedConfig), typing.get_type_hints(UnifiedConfigModel)
    for name in UnifiedConfigModel.model_fields:
        if name in STAGED:
            continue
        assert new[name] == old[name], f"{name}: {new[name]} != {old[name]}"


# Fields that `__post_init__` NORMALISES away from their declared default. The
# twin has the fields and NOT the constructor, so these five diverge by design —
# see test_post_init_is_not_replicated_and_that_blocks_the_flip.
POST_INIT_NORMALISED = {
    "messages", "authored_tools", "dynamic_tools",
    "authored_custom_tools", "authored_mcp_servers",
}


def test_defaults_match():
    built = UnifiedConfigModel(**REQUIRED)
    old = UnifiedConfig(**REQUIRED)
    for f in dataclasses.fields(UnifiedConfig):
        if f.name in STAGED or f.name in POST_INIT_NORMALISED:
            continue
        if f.default is not dataclasses.MISSING:
            expected = f.default
        elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
            expected = f.default_factory()  # type: ignore[misc]
        else:
            continue
        assert getattr(built, f.name) == expected == getattr(old, f.name), f.name


def test_only_model_and_messages_are_required():
    assert UnifiedConfigModel.model_json_schema()["required"] == ["model", "messages"]
    with pytest.raises(Exception):
        UnifiedConfigModel()


# ── the storage-shape trap ────────────────────────────────────────────────────


def test_unrecognized_keys_survives_into_to_dict():
    """🚨 The one thing generation could not carry. 4,178 of 6,485 stored
    configs hold this key; a pydantic `__dict__` would not, and a PrivateAttr is
    excluded from model_dump(). to_dict() re-includes it explicitly."""
    twin = UnifiedConfigModel(**REQUIRED)
    twin._unrecognized_keys = ["multi_speaker", "variables"]

    out = twin.to_dict()
    assert out["_unrecognized_keys"] == ["multi_speaker", "variables"]

    # And the dataclass agrees on the same input.
    old = UnifiedConfig.from_dict({"model": "gpt-4o", "multi_speaker": True})
    assert "_unrecognized_keys" in old.to_dict()


def test_the_naive_port_would_have_dropped_it():
    """Falsification: without the explicit re-inclusion, the key vanishes and
    nothing raises. This is why the twin does not simply copy the __dict__
    walk."""
    twin = UnifiedConfigModel(**REQUIRED)
    twin._unrecognized_keys = ["multi_speaker"]
    naive = {k: v for k, v in twin.__dict__.items() if v is not None}
    assert "_unrecognized_keys" not in naive
    assert "_unrecognized_keys" not in twin.model_dump()


def test_empty_unrecognized_keys_adds_no_key():
    """Sparse, like every other to_dict in this contract."""
    assert "_unrecognized_keys" not in UnifiedConfigModel(**REQUIRED).to_dict()


# ── the encoding the whole corpus rests on ────────────────────────────────────


def test_none_is_dropped_and_an_empty_dict_is_kept():
    out = UnifiedConfigModel(**REQUIRED).to_dict()
    assert all(v is not None for v in out.values())
    assert out.get("metadata") == {}


def test_extra_is_allow_not_forbid_and_that_is_deliberate():
    """FIELD_TRUTH §5/§6: 14 undeclared caller keys arrive on 4.24% of live
    requests across 23 models. Forbidding on day one breaks them. allow →
    record → triage → forbid, behind its own S0→S4."""
    assert UnifiedConfigModel.model_config["extra"] == "allow"
    twin = UnifiedConfigModel(**REQUIRED, multi_speaker=True)
    assert twin.multi_speaker is True


def test_tts_voice_stays_polymorphic():
    """array 117 / string 5 — the sole polymorphic config field, and the hint
    IS honest: the array elements are objects, not strings.

    Recorded because I got this wrong first: I asserted `["nova", "echo"]` and
    the model correctly rejected it. The corpus shows
    `[{"name": "Sam", "voice": "iapetus"}, ...]`, exactly matching the declared
    `list[dict[str, str]]`. FIELD_TRUTH §4 already said the hint was honest —
    the measurement was right and my assumption was not.
    """
    assert UnifiedConfigModel(**REQUIRED, tts_voice="kore").tts_voice == "kore"
    cast = [{"name": "Sam", "voice": "iapetus"}, {"name": "Tara", "voice": "laomedeia"}]
    assert UnifiedConfigModel(**REQUIRED, tts_voice=cast).tts_voice == cast

    with pytest.raises(Exception):
        UnifiedConfigModel(**REQUIRED, tts_voice=["nova", "echo"])


def test_post_init_is_not_replicated_and_that_blocks_the_flip():
    """🚨 THE REAL STATE OF THIS TWIN, asserted rather than described.

    `UnifiedConfig.__post_init__` is ~60 lines of business logic, not
    normalisation trivia: it defaults `authored_tools` from `tools`, derives
    `dynamic_tools` with filter-aware rules, and REHYDRATES `custom_tools` and
    `mcp_servers` from their authored counterparts on an unfiltered reload —
    changing what the config CONTAINS. It also calls `MessageList.sanitize()`,
    `_resolve_message_patterns()` and `_normalize_system_instruction()`.

    The generated twin has the 90 fields and none of that, so exactly five
    fields diverge on construction. Porting the constructor is BLOCKED, not
    merely pending: three of its steps run through `MessageList` and
    `SystemInstruction`, whose contract status is an open decision
    (PLAN.md § The last three siblings). Deciding those unblocks this.

    This test is the honest marker. It fails the moment someone ports
    __post_init__, which is the point — the row cannot look ready while the
    constructor is missing.
    """
    old, new = UnifiedConfig(**REQUIRED), UnifiedConfigModel(**REQUIRED)

    assert type(old.messages).__name__ == "MessageList"
    assert new.messages == []          # the twin keeps the raw list

    for name in ("authored_tools", "dynamic_tools", "authored_custom_tools", "authored_mcp_servers"):
        assert getattr(old, name) == [], f"{name}: __post_init__ stopped normalising"
        assert getattr(new, name) is None, f"{name}: the twin gained constructor logic"
