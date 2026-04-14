"""Tests for SkillPolicy model and frontmatter parsing (#857)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from anteroom.cli.skills import (
    SkillPolicy,
    SkillRegistry,
    _load_skills_from_dir,
    _parse_tool_policy,
)

# ---------------------------------------------------------------------------
# SkillPolicy.check_tool() tests
# ---------------------------------------------------------------------------


class TestSkillPolicyCheckTool:
    def test_default_allows_all(self) -> None:
        policy = SkillPolicy()
        allowed, reason = policy.check_tool("bash")
        assert allowed is True
        assert reason == ""

    def test_denied_by_denylist(self) -> None:
        policy = SkillPolicy(denied_tools=frozenset(["bash"]))
        allowed, reason = policy.check_tool("bash")
        assert allowed is False
        assert "denied by skill policy" in reason

    def test_denied_by_allowlist(self) -> None:
        policy = SkillPolicy(allowed_tools=frozenset(["read_file", "grep"]))
        allowed, reason = policy.check_tool("bash")
        assert allowed is False
        assert "not in the allowed tools" in reason

    def test_allowed_by_allowlist(self) -> None:
        policy = SkillPolicy(allowed_tools=frozenset(["read_file", "grep"]))
        allowed, reason = policy.check_tool("read_file")
        assert allowed is True
        assert reason == ""

    def test_denied_wins_over_allowed(self) -> None:
        policy = SkillPolicy(
            allowed_tools=frozenset(["bash", "read_file"]),
            denied_tools=frozenset(["bash"]),
        )
        allowed, reason = policy.check_tool("bash")
        assert allowed is False
        assert "denied by skill policy" in reason

    def test_empty_allowed_allows_all(self) -> None:
        policy = SkillPolicy(allowed_tools=frozenset())
        allowed, reason = policy.check_tool("anything")
        assert allowed is True


class TestSkillPolicySummary:
    def test_empty_policy_summary(self) -> None:
        policy = SkillPolicy()
        assert policy.summary() == ""

    def test_allowed_only(self) -> None:
        policy = SkillPolicy(allowed_tools=frozenset(["bash", "grep"]))
        assert policy.summary() == "allow=bash,grep"

    def test_denied_only(self) -> None:
        policy = SkillPolicy(denied_tools=frozenset(["write_file"]))
        assert policy.summary() == "deny=write_file"

    def test_both(self) -> None:
        policy = SkillPolicy(
            allowed_tools=frozenset(["read_file"]),
            denied_tools=frozenset(["bash"]),
        )
        assert policy.summary() == "allow=read_file; deny=bash"


# ---------------------------------------------------------------------------
# _parse_tool_policy() tests
# ---------------------------------------------------------------------------


class TestParseToolPolicy:
    def test_no_policy_returns_default(self) -> None:
        data: dict[str, object] = {"name": "test", "description": "test"}
        policy = _parse_tool_policy(data)
        assert policy == SkillPolicy()

    def test_hyphenated_format(self) -> None:
        data: dict[str, object] = {"allowed-tools": ["bash", "read_file"]}
        policy = _parse_tool_policy(data)
        assert policy.allowed_tools == frozenset(["bash", "read_file"])
        assert policy.origin_format == "claude"

    def test_underscored_format(self) -> None:
        data: dict[str, object] = {"allowed_tools": ["bash", "read_file"]}
        policy = _parse_tool_policy(data)
        assert policy.allowed_tools == frozenset(["bash", "read_file"])
        assert policy.origin_format == "anteroom"

    def test_denied_tools_hyphenated(self) -> None:
        data: dict[str, object] = {"denied-tools": ["write_file"]}
        policy = _parse_tool_policy(data)
        assert policy.denied_tools == frozenset(["write_file"])
        assert policy.origin_format == "claude"

    def test_denied_tools_underscored(self) -> None:
        data: dict[str, object] = {"denied_tools": ["write_file"]}
        policy = _parse_tool_policy(data)
        assert policy.denied_tools == frozenset(["write_file"])
        assert policy.origin_format == "anteroom"

    def test_hyphenated_takes_precedence(self) -> None:
        data: dict[str, object] = {
            "allowed-tools": ["bash"],
            "allowed_tools": ["grep"],
        }
        policy = _parse_tool_policy(data)
        assert policy.allowed_tools == frozenset(["bash"])
        assert policy.origin_format == "claude"

    def test_invalid_tool_name_skipped(self) -> None:
        data: dict[str, object] = {"allowed-tools": ["bash", "invalid tool!", ""]}
        policy = _parse_tool_policy(data)
        assert policy.allowed_tools == frozenset(["bash"])

    def test_comma_separated_string(self) -> None:
        data: dict[str, object] = {"allowed-tools": "bash, read_file, grep"}
        policy = _parse_tool_policy(data)
        assert policy.allowed_tools == frozenset(["bash", "read_file", "grep"])

    def test_both_allowed_and_denied(self) -> None:
        data: dict[str, object] = {
            "allowed-tools": ["bash", "read_file"],
            "denied-tools": ["write_file"],
        }
        policy = _parse_tool_policy(data)
        assert policy.allowed_tools == frozenset(["bash", "read_file"])
        assert policy.denied_tools == frozenset(["write_file"])

    def test_non_list_value_warns(self) -> None:
        data: dict[str, object] = {"allowed-tools": 42}
        policy = _parse_tool_policy(data)
        assert policy.allowed_tools == frozenset()


# ---------------------------------------------------------------------------
# SKILL.md integration tests
# ---------------------------------------------------------------------------


def _write_skill_md(skills_dir: Path, name: str, frontmatter: str, body: str = "Do something.") -> Path:
    skill_dir = skills_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    content = f"---\n{frontmatter}\n---\n\n{body}\n"
    path = skill_dir / "SKILL.md"
    path.write_text(content)
    return path


class TestParseSkillMdPolicy:
    def test_extracts_allowed_tools(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir)
            _write_skill_md(
                skills_dir,
                "deploy",
                "name: deploy\ndescription: Deploy app\nallowed-tools:\n  - bash\n  - read_file",
            )
            result = _load_skills_from_dir(skills_dir, "project")
            assert len(result.skills) == 1
            skill = result.skills[0]
            assert skill.policy.allowed_tools == frozenset(["bash", "read_file"])
            assert skill.policy.origin_format == "claude"

    def test_extracts_denied_tools(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir)
            _write_skill_md(
                skills_dir,
                "safe-review",
                "name: safe-review\ndescription: Safe review\ndenied-tools:\n  - write_file\n  - bash",
            )
            result = _load_skills_from_dir(skills_dir, "project")
            assert len(result.skills) == 1
            skill = result.skills[0]
            assert skill.policy.denied_tools == frozenset(["write_file", "bash"])

    def test_no_policy_returns_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir)
            _write_skill_md(skills_dir, "greet", "name: greet\ndescription: Greet user")
            result = _load_skills_from_dir(skills_dir, "project")
            assert len(result.skills) == 1
            assert result.skills[0].policy == SkillPolicy()

    def test_underscored_format_from_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir)
            _write_skill_md(
                skills_dir,
                "check",
                "name: check\ndescription: Check\nallowed_tools:\n  - grep\n  - read_file",
            )
            result = _load_skills_from_dir(skills_dir, "project")
            assert len(result.skills) == 1
            skill = result.skills[0]
            assert skill.policy.allowed_tools == frozenset(["grep", "read_file"])
            assert skill.policy.origin_format == "anteroom"


class TestSkillRegistryWithPolicy:
    def test_resolve_input_with_skill_returns_skill_obj(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_dir = Path(tmpdir)
            _write_skill_md(
                skills_dir,
                "deploy",
                "name: deploy\ndescription: Deploy\nallowed-tools:\n  - bash",
            )
            result = _load_skills_from_dir(skills_dir, "project")
            registry = SkillRegistry()
            registry._skills = {s.name: s for s in result.skills}
            registry._rebuild_name_index()

            is_skill, prompt, skill_obj = registry.resolve_input_with_skill("/deploy")
            assert is_skill is True
            assert skill_obj is not None
            assert skill_obj.policy.allowed_tools == frozenset(["bash"])

    def test_resolve_input_with_skill_non_skill(self) -> None:
        registry = SkillRegistry()
        is_skill, text, skill_obj = registry.resolve_input_with_skill("/unknown")
        assert is_skill is False
        assert skill_obj is None

    def test_resolve_input_with_skill_not_slash(self) -> None:
        registry = SkillRegistry()
        is_skill, text, skill_obj = registry.resolve_input_with_skill("hello")
        assert is_skill is False
        assert skill_obj is None
