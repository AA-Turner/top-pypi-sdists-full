"""Guard (2026-09-10): an offering's ``supported: false`` beats the API's
processor rule. Before this, the anthropic_chat API's ``temperature``
processor ran for the Claude 5 offerings whose override said
``supported: false``, ``temperature`` went on the wire, and every Opus 5 call
failed with "temperature is deprecated for this model".
"""

from __future__ import annotations

from matrx_ai.catalog.controls import ControlRule, compile_controls


def _compiled():
    api = {
        "temperature": ControlRule.model_validate(
            {
                "clamp": {"min": 0, "max": 1},
                "processor": "anthropic_temp_topp_exclusion",
                "processor_config": {
                    "order": 200,
                    "consumes": ["top_p", "top_k"],
                    "wire_container": "extra_body",
                },
            }
        ),
        "max_output_tokens": ControlRule.model_validate({"provider_key": "max_tokens"}),
    }
    override = {"temperature": ControlRule.model_validate({"supported": False})}
    return compile_controls(api, override)


def test_supported_false_beats_processor_and_drops_consumed_keys():
    compiled = _compiled()
    params, adjustments = compiled.outbound(
        {"temperature": 0.0, "top_p": 0.9, "max_output_tokens": 500}, context={}
    )
    assert "temperature" not in params
    assert "top_p" not in params
    assert "extra_body" not in params
    assert params.get("max_tokens") == 500
    dropped = {a.key for a in adjustments if a.action == "dropped"}
    assert {"temperature", "top_p"} <= dropped


def test_supported_processor_still_runs():
    api = {
        "temperature": ControlRule.model_validate(
            {
                "clamp": {"min": 0, "max": 1},
                "processor": "anthropic_temp_topp_exclusion",
                "processor_config": {"order": 200, "consumes": ["top_p", "top_k"]},
            }
        )
    }
    compiled = compile_controls(api, {})
    params, _ = compiled.outbound({"temperature": 0.3}, context={})
    assert params.get("temperature") == 0.3
