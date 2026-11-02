"""Tests for safe skill source preparation."""

from pathlib import Path

import pytest

from agentic_devtools.skill_injector_markdown import _generate_readme
from agentic_devtools.skill_injector_planning import _plan_skills_kind
from agentic_devtools.skill_injector_prepare_skills import _prepare_skills_kind


def _skill(source: Path, name: str) -> Path:
    path = source / name / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text(f"---\nname: {name}\ndescription: {name}\n---\n", encoding="utf-8")
    return path


def _prepare(source: Path, target: Path, **kwargs):
    return _prepare_skills_kind(
        source,
        target,
        issue_adapter=kwargs.get("issue_adapter"),
        code_hosting=kwargs.get("code_hosting"),
        plan_skills_kind=_plan_skills_kind,
        on_counts=kwargs.get("on_counts"),
    )


def test_filters_skills_and_returns_pruned_count(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _skill(source, "jira-only").write_text(
        "---\nname: jira-only\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
        encoding="utf-8",
    )
    _skill(source, "universal")

    reported_counts: list[tuple[int, int]] = []
    plan, origins, cache, injected, pruned, collision = _prepare(
        source,
        tmp_path / "target",
        issue_adapter="github",
        on_counts=lambda injected_count, pruned_count: reported_counts.append((injected_count, pruned_count)),
    )

    assert plan.added == ("universal/SKILL.md",)
    assert set(origins) == {"universal/SKILL.md"}
    assert len(cache) == 1
    assert injected == 1
    assert pruned == 1
    assert collision is False
    assert reported_counts == [(0, 1), (1, 0)]


def test_skips_unmanaged_consumer_skill_without_adopting_it(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _skill(source, "user-skill")
    _skill(source, "managed-skill")
    target = tmp_path / "target"
    notes = target / "user-skill" / "notes.md"
    notes.parent.mkdir(parents=True)
    notes.write_text("owned by consumer", encoding="utf-8")

    with pytest.warns(RuntimeWarning, match="consumer-authored"):
        plan, origins, _cache, injected, _pruned, collision = _prepare(source, target)

    assert set(origins) == {"managed-skill/SKILL.md"}
    assert plan.added == ("managed-skill/SKILL.md",)
    assert injected == 1
    assert collision is False
    assert notes.read_text(encoding="utf-8") == "owned by consumer"


def test_shared_resource_collision_blocks_dependent_skills(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _skill(source, "bundled-skill")
    (source / "fingerprint.py").write_text("bundled", encoding="utf-8")
    target = tmp_path / "target"
    target.mkdir()
    (target / "fingerprint.py").write_text("consumer", encoding="utf-8")

    with pytest.warns(RuntimeWarning, match="shared resource"):
        _plan, _origins, _cache, _injected, _pruned, collision = _prepare(source, target)

    assert collision is True


def test_shared_resource_only_collision_skips_only_shared_resource(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "fingerprint.py").write_text("bundled", encoding="utf-8")
    target = tmp_path / "target"
    target.mkdir()
    (target / "fingerprint.py").write_text("consumer", encoding="utf-8")

    with pytest.warns(RuntimeWarning, match="consumer-authored"):
        plan, origins, _cache, injected, _pruned, collision = _prepare(source, target)

    assert plan.added == ()
    assert origins == {}
    assert injected == 0
    assert collision is False


def test_case_only_managed_resource_with_same_inode_is_not_a_collision(tmp_path: Path) -> None:
    source = tmp_path / "source"
    skill = source / "my-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\ndescription: My skill\n---\n", encoding="utf-8")
    (skill / "guide.md").write_text("new", encoding="utf-8")
    target = tmp_path / "target"
    destination = target / "my-skill"
    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_text("---\ndescription: My skill\n---\n", encoding="utf-8")
    old_resource = destination / "Guide.md"
    old_resource.write_text("old", encoding="utf-8")
    (destination.parent / "agdt.README.md").write_text(
        _generate_readme([("my-skill/SKILL.md", "My skill"), ("my-skill/Guide.md", "Guide")], "skills"),
        encoding="utf-8",
    )
    (destination / "guide.md").hardlink_to(old_resource)

    plan, _origins, _cache, injected, _pruned, collision = _prepare(source, target)

    assert plan.case_renames == (("my-skill/Guide.md", "my-skill/guide.md"),)
    assert injected == 1
    assert collision is False


def test_missing_case_variant_path_is_treated_as_a_normal_addition(tmp_path: Path) -> None:
    source = tmp_path / "source"
    skill = source / "my-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\ndescription: My skill\n---\n", encoding="utf-8")
    (skill / "guide.md").write_text("new", encoding="utf-8")
    target = tmp_path / "target"
    destination = target / "my-skill"
    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_text("---\ndescription: My skill\n---\n", encoding="utf-8")
    (destination / "Guide.md").write_text("old", encoding="utf-8")
    (target / "agdt.README.md").write_text(
        _generate_readme([("my-skill/SKILL.md", "My skill"), ("my-skill/Guide.md", "Guide")], "skills"),
        encoding="utf-8",
    )

    plan, _origins, _cache, injected, _pruned, collision = _prepare(source, target)

    assert plan.added == ("my-skill/guide.md",)
    assert injected == 1
    assert collision is False


def test_unmatched_shared_resource_is_selected_without_collision(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "fingerprint.py").write_text("bundled", encoding="utf-8")

    plan, origins, _cache, injected, _pruned, collision = _prepare(source, tmp_path / "target")

    assert plan.added == ("fingerprint.py",)
    assert set(origins) == {"fingerprint.py"}
    assert injected == 0
    assert collision is False


def test_case_variant_with_different_inode_is_a_consumer_collision(tmp_path: Path) -> None:
    source = tmp_path / "source"
    skill = source / "my-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\ndescription: My skill\n---\n", encoding="utf-8")
    (skill / "guide.md").write_text("new", encoding="utf-8")
    target = tmp_path / "target"
    destination = target / "my-skill"
    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_text("---\ndescription: My skill\n---\n", encoding="utf-8")
    (destination / "Guide.md").write_text("managed", encoding="utf-8")
    (destination / "guide.md").write_text("consumer", encoding="utf-8")
    (target / "agdt.README.md").write_text(
        _generate_readme([("my-skill/SKILL.md", "My skill"), ("my-skill/Guide.md", "Guide")], "skills"),
        encoding="utf-8",
    )

    with pytest.warns(RuntimeWarning, match="skipping bundled skills"):
        _plan, origins, _cache, injected, _pruned, collision = _prepare(source, target)

    assert set(origins) == {"my-skill/SKILL.md", "my-skill/Guide.md"}
    assert injected == 0
    assert collision is False


def test_collision_preserves_existing_managed_skill_files(tmp_path: Path) -> None:
    source = tmp_path / "source"
    skill = source / "my-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\ndescription: My skill\n---\n", encoding="utf-8")
    (skill / "new.md").write_text("bundled", encoding="utf-8")
    target = tmp_path / "target"
    destination = target / "my-skill"
    destination.mkdir(parents=True)
    managed_entry = destination / "SKILL.md"
    managed_entry.write_text("---\ndescription: My skill\n---\n", encoding="utf-8")
    managed_resource = destination / "old.md"
    managed_resource.write_text("managed", encoding="utf-8")
    (destination / "new.md").write_text("consumer", encoding="utf-8")
    other_skill_resource = target / "other-skill" / "old.md"
    other_skill_resource.parent.mkdir(parents=True)
    other_skill_resource.write_text("other managed", encoding="utf-8")
    (target / "agdt.README.md").write_text(
        _generate_readme(
            [
                ("my-skill/SKILL.md", "My skill"),
                ("my-skill/old.md", "Old"),
                ("my-skill/missing.md", "Missing"),
                ("other-skill/old.md", "Other"),
            ],
            "skills",
        ),
        encoding="utf-8",
    )

    with pytest.warns(RuntimeWarning, match="skipping bundled skills"):
        plan, origins, _cache, injected, _pruned, collision = _prepare(source, target)

    assert origins == {
        "my-skill/SKILL.md": managed_entry,
        "my-skill/old.md": managed_resource,
    }
    assert plan.added == ()
    assert injected == 0
    assert collision is False
