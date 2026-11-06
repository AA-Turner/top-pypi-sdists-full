from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_files import (
    normalized_relative_path,
    normalized_sandbox_root,
)


@dataclass(frozen=True, slots=True)
class AllRegistrySkills:
    """Every skill of your workspace's AI Registry, as of the root session's start.

    ``agents.all_registry_skills()`` returns it.
    """


def all_registry_skills() -> AllRegistrySkills:
    """Give the agent every skill of your workspace's AI Registry.

    A deployed agent gets the skills that the user who starts the session can use. A local
    session uses your Mistral API key. The versions are fixed when the session starts, and each
    skill downloads the first time the agent uses it. A ``RegistrySkill`` in the same list keeps
    its own version.
    """

    return AllRegistrySkills()


class RegistrySkill(BaseModel):
    """One skill from your workspace's AI Registry, by ID and optional version."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: UUID
    """The skill's ID in the AI Registry."""
    version: int | None = Field(default=None, ge=1)
    """The exact version to use. A skill available to the agent as sandbox files needs it, so
    every session gets the same files, wherever the agent runs."""


class SandboxWorkspaceSkills(BaseModel):
    """Serve the skills already in the sandbox, such as those of a repository a sandbox hook cloned.

    The SDK looks for them once, after the sandbox hooks ran and before the first turn. A skill is
    a folder with a ``SKILL.md`` under one of ``dirs``, in ``root`` or in a repository directly
    below it.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    root: Annotated[str, AfterValidator(normalized_sandbox_root)] | None = None
    """Absolute sandbox path to look in. ``None`` is the sandbox workspace."""
    dirs: tuple[Annotated[str, AfterValidator(normalized_relative_path)], ...] = Field(
        default=(".agents/skills", ".vibe/skills"), min_length=1
    )
    """Skill folders relative to ``root`` and to each repository directly below it."""


__all__ = ["AllRegistrySkills", "RegistrySkill", "SandboxWorkspaceSkills", "all_registry_skills"]
