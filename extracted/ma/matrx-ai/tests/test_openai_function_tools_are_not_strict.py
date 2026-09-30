"""Every function tool sent to the OpenAI Responses API declares ``strict: false``.

The Responses API turns an OMITTED ``strict`` into strict mode whenever it can
normalize the schema, and strict mode makes every property required. gpt-5-mini
then filled every optional argument of our dispatcher tools — center {0,0},
"" ids, radius_km over the knob, exclude_brand_terms [] (brand subtraction off),
other actions' fields — so tool defaults and knobs were silently overridden and
some calls were impossible (live, 2026-09-28: the response echoed strict: true
for a declaration that never set it).

The rows are real ``tool.definition`` rows (fixture ``_source``).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.testing.profile_factory import make_profile
from matrx_ai.tools.models import CustomTool, ToolDefinition
from matrx_ai.tools.registry import ToolRegistry

_ROWS = json.loads(
    (Path(__file__).parent / "fixtures" / "live_multi_action_tool_rows.json").read_text()
)["rows"]


@pytest.mark.parametrize("row", _ROWS, ids=[r["name"] for r in _ROWS])
def test_a_registered_tool_declares_strict_false(row: dict) -> None:
    tool = ToolDefinition(
        name=row["name"], description=row["description"], parameters=row["parameters"]
    )
    assert tool.to_openai_responses_format()["strict"] is False


def test_an_inline_tool_declares_strict_false() -> None:
    inline = CustomTool.from_dict(
        {
            "name": "inline_probe",
            "description": "probe",
            "input_schema": {
                "type": "object",
                "properties": {"q": {"type": "string"}, "limit": {"type": "integer"}},
                "required": ["q"],
            },
        }
    )
    assert inline.get_provider_format("openai")["strict"] is False


def test_the_openai_request_carries_it_for_every_function_tool() -> None:
    registry = ToolRegistry.get_instance()
    saved = dict(registry._tools)
    try:
        for row in _ROWS:
            registry.register(
                ToolDefinition(
                    name=row["name"], description=row["description"], parameters=row["parameters"]
                )
            )
        config = UnifiedConfig(
            model="gpt-5-mini",
            messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])],
            tools=[r["name"] for r in _ROWS],
        )
        request = OpenAITranslator().to_openai(
            config, make_profile(model_name="gpt-5-mini", wire_format="openai_responses")
        )
    finally:
        registry._tools = saved
    functions = [t for t in request["tools"] if t.get("type") == "function"]
    assert len(functions) == len(_ROWS)
    assert all(t.get("strict") is False for t in functions), [
        (t["name"], t.get("strict", "<absent>")) for t in functions
    ]
