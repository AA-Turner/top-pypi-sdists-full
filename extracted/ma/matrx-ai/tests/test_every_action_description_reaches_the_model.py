"""A multi-action tool's per-action descriptions reach the model on every provider.

Dispatcher tools keep each action's guidance (cost class, what to call first,
approval, reuse) in ``parameters["$variants"][action]["description"]``. The
provider flattening had no place for that text and dropped it, so a row written
the way the tool doctrine says reached the model with none of it (OSP-24). The
SEO lanes worked around it by copying every action's text into the tool
description; seo_local's raw row also carries only ``action`` at the top level,
so Gemini — which was sent the raw row — saw one argument.

The rows here are real: ``tool.definition`` rows read from the live platform
database (fixture ``_source`` says when). The doctrine shape is derived from
each real row by removing the copied text from its tool description — nothing
is invented.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from matrx_ai.tools.models import ToolContext, ToolDefinition
from matrx_ai.tools.registry import ToolRegistry

_FIXTURE = Path(__file__).parent / "fixtures" / "live_multi_action_tool_rows.json"
_ROWS: list[dict[str, Any]] = json.loads(_FIXTURE.read_text())["rows"]

#: Every serializer a provider adapter sends (``get_provider_format`` map).
_FORMATTERS = {
    "anthropic": ToolDefinition.to_anthropic_format,
    "openai_responses": ToolDefinition.to_openai_responses_format,
    "openai_chat": ToolDefinition.to_openai_format,
    "google": ToolDefinition.to_google_format,
    "mcp": ToolDefinition.to_mcp_format,
}


def _action_texts(row: dict[str, Any]) -> dict[str, str]:
    return {
        action: spec["description"].strip()
        for action, spec in row["parameters"]["$variants"].items()
        if isinstance(spec.get("description"), str)
    }


#: Rows whose actions carry their own description (local_media's property-map
#: variants carry none; it is here for the per-action validation guard).
_DESC_ROWS = [r for r in _ROWS if _action_texts(r)]


def _doctrine_shape(row: dict[str, Any]) -> dict[str, Any]:
    """The real row with the workaround copies removed from its tool description."""
    description = row["description"]
    for text in _action_texts(row).values():
        description = description.replace(text, "")
    return {**row, "description": description}


def _tool(row: dict[str, Any]) -> ToolDefinition:
    return ToolDefinition(
        name=row["name"], description=row["description"], parameters=row["parameters"]
    )


@pytest.mark.parametrize("row", _DESC_ROWS, ids=[r["name"] for r in _DESC_ROWS])
@pytest.mark.parametrize("provider", sorted(_FORMATTERS))
def test_each_action_description_is_in_the_rendered_definition(
    row: dict[str, Any], provider: str
) -> None:
    doctrine_row = _doctrine_shape(row)
    texts = _action_texts(doctrine_row)
    assert texts, "fixture row lost its per-action descriptions"
    for text in texts.values():
        assert text not in doctrine_row["description"]  # the copy really is gone

    rendered = json.dumps(_FORMATTERS[provider](_tool(doctrine_row)), ensure_ascii=False)
    missing = [action for action, text in texts.items() if text not in rendered]
    assert not missing, f"{row['name']} on {provider}: the model never reads {missing}"


@pytest.mark.parametrize("row", _DESC_ROWS, ids=[r["name"] for r in _DESC_ROWS])
@pytest.mark.parametrize("provider", sorted(_FORMATTERS))
def test_text_the_model_already_reads_is_not_repeated(row: dict[str, Any], provider: str) -> None:
    """The renderer adds no copy of text the row already puts in front of the
    model (some live rows carry it in both the tool and discriminator
    descriptions — that is the row's own duplication, counted as the baseline)."""
    rendered = json.dumps(_FORMATTERS[provider](_tool(row)), ensure_ascii=False)
    authored = row["description"] + row["parameters"]["action"].get("description", "")
    for action, text in _action_texts(row).items():
        expected = max(authored.count(text), 1)
        assert rendered.count(json.dumps(text, ensure_ascii=False)[1:-1]) == expected, (
            f"{row['name']} on {provider}: {action}'s description rendered an extra time"
        )


def test_gemini_is_sent_every_argument_of_a_variants_only_row() -> None:
    row = next(r for r in _ROWS if r["name"] == "seo_local")
    variant_args = {
        key
        for spec in row["parameters"]["$variants"].values()
        for key in spec.get("properties", {})
    }
    assert set(row["parameters"]) == {"$variants", "action"}  # the shape that broke Gemini

    params = _tool(row).to_google_format()["parameters"]
    assert variant_args <= set(params["properties"])

    def bool_required(node: Any) -> list[Any]:
        if isinstance(node, dict):
            found = [node] if isinstance(node.get("required"), bool) else []
            return found + [n for v in node.values() for n in bool_required(v)]
        if isinstance(node, list):
            return [n for v in node for n in bool_required(v)]
        return []

    assert not bool_required(params), "a boolean `required` 400s Gemini"


@pytest.mark.parametrize("row", _DESC_ROWS, ids=[r["name"] for r in _DESC_ROWS])
def test_the_google_sdk_accepts_the_rendered_declaration(row: dict[str, Any]) -> None:
    """The SDK's own schema model is the first gate a Gemini request meets; an
    integer enum (seo_local grid_size) failed it and killed the whole request."""
    from google.genai import types

    types.Tool(function_declarations=[_tool(_doctrine_shape(row)).to_google_format()])


def _variant_choices(row: dict[str, Any], key: str) -> dict[str, list[Any]]:
    return {
        action: spec["properties"][key]["enum"]
        for action, spec in row["parameters"]["$variants"].items()
        if "enum" in spec.get("properties", {}).get(key, {})
    }


@pytest.mark.parametrize("provider", sorted(_FORMATTERS))
def test_a_field_shared_by_actions_offers_every_actions_choices(provider: str) -> None:
    """seo_keywords ``mode`` is research's auto/related/suggestions/ideas AND
    tag's append/replace; flattening kept only the first action's list, so the
    model could not send a research mode at all."""
    row = next(r for r in _ROWS if r["name"] == "seo_keywords")
    per_action = _variant_choices(row, "mode")
    assert len({json.dumps(c) for c in per_action.values()}) > 1  # the live row still differs

    rendered = _FORMATTERS[provider](_tool(row))
    schema = rendered.get("input_schema") or rendered.get("parameters") or rendered["function"][
        "parameters"
    ]
    mode = schema["properties"]["mode"]
    for action, choices in per_action.items():
        assert set(choices) <= set(mode["enum"]), f"{provider}: {action}'s modes are unsendable"
        assert f"{action}: {', '.join(choices)}" in mode["description"], (
            f"{provider}: the description never says which modes belong to {action}"
        )


@pytest.mark.parametrize("provider", sorted(_FORMATTERS))
def test_a_shared_field_never_carries_one_actions_default_for_all(provider: str) -> None:
    """seo_keywords ``mode`` defaults to append for tag and auto for research;
    the first action's default went out for both."""
    row = next(r for r in _ROWS if r["name"] == "seo_keywords")
    defaults = {
        action: spec["properties"]["mode"].get("default")
        for action, spec in row["parameters"]["$variants"].items()
        if "mode" in spec.get("properties", {})
    }
    assert len(set(defaults.values())) > 1  # the live row still disagrees

    rendered = _FORMATTERS[provider](_tool(row))
    schema = rendered.get("input_schema") or rendered.get("parameters") or rendered["function"][
        "parameters"
    ]
    mode = schema["properties"]["mode"]
    assert "default" not in mode, f"{provider}: one action's default is sent for every action"
    for action, value in defaults.items():
        assert f"{action}: {value}" in mode["description"].split("Default by action")[-1]


# ── the runner still refuses what is invalid for the CHOSEN action ─────────


def test_a_delegated_call_is_refused_for_a_value_another_action_owns() -> None:
    """local_media runs on the desktop client (no server args model); the
    server's pre-suspend check is its only server-side door. The flattened
    schema now offers archive and office formats together, so format=zip
    passes it for office_generate — the chosen action's own contract must not."""
    from matrx_ai.tools.executor import _validate_against_declared_schema

    row = next(r for r in _ROWS if r["name"] == "local_media")
    tool = _tool(row)
    base = {"action": "office_generate", "path": "/tmp/x.docx", "spec": {"blocks": []}}

    assert _validate_against_declared_schema(tool, {**base, "format": "docx"}) is None
    refused = _validate_against_declared_schema(tool, {**base, "format": "zip"})
    assert refused is not None and "format" in refused and "zip" in refused


async def test_the_dispatch_refuses_it_before_suspending_to_the_client(monkeypatch) -> None:
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.streaming import ToolStreamManager

    row = next(r for r in _ROWS if r["name"] == "local_media")
    tool = _tool(row)
    suspended: list[dict[str, Any]] = []

    async def fake_delegated(self, tool_def, args, ctx, row_id, **_kw):
        suspended.append(args)
        from matrx_ai.tools.models import ToolResult

        return ToolResult(success=True, output="delegated", tool_name=tool_def.name)

    monkeypatch.setattr(ToolExecutor, "_execute_delegated", fake_delegated)
    executor = ToolExecutor(registry=ToolRegistry.get_instance())
    ctx = ToolContext(call_id="call-osp24", tool_name="local_media", emitter=None)
    stream = ToolStreamManager(None, ctx.call_id, "local_media")
    base = {"action": "office_generate", "path": "/tmp/x.docx", "spec": {"blocks": []}}

    refused = await executor._dispatch(
        tool, {**base, "format": "zip"}, ctx, stream, client_tools=frozenset({"local_media"})
    )
    assert refused.success is False and not suspended
    assert "format" in refused.error.message and refused.error.suggested_action

    accepted = await executor._dispatch(
        tool, {**base, "format": "docx"}, ctx, stream, client_tools=frozenset({"local_media"})
    )
    assert accepted.success is True and suspended == [{**base, "format": "docx"}]
