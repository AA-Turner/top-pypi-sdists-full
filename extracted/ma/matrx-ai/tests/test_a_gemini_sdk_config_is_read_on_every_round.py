"""The cache guard reads Gemini's ``config`` (an SDK object) on EVERY round.

PB-02 / PB-06, 2026-11-09: every nested Lane Planner on gemini-3.5-flash-lite filed
``prompt_cache_prefix_drift`` "system added" between its first two calls, while the two
stored requests carried the same system text, the same tools and the same first two
contents. Round 1's history was plain dicts, so the fast path fingerprinted it and skipped
the ``GenerateContentConfig`` object entirely (no system, no tools). Round 2's history held
an SDK Part (the model's function call), took the ``wire_json`` path, read the config and
"found" a system. The shape below is the stored one (system_instruction + tools in config,
two user contents, then the model's function call and its response).
"""

from __future__ import annotations

from google.genai import types

from matrx_ai.providers.cache_guard import compare_wire_prefix, wire_prefix

SYSTEM = "Current date: 2026-11-09\n\nYou are the Lane Planner at Compass Route Relocation Advisors."


def _config(system: str = SYSTEM) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        system_instruction=system,
        tools=[types.Tool(function_declarations=[types.FunctionDeclaration(name="agent", description="Run an agent")])],
    )


def _first_contents() -> list:
    return [
        {"role": "user", "parts": [{"text": "<turn_context source=\"platform\">…</turn_context>"}]},
        {"role": "user", "parts": [{"text": "Mexico City"}]},
    ]


def _second_contents() -> list:
    return [
        *_first_contents(),
        types.Content(
            role="model",
            parts=[types.Part(function_call=types.FunctionCall(name="agent", args={"prompt": "Los Angeles"}),
                              thought_signature=b"sig")],
        ),
        {"role": "user", "parts": [{"function_response": {"name": "agent", "response": {"result": "Fog"}}}]},
    ]


def test_round_one_with_plain_history_still_reads_the_sdk_config() -> None:
    first = wire_prefix({"model": "gemini-3.5-flash-lite", "contents": _first_contents(), "config": _config()})
    assert first is not None
    # The system text comes from the SDK config; the model is a compared head too (2026-11-15).
    assert [label for label, _ in first.heads] == ["system", "model"]
    assert [name for name, _, _ in first.tools] == ["agent"]


def test_an_unchanged_gemini_child_loop_is_stable() -> None:
    first = wire_prefix({"model": "gemini-3.5-flash-lite", "contents": _first_contents(), "config": _config()})
    second = wire_prefix(
        {"model": "gemini-3.5-flash-lite", "contents": _second_contents(), "config": _config()}, first
    )
    drift = compare_wire_prefix(first, second)
    assert drift.stable, drift


def test_a_real_system_change_between_plain_rounds_is_filed() -> None:
    first = wire_prefix({"model": "gemini-3.5-flash-lite", "contents": _first_contents(), "config": _config()})
    second = wire_prefix(
        {"model": "gemini-3.5-flash-lite", "contents": [*_first_contents(), {"role": "user", "parts": [{"text": "x"}]}],
         "config": _config(SYSTEM + "\nchanged")},
        first,
    )
    assert "system changed" in compare_wire_prefix(first, second).changed


def test_a_gemini_tool_change_is_named_by_its_functions() -> None:
    """A Gemini Tool block was fingerprinted ``<nameless>``: a changed tool list said only
    ``tools[0] (<nameless>) is now <nameless>``. The names come from its function declarations."""
    first = wire_prefix({"model": "gemini-3.5-flash-lite", "contents": _first_contents(), "config": _config()})
    other = types.GenerateContentConfig(
        system_instruction=SYSTEM,
        tools=[
            types.Tool(function_declarations=[
                types.FunctionDeclaration(name="agent", description="Run an agent"),
                types.FunctionDeclaration(name="web", description="Read a page"),
            ]),
            types.Tool(google_search=types.GoogleSearch()),
        ],
    )
    second = wire_prefix(
        {"model": "gemini-3.5-flash-lite", "contents": [*_first_contents(), {"role": "user", "parts": [{"text": "x"}]}],
         "config": other},
        first,
    )
    assert [name for name, _, _ in second.tools] == ["agent,web", "<google_search>"]
    assert compare_wire_prefix(first, second).tools_by_content == ("tools[0] (agent) is now agent,web",)
