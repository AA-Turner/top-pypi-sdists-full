"""Run overrides carry THREE states per setting (settings-translation F-a).

Owner's words (GROUND-TRUTH): "the difference between something being set to
none and something not being included at all". A run override used to skip
every None, so a run could never return a stored setting to "not set":

* absent             -> inherit the stored value
* "none" / False     -> off (a real value, applied)
* explicit ``null``  -> unset: the stored key is removed, the model default applies
"""

from __future__ import annotations

from matrx_ai.config.llm_params import LLMParams, settle_layered_overrides
from matrx_ai.config.message_config import MessageList
from matrx_ai.config.unified_config import UnifiedConfig

MODEL = "572667d5-bc84-449c-800e-e89acd36b5f5"


def _stored() -> UnifiedConfig:
    """An agent that stored real settings."""
    return UnifiedConfig(
        model=MODEL,
        messages=MessageList(_messages=[]),
        reasoning_effort="high",
        temperature=0.3,
        include_thoughts=True,
        stop_sequences=["END"],
    )


def test_explicit_json_null_unsets_the_stored_key():
    cfg = _stored()
    cfg.apply_overrides(LLMParams.model_validate_json('{"reasoning_effort": null}'))
    assert cfg.reasoning_effort is None
    # Every other stored setting is untouched.
    assert cfg.temperature == 0.3
    assert cfg.include_thoughts is True
    assert cfg.stop_sequences == ["END"]


def test_absent_key_inherits_the_stored_value():
    cfg = _stored()
    cfg.apply_overrides(LLMParams.model_validate_json('{"temperature": 0.9}'))
    assert cfg.reasoning_effort == "high"
    assert cfg.temperature == 0.9


def test_a_default_none_field_never_masquerades_as_explicit():
    cfg = _stored()
    # Constructed in Python with no reasoning_effort: the field is None but unset.
    cfg.apply_overrides(LLMParams(temperature=0.5))
    assert cfg.reasoning_effort == "high"
    assert cfg.include_thoughts is True


def test_off_values_are_applied_not_unset():
    cfg = _stored()
    cfg.apply_overrides(
        LLMParams.model_validate_json('{"reasoning_effort": "none", "include_thoughts": false}')
    )
    assert cfg.reasoning_effort == "none"
    assert cfg.include_thoughts is False


def test_explicit_null_on_a_list_field_restores_its_declared_default():
    cfg = _stored()
    cfg.apply_overrides(LLMParams.model_validate_json('{"stop_sequences": null}'))
    assert cfg.stop_sequences == []  # its declared default_factory


def test_explicit_null_never_unsets_model_or_stream():
    cfg = _stored()
    cfg.stream = True
    cfg.apply_overrides(LLMParams.model_validate_json('{"model": null, "stream": null}'))
    assert cfg.model == MODEL
    assert cfg.stream is True


def test_a_layered_stack_drops_cancel_below_nulls_but_keeps_the_top_layers():
    merged = {"model": MODEL, "temperature": None, "reasoning_effort": None, "offering_id": None}
    assert settle_layered_overrides(merged) == {"model": MODEL, "offering_id": None}
    assert settle_layered_overrides(merged, keep_null={"reasoning_effort"}) == {
        "model": MODEL,
        "offering_id": None,
        "reasoning_effort": None,
    }
