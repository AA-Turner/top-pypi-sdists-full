"""Types for skill identifier computation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SkillFileInput:
    name: str
    content: str


@dataclass(frozen=True)
class SkillIdentifier:
    root: str
    file_hashes: dict[str, str]
