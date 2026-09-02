"""Together reasoning_effort — OUR default is high, never provider max.

The contract now lives in the DB rules (the together_reasoning processor on
the together_chat api). These tests run the REAL translator with the golden
rule snapshot and assert the wire value per unified effort.
"""

from __future__ import annotations

from test_chat_param_golden import load_golden

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers.together.translator import TogetherTranslator
from matrx_ai.testing.profile_factory import make_profile


def _profile():
    payload = load_golden("together_text_standard")
    return make_profile(
        model_name="zai-org/GLM-5.2",
        wire_format=payload["wire_format"],
        rules=payload["rules"],
        value_orders=payload["value_orders"],
    )


def _cfg(**kwargs) -> UnifiedConfig:
    msg = UnifiedMessage(role="user", content=[TextContent(text="hi")])
    return UnifiedConfig(model="zai-org/GLM-5.2", messages=[msg], **kwargs)


def _request(**kwargs):
    return TogetherTranslator().to_together(_cfg(**kwargs), _profile())


def test_unset_defaults_to_high_not_max():
    assert _request()["reasoning_effort"] == "high"


def test_medium_snaps_to_high_not_max():
    assert _request(reasoning_effort="medium")["reasoning_effort"] == "high"


def test_explicit_high_passthrough():
    assert _request(reasoning_effort="high")["reasoning_effort"] == "high"


def test_xhigh_maps_to_max():
    assert _request(reasoning_effort="xhigh")["reasoning_effort"] == "max"


def test_none_disables_via_reasoning_enabled_false():
    req = _request(reasoning_effort="none")
    assert "reasoning_effort" not in req
    assert req["reasoning"] == {"enabled": False}


def test_disable_reasoning_true_disables():
    req = _request(disable_reasoning=True)
    assert "reasoning_effort" not in req
    assert req["reasoning"] == {"enabled": False}


def test_auto_and_low_snap_to_high():
    for effort in ("auto", "low", "minimal"):
        assert _request(reasoning_effort=effort)["reasoning_effort"] == "high", effort


def test_streaming_requests_terminal_provider_usage():
    request = _request(stream=True)

    assert request["stream"] is True
    assert request["extra_body"] == {"stream_options": {"include_usage": True}}


def test_non_streaming_does_not_send_stream_options():
    request = _request(stream=False)

    assert "stream" not in request
    assert "extra_body" not in request
