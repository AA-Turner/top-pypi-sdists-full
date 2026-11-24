"""A processor rule's declared ``off.send`` goes INTO its processor, never raw onto the wire.

Live 2026-11-08 (system_error cd2ba4df, iOS chat, gemini-3.8-flash): the offering's
``reasoning_effort`` cell is a ``google_thinking`` processor with ``off: {send: "low"}``.
A thinking-off request (``thinking_budget=0`` or ``reasoning_effort="none"``) wrote
``reasoning_effort='low'`` straight into google-genai's ``GenerateContentConfig``, which
has no such field — a 400 on every such call. And the record's diagnosis named the wrong
settings ("suspect: automatic_continuation, max_output_tokens") although pydantic named
the refused field exactly. Both halves are pinned here.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from google.genai import types

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers import setting_rejection
from matrx_ai.providers.errors import classify_provider_error

CONSUMES = ["thinking_budget", "thinking_level", "include_thoughts", "reasoning_summary", "clear_thinking"]

# The live cells of offering cb1f1119 (gemini-3.8-flash), as compiled on 2026-11-08.
LIVE_FLASH_RULES = {
    "reasoning_effort": {
        "off": {"send": "low"},
        "default": "medium",
        "processor": "google_thinking",
        "supported": True,
        "ui_values": ["auto", "low", "medium", "high"],
        "processor_config": {
            "mode": "gemini_3",
            "order": 100,
            "family": "flash",
            "consumes": CONSUMES,
            "default_include_thoughts": True,
        },
    },
    "thinking_budget": {"supported": False},
    "include_thoughts": {"off": {"send": "false"}, "accepts": [True, False], "supported": True},
    "temperature": {},
}


def _controls() -> CompiledControlsMap:
    return CompiledControlsMap(
        rules={key: ControlRule.model_validate(rule) for key, rule in LIVE_FLASH_RULES.items()}
    )


@pytest.mark.parametrize(
    "canonical",
    [
        {"thinking_budget": 0},
        {"reasoning_effort": "none"},
        # "off" is the spoken "none": it must reach the cell's declared off, never
        # fall through to the provider's own default (no thinking_level sent).
        {"reasoning_effort": "off"},
        {"reasoning_effort": "OFF", "include_thoughts": False},
        {"thinking_budget": 0, "include_thoughts": False, "temperature": 0.1},
    ],
)
def test_off_send_reaches_the_processor_not_the_wire(canonical: dict) -> None:
    params, adjustments = _controls().outbound(dict(canonical))
    assert "reasoning_effort" not in params, params
    assert params["thinking_config"]["thinking_level"] == "low"
    # The adjusted value is still recorded (faithful mapping, never silent).
    assert any(a.action == "mapped" and a.sent_value == "low" for a in adjustments)
    # Exactly what the Google translator does with these params: it must validate.
    types.GenerateContentConfig(**params)


def test_off_send_on_a_plain_rule_still_writes_its_wire_key() -> None:
    controls = CompiledControlsMap(
        rules={"reasoning_effort": ControlRule.model_validate({"off": {"send": "minimal"}})}
    )
    params, _ = controls.outbound({"reasoning_effort": "none"})
    assert params == {"reasoning_effort": "minimal"}


@pytest.mark.parametrize(
    "canonical", [{"reasoning_effort": "none"}, {"reasoning_effort": "off"}, {"thinking_budget": 0}]
)
def test_an_off_value_send_keeps_its_wire_write(canonical: dict) -> None:
    # Live together offering c2e4a6b8: off sends effort "none", which IS an off value —
    # fed to the processor it would vanish and the model would reason at its default.
    rule = {
        "off": {"send": "none"},
        "accepts": ["minimal", "low", "medium", "high", "xhigh", "max"],
        "processor": "together_reasoning",
        "supported": True,
        "processor_config": {"order": 100, "consumes": CONSUMES, "effort_map": {"max": "max"}},
    }
    controls = CompiledControlsMap(rules={"reasoning_effort": ControlRule.model_validate(rule)})
    params, _ = controls.outbound(dict(canonical))
    assert params == {"reasoning_effort": "none"}


def _sdk_validation_error() -> Exception:
    try:
        types.GenerateContentConfig(reasoning_effort="low")
    except Exception as exc:  # noqa: BLE001
        return exc
    raise AssertionError("google-genai accepted a foreign key")


def test_classifier_names_the_field_pydantic_named() -> None:
    info = classify_provider_error("google", _sdk_validation_error())
    rejection = info.details["setting_rejection"]
    assert rejection["provider_param"] == "reasoning_effort"
    assert rejection["opaque"] is False
    assert rejection["shape"] == "unsupported"


def test_safety_net_reads_the_pydantic_field_instead_of_guessing() -> None:
    exc = _sdk_validation_error()
    info = SimpleNamespace(
        error_type="invalid_request",
        status_code=400,
        message=str(exc),
        user_message="",
        details={"message": str(exc), "provider": "unknown"},
    )
    candidate = setting_rejection.net_candidate(info)
    assert candidate is not None
    assert candidate.details["setting_rejection"]["provider_param"] == "reasoning_effort"
    assert candidate.details["setting_rejection"]["opaque"] is False


def test_pydantic_field_reader() -> None:
    assert setting_rejection.pydantic_field(str(_sdk_validation_error())) == "reasoning_effort"
    assert setting_rejection.pydantic_field("Request contains an invalid argument.") is None
