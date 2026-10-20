"""What a send is made of — the split the Advanced session panel draws.

The provider reports total input tokens only; this measures the same config
the send boundary hands it, by part, so a reader can apportion the real total.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config import send_boundary
from matrx_ai.config.context_breakdown import LABELS, measure


def _config(**kw):
    base = dict(
        model="claude-x",
        system_instruction="You are a careful analyst.",  # 26 chars
        messages=[
            {"role": "user", "content": "What changed?"},  # 13
            SimpleNamespace(
                role="assistant", content=[SimpleNamespace(type="text", text="Two things.")]
            ),  # 11
            SimpleNamespace(
                role="tool",
                content=[
                    SimpleNamespace(type="tool_result", text='{"rows": 3}')
                ],  # 11, tool activity
            ),
        ],
        tools=[],
        tool_declarations={
            "anthropic": [
                {"name": "web_search", "description": "search"},
                {"name": "mcp.github.list_repos", "description": "repos"},
                {"name": "custom_tool_1", "description": "an agent"},
            ]
        },
    )
    base.update(kw)
    return SimpleNamespace(**base)


def test_every_part_is_measured_in_its_own_category():
    out = measure(_config())
    cats = {c["key"]: c for c in out["categories"]}
    assert [c["key"] for c in out["categories"]] == list(LABELS)
    assert cats["system_prompt"]["chars"] == 26
    assert cats["messages"]["chars"] == 24 and cats["messages"]["items"] == 3
    assert cats["tool_activity"]["chars"] == 11
    assert cats["system_tools"]["items"] == 1 and cats["mcp_tools"]["items"] == 1
    assert cats["agent_tools"]["items"] == 1
    assert out["total_chars"] == sum(c["chars"] for c in out["categories"])
    assert out["unit"] == "chars"


def test_a_system_role_message_counts_as_system_prompt():
    out = measure(_config(system_instruction=None, messages=[{"role": "system", "content": "abc"}]))
    cats = {c["key"]: c["chars"] for c in out["categories"]}
    assert cats["system_prompt"] == 3 and cats["messages"] == 0


def test_the_send_boundary_keeps_the_last_breakdown_until_taken():
    send_boundary._remember_breakdown("conv-1", _config())
    taken = send_boundary.take_context_breakdown("conv-1")
    assert taken is not None and taken["total_chars"] > 0
    assert send_boundary.take_context_breakdown("conv-1") is None
