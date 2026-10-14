# Copyright 2026 EPAM Systems, Inc. ("EPAM")
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Mirrored models for the typed workflow definition & builder.

These models structurally mirror (field-for-field, no code/package dependency)
the backend classes in
``codemie/src/codemie/core/workflow_models/workflow_models.py``.
"""

from typing import Callable, Literal

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

from ...models.assistant import MCPServerConfig
from ...models.workflow import WorkflowMode

# These models are the builder's own input surface, not API response models
# (which use `extra="ignore"` elsewhere in the SDK, see codemie-python/CLAUDE.md).
# A typo'd or renamed kwarg here changes workflow behaviour silently instead of
# erroring, so `extra="forbid"` catches it at construction time. `frozen=True`
# backs the builder's and this module's own "render() result is immutable, safe
# to branch and reuse" claim: without it, instances are shared across builder
# branches and `render()` calls, so mutating one leaks into every branch/render
# that still references it.
_MIRRORED_MODEL_CONFIG = ConfigDict(frozen=True, extra="forbid")


class WorkflowAssistantTool(BaseModel):
    """A tool reference attached to an inline :class:`WorkflowAssistant`."""

    model_config = _MIRRORED_MODEL_CONFIG

    name: str
    integration_alias: str | None = None


class WorkflowMCPServer(BaseModel):
    """An MCP server configuration attached to an inline :class:`WorkflowAssistant`.

    Structurally mirrors the fields of the backend's ``MCPServerDetails``
    (``codemie/src/codemie/rest_api/models/assistant.py``) that matter for the
    enabled-without-config check mirrored on :class:`WorkflowAssistant`.
    ``config`` reuses ``MCPServerConfig`` -- the exact type
    ``MCPServerDetails.config`` already has on the backend and on
    ``AssistantCreateRequest.mcp_servers[].config`` -- rather than a bare
    ``dict``: an earlier pass left it untyped even though the model it
    needed already lives in this same SDK package, with no cross-repo
    dependency to avoid.
    """

    model_config = _MIRRORED_MODEL_CONFIG

    name: str
    enabled: bool = True
    config: MCPServerConfig | None = None
    command: str | None = None
    mcp_config_id: str | None = None
    description: str | None = None
    mcp_connect_url: str | None = None
    integration_alias: str | None = None

    @field_validator("config", mode="before")
    @classmethod
    def reject_unknown_config_keys(cls, value):
        """`MCPServerConfig` silently ignores unknown keys, so a typo such as
        `comand` would vanish from the rendered YAML. Reject it instead."""
        if isinstance(value, dict):
            unknown = sorted(set(value) - set(MCPServerConfig.model_fields))
            if unknown:
                raise ValueError(
                    f"unknown MCP server config key(s): {', '.join(unknown)}"
                )
        return value

    @field_serializer("config")
    def render_only_the_keys_the_caller_set(
        self, config: MCPServerConfig | None
    ) -> dict | None:
        """`MCPServerConfig` fills in defaults (`args`, `headers`, `env`,
        `single_usage`). Rendering them would change every existing workflow
        that has an MCP server, so render only what the caller wrote."""
        if config is None:
            return None
        return config.model_dump(exclude_unset=True, exclude_none=True)


class WorkflowAssistant(BaseModel):
    """An inline assistant definition embedded in a workflow."""

    model_config = _MIRRORED_MODEL_CONFIG

    id: str | None = None
    assistant_id: str | None = None
    name: str | None = None
    model: str | None = None
    temperature: float | None = None
    system_prompt: str | None = None
    limit_tool_output_tokens: int | None = Field(default=10000)
    tools: list[WorkflowAssistantTool] = Field(default_factory=list)
    datasource_ids: list[str] | None = Field(default_factory=list)
    exclude_extra_context_tools: bool = False
    mcp_servers: list[WorkflowMCPServer] = Field(default_factory=list)
    skill_ids: list[str] | None = Field(default_factory=list)

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, value: float | None) -> float | None:
        """Reject a temperature outside the backend's supported 0..2 range."""
        if value is not None and not 0 <= value <= 2:
            raise ValueError(f"Temperature value should be 0..2, but set: '{value}'")
        return value

    @model_validator(mode="after")
    def validate_mcp_servers(self) -> "WorkflowAssistant":
        """Reject an enabled MCP server with no config/command/catalog reference.

        Mirrors the backend's ``WorkflowAssistant.validate_mcp_servers``.
        """
        for server in self.mcp_servers:
            if server.enabled and not (
                server.config is not None or server.command or server.mcp_config_id
            ):
                raise ValueError(
                    f"MCP server {server.name!r} is enabled but missing "
                    "configuration. Provide 'config', 'command', or "
                    "'mcp_config_id'."
                )
        return self

    @model_validator(mode="after")
    def validate_identity(self) -> "WorkflowAssistant":
        """Require at least one of system_prompt/assistant_id/name.

        A fully empty inline assistant can be neither rendered inline (no
        `system_prompt`), passed through pre-resolved (no `assistant_id`),
        nor resolved later (no `name`), so it is rejected at construction
        time with a clear message instead of failing confusingly downstream.
        """
        if (
            self.system_prompt is None
            and self.assistant_id is None
            and self.name is None
        ):
            raise ValueError(
                "WorkflowAssistant requires at least one of "
                "system_prompt, assistant_id, or name"
            )
        return self


class WorkflowTool(BaseModel):
    """A tool declared once per workflow and run by ``tool_id`` states.

    ``tool`` is the tool's name; ``id`` is what a state refers to.
    """

    model_config = _MIRRORED_MODEL_CONFIG

    id: str
    tool: str
    tool_args: dict | None = None
    integration_alias: str | None = None
    tool_result_json_pointer: str | None = None
    trace: bool = False
    mcp_server: WorkflowMCPServer | None = None
    resolve_dynamic_values_in_response: bool = False
    input_key: str | None = None
    tokens_size_limit: int | None = None


class CustomWorkflowNode(BaseModel):
    """A ready-made processing step declared once per workflow.

    ``id`` is what a state refers to; ``custom_node_id`` is the kind of node
    (for example ``transform_node``).
    """

    model_config = _MIRRORED_MODEL_CONFIG

    id: str
    custom_node_id: str
    name: str | None = None
    model: str | None = None
    system_prompt: str | None = None
    config: dict = Field(default_factory=dict)


class WorkflowStateCondition(BaseModel):
    """A boolean branch: evaluate ``expression`` and go to ``then``/``otherwise``."""

    model_config = _MIRRORED_MODEL_CONFIG

    expression: str
    then: str
    otherwise: str


class WorkflowStateSwitchCondition(BaseModel):
    """One ``condition`` -> ``state_id`` case inside a :class:`WorkflowStateSwitch`."""

    model_config = _MIRRORED_MODEL_CONFIG

    condition: str
    state_id: str


class WorkflowStateSwitch(BaseModel):
    """A multi-way branch evaluated case-by-case, falling back to ``default``."""

    model_config = _MIRRORED_MODEL_CONFIG

    cases: list[WorkflowStateSwitchCondition]
    default: str


class WorkflowRetryPolicy(BaseModel):
    """Per-state retry policy.

    Unlike the backend model (where every field is optional), the SDK's
    builder-level retry-policy call requires all four fields explicitly.
    """

    model_config = _MIRRORED_MODEL_CONFIG

    initial_interval: float
    backoff_factor: float
    max_interval: float
    max_attempts: int


class WorkflowNextState(BaseModel):
    """Where a state transitions to, and how context/history carry across it."""

    model_config = _MIRRORED_MODEL_CONFIG

    state_id: str | None = None
    state_ids: list[str] | None = None
    iter_key: str | None = None
    output_key: str | None = None
    condition: WorkflowStateCondition | None = None
    switch: WorkflowStateSwitch | None = None
    store_in_context: bool = True
    include_in_llm_history: bool = True
    clear_prior_messages: bool = False
    clear_context_store: bool | Literal["keep_current"] = False
    reset_keys_in_context_store: list[str] | None = None
    include_in_iterator_context: list[str] = Field(default_factory=lambda: ["*"])
    append_to_context: bool = False

    @model_validator(mode="after")
    def check_exclusive(self) -> "WorkflowNextState":
        """Reject setting more than one of state_id/state_ids/condition/switch."""
        set_groups = [self.state_id, self.state_ids, self.condition, self.switch]
        if sum(g is not None for g in set_groups) > 1:
            raise ValueError(
                "state_id/state_ids/condition/switch are mutually exclusive"
            )
        return self


class WorkflowState(BaseModel):
    """A single node in the workflow graph."""

    model_config = _MIRRORED_MODEL_CONFIG

    id: str
    assistant_id: str | None = None
    custom_node_id: str | None = None
    tool_id: str | None = None
    workflow_id: str | None = None
    task: str = ""
    next: WorkflowNextState
    retry_policy: WorkflowRetryPolicy | None = None
    interrupt_before: bool = False
    output_schema: str | None = None
    tool_args: dict | None = None
    resolve_dynamic_values_in_prompt: bool = False
    result_as_human_message: bool = False
    finish_iteration: bool = False

    @model_validator(mode="after")
    def check_state_type(self) -> "WorkflowState":
        """Require exactly one of assistant_id/custom_node_id/tool_id/workflow_id."""
        refs = [self.assistant_id, self.custom_node_id, self.tool_id, self.workflow_id]
        n = sum(r is not None for r in refs)
        if n == 0:
            raise ValueError(
                f"WorkflowState {self.id!r} needs exactly one of assistant_id/"
                "custom_node_id/tool_id/workflow_id, got none"
            )
        if n > 1:
            raise ValueError(
                f"WorkflowState {self.id!r} may set only one of assistant_id/"
                f"custom_node_id/tool_id/workflow_id, got {n}"
            )
        return self


class WorkflowDefinition(BaseModel):
    """A complete, typed workflow ready to render to the backend's YAML config."""

    model_config = _MIRRORED_MODEL_CONFIG

    name: str
    description: str | None = None
    mode: WorkflowMode
    shared: bool = False
    icon_url: str | None = None
    assistants: dict[str, WorkflowAssistant] = Field(default_factory=dict)
    tools: list[WorkflowTool] = Field(default_factory=list)
    custom_nodes: list[CustomWorkflowNode] = Field(default_factory=list)
    states: list[WorkflowState] = Field(default_factory=list)

    def to_yaml_config(
        self, resolve_assistant_name: Callable[[str], str] | None = None
    ) -> str:
        """Render the backend's flat ``yaml_config`` wire format.

        ``assistants``/``states`` are emitted as YAML lists (matching
        ``execution_config_schema.yaml``), and each state's own
        ``retry_policy``/``interrupt_before`` stay nested under that state's
        own entry rather than being hoisted to the top level.
        """
        payload = {
            "assistants": [
                self._resolve_assistant(key, assistant, resolve_assistant_name)
                for key, assistant in self.assistants.items()
            ],
            "tools": [tool.model_dump(exclude_none=True) for tool in self.tools],
            "custom_nodes": [
                node.model_dump(exclude_none=True) for node in self.custom_nodes
            ],
            "states": [state.model_dump(exclude_none=True) for state in self.states],
        }
        return yaml.safe_dump(
            payload, sort_keys=False, default_flow_style=False, allow_unicode=True
        )

    @staticmethod
    def _resolve_assistant(
        key: str,
        assistant: WorkflowAssistant,
        resolve_assistant_name: Callable[[str], str] | None,
    ) -> dict:
        """Dump one assistant, resolving a name-only reference if needed.

        Only a *name-only* reference (`name` set, `assistant_id` and
        `system_prompt` both unset) needs resolution. An inline assistant
        that also carries a `name` (e.g. for display) has `assistant_id is
        None` too, but its `system_prompt` makes it a complete inline
        definition, not a reference — it must pass through unresolved, or a
        same-named platform assistant silently takes its place.

        `assistant.id` is set from the dict key when the caller omitted it,
        so a `WorkflowAssistant` built without a builder (e.g. constructed
        directly in a `WorkflowDefinition.assistants` dict) still renders
        with the id the backend requires.
        """
        data = assistant.model_dump(exclude_none=True)
        data.setdefault("id", key)
        if (
            assistant.assistant_id is None
            and assistant.name is not None
            and assistant.system_prompt is None
        ):
            if resolve_assistant_name is None:
                raise ValueError(f"unresolved assistant reference: {assistant.name!r}")
            data["assistant_id"] = resolve_assistant_name(assistant.name)
        return data
