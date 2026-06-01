from __future__ import annotations

from typing import Protocol


class HasSkillNames(Protocol):
    name: str
    install_name: str | None


def skill_install_name(skill: HasSkillNames) -> str:
    return skill.install_name or skill.name
