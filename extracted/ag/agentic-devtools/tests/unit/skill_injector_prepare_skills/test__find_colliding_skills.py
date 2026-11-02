"""Tests for identifying consumer-authored skill target collisions."""

from pathlib import Path

from agentic_devtools.skill_injector_prepare_skills import _find_colliding_skills


def test_empty_origins_have_no_collisions(tmp_path: Path) -> None:
    assert _find_colliding_skills(tmp_path, {}, set(), set(), {}) == set()


def test_existing_unmanaged_shared_resource_is_a_collision(tmp_path: Path) -> None:
    (tmp_path / "fingerprint.py").write_text("consumer", encoding="utf-8")

    collisions = _find_colliding_skills(
        tmp_path,
        {"fingerprint.py": tmp_path / "source-fingerprint.py"},
        set(),
        set(),
        {},
    )

    assert collisions == {"fingerprint.py"}


def test_case_variant_same_inode_is_not_a_collision(tmp_path: Path) -> None:
    skill = tmp_path / "my-skill"
    skill.mkdir()
    current = skill / "guide.md"
    current.write_text("managed", encoding="utf-8")
    prior = skill / "Guide.md"
    prior.hardlink_to(current)

    collisions = _find_colliding_skills(
        tmp_path,
        {"my-skill/guide.md": current},
        {"my-skill/Guide.md"},
        {"my-skill"},
        {"my-skill/guide.md": "my-skill/Guide.md"},
    )

    assert collisions == set()
