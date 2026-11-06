"""Which definition a child Session runs on a deployed worker.

The control plane passes on the start request that its caller wrote, so the definition inside it is
never run. This worker derives the definition from its own root definition, the root's customization
and each parent's spawn choice. A configuration field added later is therefore derived by default; only
the fields a Session's runtime settles when it opens are copied from the request, and each one must stay
overwritten there before anything reads it.
"""

import posixpath
import re
from collections.abc import Callable, Sequence

from mistralai.vibe.harness.app_server.session.models.configuration import (
    MaterializedSkillDefinition,
    SessionSkillDefinition,
    calculate_skill_catalog_fingerprint,
)
from mistralai.vibe.harness.runtime.agents.configuration import resolve_child_definition
from mistralai.vibe.harness.runtime.agents.models import StartSessionRequest
from mistralai.vibe.harness.runtime.hosts.workflows import WorkflowHarnessDefinition
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.assembly import assemble, registry_skills, sandbox_skills
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring.skills import SandboxWorkspaceSkills


class ChildDefinitionRefusal(ValueError):
    """A child definition the worker refuses, with a fixed reason that never quotes the request."""


# Settled by the Session that opens a definition: `with_runtime_sandbox` replaces the sandbox and the
# working directory from the sandbox it borrows. A parent that served its skill sources sends none.
_RUNTIME_OWNED_AGENT_CONFIG_FIELDS = ("sandbox", "workdir", "skill_sources")

type FilesRoot = Callable[[str], str | None]
"""Where the worker's sandbox writes the files of a namespace such as ``/skills``, or None if it writes none."""

_SESSION_ID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")


def verified_child_definition(
    root: WorkflowHarnessDefinition,
    child: StartSessionRequest,
    skill_files: sandbox_skills.SandboxSkillFiles | None = None,
    files_root: FilesRoot | None = None,
) -> WorkflowHarnessDefinition:
    """The child's definition, derived from this worker's own agent; the request supplies only runtime state.

    The definition in the request is never run: only the fields its parent's runtime settled at open are
    taken from it. A forged definition is therefore ignored rather than compared, which also keeps a
    child working when its parent hands down a normalized form of the same configuration.

    Raises ``ChildDefinitionRefusal`` when the request has no lineage, when its lineage does not lead to its
    agent path and configuration, or when it names skill sources the derived definition does not have, or
    a skill the worker does not serve. `files_root` maps a skill folder to where the worker's sandbox
    writes it, so a skill the sandbox wrote under a folder of its own is served too.
    """

    lineage = child.lineage
    if lineage is None:
        raise ChildDefinitionRefusal("Child Session request carries no lineage, so its definition cannot be verified")
    if len(lineage.layers) != child.agent_path.count("/") - 1 or (
        not lineage.layers or lineage.layers[-1].config_name != child.config_name
    ):
        raise ChildDefinitionRefusal("Child Session lineage does not match its agent path and configuration")
    derived = root
    if lineage.root_customization is not None:
        customization = wire.SessionAgentCustomization.model_validate(lineage.root_customization)
        derived = derived.model_copy(
            update={"agent_config": assemble.with_session_agent_customization(derived.agent_config, customization)}
        )
    for layer in lineage.layers:
        derived = resolve_child_definition(derived, layer.config_name, instructions=layer.instructions)
    received = child.definition
    if received.agent_config.skill_sources not in (derived.agent_config.skill_sources, []):
        raise ChildDefinitionRefusal("Child Session definition does not match this agent's configuration")
    runtime_state: dict[str, object] = {
        name: getattr(received.agent_config, name) for name in _RUNTIME_OWNED_AGENT_CONFIG_FIELDS
    }
    runtime_state.update(_served_skill_catalog(received.agent_config.skills, derived, skill_files, files_root))
    return derived.model_copy(
        update={
            "session_id": str(child.session_id),
            "sandbox": received.sandbox,
            "agent_config": derived.agent_config.model_copy(update=runtime_state),
        }
    )


def _served_skill_catalog(
    received: Sequence[SessionSkillDefinition],
    derived: WorkflowHarnessDefinition,
    skill_files: sandbox_skills.SandboxSkillFiles | None,
    files_root: FilesRoot | None,
) -> dict[str, object]:
    """The skill catalog a parent served and its fingerprint, once every skill is one this worker serves.

    A catalog entry is a path the child's skill tool reads, and a Registry-shaped path makes the worker
    download that Registry skill. So a received skill must be one the derived definition declares, or a
    materialized skill at a path this worker writes or finds skills at. The fingerprint is computed from
    the catalog, never taken from the request.
    """

    declared = derived.agent_config.skills
    if list(received) == declared:
        return {"skills": declared, "skill_catalog_fingerprint": derived.agent_config.skill_catalog_fingerprint}
    served: list[MaterializedSkillDefinition] = []
    for skill in received:
        if not isinstance(skill, MaterializedSkillDefinition):
            raise ChildDefinitionRefusal("Child Session request lists an inline skill the agent does not declare")
        if skill not in declared and not _served_skill_path(skill, skill_files, files_root):
            raise ChildDefinitionRefusal(
                "Child Session request lists a skill outside the folders the worker serves skills from"
            )
        served.append(skill)
    return {"skills": served, "skill_catalog_fingerprint": calculate_skill_catalog_fingerprint(served)}


def _served_skill_path(
    skill: MaterializedSkillDefinition,
    skill_files: sandbox_skills.SandboxSkillFiles | None,
    files_root: FilesRoot | None,
) -> bool:
    path = skill.path
    if not path.startswith("/") or posixpath.normpath(path) != path:
        return False
    if not path.endswith("/" + contracts.SKILL_ENTRY_FILE):
        return False
    try:
        binding = registry_skills.registry_skill_binding(skill)
    except ValueError:
        return False
    if binding is not None:
        # A discovered Registry entry: only where the root publishes them, and only on a worker that discovers.
        _, root = binding
        return root in _folders(sandbox_skills.SKILLS_ROOT, files_root) and _discovers_registry_skills(skill_files)
    if path.startswith(sandbox_skills.SUBAGENT_SKILLS_ROOT + "/") or any(
        path.startswith(folder + "/") for folder in _folders(sandbox_skills.SKILLS_ROOT, files_root)
    ):
        return True
    if files_root is not None and any(
        path.startswith(folder + "/")
        # A child writes its own skills under its Session ID; a descendant that inherits them names that folder.
        for session_id in _SESSION_ID.findall(path)
        for folder in _folders(posixpath.join(sandbox_skills.SUBAGENT_SKILLS_ROOT, session_id), files_root)
    ):
        return True
    return skill_files is not None and any(_in_workspace_skills(path, found) for found in skill_files.workspace)


def _folders(namespace: str, files_root: FilesRoot | None) -> tuple[str, ...]:
    """The folder named `namespace` and the one the worker's sandbox writes it to, when that differs."""

    written = files_root(namespace) if files_root is not None else None
    return (namespace,) if written is None or written == namespace else (namespace, written)


def _discovers_registry_skills(skill_files: sandbox_skills.SandboxSkillFiles | None) -> bool:
    return skill_files is not None and any(
        isinstance(ref, dict) and ref.get("kind") == "all_registry" for ref in skill_files.refs
    )


def _in_workspace_skills(path: str, found: SandboxWorkspaceSkills) -> bool:
    """Whether `path` is a skill folder's entry under one of `found`'s folders, in its root or one repository below."""

    for folder in found.dirs:
        match = re.fullmatch(rf"(/.*)/{re.escape(folder)}/[^/]+/{re.escape(contracts.SKILL_ENTRY_FILE)}", path)
        if match is None:
            continue
        if found.root is None:
            # The sandbox workspace, which the child borrows from its root and which no request can move.
            return True
        base = match.group(1)
        if base == found.root or posixpath.dirname(base) == found.root:
            return True
    return False


__all__ = ["ChildDefinitionRefusal", "verified_child_definition"]
