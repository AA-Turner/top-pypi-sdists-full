from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, JsonValue

from mistralai.vibe.harness.runtime.capabilities.skills import SkillSourceFile, local_skill_folder
from mistralai.vibe_agents.sdk.authoring.errors import SdkError

from . import config, errors

if TYPE_CHECKING:
    from mistralai.vibe_agents.sdk.authoring.agent import Agent as UnifiedAgent
    from mistralai.vibe_agents.sdk.authoring.contracts import Harness as UnifiedHarness
    from mistralai.vibe_agents.sdk.authoring.contracts import HarnessSkill
    from mistralai.vibe_agents.sdk.authoring.subagent import Subagent
    from mistralai.vibe_agents.session_workflow.inputs import SubagentPolicy

    type AgentAppAgent = UnifiedAgent
    type AgentAppHarness = UnifiedHarness
else:
    type AgentAppAgent = object
    type AgentAppHarness = object


class ProjectSkill(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    content: str


class AgentApp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    root: Path
    agent: AgentAppAgent
    harness: AgentAppHarness
    skills: list[ProjectSkill]
    description: str | None


def load_app(root: Path) -> AgentApp:
    """Resolve a project directory into the Agent the CLI runs. Internal to `agents` and the worker.

    Not a supported way to get an Agent: an author builds one in Python and the CLI imports it, so a
    caller reaching for this is either the CLI, the worker, or a test standing in for one.
    """

    root = Path(root)
    try:
        config.reject_project_runtime_declaration(root)
    except ValueError as exc:
        raise errors.invalid_project_runtime(exc) from exc

    from mistralai.vibe_agents.sdk.app import entrypoint  # noqa: PLC0415

    spec = _resolve_entrypoint(root)
    try:
        agent = entrypoint.resolve_agent(spec, root)
    except errors.AgentProjectError:
        raise
    except SdkError as exc:
        raise errors.AgentProjectError(str(exc)) from exc

    agent._require_real_model()
    harness = agent._resolve_harness(None)
    _require_rebuildable_hooks(harness, agent.subagents)
    _require_permission_rules_matching_agent_tools(agent, harness)
    return AgentApp(
        name=agent.name,
        root=root,
        agent=agent,
        harness=harness,
        # The project catalog `agents info` and the deploy payload read. It lists the skills the
        # project ships; a Registry skill is already in the Registry.
        skills=_local_skill_catalog(harness.skills),
        description=agent.description,
    )


def _require_permission_rules_matching_agent_tools(agent: AgentAppAgent, harness: AgentAppHarness) -> None:
    """Fail before a deploy when a permission rule names one of the agent's namespaces but none of its tools."""

    from mistralai.vibe_agents.sdk.assembly import assemble  # noqa: PLC0415

    try:
        assemble.check_permission_policy_tools(agent._to_agent_config(), harness, agent.subagents)
    except SdkError as exc:
        raise errors.AgentProjectError(str(exc)) from exc


def _require_rebuildable_hooks(harness: AgentAppHarness, subagents: Sequence[Subagent]) -> None:
    """Fail when a worker could not rebuild one of the tree's Hooks, naming the Hook."""

    from mistralai.vibe_agents.sdk.assembly.stateful_hooks import check_hooks_rebuildable  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.assembly.subagents import authored_subagent_layers  # noqa: PLC0415

    try:
        check_hooks_rebuildable(
            [
                ((), (*harness.guardrails, *harness.hooks)),
                *((path, layer.hooks or ()) for path, layer in authored_subagent_layers(subagents)),
            ]
        )
    except SdkError as exc:
        raise errors.AgentProjectError(str(exc)) from exc


def declared_session_input_schemas(
    agent: AgentAppAgent, harness: AgentAppHarness | None = None
) -> dict[str, dict[str, JsonValue]]:
    """Map each Session input ID the agent's tools, hooks and sandbox hooks declare to its JSON Schema."""

    from mistralai.vibe_agents.sdk.assembly import assemble  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.authoring import session_input  # noqa: PLC0415

    return session_input.session_input_schemas(
        assemble.declared_session_input_classes(
            agent._to_agent_config(), agent._resolve_harness(harness), subagents=agent.subagents
        )
    )


def declared_subagent_policy(agent: AgentAppAgent) -> SubagentPolicy | None:
    """The subagent policy the agent registers as the default for its Session Trees.

    This is the code-declared `AgentConfig.subagent_policy`: the Agent's own policy, or the
    default one when it declares subagents and no policy. Any other agent reports none, so its
    Sessions run without subagents.
    """

    from mistralai.vibe_agents.session_workflow.inputs import SubagentPolicy  # noqa: PLC0415

    declared = agent._to_agent_config().effective_subagent_policy()
    if declared is None:
        return None
    return SubagentPolicy(
        concurrent_child_turn_limit=declared.concurrent_child_turn_limit,
        idle_message_starts=declared.idle_message_starts,
        max_depth=declared.max_depth,
    )


def _local_skill_catalog(harness_skills: Sequence[HarnessSkill]) -> list[ProjectSkill]:
    from mistralai.vibe_agents.sdk.authoring.contracts import LocalSkillBundle  # noqa: PLC0415

    skills: list[ProjectSkill] = []
    for bundle in harness_skills:
        if not isinstance(bundle, LocalSkillBundle):
            continue
        folder = local_skill_folder(
            [SkillSourceFile(path=file.path, content_base64=file.content_base64) for file in bundle.files]
        )
        skills.append(ProjectSkill(name=folder.name, description=folder.description, content=folder.body))
    return skills


def _resolve_entrypoint(root: Path) -> str:
    from mistralai.vibe_agents.sdk.app import entrypoint  # noqa: PLC0415

    try:
        declared = config.read_project_entrypoint_from_pyproject(root)
    except ValueError as exc:
        raise errors.AgentProjectError(str(exc)) from exc

    if declared is not None:
        return declared
    # Falling back to the default only pays off if its module is there; otherwise the resolver would
    # report a missing 'main' import, which reads like a typo rather than a project that never opted in.
    default_module = entrypoint.DEFAULT_ENTRYPOINT.split(":")[0]
    if not (root / f"{default_module}.py").is_file():
        raise errors.AgentProjectError(
            f"No agent found in {root.resolve()}. Put one in {default_module}.py as "
            f"`{entrypoint.DEFAULT_ENTRYPOINT.split(':')[1]} = agents.Agent(...)`, or name another "
            'module in pyproject.toml:\n\n  [tool.mistralai.agents]\n  entrypoint = "module:attr"'
        )
    return entrypoint.DEFAULT_ENTRYPOINT
