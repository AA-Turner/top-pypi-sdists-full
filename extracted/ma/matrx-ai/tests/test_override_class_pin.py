"""A class pin (offering_id) follows its model through run overrides.

Live case (2026-10-01): an agent pinned to Matrx Lightning for Qwen3.8 27B
gets a run override to another model. The old pin belongs to Qwen, so leaving
it in place made the run raise; and a run that clears the pin had no way to say
so, because overrides skip None values."""

from __future__ import annotations

from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.message_config import MessageList
from matrx_ai.config.unified_config import UnifiedConfig

QWEN = "572667d5-bc84-449c-800e-e89acd36b5f5"
LIGHTNING = "29874e67-5683-40c2-9adb-fb797ea9a176"
OTHER_MODEL = "11111111-1111-4111-8111-111111111111"
OTHER_PIN = "22222222-2222-4222-8222-222222222222"


def _pinned() -> UnifiedConfig:
    return UnifiedConfig(model=QWEN, messages=MessageList(_messages=[]), offering_id=LIGHTNING)


def test_model_override_without_class_drops_the_old_models_pin():
    cfg = _pinned()
    cfg.apply_overrides(LLMParams(model=OTHER_MODEL))
    assert cfg.model == OTHER_MODEL
    assert cfg.offering_id is None


def test_model_override_with_class_takes_that_class():
    cfg = _pinned()
    cfg.apply_overrides(LLMParams(model=OTHER_MODEL, offering_id=OTHER_PIN))
    assert cfg.offering_id == OTHER_PIN


def test_explicit_null_class_clears_the_pin():
    cfg = _pinned()
    cfg.apply_overrides(LLMParams.model_validate({"offering_id": None}))
    assert cfg.offering_id is None


def test_unrelated_override_keeps_the_pin():
    cfg = _pinned()
    cfg.apply_overrides(LLMParams(temperature=0.2))
    assert cfg.offering_id == LIGHTNING


def test_same_model_override_keeps_the_pin():
    cfg = _pinned()
    cfg.apply_overrides(LLMParams(model=QWEN))
    assert cfg.offering_id == LIGHTNING
