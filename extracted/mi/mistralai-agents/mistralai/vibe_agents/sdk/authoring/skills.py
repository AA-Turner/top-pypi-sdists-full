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
    """Discover every accessible AI Registry skill when the root Session starts."""


def all_registry_skills() -> AllRegistrySkills:
    """List every AI Registry skill accessible in the Session's workspace.

    A served Agent discovers skills on behalf of the user who starts the Session. A local
    Session uses the process's Mistral API key. Registry versions are pinned at startup;
    contents are downloaded on first skill-tool use. Authored RegistrySkill references
    alongside this selection keep their explicit pins and startup provisioning.
    """

    return AllRegistrySkills()


class RegistrySkill(BaseModel):
    """Reference an AI Registry skill for a managed agent session."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: UUID
    version: int | None = Field(default=None, ge=1)
    """The exact version to serve. Skills served as sandbox files require it, so every Session and
    every worker serves the same files. Without it, a runtime that pins skills itself picks one."""


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
