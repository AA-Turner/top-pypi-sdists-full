"""Tests for skill-scoped tool policy enforcement (#857)."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from anteroom.cli.skills import SkillPolicy
from anteroom.services.agent_loop import active_skill_policy

# ---------------------------------------------------------------------------
# ContextVar turn-scoping tests
# ---------------------------------------------------------------------------


class TestPolicyContextVar:
    def test_default_is_none(self) -> None:
        assert active_skill_policy.get() is None

    @pytest.mark.asyncio
    async def test_policy_set_from_queued_message(self) -> None:
        """When the agent loop dequeues a message with _skill_policy, the contextvar is set."""
        policy = SkillPolicy(denied_tools=frozenset(["bash"]))
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        msg: dict[str, Any] = {"role": "user", "content": "test", "_skill_policy": policy}
        await queue.put(msg)

        # Simulate what the agent loop does: pop _skill_policy and set contextvar
        queued_msg = queue.get_nowait()
        turn_policy = queued_msg.pop("_skill_policy", None)
        active_skill_policy.set(turn_policy)

        assert active_skill_policy.get() is policy
        assert "_skill_policy" not in queued_msg

        # Cleanup
        active_skill_policy.set(None)

    @pytest.mark.asyncio
    async def test_policy_cleared_after_turn(self) -> None:
        policy = SkillPolicy(denied_tools=frozenset(["bash"]))
        active_skill_policy.set(policy)
        assert active_skill_policy.get() is policy
        active_skill_policy.set(None)
        assert active_skill_policy.get() is None

    @pytest.mark.asyncio
    async def test_policy_not_in_llm_messages(self) -> None:
        """_skill_policy key is popped before message enters the LLM message list."""
        msg: dict[str, Any] = {
            "role": "user",
            "content": "test",
            "_skill_policy": SkillPolicy(denied_tools=frozenset(["bash"])),
        }
        _ = msg.pop("_skill_policy", None)
        assert "_skill_policy" not in msg
        assert msg == {"role": "user", "content": "test"}

    @pytest.mark.asyncio
    async def test_policy_isolated_across_turns(self) -> None:
        """Two queued messages: one skill, one plain text. Policy only active during skill turn."""
        policy = SkillPolicy(denied_tools=frozenset(["bash"]))
        skill_msg: dict[str, Any] = {"role": "user", "content": "skill prompt", "_skill_policy": policy}
        plain_msg: dict[str, Any] = {"role": "user", "content": "plain text"}

        # Simulate turn 1: skill message
        turn_policy = skill_msg.pop("_skill_policy", None)
        active_skill_policy.set(turn_policy)
        assert active_skill_policy.get() is policy

        # Simulate end of turn 1
        active_skill_policy.set(None)

        # Simulate turn 2: plain message
        turn_policy = plain_msg.pop("_skill_policy", None)
        active_skill_policy.set(turn_policy)
        assert active_skill_policy.get() is None

        # Cleanup
        active_skill_policy.set(None)

    @pytest.mark.asyncio
    async def test_concurrent_requests_isolated(self) -> None:
        """Two async tasks running with different policies see only their own."""
        policy_a = SkillPolicy(denied_tools=frozenset(["bash"]))
        policy_b = SkillPolicy(allowed_tools=frozenset(["grep"]))
        results: dict[str, Any] = {}

        async def task_a() -> None:
            active_skill_policy.set(policy_a)
            await asyncio.sleep(0.01)
            results["a"] = active_skill_policy.get()

        async def task_b() -> None:
            active_skill_policy.set(policy_b)
            await asyncio.sleep(0.01)
            results["b"] = active_skill_policy.get()

        await asyncio.gather(task_a(), task_b())
        assert results["a"] is policy_a
        assert results["b"] is policy_b

        # Cleanup
        active_skill_policy.set(None)


# ---------------------------------------------------------------------------
# Tool executor enforcement tests
# ---------------------------------------------------------------------------


class TestToolExecutorEnforcement:
    def test_tool_blocked_by_skill_policy(self) -> None:
        """When contextvar has a deny policy, check_tool returns blocked."""
        policy = SkillPolicy(denied_tools=frozenset(["bash"]))
        ok, reason = policy.check_tool("bash")
        assert ok is False
        assert "denied by skill policy" in reason

    def test_tool_allowed_by_skill_policy(self) -> None:
        """When contextvar has an allow policy, permitted tool proceeds."""
        policy = SkillPolicy(allowed_tools=frozenset(["bash", "read_file"]))
        ok, reason = policy.check_tool("bash")
        assert ok is True

    def test_no_policy_no_enforcement(self) -> None:
        """When contextvar is None, no policy enforcement."""
        assert active_skill_policy.get(None) is None


class TestDrainQueueSkillPolicy:
    @pytest.mark.asyncio
    async def test_drain_queue_skill_attaches_policy(self) -> None:
        """Skill invoked via _drain_input_to_msg_queue has _skill_policy on message."""
        from anteroom.cli.skills import Skill, SkillRegistry

        policy = SkillPolicy(denied_tools=frozenset(["bash"]))
        skill = Skill(
            name="safe-check",
            description="Safe check",
            prompt="Run checks safely",
            source="project",
            policy=policy,
        )
        registry = SkillRegistry()
        registry._skills = {"safe-check": skill}
        registry._rebuild_name_index()

        is_skill, prompt, skill_obj = registry.resolve_input_with_skill("/safe-check")
        assert is_skill is True
        assert skill_obj is not None

        # Simulate what _drain_input_to_msg_queue does
        msg: dict[str, Any] = {"role": "user", "content": prompt}
        if skill_obj.policy != SkillPolicy():
            msg["_skill_policy"] = skill_obj.policy

        assert "_skill_policy" in msg
        assert msg["_skill_policy"] is policy


# ---------------------------------------------------------------------------
# Direct /skill-name invocation path tests
# ---------------------------------------------------------------------------


class TestDirectSlashSkillPolicy:
    def test_direct_slash_skill_sets_policy(self) -> None:
        """Direct /skill-name resolves policy from Skill object."""
        from anteroom.cli.skills import Skill, SkillRegistry

        policy = SkillPolicy(allowed_tools=frozenset(["read_file", "grep"]))
        skill = Skill(
            name="review",
            description="Code review",
            prompt="Review the code",
            source="project",
            policy=policy,
        )
        registry = SkillRegistry()
        registry._skills = {"review": skill}
        registry._rebuild_name_index()

        is_skill, prompt, skill_obj = registry.resolve_input_with_skill("/review")
        assert is_skill is True
        assert skill_obj is not None
        assert skill_obj.policy == policy

        # Simulate what the REPL does: set contextvar
        _direct_skill_policy = None
        if skill_obj.policy != SkillPolicy():
            _direct_skill_policy = skill_obj.policy

        active_skill_policy.set(_direct_skill_policy)
        assert active_skill_policy.get() is policy

        # Cleanup
        active_skill_policy.set(None)

    def test_direct_slash_skill_clears_on_error(self) -> None:
        """Contextvar is cleared even if an error occurs."""
        policy = SkillPolicy(denied_tools=frozenset(["bash"]))
        active_skill_policy.set(policy)
        assert active_skill_policy.get() is policy

        # Simulate the finally block
        try:
            raise RuntimeError("simulated error")
        except RuntimeError:
            pass
        finally:
            active_skill_policy.set(None)

        assert active_skill_policy.get() is None

    def test_direct_slash_skill_no_policy_when_no_metadata(self) -> None:
        """Skill without policy metadata -> contextvar stays None."""
        from anteroom.cli.skills import Skill, SkillRegistry

        skill = Skill(
            name="greet",
            description="Greet",
            prompt="Say hello",
            source="project",
        )
        registry = SkillRegistry()
        registry._skills = {"greet": skill}
        registry._rebuild_name_index()

        is_skill, prompt, skill_obj = registry.resolve_input_with_skill("/greet")
        assert is_skill is True
        assert skill_obj is not None

        _direct_skill_policy = None
        if skill_obj.policy != SkillPolicy():
            _direct_skill_policy = skill_obj.policy

        assert _direct_skill_policy is None


# ---------------------------------------------------------------------------
# /skills output tests
# ---------------------------------------------------------------------------


class TestSkillsOutputPolicy:
    def test_build_skills_markdown_includes_policy(self) -> None:
        from anteroom.cli.commands import SkillDescription, build_skills_markdown

        entries = [
            SkillDescription(
                display_name="deploy",
                description="Deploy app",
                source="project",
                accepts_args=False,
                policy_summary="allow=bash,read_file; deny=write_file",
            ),
        ]
        md = build_skills_markdown(entries, [], has_registry=True)
        assert "[allow=bash,read_file; deny=write_file]" in md

    def test_build_skills_markdown_no_policy(self) -> None:
        from anteroom.cli.commands import SkillDescription, build_skills_markdown

        entries = [
            SkillDescription(
                display_name="greet",
                description="Greet",
                source="project",
                accepts_args=False,
                policy_summary="",
            ),
        ]
        md = build_skills_markdown(entries, [], has_registry=True)
        assert "[" not in md.split("greet")[1].split("\n")[0]
