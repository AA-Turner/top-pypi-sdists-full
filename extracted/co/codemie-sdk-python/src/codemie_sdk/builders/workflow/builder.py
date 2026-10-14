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

"""Fluent, immutable builder for :class:`WorkflowDefinition`.

Every mutator method returns a brand-new :class:`WorkflowBuilder`; the
receiver is never mutated. Internal state lives in a private, frozen
dataclass (`_BuilderState`) that is copied via `dataclasses.replace` on
every mutation, so independent branches of the same builder chain never
observe each other's changes.
"""

from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Any

from ...models.workflow import WorkflowMode
from .definition import (
    CustomWorkflowNode,
    WorkflowAssistant,
    WorkflowDefinition,
    WorkflowMCPServer,
    WorkflowNextState,
    WorkflowRetryPolicy,
    WorkflowState,
    WorkflowTool,
)
from .publish import _publish

if TYPE_CHECKING:
    from ...client.client import CodeMieClient


@dataclass(frozen=True)
class _BuilderState:
    """Immutable snapshot of everything a :class:`WorkflowBuilder` holds."""

    name: str
    description: str | None = None
    mode: WorkflowMode = WorkflowMode.SEQUENTIAL
    shared: bool = False
    icon_url: str | None = None
    assistants: dict[str, WorkflowAssistant] = field(default_factory=dict)
    tools: dict[str, WorkflowTool] = field(default_factory=dict)
    custom_nodes: dict[str, CustomWorkflowNode] = field(default_factory=dict)
    states: tuple[WorkflowState, ...] = ()


class WorkflowBuilder:
    """Fluent, immutable builder for a :class:`WorkflowDefinition`.

    Every method returns a new :class:`WorkflowBuilder`; the instance a
    method is called on is left completely untouched, so branching a
    builder into two independent chains is always safe.
    """

    def __init__(self, name: str | None = None, *, _state: _BuilderState | None = None):
        if _state is not None:
            self._state = _state
        else:
            if not name:
                raise ValueError("workflow name is required")
            self._state = _BuilderState(name=name)

    def _replaced(self, **changes: Any) -> "WorkflowBuilder":
        """Return a new builder wrapping a copy of this state with changes applied."""
        return WorkflowBuilder(_state=replace(self._state, **changes))

    def with_description(self, description: str) -> "WorkflowBuilder":
        return self._replaced(description=description)

    def with_mode(self, mode: WorkflowMode) -> "WorkflowBuilder":
        return self._replaced(mode=mode)

    def with_shared(self, shared: bool) -> "WorkflowBuilder":
        return self._replaced(shared=shared)

    def with_icon_url(self, icon_url: str) -> "WorkflowBuilder":
        return self._replaced(icon_url=icon_url)

    def add_assistant(
        self,
        id: str,
        *,
        system_prompt: str | None = None,
        assistant_id: str | None = None,
        **fields: Any,
    ) -> "WorkflowBuilder":
        """Register an inline assistant definition under the builder-local `id`.

        Raises `ValueError` if neither `system_prompt` nor `assistant_id` is
        given, mirroring the backend's `anyOf` requirement.
        """
        if system_prompt is None and assistant_id is None:
            raise ValueError(
                f"assistant {id!r} requires either system_prompt or assistant_id"
            )
        assistant = WorkflowAssistant(
            id=id,
            system_prompt=system_prompt,
            assistant_id=assistant_id,
            **fields,
        )
        return self._with_assistant(id, assistant)

    def add_assistant_ref(self, id: str, assistant_name: str) -> "WorkflowBuilder":
        """Register a deliberately unresolved, name-only assistant reference."""
        assistant = WorkflowAssistant(id=id, name=assistant_name)
        return self._with_assistant(id, assistant)

    def _with_assistant(
        self, id: str, assistant: WorkflowAssistant
    ) -> "WorkflowBuilder":
        if id in self._state.assistants:
            raise ValueError(f"duplicate assistant id: {id!r}")
        new_assistants = {**self._state.assistants, id: assistant}
        return self._replaced(assistants=new_assistants)

    def add_state(
        self,
        id: str,
        assistant: str,
        task: str,
        next: WorkflowNextState,
        *,
        retry_policy: WorkflowRetryPolicy | None = None,
        interrupt_before: bool = False,
        **fields: Any,
    ) -> "WorkflowBuilder":
        """Append a state that runs the assistant registered under `assistant`.

        Raises `ValueError` naming the id if `assistant` was not previously
        registered via `add_assistant`/`add_assistant_ref` on this chain.
        """
        if assistant not in self._state.assistants:
            raise ValueError(f"unknown assistant id: {assistant!r}")
        state = WorkflowState(
            id=id,
            assistant_id=assistant,
            task=task,
            next=next,
            retry_policy=retry_policy,
            interrupt_before=interrupt_before,
            **fields,
        )
        return self._with_state(state)

    def add_tool(
        self,
        id: str,
        tool: str,
        *,
        tool_args: dict | None = None,
        integration_alias: str | None = None,
        mcp_server: WorkflowMCPServer | None = None,
        **fields: Any,
    ) -> "WorkflowBuilder":
        """Declare a tool under `id` so tool states can run it.

        `tool` is the tool's name; `id` is what `add_tool_state` refers to.
        Set `mcp_server` for a tool that is served by an MCP server.
        """
        declared = WorkflowTool(
            id=id,
            tool=tool,
            tool_args=tool_args,
            integration_alias=integration_alias,
            mcp_server=mcp_server,
            **fields,
        )
        if id in self._state.tools:
            raise ValueError(f"duplicate tool id: {id!r}")
        return self._replaced(tools={**self._state.tools, id: declared})

    def add_custom_node(
        self,
        id: str,
        custom_node_id: str | None = None,
        *,
        name: str | None = None,
        model: str | None = None,
        system_prompt: str | None = None,
        config: dict | None = None,
    ) -> "WorkflowBuilder":
        """Declare a custom node under `id` so custom-node states can run it.

        `custom_node_id` is the kind of node (for example
        `"state_processor_node"`) and defaults to `id`, as on the platform.
        """
        node = CustomWorkflowNode(
            id=id,
            custom_node_id=custom_node_id or id,
            name=name,
            model=model,
            system_prompt=system_prompt,
            config=config or {},
        )
        if id in self._state.custom_nodes:
            raise ValueError(f"duplicate custom node id: {id!r}")
        return self._replaced(custom_nodes={**self._state.custom_nodes, id: node})

    def add_transform_node(
        self,
        id: str,
        mappings: list[dict],
        *,
        name: str | None = None,
        input_source: str | None = None,
        input_key: str | None = None,
        output_schema: dict | None = None,
        default_output: dict | None = None,
        on_error: str | None = None,
    ) -> "WorkflowBuilder":
        """Declare a transform node: a custom node that reshapes data without an LLM.

        Each mapping is a dict with an `output_field` and a `type`
        (`extract`, `template`, `condition`, `constant`, `script` or
        `array_map`) plus that type's own keys. Only the options you pass
        reach the node's config.
        """
        if not mappings:
            raise ValueError(f"transform node {id!r} needs at least one mapping")
        if any("output_field" not in mapping for mapping in mappings):
            raise ValueError(
                f"every mapping of transform node {id!r} needs an 'output_field'"
            )
        options = {
            "input_source": input_source,
            "input_key": input_key,
            "output_schema": output_schema,
            "default_output": default_output,
            "on_error": on_error,
        }
        config = {"mappings": list(mappings)}
        config.update(
            {key: value for key, value in options.items() if value is not None}
        )
        return self.add_custom_node(id, "transform_node", name=name, config=config)

    def add_tool_state(
        self,
        id: str,
        tool_id: str,
        next: WorkflowNextState,
        *,
        tool_args: dict | None = None,
        retry_policy: WorkflowRetryPolicy | None = None,
        interrupt_before: bool = False,
        **fields: Any,
    ) -> "WorkflowBuilder":
        """Append a state that runs the tool declared under `tool_id`.

        Raises `ValueError` if `tool_id` was not declared with `add_tool`.
        """
        if tool_id not in self._state.tools:
            raise ValueError(f"unknown tool id: {tool_id!r}")
        state = WorkflowState(
            id=id,
            tool_id=tool_id,
            tool_args=tool_args,
            next=next,
            retry_policy=retry_policy,
            interrupt_before=interrupt_before,
            **fields,
        )
        return self._with_state(state)

    def add_custom_node_state(
        self,
        id: str,
        custom_node_id: str,
        next: WorkflowNextState,
        *,
        task: str = "",
        retry_policy: WorkflowRetryPolicy | None = None,
        interrupt_before: bool = False,
        **fields: Any,
    ) -> "WorkflowBuilder":
        """Append a state that runs the custom node declared under `custom_node_id`.

        Works for transform nodes too. Raises `ValueError` if the node was not
        declared with `add_custom_node` or `add_transform_node`.
        """
        if custom_node_id not in self._state.custom_nodes:
            raise ValueError(f"unknown custom node id: {custom_node_id!r}")
        state = WorkflowState(
            id=id,
            custom_node_id=custom_node_id,
            task=task,
            next=next,
            retry_policy=retry_policy,
            interrupt_before=interrupt_before,
            **fields,
        )
        return self._with_state(state)

    def add_sub_workflow_state(
        self,
        id: str,
        workflow_id: str,
        next: WorkflowNextState,
        *,
        retry_policy: WorkflowRetryPolicy | None = None,
        interrupt_before: bool = False,
        **fields: Any,
    ) -> "WorkflowBuilder":
        """Append a state that runs another, already existing workflow."""
        state = WorkflowState(
            id=id,
            workflow_id=workflow_id,
            next=next,
            retry_policy=retry_policy,
            interrupt_before=interrupt_before,
            **fields,
        )
        return self._with_state(state)

    def _with_state(self, state: WorkflowState) -> "WorkflowBuilder":
        if any(existing.id == state.id for existing in self._state.states):
            raise ValueError(f"duplicate state id: {state.id!r}")
        return self._replaced(states=self._state.states + (state,))

    def render(self) -> WorkflowDefinition:
        """Build the final, immutable :class:`WorkflowDefinition`."""
        return WorkflowDefinition(
            name=self._state.name,
            description=self._state.description,
            mode=self._state.mode,
            shared=self._state.shared,
            icon_url=self._state.icon_url,
            assistants=dict(self._state.assistants),
            tools=list(self._state.tools.values()),
            custom_nodes=list(self._state.custom_nodes.values()),
            states=list(self._state.states),
        )

    def publish(
        self,
        client: "CodeMieClient",
        project: str,
        *,
        workflow_id: str | None = None,
    ) -> dict:
        """Render this builder's own state and create or update it on the live platform.

        Resolves every name-only assistant reference this builder holds
        against the live platform (scoped to `project`), renders the
        `yaml_config`, and dispatches to
        `WorkflowService.create_workflow`/`.update` — both used completely
        unmodified.

        Args:
            client: An authenticated `CodeMieClient`.
            project: Project the workflow belongs to; also scopes
                assistant-name resolution for any unresolved
                `WorkflowAssistant` reference.
            workflow_id: When given, updates that existing workflow instead
                of creating a new one.

        Returns:
            Whatever `WorkflowService.create_workflow`/`.update` returns
            today (currently the raw response `dict`, not a `Workflow`
            model).

        Raises:
            ValueError: An assistant name this builder holds matches zero or
                more than one assistant in `project`.
            Exception: Whatever `create_workflow`/`.update` raises
                (currently an unwrapped `requests.HTTPError` on backend
                rejection) propagates unchanged — never wrapped, reshaped,
                or swallowed here.
        """
        return _publish(client, self.render(), project, workflow_id=workflow_id)
