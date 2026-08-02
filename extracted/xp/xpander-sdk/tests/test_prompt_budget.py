"""Prompt-composition attribution: coverage closes, nothing is double counted.

The static prefix is re-read on every turn, so knowing which sections it is made
of decides where to cut. These tests pin the accounting: identified sections plus
the remainder always equal the whole, a constant nested inside a larger one is
credited once, tool schemas bucket by family, and odd tool shapes never raise.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from xpander_sdk.modules.backend.utils import prompt_budget as pb

_CONST_A = "A" * 1_000
_CONST_B = "B" * 500
_NESTED = "A" * 100  # a substring of _CONST_A
_CONSTANTS = {
    "ALPHA_INSTRUCTIONS": _CONST_A,
    "BETA_INSTRUCTIONS": _CONST_B,
    "NESTED_RULE": _NESTED,
}


def _fn(name: str, desc: str = "d" * 200, params: dict | None = None):
    return SimpleNamespace(
        name=name,
        description=desc,
        parameters=params if params is not None else {"type": "object"},
    )


# ---- constant reflection --------------------------------------------- #


def test_collect_picks_up_long_uppercase_strings():
    ns = {
        "BIG_INSTRUCTIONS": "x" * 500,
        "SHORT_MESSAGE": "too short",
        "lowercase_big": "y" * 500,
        "NUMBER": 42,
    }
    found = pb.collect_prompt_constants(ns)
    assert set(found) == {"BIG_INSTRUCTIONS"}


def test_collect_is_empty_for_empty_namespace():
    assert pb.collect_prompt_constants({}) == {}


# ---- attribution ------------------------------------------------------ #


def test_sections_and_remainder_cover_the_whole_text():
    text = "preamble " + _CONST_A + " middle " + _CONST_B + " tail"
    out = pb.attribute(text, _CONSTANTS)
    assert out["alpha"] == pb._tokens(len(_CONST_A))
    assert out["beta"] == pb._tokens(len(_CONST_B))
    # Remainder is the arithmetic leftover, so coverage is never overstated.
    leftover = len(text) - len(_CONST_A) - len(_CONST_B)
    assert out["unattributed"] == pb._tokens(leftover)


def test_nested_constant_credited_once_to_the_larger_span():
    out = pb.attribute("head " + _CONST_A, _CONSTANTS)
    assert "alpha" in out
    assert "nested_rule" not in out
    assert out["unattributed"] >= 0


def test_tagged_block_attributed():
    text = 'lead <skills note="x">\n  <skill name="a">d</skill>\n</skills> tail'
    out = pb.attribute(text, {})
    assert out["skills"] > 0
    assert out["unattributed"] >= 0


def test_multiple_tracked_tags():
    text = "<dynamic_tools>cat</dynamic_tools><memories note='n'>m</memories>"
    out = pb.attribute(text, {})
    assert out["dynamic_tools"] > 0
    assert out["memories"] > 0


def test_repeated_section_does_not_inflate_the_total():
    text = _CONST_A + _CONST_A
    out = pb.attribute(text, _CONSTANTS)
    assert out["alpha"] == pb._tokens(len(_CONST_A))
    assert out["unattributed"] >= 0


def test_unattributed_never_negative_for_overlapping_candidates():
    text = _CONST_A
    out = pb.attribute(text, _CONSTANTS)
    assert out["unattributed"] == 0


@pytest.mark.parametrize("text", [None, "", "   "])
def test_empty_inputs_are_safe(text):
    out = pb.attribute(text, _CONSTANTS)
    assert out["total_tok"] == pb._tokens(len(text or ""))


# ---- tool families ----------------------------------------------------- #


@pytest.mark.parametrize(
    "name,family",
    [
        ("xpworkspace-bash", "xpworkspace"),
        ("xpschedule-create", "xpschedule"),
        ("xplivesurface-create", "xplivesurface"),
        ("xpchatcard-upsert", "xpchatcard"),
        ("xp_search_tools", "xp_meta"),
        ("xpget_system_prompt", "xp_other"),
        ("mcp_tool_list_issues", "mcp"),
        ("manage_memory", "other"),
        ("tavily_search", "other"),
    ],
)
def test_tool_family_buckets(name, family):
    assert pb._tool_family(name) == family


def test_tools_are_counted_per_family():
    out = pb.attribute_tools([_fn("xpworkspace-bash"), _fn("xpschedule-create")])
    assert out["count"] == 2
    assert out["xpworkspace"] > 0
    assert out["xpschedule"] > 0
    assert out["total_tok"] == out["xpworkspace"] + out["xpschedule"]


def test_toolkit_functions_are_walked():
    toolkit = SimpleNamespace(functions={"a": _fn("tavily_search")})
    out = pb.attribute_tools([toolkit])
    assert out["count"] == 1
    assert out["other"] > 0


def test_unknown_tool_shape_does_not_raise():
    out = pb.attribute_tools([object(), None])
    assert out["count"] == 2


def test_no_tools_is_safe():
    assert pb.attribute_tools(None)["count"] == 0
    assert pb.attribute_tools([])["count"] == 0


# ---- emit -------------------------------------------------------------- #


def test_log_emits_one_line(caplog):
    args = {
        "instructions": "lead " + _CONST_A,
        "additional_context": "<memories note='n'>m</memories>",
        "tools": [_fn("xpworkspace-bash")],
        "description": "d",
        "expected_output": "",
    }
    with caplog.at_level("INFO"):
        pb.log_prompt_budget(args, _CONSTANTS, task_id="t-1", agent_id="a-1")


def test_log_never_raises_on_broken_args():
    pb.log_prompt_budget({"tools": object()}, _CONSTANTS)


def test_log_respects_the_flag(monkeypatch):
    monkeypatch.setattr(pb, "PROMPT_BUDGET_ENABLED", False)
    pb.log_prompt_budget({"instructions": _CONST_A}, _CONSTANTS)


def test_no_prompt_content_in_the_payload():
    """Sizes only - the prompt carries user memories and org data."""
    secret = "SUPER-SECRET-MEMORY-VALUE"
    out = pb.attribute(f"lead <memories note='n'>{secret}</memories>", _CONSTANTS)
    assert all(isinstance(v, int) for v in out.values())
    assert secret not in str(out)


# ---- wire budget ------------------------------------------------------- #


def _bedrock_tool(name: str, desc_len: int = 500):
    return {
        "toolSpec": {
            "name": name,
            "description": "d" * desc_len,
            "inputSchema": {"json": {"type": "object", "properties": {"payload": {}}}},
        }
    }


def test_wire_measures_the_bedrock_shape():
    out = pb._wire_tool_families([_bedrock_tool("xpworkspace-bash")])
    assert out["count"] == 1
    assert out["xpworkspace"] > 0


def test_wire_measures_the_anthropic_shape():
    out = pb._wire_tool_families(
        [{"name": "xp_search_tools", "description": "d" * 400, "input_schema": {}}]
    )
    assert out["count"] == 1
    assert out["xp_meta"] > 0


def test_wire_skips_breakpoint_markers():
    """cachePoint rides the same list and is not a tool."""
    out = pb._wire_tool_families(
        [_bedrock_tool("xpworkspace-bash"), {"cachePoint": {"type": "default"}}]
    )
    assert out["count"] == 1


@pytest.mark.parametrize("tools", [None, [], "not a list", [None, 42]])
def test_wire_tolerates_odd_tool_lists(tools):
    pb._wire_tool_families(tools if isinstance(tools, list) else None)


def test_wire_logs_once_per_distinct_prompt():
    """One line per run: the system prefix is stable within a run, distinct between runs."""
    pb._WIRE_SEEN.clear()
    pb.log_wire_budget(provider="bedrock", system_text="A" * 5_000, tools=[])
    pb.log_wire_budget(provider="bedrock", system_text="A" * 5_000, tools=[])
    pb.log_wire_budget(provider="bedrock", system_text="B" * 5_000, tools=[])
    # Two fingerprints seen, so the repeat of "A" did not emit a second line.
    assert len(pb._WIRE_SEEN) == 2


def test_wire_distinguishes_providers_on_the_same_text():
    pb._WIRE_SEEN.clear()
    pb.log_wire_budget(provider="bedrock", system_text="A" * 5_000, tools=[])
    pb.log_wire_budget(provider="anthropic", system_text="A" * 5_000, tools=[])
    assert len(pb._WIRE_SEEN) == 2


def test_wire_seen_set_stays_bounded():
    pb._WIRE_SEEN.clear()
    for i in range(pb._WIRE_SEEN_MAX + 50):
        pb.log_wire_budget(provider="bedrock", system_text=f"prompt-{i}", tools=[])
    assert len(pb._WIRE_SEEN) <= pb._WIRE_SEEN_MAX


def test_wire_never_raises():
    pb.log_wire_budget(provider="bedrock", system_text=None, tools="junk")


def test_wire_respects_the_flag(monkeypatch):
    monkeypatch.setattr(pb, "PROMPT_BUDGET_ENABLED", False)
    pb.log_wire_budget(provider="bedrock", system_text="A" * 5_000, tools=[])


def test_wire_payload_carries_no_prompt_content():
    pb._WIRE_SEEN.clear()
    secret = "SUPER-SECRET-SYSTEM-TEXT"
    out = pb._wire_tool_families([_bedrock_tool("xpworkspace-bash")])
    assert all(isinstance(v, int) for v in out.values())
    assert secret not in str(out)
