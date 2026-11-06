"""Authored child agents that carry their own tool functions and Hooks."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from mistralai.vibe.harness.app_server.session import McpHttpSourceConfiguration
from mistralai.vibe.harness.runtime.completion import CompletionConfig
from mistralai.workflows.plugins.mistralai.connectors import decorator as connector_decorator

from . import connector_selection, contracts, mcp_sources
from . import tool as tool_authoring
from . import types as authoring_types
from .errors import SdkError
from .skills import AllRegistrySkills, RegistrySkill


class Subagent:
    """A child agent that its parent starts with the ``agents.spawn`` tool.

    A subagent runs in its own session, below its parent's, as the user who started the root
    session. It uses the parent's value for every field you leave as ``None``. A field you set
    replaces the parent's value, and an empty list gives the subagent none: nothing is merged.

    ``model``, ``reasoning_effort`` and ``temperature`` follow the same rules as on
    ``agents.Agent``. ``provider`` needs ``model`` too. The parent's ``output_type`` never reaches
    a subagent: its result is its final answer.

    A subagent always runs under the root agent's permission policy and mode. To make it stricter,
    give it fewer tools.

    A subagent can have tools and hooks that its parent does not have. Their functions run where
    the parent's run. Tool names are shared by the whole tree, so two different
    functions cannot have the same name anywhere in it.

    Connectors: ``connectors=[]`` gives the subagent none. A list takes the same items as
    ``Agent(connectors=...)``: ``agents.connector(...)`` gives it exactly those connectors, and
    ``agents.all_connectors(...)`` gives it every connector the user can use.

    ``builtins`` is the one field that merges: each field you set in ``agents.Builtins(...)``
    replaces the parent's value, and each field you leave out keeps it. For example,
    ``agents.Builtins(skills=False)`` turns off only skills. Turning off ``programmatic_tool_calling``
    also needs ``subagents=False``. A subagent that sets its own skills or subagents needs that
    built-in on. ``sandbox_access`` sets the subagent's access to the sandbox the whole tree shares;
    a tree with no sandbox takes only ``"none"``.

    ``skills`` takes local bundles and registry skills. On a sandbox that holds files, a subagent's
    own skills are written into it when the subagent starts. ``agents.all_registry_skills()`` is for the
    root agent only: a subagent that leaves ``skills`` unset uses the root's skills.

    To add a tool to the parent's, pass the parent's list and the child's extended list::

        BASE = [lookup, search]
        agent = agents.Agent(
            model="mistral-large-4",
            tools=BASE,
            subagents=[
                agents.Subagent(
                    name="deployer",
                    description="Deploys a reviewed build.",
                    instructions="Deploy only what you are asked to deploy.",
                    tools=[*BASE, deploy],
                )
            ],
        )

    Args:
        name: The child's name, which the parent passes to ``agents.spawn``.
        description: What the child does, which the parent reads to choose it.
        instructions: The child's instructions, added to the agent loop's default system prompt.
        model: The model. ``None`` inherits the parent's.
        provider: The built-in completion provider, with ``model``. ``None`` inherits the parent's.
        completion: A completion configuration, used instead of ``provider``. ``None`` inherits the parent's.
        reasoning_effort: How much the model reasons. ``None`` inherits the parent's.
        temperature: The sampling temperature. ``None`` inherits the parent's.
        max_iterations: The most steps of the agent loop in one turn. ``None`` inherits the parent's.
        first_output_timeout_seconds: How long one model call waits for its first output. ``None``
            inherits the parent's.
        auto_compact_threshold: The number of tokens at which the loop summarizes older turns. ``None``
            inherits the parent's.
        tools: The child's tools. ``None`` inherits the parent's; ``[]`` gives it none.
        hooks: The child's hooks. ``None`` inherits the parent's; ``[]`` gives it none.
        mcps: The child's MCP servers, by name. ``None`` inherits the parent's; ``{}`` gives it none.
        connectors: The child's connectors. ``None`` inherits the parent's; ``[]`` gives it none.
        skills: The child's skills. ``None`` inherits the parent's; ``[]`` gives it none.
        subagents: The child's own subagents. ``None`` inherits the parent's; ``[]`` gives it none.
        builtins: The built-in features to change: each field set replaces the parent's. ``None``
            inherits them all.
        sandbox_access: The child's access to the tree's sandbox. ``None`` inherits the parent's.
    """

    __slots__ = (
        "_auto_compact_threshold",
        "_builtins",
        "_completion",
        "_connectors",
        "_connector_discovery",
        "_description",
        "_first_output_timeout_seconds",
        "_hooks",
        "_instructions",
        "_max_iterations",
        "_mcps",
        "_model",
        "_name",
        "_provider",
        "_reasoning_effort",
        "_sandbox_access",
        "_skills",
        "_subagents",
        "_temperature",
        "_tools",
    )

    def __init__(
        self,
        *,
        name: str,
        description: str,
        instructions: str,
        model: str | None = None,
        provider: authoring_types.LLMProvider | str | None = None,
        completion: CompletionConfig | None = None,
        reasoning_effort: authoring_types.ReasoningEffort | None = None,
        temperature: float | None = None,
        max_iterations: int | None = None,
        first_output_timeout_seconds: float | None = None,
        auto_compact_threshold: int | None = None,
        tools: contracts.HarnessTools | None = None,
        hooks: Sequence[contracts.Hook] | None = None,
        mcps: Mapping[str, McpHttpSourceConfiguration] | None = None,
        connectors: Sequence[contracts.HarnessConnector] | None = None,
        skills: Sequence[contracts.HarnessSkill] | None = None,
        subagents: Sequence[Subagent] | None = None,
        builtins: authoring_types.Builtins | None = None,
        sandbox_access: contracts.SandboxAccess | None = None,
    ) -> None:
        for field, value in (("name", name), ("description", description), ("instructions", instructions)):
            if not value.strip():
                raise SdkError(f"Subagent {field} must not be blank")
        if model is not None and not model.strip():
            raise SdkError(f"Subagent {name!r} model must not be blank; omit it to inherit")
        if provider is not None and completion is not None:
            raise SdkError(f"Subagent {name!r}: pass either provider or completion, not both")
        if provider is not None and model is None:
            raise SdkError(f"Subagent {name!r} sets provider, which needs model as well")
        if completion is not None and model is not None and completion.model != model:
            raise SdkError(f"Subagent {name!r} completion.model {completion.model!r} must match model {model!r}")
        if max_iterations is not None and max_iterations <= 0:
            raise SdkError(f"Subagent {name!r} max_iterations must be greater than 0; omit it to inherit")
        authoring_types.check_temperature(temperature, owner=f"Subagent {name!r}")
        if first_output_timeout_seconds is not None and first_output_timeout_seconds <= 0:
            raise SdkError(f"Subagent {name!r} first_output_timeout_seconds must be greater than 0")
        if auto_compact_threshold is not None and auto_compact_threshold <= 0:
            raise SdkError(f"Subagent {name!r} auto_compact_threshold must be greater than 0; omit it to inherit")
        if builtins is not None and not isinstance(builtins, authoring_types.Builtins):
            raise TypeError("Subagent builtins must be agents.Builtins")
        if sandbox_access is not None and sandbox_access not in contracts.SANDBOX_ACCESS_LEVELS:
            raise SdkError(
                f"Subagent {name!r} sandbox_access must be one of {contracts.SANDBOX_ACCESS_LEVELS}, "
                f"not {sandbox_access!r}"
            )
        if hooks is not None and any(not isinstance(hook, contracts.Hook) for hook in hooks):
            raise TypeError("Subagent hooks must subclass agents.Hook")
        connector_discovery = None
        if connectors is not None:
            try:
                connectors, connector_discovery = contracts.split_connectors(connectors, owner=f"Subagent {name!r}")
            except (TypeError, ValueError) as error:
                raise SdkError(str(error)) from error
        if mcps is not None:
            # Whether a source left at the default model_access is direct depends on the builtins
            # this Subagent inherits, so assembly checks those sources again once they are known.
            mcp_sources.check_mcp_sources(mcps, programmatic=None, owner=f"Subagent {name!r}")
            authored_tools = [
                *(tool_authoring.authored_tool(tool) for tool in tools or ()),
                *(tool for hook in hooks or () for tool in hook.tools),
            ]
            mcp_sources.refuse_tool_namespaces(authored_tools, mcps, subagent=(name,))
        for skill in skills or ():
            if isinstance(skill, AllRegistrySkills):
                raise TypeError(
                    "all_registry_skills() is only supported on the root Harness; omit Subagent skills to inherit"
                )
            if not isinstance(skill, contracts.LocalSkillBundle | RegistrySkill):
                raise TypeError("Subagent skills must be agents.LocalSkillBundle or agents.RegistrySkill")
        self._name = name
        self._description = description
        self._instructions = instructions
        self._model = model
        self._provider = provider
        self._completion = None if completion is None else completion.model_copy(deep=True)
        self._reasoning_effort = reasoning_effort
        self._temperature = temperature
        self._max_iterations = max_iterations
        self._first_output_timeout_seconds = first_output_timeout_seconds
        self._auto_compact_threshold = auto_compact_threshold
        self._tools = None if tools is None else tuple(tool_authoring.authored_tool(tool) for tool in tools)
        self._hooks = None if hooks is None else tuple(hooks)
        self._mcps = None if mcps is None else {key: source.model_copy(deep=True) for key, source in mcps.items()}
        self._connectors = None if connectors is None else tuple(connectors)
        self._connector_discovery = connector_discovery
        self._skills = None if skills is None else tuple(skills)
        self._subagents = None if subagents is None else tuple(subagents)
        self._builtins = builtins
        self._sandbox_access = sandbox_access

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def instructions(self) -> str:
        return self._instructions

    @property
    def model(self) -> str | None:
        return self._model

    @property
    def provider(self) -> authoring_types.LLMProvider | str | None:
        return self._provider

    @property
    def completion(self) -> CompletionConfig | None:
        return None if self._completion is None else self._completion.model_copy(deep=True)

    @property
    def reasoning_effort(self) -> authoring_types.ReasoningEffort | None:
        return self._reasoning_effort

    @property
    def temperature(self) -> float | None:
        return self._temperature

    @property
    def max_iterations(self) -> int | None:
        return self._max_iterations

    @property
    def first_output_timeout_seconds(self) -> float | None:
        return self._first_output_timeout_seconds

    @property
    def auto_compact_threshold(self) -> int | None:
        return self._auto_compact_threshold

    @property
    def tools(self) -> Sequence[contracts.HarnessTool] | None:
        return self._tools

    @property
    def hooks(self) -> Sequence[contracts.Hook] | None:
        return self._hooks

    @property
    def mcps(self) -> dict[str, McpHttpSourceConfiguration] | None:
        if self._mcps is None:
            return None
        return {key: source.model_copy(deep=True) for key, source in self._mcps.items()}

    @property
    def connectors(self) -> Sequence[connector_decorator.ConnectorSlot] | None:
        return self._connectors

    @property
    def connector_discovery(self) -> connector_selection.AllConnectors | None:
        return self._connector_discovery

    @property
    def skills(self) -> Sequence[contracts.HarnessSkill] | None:
        return self._skills

    @property
    def subagents(self) -> Sequence[Subagent] | None:
        return self._subagents

    @property
    def builtins(self) -> authoring_types.Builtins | None:
        return self._builtins

    @property
    def sandbox_access(self) -> contracts.SandboxAccess | None:
        return self._sandbox_access

    def __repr__(self) -> str:
        return f"Subagent(name={self._name!r})"


__all__ = ["Subagent"]
