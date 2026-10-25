"""A capability downgrade's JSON contract reaches the provider request.

2026-10-24 live (Haiku 5.5, Output Schema ``visual_map``): the downgrade fired and logged
"schema_sent_as_prompt_guidance: true", yet the request carried 4,138 input tokens and no contract —
the send boundary had already rendered this turn's block into the platform's host turn, the contract
joined the staged slots after that, and the translator does not re-render a placed block. Haiku
answered with a Mermaid fence. The order below is the real one: boundary first, then the gate.
"""

from __future__ import annotations

import contextlib
import io
import json
from types import SimpleNamespace

import pytest

from matrx_ai.config import MessageList, UnifiedConfig
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.unified_client import _downgrade_response_format
from matrx_ai.testing.profile_factory import make_profile

TYPED = "Draw the platform's pieces."
SCHEMA = {
    "type": "object",
    "properties": {"spec": {"type": "object", "additionalProperties": True}, "type": {"type": "string"}},
    "required": ["spec", "type"],
}


@pytest.fixture(autouse=True)
def _restore_gate_findings_context():
    """Request construction records no provider outcome to flush its gate finding."""
    from matrx_ai.providers.structured_output_findings import _GATE_PENDING

    token = _GATE_PENDING.set([])
    try:
        yield
    finally:
        _GATE_PENDING.reset(token)


def _caps():
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    return resolve_model_capabilities(SimpleNamespace(
        name="m", capabilities={"input": ["text"], "output": ["text"], "features": ["function_calling", "structured_output"]}))


def test_the_downgrade_contract_rides_in_the_request() -> None:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=[]),
                           response_format={"type": "json_schema", "json_schema": {"name": "x", "schema": SCHEMA}})
    config.system_instruction = "You draw."
    config.messages.append_or_extend_user_input(TYPED)
    config.messages.attach_turn_context("<live_date>now</live_date>", slot="live_date")
    profile = make_profile(model_name="m", wire_format="anthropic_chat")
    prep = order_for_wire(config, profile)
    wire = prep.wire_config if prep.wire_config is not None else config
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        _downgrade_response_format(wire, _caps(), "anthropic_chat")
        request = AnthropicTranslator().build_request(wire, profile)
    assert wire.response_format == {"type": "json_object"}
    text = json.dumps(request)
    assert "FINAL ANSWER FORMAT" in text, "the downgrade's contract never reached the provider request"
    assert text.index("FINAL ANSWER FORMAT") < text.rindex(TYPED), "the contract must sit before the typed text"
