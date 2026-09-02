"""
Rebuilt Agent System - Proper architecture using core components.

Key Principles:
1. Agent uses UnifiedConfig directly (no modifications)
2. Prompts/PromptBuiltins are just sources to create agents
3. Variables are separate from config (applied when needed)
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from matrx_ai.agents.types import AgentConfig
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.unified_config import UnifiedConfig, UnifiedMessage
from matrx_ai.config.usage_config import AggregatedUsage, TokenUsage
from matrx_ai.orchestrator.executor import execute_ai_request
from matrx_ai.orchestrator.requests import CompletedRequest

# ============================================================================
# AGENT EXECUTE RESULT
# ============================================================================


@dataclass
class AgentExecuteResult:
    output: str
    assistant_response: UnifiedMessage | None
    config: UnifiedConfig
    usage: AggregatedUsage = field(default_factory=AggregatedUsage)
    usage_history: list[TokenUsage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# AGENT
# ============================================================================


class Agent:
    """
    An LLM Agent - UnifiedConfig + variable management.

    Core components:
    - config: UnifiedConfig (the actual dataclass, unmodified)
    - variable_defaults: Dict[str, AgentVariable] (defined variables)
    - variable_values: Dict[str, Any] (current values)

    Prompts/PromptBuiltins are sources to create agents, not core to the agent itself.
    """

    def __init__(
        self,
        config: UnifiedConfig,
        variable_defaults: dict[str, AgentVariable] | None = None,
        name: str | None = None,
        context_policies: list[dict[str, Any]] | None = None,
        output_schema: dict[str, Any] | None = None,
        auto_tools_disabled: bool = False,
        auto_context_disabled: bool = False,
        matrx_actions: dict[str, Any] | None = None,
    ):
        """
        Initialize agent with core components.

        Args:
            config: UnifiedConfig instance (the actual dataclass)
            variable_defaults: Dict of variable definitions
            name: Optional name for identification in logs
            context_policies: Agent-defined deferred context policy descriptors.
                           Carried from the DB record so callers (routers, tools,
                           sub-agents) can access slot metadata without a second
                           DB lookup.
        """
        self.name = name or "Agent"
        self.config = config
        self.variable_defaults = variable_defaults or {}
        self.context_policies: list[dict[str, Any]] = context_policies or []
        # Preserve the definition's tool-injection policy on direct/programmatic
        # runs. The host preparation hook reads this before merging any surface
        # or capability defaults.
        self.auto_tools_disabled: bool = auto_tools_disabled
        # Mirror of auto_tools_disabled for the context channel. Carried from the
        # DB record so every consumer (routers, sub-agents, the programmatic
        # runner) can honour it without a second lookup.
        self.auto_context_disabled: bool = auto_context_disabled
        self.output_schema: dict[str, Any] | None = output_schema
        # Opaque host-interpreted apply config (``agx_agent.matrx_actions``).
        # matrx-ai never reads its contents — it CARRIES it, exactly as
        # ``AgentConfig`` does, so a host that builds an Agent directly can put
        # the agent layer of its apply-policy cascade on the request context
        # without a second load of the same row. ``None`` = not declared.
        self.matrx_actions: dict[str, Any] | None = matrx_actions
        self.variable_values: dict[str, Any] = {}
        self._variables_applied = False

        self.request_metadata: dict[str, Any] = {}
        self.last_completed_request: CompletedRequest | None = None

        # Caller-supplied context objects for a direct/programmatic run — the
        # exact mirror of the HTTP request body's ``context`` dict (key →
        # content, or key → rich {"content": ..., ...}). The host's
        # programmatic-prepare hook merges these into its context-object
        # application; this package never interprets them. Set by callers such
        # as aidream's ``run_mandate`` consumption-map decomposition.
        self.request_context: dict[str, Any] = {}

        # Identity of the agx_agent record this agent was loaded from, when
        # applicable. Set by ``Agent.from_agent`` (the agx loader); stays None
        # for inline / prompt / builtin agents that have no agx_agent row.
        # ``run_agent`` reads these to stamp agent attribution onto the request
        # AppContext so cx_user_request.agent_id / cx_conversation.initial_agent_id
        # are never written NULL. See agents/source_tracking.py.
        self.source_id: str | None = None
        self.source_is_version: bool = False

    def clone(self) -> Agent:
        """
        Create a complete, independent copy of this agent.

        Deep copies all components:
        - config (UnifiedConfig with all messages)
        - variable_defaults (AgentVariable definitions)
        - variable_values (current variable values)

        Resets the variables_applied flag so clones can reapply variables to their copy.

        IMPORTANT: Best practice is to clone BEFORE applying variables or executing.
        If you clone after variables are applied, the placeholders ({{var}}) are gone,
        so setting new variables on the clone won't work as expected.

        Recommended pattern:
            base = await Agent.from_prompt("id")  # Don't apply variables yet
            agent1 = base.clone().with_variables(topic="AI")
            agent2 = base.clone().with_variables(topic="ML")

        Returns:
            New Agent instance (completely independent)
        """
        cloned = Agent(
            config=deepcopy(self.config),
            variable_defaults=deepcopy(self.variable_defaults),
            name=self.name,
            context_policies=list(self.context_policies),
            auto_tools_disabled=self.auto_tools_disabled,
            auto_context_disabled=self.auto_context_disabled,
            matrx_actions=self.matrx_actions,
        )
        # Copy variable_values but not the applied flag
        cloned.variable_values = {}  # Start fresh for new variables
        cloned.request_context = deepcopy(self.request_context)
        # Reset the applied flag
        cloned._variables_applied = False
        return cloned

    def clone_with_variables(self, **variables) -> Agent:
        """
        Clone and immediately set/apply variables (convenience method).

        Common pattern: Create base agent, then make variations with different variables.

        Args:
            **variables: Variable names and values to set and apply

        Returns:
            New Agent instance with variables applied

        Example:
            base = await Agent.from_prompt("prompt-id")

            # Create multiple variations
            agent_en = base.clone_with_variables(language="English")
            agent_es = base.clone_with_variables(language="Spanish")
            agent_fr = base.clone_with_variables(language="French")
        """
        return self.clone().with_variables(**variables)

    def clone_with_overrides(self, **overrides: Any) -> Agent:
        """Clone and immediately apply config overrides (convenience method)."""
        return self.clone().apply_config_overrides(**overrides)

    def clone_with(
        self,
        variables: dict[str, Any] | None = None,
        config_overrides: LLMParams | dict[str, Any] | None = None,
    ) -> Agent:
        """Clone and apply both variables and config overrides."""
        cloned = self.clone()

        if variables:
            cloned.with_variables(**variables)

        if config_overrides is not None:
            if isinstance(config_overrides, LLMParams):
                cloned.apply_config_overrides(overrides=config_overrides)
            else:
                cloned.apply_config_overrides(**config_overrides)

        return cloned

    def set_variable(self, name: str, value: Any) -> Agent:
        """
        Set a variable value.

        Args:
            name: Variable name
            value: Variable value (will be converted to string when replaced)

        Returns:
            Self (for method chaining)

        Example:
            agent.set_variable("topic", "AI Safety")
        """
        self.variable_values[name] = value
        return self

    def set_variables(self, **variables) -> Agent:
        """
        Set multiple variable values at once.

        Args:
            **variables: Variable names and values as kwargs

        Returns:
            Self (for method chaining)

        Example:
            agent.set_variables(topic="AI Safety", audience="developers")
        """
        self.variable_values.update(variables)
        return self

    def apply_variables(self, force: bool = False) -> Agent:
        """
        Apply variable replacements to the config.
        Replaces all {{variable_name}} placeholders in system_instruction and messages.

        Variables are only applied once by default to avoid issues with multi-turn conversations.
        Use force=True to reapply variables.

        Uses explicit values from ``variable_values`` when supplied, otherwise
        the saved Builder defaults. Variables with neither become "".

        Args:
            force: If True, apply variables even if already applied

        Returns:
            Self (for method chaining)

        Example:
            agent.set_variables(topic="AI", audience="devs").apply_variables()
        """
        # Skip if already applied (unless forced)
        if self._variables_applied and not force:
            return self

        # Build final values dict (variable_values + defaults)
        final_values = {}

        for var_name, var_def in self.variable_defaults.items():
            if var_name in self.variable_values:
                # Use explicitly set value
                final_values[var_name] = self.variable_values[var_name]
            else:
                # Use AgentVariable.get_value() to handle defaults and required
                final_values[var_name] = var_def.get_value()

        # Also include any variable_values that aren't in variable_defaults
        for var_name, var_value in self.variable_values.items():
            if var_name not in final_values:
                final_values[var_name] = var_value

        # Resolve explicit automatic-assignment markers from the trusted variable definition.
        # Structured-list choices become internal picklist refs and flow through the existing
        # secret-safe picklist resolver immediately below.
        final_values = _resolve_auto_assignment_final_values(self.variable_defaults, final_values)

        # Resolve picklist-bound variables (envelopes -> canonical placeholder tokens, plus
        # staged wire swaps that the executor injects into the provider send-clone only).
        # The authoritative list binding comes from variable_defaults, not the client value.
        # Covers the matrx-ai internal substitution chain (prompts / prompt-apps /
        # agent-blocks). Best-effort: any failure falls through to the replace_variables
        # tripwire, which keeps the raw envelope away from the model.
        final_values = _resolve_picklist_final_values(self.variable_defaults, final_values)

        # Use UnifiedConfig's replace_variables method
        self.config.replace_variables(final_values)

        # Mark as applied
        self._variables_applied = True

        return self

    def with_variables(self, **variables) -> Agent:
        """
        Set variables and apply them in one call (convenience method).
        This is the most common usage pattern.

        Args:
            **variables: Variable names and values as kwargs

        Returns:
            Self (for method chaining)

        Example:
            agent.with_variables(topic="AI Safety", audience="developers")
        """
        self.set_variables(**variables)
        self.apply_variables()
        return self

    def apply_config_overrides(
        self,
        overrides: LLMParams | None = None,
        **kwargs: Any,
    ) -> Agent:
        """Apply config overrides to the agent's UnifiedConfig.

        Accepts either a typed LLMParams instance (from API layer) or
        keyword arguments (for internal Python callers).

        Returns self for method chaining.
        """
        if overrides is not None:
            self.config.apply_overrides(overrides)
        if kwargs:
            self.config.apply_overrides(LLMParams(**kwargs))
        return self

    @classmethod
    def from_dict(
        cls,
        config_dict: dict[str, Any],
        variable_defaults: dict[str, AgentVariable] | None = None,
        variables: dict[str, Any] | None = None,
        config_overrides: LLMParams | dict[str, Any] | None = None,
    ) -> Agent:
        config = UnifiedConfig.from_dict(config_dict)
        agent = cls(config=config, variable_defaults=variable_defaults)

        if variables:
            agent.with_variables(**variables)

        if config_overrides is not None:
            if isinstance(config_overrides, LLMParams):
                agent.apply_config_overrides(overrides=config_overrides)
            else:
                agent.apply_config_overrides(**config_overrides)

        return agent

    @classmethod
    def _build_from_config(
        cls,
        agent_config: AgentConfig,
        variables: dict[str, Any] | None = None,
        config_overrides: LLMParams | dict[str, Any] | None = None,
    ) -> Agent:
        agent = cls(
            config=agent_config.config,
            variable_defaults=agent_config.variable_defaults,
            name=agent_config.name,
            context_policies=agent_config.context_policies,
            output_schema=agent_config.output_schema,
            auto_tools_disabled=agent_config.auto_tools_disabled,
            auto_context_disabled=agent_config.auto_context_disabled,
            matrx_actions=agent_config.matrx_actions,
        )
        if variables:
            agent.with_variables(**variables)
        if config_overrides is not None:
            if isinstance(config_overrides, LLMParams):
                agent.apply_config_overrides(overrides=config_overrides)
            else:
                agent.apply_config_overrides(**config_overrides)
        return agent

    @classmethod
    async def from_id(
        cls,
        prompt_id: str,
        variables: dict[str, Any] | None = None,
        config_overrides: LLMParams | dict[str, Any] | None = None,
        source: str | None = None,
    ) -> Agent:
        is_version = source in ("prompt_version", "builtin_version")
        return await cls.from_agent(
            prompt_id,
            is_version=is_version,
            variables=variables,
            config_overrides=config_overrides,
        )

    @classmethod
    async def from_prompt(
        cls,
        prompt_id: str,
        variables: dict[str, Any] | None = None,
        config_overrides: LLMParams | dict[str, Any] | None = None,
    ) -> Agent:
        return await cls.from_agent(
            prompt_id,
            variables=variables,
            config_overrides=config_overrides,
        )

    @classmethod
    async def from_builtin(
        cls,
        builtin_id: str,
        variables: dict[str, Any] | None = None,
        config_overrides: LLMParams | dict[str, Any] | None = None,
    ) -> Agent:
        return await cls.from_agent(
            builtin_id,
            variables=variables,
            config_overrides=config_overrides,
        )

    @classmethod
    async def from_agent(
        cls,
        agent_id: str,
        is_version: bool = False,
        variables: dict[str, Any] | None = None,
        config_overrides: LLMParams | dict[str, Any] | None = None,
    ) -> Agent:
        from matrx_ai.db.agx_manager import agx

        agent_config = await agx.load_for_execution(agent_id, is_version=is_version)
        agent = cls._build_from_config(agent_config, variables, config_overrides)
        # Carry the DB identity so run_agent can stamp agent attribution onto
        # the request context (the cx_* rows are written NULL otherwise).
        agent.source_id = agent_id
        agent.source_is_version = is_version
        return agent

    def set_user_input(self, user_input: str | list[dict[str, Any]]) -> Agent:
        self.config.append_or_extend_user_input(user_input)
        return self

    async def execute(
        self, user_input: str | list[dict[str, Any]] | None = None
    ) -> AgentExecuteResult:
        """Execute the agent with optional user input.

        Applies variables on first execution, appends user_input if provided,
        then delegates entirely to execute_ai_request() which reads all context
        (user_id, conversation_id, emitter, debug) from AppContext.

        This works identically whether called from an API route task, a tool
        spawning a sub-agent, or a local test script.
        """
        # Defaults are executable configuration too. In particular, a saved
        # document file_id must fill a template document block even when an
        # agent is invoked directly with no caller-provided variables.
        if (self.variable_values or self.variable_defaults) and not self._variables_applied:
            self.apply_variables()
        if user_input:
            self.set_user_input(user_input)

        # Edge normalization: a DB-loaded agent carries its tools as
        # ``agx_agent.tools`` UUIDs. The HTTP request path resolves them to
        # canonical names via ``merge_request_tools``; the direct-execution path
        # (every ``NamedAgent`` / ``run_agent`` internal call) does not. Resolve
        # here so a raw tool UUID can never reach the provider boundary. Idempotent
        # for already-name'd tool lists, so the HTTP path re-normalizing is a no-op.
        if self.config.tools:
            from matrx_ai.tools.merge import canonical_tool_names

            self.config.tools = canonical_tool_names(self.config.tools)

        # A host may own richer resource semantics than this standalone
        # package can know about. HTTP/workflow starts prepare those resources
        # before reaching matrx-ai; direct child agents do not, so invoke the
        # one host boundary hook here after variables + user input are final.
        from matrx_ai._ext import get_programmatic_agent_prepare_hook

        prepare_hook = get_programmatic_agent_prepare_hook()
        if prepare_hook is not None:
            from matrx_connect.context.app_context import (
                set_app_context,
                try_get_app_context,
            )

            current_ctx = try_get_app_context()
            if current_ctx is not None:
                prepared_ctx = await prepare_hook(agent=self, app_ctx=current_ctx)
                if prepared_ctx is not None and prepared_ctx is not current_ctx:
                    set_app_context(prepared_ctx)

        # Attribution tripwire: a DB-backed agent (loaded via Agent.from_agent)
        # MUST execute with its agent id stamped on the request context, or the
        # cx_* rows persist with NULL agent attribution — the failure that hid
        # every research / podcast / NER programmatic agent run from CX Explorer.
        # run_agent stamps it from source_id; this catches any path that runs a
        # DB agent WITHOUT going through run_agent. Loud, non-blocking for now.
        if self.source_id:
            from matrx_connect.context.app_context import try_get_app_context

            from matrx_ai.agents.source_tracking import warn_missing_agent_attribution

            _ctx = try_get_app_context()
            if _ctx is not None and not (_ctx.agent_id or _ctx.agent_version_id):
                warn_missing_agent_attribution(
                    _ctx,
                    handler="matrx_ai.agents.definition.Agent.execute",
                    label=self.name,
                )

        # Direct/programmatic children bypass the host HTTP merge funnel. Run
        # the package's canonical reconciliation unconditionally at the final
        # execution boundary so hard exclusions, executor viability, and the
        # delegation set cannot be inherited stale from a parent context.
        from matrx_connect.context.app_context import set_app_context, try_get_app_context

        from matrx_ai.tools.merge import (
            active_tool_executors,
            merge_request_tools,
        )

        execution_ctx = try_get_app_context()
        if execution_ctx is not None:
            execution_ctx = merge_request_tools(
                self.config,
                execution_ctx,
                [],
                active_executors=active_tool_executors(execution_ctx),
            )
            set_app_context(execution_ctx)

        completed = await execute_ai_request(
            self.config,
            metadata=self.request_metadata,
        )
        return self._clean_up_response(completed)

    def _clean_up_response(self, response: CompletedRequest) -> AgentExecuteResult:
        last_response = response.request.config.messages.get_last_by_role("assistant")
        last_output = response.request.config.get_last_output()
        self.config = response.request.config
        self.last_completed_request = response
        return AgentExecuteResult(
            output=last_output,
            assistant_response=last_response,
            config=self.config,
            usage=response.total_usage,
            usage_history=list(response.request.usage_history),
            metadata=response.metadata,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "config": self.config,
            "variable_defaults": self.variable_defaults,
            "variable_values": self.variable_values,
            "variables_applied": self._variables_applied,
            "context_policies": self.context_policies,
            "auto_context_disabled": self.auto_context_disabled,
        }


def _resolve_picklist_final_values(variable_defaults: dict, final_values: dict) -> dict:
    """Resolve picklist reference envelopes in ``final_values`` to canonical placeholder
    tokens, staging the secret descriptions for the provider send-clone. The authoritative
    list binding is read from ``variable_defaults`` (the agent definition). Best-effort —
    any failure returns ``final_values`` unchanged and the replace_variables tripwire keeps
    the raw envelope away from the model.
    """
    try:
        from matrx_ai.config.picklist_runtime import value_has_picklist_ref

        if not any(value_has_picklist_ref(v) for v in final_values.values()):
            return final_values

        from matrx_ai._ext import get_ext, has_ext
        from matrx_ai.agents.variables import picklist_bindings_from_variables

        if not has_ext("picklist_resolve_sync"):
            return final_values

        user_id = None
        try:
            from matrx_connect.context.app_context import get_app_context

            user_id = getattr(get_app_context(), "user_id", None)
        except Exception:
            user_id = None

        bindings = picklist_bindings_from_variables(variable_defaults)
        return get_ext("picklist_resolve_sync")(final_values, bindings=bindings, user_id=user_id)
    except Exception:
        return final_values


def _resolve_auto_assignment_final_values(variable_defaults: dict, final_values: dict) -> dict:
    from matrx_ai.agents.auto_assignment import (
        has_auto_assign_tag,
        random_assignment_bindings_from_variables,
    )

    if not any(has_auto_assign_tag(value) for value in final_values.values()):
        return final_values

    from matrx_ai._ext import get_ext, has_ext

    if not has_ext("auto_assign_resolve_sync"):
        raise RuntimeError(
            "An auto-assignment marker reached Agent.apply_variables, but this host has not "
            "configured auto_assign_resolve_sync."
        )
    bindings = random_assignment_bindings_from_variables(variable_defaults)
    return get_ext("auto_assign_resolve_sync")(final_values, bindings=bindings)
