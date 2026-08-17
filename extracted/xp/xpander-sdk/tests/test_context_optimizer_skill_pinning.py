"""Loaded skill playbooks survive Layer 2 compaction via the pin harvest/re-inject cycle.

Layer 2 keeps only system messages, and the <skills> prompt forbids re-loading a
skill - so before these pins, a compaction silently destroyed the playbook the
agent was mid-way through following.
"""

from __future__ import annotations

from types import SimpleNamespace

from agno.models.message import Message

from xpander_sdk.core.context_optimizer.constants import (
    PINNED_SKILL_MAX_CHARS,
    PINNED_SKILLS_MAX,
)
from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
)


def _make_optimizer() -> XPanderContextOptimizer:
    """A minimal optimizer with agent/task identity set."""
    opt = XPanderContextOptimizer(context_window=200_000)
    opt.agent = SimpleNamespace(
        id="agent-1", configuration=SimpleNamespace(organization_id="org-1")
    )
    opt.task = SimpleNamespace(id="task-1")
    return opt


def _playbook(name: str, body: str = "Steps: do the thing.") -> str:
    """A rendered <skill_playbook> span as the load builtin emits it."""
    return f'<skill_playbook name="{name}" version="1.0.0">\n{body}\n</skill_playbook>'


def _skill_msg(
    name: str, tool_name: str = "xpload_skill", body: str = "Steps: do the thing."
) -> Message:
    """A tool message carrying a successful skill-load result."""
    return Message(
        role="tool",
        content=_playbook(name, body),
        tool_call_id=f"tc-{name}",
        tool_name=tool_name,
    )


def test_harvest_pins_xpload_skill_only() -> None:
    # the gateway's load_skill result is an 8K routing aid - L1-skipped but never pinned
    opt = _make_optimizer()
    opt._harvest_skill_playbooks(
        [
            Message(role="system", content="sys"),
            _skill_msg("live-surface-generator"),
            _skill_msg("skills-generator", tool_name="load_skill"),
        ]
    )
    assert set(opt._pinned_skill_playbooks) == {"live-surface-generator"}


def test_harvest_pins_only_the_playbook_span() -> None:
    # the apply-now tail must not ride the pin - it would re-instruct a restart every compaction
    opt = _make_optimizer()
    msg = Message(
        role="tool",
        content=_playbook("a")
        + "\n\nAPPLY NOW: follow the playbook EXACTLY, starting with its first command.",
        tool_call_id="tc-a",
        tool_name="xpload_skill",
    )
    opt._harvest_skill_playbooks([msg])
    pinned = opt._pinned_skill_playbooks["a"]
    assert pinned.endswith("</skill_playbook>")
    assert "APPLY NOW" not in pinned


def test_failure_shaped_results_are_not_pinned() -> None:
    opt = _make_optimizer()
    failure = Message(
        role="tool",
        content="Unknown skill 'foo'. Available skills: bar, baz.",
        tool_call_id="tc-f",
        tool_name="xpload_skill",
    )
    opt._harvest_skill_playbooks([failure])
    assert opt._pinned_skill_playbooks == {}


def test_non_skill_tools_are_ignored() -> None:
    opt = _make_optimizer()
    other = Message(
        role="tool",
        content=_playbook("sneaky"),
        tool_call_id="tc-o",
        tool_name="xpworkspace-bash",
    )
    opt._harvest_skill_playbooks([other])
    assert opt._pinned_skill_playbooks == {}


def test_newest_wins_and_eviction_is_bounded() -> None:
    opt = _make_optimizer()
    opt._harvest_skill_playbooks([_skill_msg("a"), _skill_msg("b")])
    # reload of "a" refreshes it (moves to newest) and a third skill evicts the oldest
    opt._harvest_skill_playbooks([_skill_msg("a", body="v2 steps"), _skill_msg("c")])
    assert len(opt._pinned_skill_playbooks) == PINNED_SKILLS_MAX
    assert set(opt._pinned_skill_playbooks) == {"a", "c"}
    assert "v2 steps" in opt._pinned_skill_playbooks["a"]


def test_pinned_content_is_capped_with_marker() -> None:
    opt = _make_optimizer()
    opt._harvest_skill_playbooks(
        [_skill_msg("big", body="x" * (PINNED_SKILL_MAX_CHARS * 2))]
    )
    pinned = opt._pinned_skill_playbooks["big"]
    assert len(pinned) <= PINNED_SKILL_MAX_CHARS
    # a cut pin says so and stays well-formed, never posing as a complete procedure
    assert "[truncated - full files in ./skills/]" in pinned
    assert pinned.endswith("</skill_playbook>")


def test_render_is_empty_without_pins_and_single_message_with_them() -> None:
    opt = _make_optimizer()
    assert opt._render_pinned_skill_playbooks() == ""
    opt._harvest_skill_playbooks([_skill_msg("a"), _skill_msg("b")])
    rendered = opt._render_pinned_skill_playbooks()
    assert rendered.count('<skill_playbook name="a"') == 1
    assert rendered.count('<skill_playbook name="b"') == 1
    assert "do not load these skills again" in rendered


def test_repeat_compaction_yields_exactly_one_pin_message() -> None:
    """Simulates the L2 wipe/re-inject sequence twice - the pin never duplicates."""
    opt = _make_optimizer()
    messages = [
        Message(role="system", content="sys"),
        _skill_msg("live-surface-generator"),
    ]

    for _ in range(2):
        opt._harvest_skill_playbooks(messages)
        system_messages = [m for m in messages if m.role == "system"]
        messages.clear()
        messages.extend(system_messages)
        pinned = opt._render_pinned_skill_playbooks()
        if pinned:
            messages.append(Message(role="user", content=pinned))
        messages.append(Message(role="user", content="continuation"))

    pin_messages = [m for m in messages if "skill_playbook" in (m.content or "")]
    assert len(pin_messages) == 1
    assert '<skill_playbook name="live-surface-generator"' in pin_messages[0].content


def test_fresh_optimizer_reharvests_pins_from_a_prior_pin_message() -> None:
    """A new optimizer instance (e.g. a plan retry) rebuilds pins from the injected pin message."""
    first = _make_optimizer()
    first._harvest_skill_playbooks([_skill_msg("live-surface-generator")])
    pin_message = Message(role="user", content=first._render_pinned_skill_playbooks())

    fresh = _make_optimizer()
    fresh._harvest_skill_playbooks([Message(role="system", content="sys"), pin_message])
    assert "live-surface-generator" in fresh._pinned_skill_playbooks
    assert fresh._pinned_skill_playbooks["live-surface-generator"].endswith(
        "</skill_playbook>"
    )


def test_arbitrary_user_messages_are_not_harvested() -> None:
    opt = _make_optimizer()
    opt._harvest_skill_playbooks(
        [Message(role="user", content=_playbook("pasted-by-user"))]
    )
    assert opt._pinned_skill_playbooks == {}


def test_dispatched_skill_load_is_harvested_via_effective_name() -> None:
    opt = _make_optimizer()
    msg = Message(
        role="tool",
        content=_playbook("via-dispatch"),
        tool_call_id="tc-d",
        tool_name="xp_execute_tool",
        tool_args={"payload": {"name": "xpload_skill", "arguments": {}}},
    )
    opt._harvest_skill_playbooks([msg])
    assert "via-dispatch" in opt._pinned_skill_playbooks
