"""Tests for verify_authored in derive_customization_disposition."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.scripts.derive_customization_disposition import derive, row


def test_nothing_authored_yet(tmp_path: Path) -> None:
    """Before any authoring, every surviving target slug is outstanding."""
    authored, missing, unexpected = derive.verify_authored([row(target="agdt-example")], tmp_path)
    assert (authored, missing, unexpected) == ([], ["agdt-example"], [])


def test_authored_skill_is_matched(tmp_path: Path) -> None:
    """A directory holding a correctly named `SKILL.md` is an authored skill."""
    skill = tmp_path / ".agents" / "skills" / "agdt-example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: agdt-example\n---\n# Example\n", encoding="utf-8")
    authored, missing, unexpected = derive.verify_authored([row(target="agdt-example")], tmp_path)
    assert (authored, missing, unexpected) == (["agdt-example"], [], [])


def test_skill_without_name_is_not_matched(tmp_path: Path) -> None:
    """A skill without a frontmatter name does not satisfy an authored target."""
    skill = tmp_path / ".agents" / "skills" / "agdt-example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Example\n", encoding="utf-8")
    authored, missing, unexpected = derive.verify_authored([row(target="agdt-example")], tmp_path)
    assert (authored, missing, unexpected) == ([], ["agdt-example"], [])


def test_expected_non_agdt_skill_is_matched(tmp_path: Path) -> None:
    """An expected non-`agdt-*` target name is still matched when authored."""
    skill = tmp_path / ".agents" / "skills" / "ai-pr-loop-supervision"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: ai-pr-loop-supervision\n---\n# Example\n",
        encoding="utf-8",
    )
    authored, missing, unexpected = derive.verify_authored([row(target="ai-pr-loop-supervision")], tmp_path)
    assert (authored, missing, unexpected) == (["ai-pr-loop-supervision"], [], [])


def test_non_agdt_subagent_target_ignores_skill_of_same_name(tmp_path: Path) -> None:
    """A non-`agdt-*` subagent target is not satisfied by an unrelated same-named skill."""
    skill = tmp_path / ".agents" / "skills" / "ai-pr-loop-supervision-admission"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Example\n", encoding="utf-8")
    authored, missing, unexpected = derive.verify_authored(
        [row(target="ai-pr-loop-supervision-admission", disposition="subagent")],
        tmp_path,
    )
    assert (authored, missing, unexpected) == ([], ["ai-pr-loop-supervision-admission"], [])


def test_authored_subagent_is_matched(tmp_path: Path) -> None:
    """A re-slugged `agdt-*.agent.md` file is an authored subagent."""
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt-example.agent.md").write_text("# Example\n", encoding="utf-8")
    authored, missing, unexpected = derive.verify_authored(
        [row(target="agdt-example", disposition="subagent", path=".github/agents/agdt.example.agent.md")],
        tmp_path,
    )
    assert (authored, missing, unexpected) == (["agdt-example"], [], [])


def test_frontmatter_name_matches_authored_subagent(tmp_path: Path) -> None:
    """A valid frontmatter name matches an authored subagent independently of its filename."""
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt.ai-pr-loop-supervision.worker.agent.md").write_text(
        "---\nname: ai-pr-loop-supervision-worker\n---\n# Worker\n",
        encoding="utf-8",
    )
    authored, missing, unexpected = derive.verify_authored(
        [row(target="ai-pr-loop-supervision-worker", disposition="subagent")],
        tmp_path,
    )
    assert (authored, missing, unexpected) == (["ai-pr-loop-supervision-worker"], [], [])


def test_legacy_namespace_with_non_agdt_frontmatter_is_unexpected(tmp_path: Path) -> None:
    """A legacy-namespaced agent with a non-`agdt-*` target remains visible to verification."""
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt.ai-pr-loop-supervision.workflow-monitor.agent.md").write_text(
        "---\nname: ai-pr-loop-workflow-monitor\n---\n# Monitor\n",
        encoding="utf-8",
    )
    authored, missing, unexpected = derive.verify_authored(
        [row(disposition="delete", target="-", slug="agdt.ai-pr-loop-supervision.workflow-monitor")],
        tmp_path,
    )
    assert (authored, missing, unexpected) == (["ai-pr-loop-workflow-monitor"], [], ["ai-pr-loop-workflow-monitor"])


def test_invalid_frontmatter_name_does_not_fall_back_to_filename(tmp_path: Path) -> None:
    """An invalid declared name leaves the expected target unsatisfied."""
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt-example.agent.md").write_text(
        "---\nname: invalid_name\n---\n# Example\n",
        encoding="utf-8",
    )
    authored, missing, unexpected = derive.verify_authored(
        [row(target="agdt-example", disposition="subagent")],
        tmp_path,
    )
    assert (authored, missing, unexpected) == ([], ["agdt-example"], [])


@pytest.mark.parametrize("declaration", ["name:\n", "name: # no target\n"])
def test_empty_frontmatter_name_does_not_fall_back_to_filename(tmp_path: Path, declaration: str) -> None:
    """An empty declared name leaves the expected target unsatisfied."""
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt-example.agent.md").write_text(
        f"---\n{declaration}---\n# Example\n",
        encoding="utf-8",
    )
    authored, missing, unexpected = derive.verify_authored(
        [row(target="agdt-example", disposition="subagent")],
        tmp_path,
    )
    assert (authored, missing, unexpected) == ([], ["agdt-example"], [])


def test_legacy_dot_named_agent_is_ignored(tmp_path: Path) -> None:
    """The legacy dot-named corpus under `.github/agents` must not satisfy authored output."""
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt.example.agent.md").write_text("# Legacy\n", encoding="utf-8")
    authored, missing, unexpected = derive.verify_authored(
        [row(target="agdt-example", disposition="subagent", path=".github/agents/agdt.example.agent.md")],
        tmp_path,
    )
    assert (authored, missing, unexpected) == ([], ["agdt-example"], [])


def test_unexpected_authored_unit_is_reported(tmp_path: Path) -> None:
    """A skill this map does not expect is a divergence worth failing on."""
    skill = tmp_path / ".agents" / "skills" / "agdt-surprise"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: agdt-surprise\n---\n# Surprise\n", encoding="utf-8")
    _, _, unexpected = derive.verify_authored([row(disposition="delete", target="-")], tmp_path)
    assert unexpected == ["agdt-surprise"]


def test_existing_skill_for_deleted_wrapper_is_reported_unexpected(tmp_path: Path) -> None:
    """A deleted wrapper does not exempt a same-named authored skill from verification."""
    skill = tmp_path / ".agents" / "skills" / "agdt-example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: agdt-example\n---\n# Example\n", encoding="utf-8")
    authored, missing, unexpected = derive.verify_authored(
        [
            row(
                disposition="delete",
                target="-",
                slug="agdt.example",
                batch="wrappers",
                reason="T0: wraps an `agdt-*` entry point and adds nothing to it.",
            )
        ],
        tmp_path,
    )
    assert (authored, missing, unexpected) == (["agdt-example"], [], ["agdt-example"])


def test_non_migration_skill_is_ignored(tmp_path: Path) -> None:
    """Skills outside the ``agdt-*`` namespace are not migration artifacts."""
    non_agdt = tmp_path / ".agents" / "skills" / "run-targeted-checks"
    non_agdt.mkdir(parents=True)
    (non_agdt / "SKILL.md").write_text("# Unrelated\n", encoding="utf-8")
    authored, missing, unexpected = derive.verify_authored([row(target="agdt-example")], tmp_path)
    assert (authored, missing, unexpected) == ([], ["agdt-example"], [])


def test_kind_mismatch_raises(tmp_path: Path) -> None:
    """A target expected as a skill cannot be satisfied by an authored subagent."""
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt-example.agent.md").write_text("# Example\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expects a skill artifact"):
        derive.verify_authored([row(target="agdt-example", disposition="skill")], tmp_path)


def test_duplicate_claims_raise(tmp_path: Path) -> None:
    """The same target slug authored in two locations must fail verification."""
    skill = tmp_path / ".agents" / "skills" / "agdt-example"
    agent = tmp_path / ".github" / "agents"
    skill.mkdir(parents=True)
    agent.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: agdt-example\n---\n# One\n", encoding="utf-8")
    (agent / "agdt-example.agent.md").write_text("# Two\n", encoding="utf-8")
    with pytest.raises(ValueError, match="multiple authored artifacts"):
        derive.verify_authored([row(target="agdt-example", disposition="skill")], tmp_path)


def test_incompatible_expected_kinds_raise(tmp_path: Path) -> None:
    """A single target slug cannot be both a skill target and a subagent target."""
    with pytest.raises(ValueError, match="incompatible dispositions"):
        derive.verify_authored(
            [
                row(target="agdt-example", disposition="skill"),
                row(target="agdt-example", disposition="subagent", path=".github/agents/agdt.sample.agent.md"),
            ],
            tmp_path,
        )


def test_collapse_only_target_does_not_require_authored_skill(tmp_path: Path) -> None:
    """A collapse-only target is tracked as documentation output, not authored skill/subagent."""
    authored, missing, unexpected = derive.verify_authored(
        [row(disposition="collapse", target="agdt-collapse-only")],
        tmp_path,
    )
    assert (authored, missing, unexpected) == ([], [], [])


def test_legacy_slug_for_collapse_only_target_is_unexpected(tmp_path: Path) -> None:
    """A collapse-only row must not register a legacy slug expectation with empty artifact kinds."""
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt-collapse-only.agent.md").write_text("# Collapse-only\n", encoding="utf-8")

    authored, missing, unexpected = derive.verify_authored(
        [row(disposition="collapse", target="agdt-collapse-only", slug="agdt.collapse.only")],
        tmp_path,
    )
    assert (authored, missing, unexpected) == (["agdt-collapse-only"], [], ["agdt-collapse-only"])


def test_legacy_slug_honors_expected_artifact_kind(tmp_path: Path) -> None:
    """A legacy dotted slug must still match the artifact kind allowed by its target rows."""
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt-example.agent.md").write_text("# Example\n", encoding="utf-8")

    with pytest.raises(ValueError, match="expects a skill artifact"):
        derive.verify_authored(
            [row(target="agdt-example", disposition="skill", path=".agents/skills/agdt.example/SKILL.md")],
            tmp_path,
        )
