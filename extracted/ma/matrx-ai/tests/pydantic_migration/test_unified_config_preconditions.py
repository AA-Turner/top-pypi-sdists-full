"""Preconditions for the `UnifiedConfig` twin — measured BEFORE writing it.

Phase 1b.2's last and largest type: 91 fields, 99 construction sites, 35
`replace`/`fields`/`asdict` call sites. This file exists because the measurement
that should govern that twin is worth pinning before the transcription, not
after — three of the four earlier shapes hid a declared type that was false, and
finding out during a 90-field port is the expensive way.

WHAT THE CORPUS SAID (6,485 stored `unified_payload->'config'` objects):

  * **56 of 57 observed keys agree with their declared type.** `UnifiedConfig`
    is markedly more honest than `UnifiedMessage`, `UnifiedResponse` or
    `ToolResultContent`, each of which lied. Worth recording as a negative
    result: the annotations here can largely be trusted.
  * **Zero explicit nulls**, confirming FIELD_TRUTH §2 at the config level
    specifically. (The REQUEST WRAPPER around it is a different story —
    `created_by` and `status` are explicitly null in all 6,485 rows — which is
    why §2's scope note matters.)
  * `tts_voice` is the one polymorphic field (`array` 117 / `string` 5), and its
    declared type already says so.
  * 33 declared fields have never been populated at all.

THE ONE MISMATCH IS THE DANGEROUS ONE, and it is what this file pins.
"""

from __future__ import annotations

import dataclasses

from matrx_ai.config.unified_config import UnifiedConfig


def test_unrecognized_keys_is_not_a_declared_field():
    """It is set by post-construction setattr in `from_dict` (line ~722),
    which a dataclass permits and which lands the value in `__dict__`."""
    assert "_unrecognized_keys" not in {f.name for f in dataclasses.fields(UnifiedConfig)}


def test_unrecognized_keys_reaches_to_dict_and_therefore_storage():
    """🚨 THE PRECONDITION THE TWIN MUST MEET.

    `to_dict()` walks `self.__dict__`, so the dynamically-set attribute is
    serialised — which is why the key is present in 4,178 of 6,485 stored
    config payloads.

    A pydantic model's `__dict__` holds only DECLARED FIELDS; a private attr
    lives in `__pydantic_private__` and is excluded from `model_dump()`. So a
    twin that models this as a bare `PrivateAttr` and copies the `__dict__`
    walk will silently stop persisting a key that 4,178 production rows carry.
    Nothing would raise. The twin must re-include it explicitly.
    """
    cfg = UnifiedConfig.from_dict({"model": "gpt-4o", "multi_speaker": True})

    assert cfg._unrecognized_keys, "from_dict stopped recording unrecognized keys"
    assert "multi_speaker" in cfg._unrecognized_keys
    assert "_unrecognized_keys" in cfg.__dict__

    serialized = cfg.to_dict()
    assert "_unrecognized_keys" in serialized, (
        "to_dict no longer carries _unrecognized_keys — the storage shape changed"
    )
    assert "multi_speaker" in serialized["_unrecognized_keys"]


def test_a_known_passthrough_key_is_recorded_without_warning():
    """`multi_speaker` is one of the 14 caller keys measured as silently
    dropped (FIELD_TRUTH §5). It is recorded here rather than lost — the
    warning is suppressed for known passthroughs, the RECORDING is not."""
    from matrx_ai.config.unified_config import _KNOWN_PASSTHROUGH_KEYS

    assert "multi_speaker" in _KNOWN_PASSTHROUGH_KEYS
    cfg = UnifiedConfig.from_dict({"model": "m", "multi_speaker": True})
    assert "multi_speaker" in cfg._unrecognized_keys


def test_to_dict_drops_none_exactly_as_the_other_shapes_do():
    """Same encoding as UnifiedResponse: absence IS None, and an empty dict is
    KEPT. This is why the corpus shows zero explicit nulls at config level."""
    cfg = UnifiedConfig.from_dict({"model": "m"})
    out = cfg.to_dict()
    assert all(v is not None for v in out.values())
    assert out.get("metadata") == {}


def test_the_declared_field_count_the_plan_rests_on():
    """91 declared, 57 ever populated. If either moves, the plan's Phase 1b.2
    sizing moves with it."""
    assert len(dataclasses.fields(UnifiedConfig)) == 91
