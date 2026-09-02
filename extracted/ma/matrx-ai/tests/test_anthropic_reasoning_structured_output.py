"""Regression: legacy reasoning settings + structured output on Anthropic
must never silently shrink the output budget or drop the schema.

Feedback 0788c8a5 (2026-08-23): the Website Factory Page Writer, re-tiered
from Gemini to claude-sonnet-5 while keeping legacy Gemini settings
(``reasoning_effort`` + ``reasoning_summary``), produced ~800-token truncated
runs with literal "placeholder" strings in required schema fields. Live
diagnosis showed the translator builds a fully valid request for this combo
(full max_tokens, adaptive thinking, effort + format merged into one
output_config) and the placeholder collapse is a MODEL-side stochastic
constrained-decoding failure that reproduces with and without the reasoning
settings. Two guarantees are locked here:

1. Request build — reasoning settings + json_schema on an adaptive Anthropic
   offering yields the FULL caller budget on ``max_tokens`` and a merged
   ``output_config`` carrying both ``effort`` and ``format`` (the merge-not-
   clobber seam in ``AnthropicTranslator.to_anthropic``). Budget-mode
   offerings keep ``max_tokens > thinking.budget_tokens`` with the schema
   intact.
2. Response parse — a schema-valid result whose fields are literal
   "placeholder" filler is REJECTED loudly by ``_parse_with_schema``
   (DegenerateOutputError), never silently persisted.

    uv run pytest packages/matrx-ai/tests/test_anthropic_reasoning_structured_output.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent))

from test_chat_param_golden import load_golden  # noqa: E402

from matrx_ai.agents.executor import _parse_with_schema  # noqa: E402
from matrx_ai.agents.response_parser import find_degenerate_strings  # noqa: E402
from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage  # noqa: E402
from matrx_ai.providers.anthropic.translator import AnthropicTranslator  # noqa: E402
from matrx_ai.testing.profile_factory import make_profile  # noqa: E402

SCHEMA = {
    "type": "object",
    "properties": {
        "meta_title": {"type": "string"},
        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"heading": {"type": "string"}, "body": {"type": "string"}},
                "required": ["heading", "body"],
            },
        },
    },
    "required": ["meta_title", "sections"],
}

RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {"name": "page", "schema": SCHEMA, "strict": True},
}


def _profile(family: str):
    payload = load_golden(family)
    return make_profile(
        model_name="claude-sonnet-5",
        wire_format=payload["wire_format"],
        rules=payload["rules"],
        value_orders=payload["value_orders"],
    )


def _request(family: str, **settings) -> dict:
    cfg = UnifiedConfig(
        model="claude-sonnet-5",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="write the page")])],
        max_output_tokens=24000,
        response_format=RESPONSE_FORMAT,
        **settings,
    )
    return AnthropicTranslator().to_anthropic(cfg, _profile(family))


# ---------------------------------------------------------------------------
# 1. Request build — the full budget survives the reasoning settings
# ---------------------------------------------------------------------------


def test_adaptive_reasoning_plus_schema_keeps_full_budget():
    req = _request(
        "anthropic_adaptive", reasoning_effort="medium", reasoning_summary="always"
    )
    assert req["max_tokens"] == 24000, "caller budget must never be capped"
    assert req["thinking"] == {"type": "adaptive", "display": "summarized"}
    # effort and format must COEXIST on one output_config (merge, not clobber)
    assert req["output_config"]["effort"] == "medium"
    fmt = req["output_config"]["format"]
    assert fmt["type"] == "json_schema"
    assert fmt["schema"]["required"] == ["meta_title", "sections"]


def test_adaptive_schema_without_reasoning_settings_keeps_format():
    req = _request("anthropic_adaptive")
    assert req["max_tokens"] == 24000
    assert "thinking" not in req  # sonnet-5 defaults to adaptive server-side
    assert req["output_config"]["format"]["type"] == "json_schema"
    assert "effort" not in req["output_config"]


def test_adaptive_reasoning_none_disables_thinking_keeps_schema():
    req = _request("anthropic_adaptive", reasoning_effort="none")
    assert req["max_tokens"] == 24000
    assert "thinking" not in req
    assert req["output_config"]["format"]["type"] == "json_schema"


def test_budget_mode_reasoning_plus_schema_keeps_budget_and_format():
    req = _request(
        "anthropic_standard", reasoning_effort="medium", reasoning_summary="always"
    )
    thinking = req["thinking"]
    assert thinking["type"] == "enabled"
    assert req["max_tokens"] == 24000
    assert req["max_tokens"] > thinking["budget_tokens"]
    assert req["output_config"]["format"]["type"] == "json_schema"


# ---------------------------------------------------------------------------
# 2. Response parse — the placeholder collapse is rejected loudly
# ---------------------------------------------------------------------------


class _Section(BaseModel):
    heading: str
    body: str


class _Page(BaseModel):
    meta_title: str
    sections: list[_Section]


DEGENERATE_OUTPUT = (
    '{"meta_title": "placeholder", "sections": '
    '[{"heading": "placeholder", "body": "placeholder"}]}'
)

HEALTHY_OUTPUT = (
    '{"meta_title": "Emergency Roof Repair Tampa | 24/7", "sections": '
    '[{"heading": "Our Process", "body": "We use a placeholder tarp system '
    'before the full repair — the word placeholder in prose is fine."}]}'
)


def test_parse_rejects_placeholder_stuffed_output():
    parsed, error = _parse_with_schema(DEGENERATE_OUTPUT, _Page, "test")
    assert parsed is None
    assert error is not None and "DegenerateOutputError" in error
    assert "meta_title" in error


def test_parse_accepts_prose_containing_the_word_placeholder():
    parsed, error = _parse_with_schema(HEALTHY_OUTPUT, _Page, "test")
    assert error is None
    assert parsed is not None
    assert parsed.meta_title.startswith("Emergency")


def test_find_degenerate_strings_paths_and_variants():
    data = {
        "a": "Placeholder",
        "b": "(placeholder)",
        "c": ["fine", "[PLACEHOLDER]"],
        "d": {"e": "real content mentioning a placeholder inline"},
        "f": "n/a",  # plausible business value — must stay legal
    }
    hits = find_degenerate_strings(data)
    assert set(hits) == {"$.a", "$.b", "$.c[1]"}
