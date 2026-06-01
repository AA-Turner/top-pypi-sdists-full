#!/usr/bin/env python3
"""
⚠️  TEMPORARY DEVELOPMENT TOOL - WILL BE REPLACED BY MISTRAL AI STUDIO ⚠️

This script is a temporary CLI utility for local development and testing purposes only.
It will be deprecated and replaced by the Mistral AI Studio interface.

Kick off a workflow execution, stream its events, and interact when human input is required.

Example:
    python -m mistralai.workflows.scripts.dev_interactive_workflow_cli rfc_builder_workflow --input '{"content": "hello"}'
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import signal
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import IO, Any, Dict, List, Optional

import httpx
import jsonpatch  # type: ignore[import-untyped]
from dotenv import load_dotenv
from mistralai.client.sdk import Mistral
from pydantic import BaseModel, create_model
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

load_dotenv()

from mistralai.workflows.client import get_mistral_client, translate_model
from mistralai.workflows.protocol.v1.events import (
    CustomTaskCanceled,
    CustomTaskCompleted,
    CustomTaskFailed,
    CustomTaskInProgress,
    CustomTaskStarted,
    CustomTaskTimedOut,
    WorkflowEvent,
    WorkflowExecutionCanceled,
    WorkflowExecutionCompleted,
    WorkflowExecutionContinuedAsNew,
    WorkflowExecutionFailed,
    WorkflowExecutionStarted,
    WorkflowTaskFailed,
    WorkflowTaskTimedOut,
)
from mistralai.workflows.protocol.v1.streaming import StreamEventSsePayload

# ----- CLI helpers -----------------------------------------------------------


class GenericModel(BaseModel):
    class Config:
        extra = "allow"


class UpdateWorkflowInput(BaseModel):
    input: Any
    task_id: str


def parse_input(value: str) -> Any:
    """Parse JSON from a string or file path."""
    if os.path.exists(value):
        with open(value, "r", encoding="utf-8") as f:
            return json.load(f)
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:  # pragma: no cover - CLI helper
        raise argparse.ArgumentTypeError(f"Invalid JSON for --input: {exc}") from exc


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Execute a workflow and stream its events.")
    parser.add_argument("workflow_name", help="Name of the workflow to execute.")
    parser.add_argument(
        "--input",
        required=True,
        type=parse_input,
        help="Workflow input JSON (string or path to a JSON file).",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:7444",
        help="Workflows API base URL (default: http://localhost:7444).",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("MISTRAL_API_KEY"),
        help="Mistral API key for authorization (default: MISTRAL_API_KEY env var).",
    )
    parser.add_argument(
        "--stream",
        default="*",
        help="Stream name filter for SSE subscription (default: '*').",
    )
    parser.add_argument(
        "--update-name",
        default=None,
        help=(
            "Override the update name to reply with. "
            "Defaults to the custom_task_type from the stream (or 'wait_for_input')."
        ),
    )
    parser.add_argument(
        "--dump-raw-events",
        action="store_true",
        help=("If set, dump the raw SSE stream lines into an auto-generated file for later inspection."),
    )
    parser.add_argument(
        "--schema-display",
        choices=["human", "json-schema"],
        default="human",
        help=(
            "How to display input schema: 'human' for clean readable format, "
            "'json-schema' for full schema (default: human)."
        ),
    )
    return parser


# ----- Helpers for raw event dumping -----------------------------------------


def dump_sse_payload_to_file(payload: StreamEventSsePayload, sink: IO[str]) -> None:
    sink.write(f"data: {payload.model_dump_json()}\n\n")
    sink.flush()


# ----- Event rendering -------------------------------------------------------


def pretty_json(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False)


@dataclass
class TaskInfo:
    custom_task_id: str
    task_type: str = "unknown"
    status: str = "scheduled"
    payload: Any = None
    last_error: Optional[str] = None


@dataclass
class WorkflowExecutionInfo:
    """Tracks the state of a workflow execution."""

    workflow_exec_id: str
    workflow_name: str = "unknown"
    status: str = "unknown"
    input_data: Any = None
    result: Any = None
    last_error: Optional[str] = None
    new_execution_run_id: Optional[str] = None


@dataclass
class CustomTaskState:
    tasks: Dict[str, TaskInfo] = field(default_factory=dict)
    workflows: Dict[str, WorkflowExecutionInfo] = field(default_factory=dict)
    internal_status: str = ""

    def get_task(self, task_id: str) -> TaskInfo:
        if task_id not in self.tasks:
            self.tasks[task_id] = TaskInfo(custom_task_id=task_id)
        return self.tasks[task_id]

    def set_task_type(self, task_id: str, task_type: str) -> None:
        task = self.get_task(task_id)
        task.task_type = task_type

    def update_payload(self, task_id: str, payload: Any) -> None:
        task = self.get_task(task_id)
        task.payload = payload

    def update_status(self, task_id: str, status: str) -> None:
        task = self.get_task(task_id)
        task.status = status

    def record_error(self, task_id: str, error: str) -> None:
        task = self.get_task(task_id)
        task.last_error = error

    def get_type(self, task_id: str) -> str:
        return self.get_task(task_id).task_type

    # Workflow execution methods
    def get_workflow(self, workflow_exec_id: str) -> WorkflowExecutionInfo:
        if workflow_exec_id not in self.workflows:
            self.workflows[workflow_exec_id] = WorkflowExecutionInfo(workflow_exec_id=workflow_exec_id)
        return self.workflows[workflow_exec_id]

    def update_workflow_status(self, workflow_exec_id: str, status: str) -> None:
        workflow = self.get_workflow(workflow_exec_id)
        workflow.status = status

    def set_workflow_name(self, workflow_exec_id: str, workflow_name: str) -> None:
        workflow = self.get_workflow(workflow_exec_id)
        workflow.workflow_name = workflow_name

    def set_workflow_input(self, workflow_exec_id: str, input_data: Any) -> None:
        workflow = self.get_workflow(workflow_exec_id)
        workflow.input_data = input_data

    def set_workflow_result(self, workflow_exec_id: str, result: Any) -> None:
        workflow = self.get_workflow(workflow_exec_id)
        workflow.result = result

    def record_workflow_error(self, workflow_exec_id: str, error: str) -> None:
        workflow = self.get_workflow(workflow_exec_id)
        workflow.last_error = error

    def set_workflow_continued_as_new(self, workflow_exec_id: str, new_run_id: str) -> None:
        workflow = self.get_workflow(workflow_exec_id)
        workflow.new_execution_run_id = new_run_id


# Type adapter for parsing workflow events


def _set_value_at_path(obj: Any, path: str, value: Any) -> Any:
    """Set a value at a JSON pointer path, returning the modified object."""
    if not path or path == "/":
        return value
    parts = path.split("/")[1:]  # Skip empty string before first /
    current = obj
    for part in parts[:-1]:
        if isinstance(current, dict):
            current = current[part]
        elif isinstance(current, list):
            current = current[int(part)]
    # Set the final value
    final_key = parts[-1]
    if isinstance(current, dict):
        current[final_key] = value
    elif isinstance(current, list):
        current[int(final_key)] = value
    return obj


def _get_value_at_path(obj: Any, path: str) -> Any:
    """Get value at a JSON pointer path."""
    if not path or path == "/":
        return obj
    parts = path.split("/")[1:]  # Skip empty string before first /
    current = obj
    for part in parts:
        if current is None:
            return None
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return current


def _apply_json_patches(patches: List[Dict[str, Any]], obj: Any) -> Any:
    """
    Apply JSON patches with support for the custom "append" operation.

    The "append" operation is used for efficient string streaming where
    text is appended to an existing string value.
    """
    import copy

    result = copy.deepcopy(obj)

    # Separate standard patches from custom "append" patches
    standard_patches = []
    append_patches = []

    for patch in patches:
        if patch.get("op") == "append":
            append_patches.append(patch)
        else:
            standard_patches.append(patch)

    # Apply standard patches first using jsonpatch library
    if standard_patches:
        result = jsonpatch.JsonPatch(standard_patches).apply(result, in_place=False)

    # Apply custom "append" patches
    for patch in append_patches:
        path = patch["path"]
        value = patch.get("value", "")
        current_value = _get_value_at_path(result, path)
        if isinstance(current_value, str) and isinstance(value, str):
            new_value = current_value + value
            result = _set_value_at_path(result, path, new_value)

    return result


class EventView:
    def __init__(self, state: CustomTaskState, console: Optional[Console] = None):
        self.state = state
        self.console = console or Console()
        self.last_stream = ""
        self.last_seq: Optional[int] = None
        self.last_timestamp = ""
        self.last_event: Optional[WorkflowEvent] = None

    def apply_event(self, payload: StreamEventSsePayload) -> None:
        self.last_stream = payload.stream
        self.last_seq = payload.broker_sequence
        self.last_timestamp = str(payload.timestamp) if payload.timestamp else ""

        event = payload.data
        self.last_event = event

        # Handle custom task events
        if isinstance(event, CustomTaskStarted):
            started_attrs = event.attributes
            self.state.set_task_type(started_attrs.custom_task_id, started_attrs.custom_task_type)
            self.state.update_payload(started_attrs.custom_task_id, started_attrs.payload.value)
            self.state.update_status(started_attrs.custom_task_id, "started")

        elif isinstance(event, CustomTaskInProgress):
            in_progress_attrs = event.attributes
            payload_data = in_progress_attrs.payload
            if payload_data.type == "json_patch":
                # Apply JSON patches (with custom "append" op support)
                patches = [p.model_dump() for p in payload_data.value]
                previous = self.state.get_task(in_progress_attrs.custom_task_id).payload or {}
                try:
                    updated = _apply_json_patches(patches, previous)
                except Exception as exc:  # pragma: no cover - defensive
                    self.state.record_error(in_progress_attrs.custom_task_id, str(exc))
                    return
                self.state.update_payload(in_progress_attrs.custom_task_id, updated)
            else:
                # JSON payload - replace entirely
                self.state.update_payload(in_progress_attrs.custom_task_id, payload_data.value)
            self.state.update_status(in_progress_attrs.custom_task_id, "in_progress")

        elif isinstance(event, CustomTaskCompleted):
            completed_attrs = event.attributes
            self.state.update_status(completed_attrs.custom_task_id, "completed")
            self.state.update_payload(completed_attrs.custom_task_id, completed_attrs.payload.value)

        elif isinstance(event, CustomTaskFailed):
            failed_attrs = event.attributes
            self.state.update_status(failed_attrs.custom_task_id, "failed")
            self.state.record_error(failed_attrs.custom_task_id, failed_attrs.failure.message)

        elif isinstance(event, CustomTaskTimedOut):
            timed_out_attrs = event.attributes
            self.state.update_status(timed_out_attrs.custom_task_id, "timed_out")
            if timed_out_attrs.timeout_type:
                self.state.record_error(timed_out_attrs.custom_task_id, f"Timeout: {timed_out_attrs.timeout_type}")

        elif isinstance(event, CustomTaskCanceled):
            canceled_attrs = event.attributes
            self.state.update_status(canceled_attrs.custom_task_id, "canceled")
            if canceled_attrs.reason:
                self.state.record_error(canceled_attrs.custom_task_id, f"Canceled: {canceled_attrs.reason}")

        # Handle workflow execution events
        elif isinstance(event, WorkflowExecutionStarted):
            wf_started_attrs = event.attributes
            self.state.set_workflow_name(event.workflow_exec_id, wf_started_attrs.workflow_name)
            self.state.set_workflow_input(event.workflow_exec_id, wf_started_attrs.input.value)
            self.state.update_workflow_status(event.workflow_exec_id, "started")

        elif isinstance(event, WorkflowExecutionCompleted):
            wf_completed_attrs = event.attributes
            self.state.set_workflow_result(event.workflow_exec_id, wf_completed_attrs.result.value)
            self.state.update_workflow_status(event.workflow_exec_id, "completed")

        elif isinstance(event, WorkflowExecutionFailed):
            wf_failed_attrs = event.attributes
            self.state.update_workflow_status(event.workflow_exec_id, "failed")
            self.state.record_workflow_error(event.workflow_exec_id, wf_failed_attrs.failure.message)

        elif isinstance(event, WorkflowExecutionCanceled):
            wf_canceled_attrs = event.attributes
            self.state.update_workflow_status(event.workflow_exec_id, "canceled")
            if wf_canceled_attrs.reason:
                self.state.record_workflow_error(event.workflow_exec_id, f"Canceled: {wf_canceled_attrs.reason}")

        elif isinstance(event, WorkflowExecutionContinuedAsNew):
            continued_attrs = event.attributes
            self.state.update_workflow_status(event.workflow_exec_id, "continued_as_new")
            self.state.set_workflow_continued_as_new(event.workflow_exec_id, continued_attrs.new_execution_run_id)

        elif isinstance(event, WorkflowTaskTimedOut):
            wf_timed_out_attrs = event.attributes
            self.state.update_workflow_status(event.workflow_exec_id, "task_timed_out")
            if wf_timed_out_attrs.timeout_type:
                timeout_msg = f"Task timeout: {wf_timed_out_attrs.timeout_type}"
                self.state.record_workflow_error(event.workflow_exec_id, timeout_msg)

        elif isinstance(event, WorkflowTaskFailed):
            wf_failed_task_attrs = event.attributes
            self.state.update_workflow_status(event.workflow_exec_id, "task_failed")
            self.state.record_workflow_error(event.workflow_exec_id, wf_failed_task_attrs.failure.message)

    def render(self) -> Panel:
        from rich.console import Group

        # Build workflow execution table
        workflow_table = Table(title="Workflow Executions", show_lines=False, pad_edge=False)
        workflow_table.add_column("Execution ID", overflow="fold")
        workflow_table.add_column("Workflow Name")
        workflow_table.add_column("Status")
        workflow_table.add_column("Result/Error")

        for workflow in self.state.workflows.values():
            result_preview = ""
            if workflow.result is not None:
                result_preview = pretty_json(workflow.result)
                if len(result_preview) > 200:
                    result_preview = result_preview[:200] + " ... (truncated)"
            elif workflow.last_error:
                result_preview = f"⚠ {workflow.last_error}"
            elif workflow.new_execution_run_id:
                result_preview = f"→ {workflow.new_execution_run_id}"

            workflow_table.add_row(
                workflow.workflow_exec_id,
                workflow.workflow_name,
                workflow.status,
                result_preview,
            )

        # Build custom tasks table
        task_table = Table(title="Custom Tasks", show_lines=False, pad_edge=False)
        task_table.add_column("ID", overflow="fold")
        task_table.add_column("Type")
        task_table.add_column("Status")
        task_table.add_column("Payload (last)")

        for task in self.state.tasks.values():
            payload_preview = ""
            if task.payload is not None:
                payload_preview = pretty_json(task.payload)
                # if len(payload_preview) > 600:
                #     payload_preview = payload_preview[:600] + " ... (truncated)"
            status = task.status
            if task.last_error:
                status += f" ⚠ {task.last_error}"
            task_table.add_row(task.custom_task_id, task.task_type, status, payload_preview)

        header = f"{self.last_stream} · seq {self.last_seq} · {self.last_timestamp}"
        subtitle = self.state.internal_status or "Streaming…"

        # Combine tables - show workflow table only if there are workflows
        content: Group | Table
        if self.state.workflows:
            content = Group(workflow_table, "", task_table)
        else:
            content = task_table

        return Panel(content, title=header, subtitle=subtitle, border_style="cyan")


def is_le_chat_human_feedback(initial_payload: Any) -> bool:
    """
    Identify a LeChatPayloadHumanFeedback payload.

    Based on examples/workflow_rfc_streaming.py and protocol streaming payloads:
    the presence of input_schema.
    """
    if not isinstance(initial_payload, dict):
        return False
    return "input_schema" in initial_payload


# ----- Workflow runner -------------------------------------------------------


@dataclass
class SchemaNode:
    """AST node for schema representation."""

    kind: str  # "primitive", "object", "array", "union", "enum", "literal"
    value: Any = None  # For primitives/literals
    children: List[Any] = field(default_factory=list)  # For compound types
    props: Dict[str, Any] = field(default_factory=dict)  # For objects (name -> (node, required))


class SchemaFormatter:
    """Convert JSON schema to human-readable format with smart indentation."""

    MAX_LINE_WIDTH = 80
    INDENT = "  "

    TYPE_MAP = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "null": "null",
    }

    def __init__(self, schema: Any):
        self.defs = schema.get("$defs", {}) if isinstance(schema, dict) else {}

    def format(self, schema: Any) -> str:
        """Format the schema with smart indentation."""
        node = self._parse(schema)
        return self._render(node, 0)

    def _parse(self, schema: Any) -> SchemaNode:
        """Parse JSON schema into AST."""
        if not isinstance(schema, dict):
            return SchemaNode(kind="primitive", value=str(schema))

        # Handle $ref
        if "$ref" in schema:
            ref_path = schema["$ref"]
            if ref_path.startswith("#/$defs/"):
                ref_name = ref_path[len("#/$defs/") :]
                if ref_name in self.defs:
                    return self._parse(self.defs[ref_name])
                return SchemaNode(kind="primitive", value=ref_name)
            return SchemaNode(kind="primitive", value=ref_path)

        # Handle anyOf / oneOf (union types)
        for union_key in ("anyOf", "oneOf"):
            if union_key in schema:
                options = schema[union_key]
                children = []
                for opt in options:
                    if isinstance(opt, dict) and opt.get("type") == "null":
                        children.append(SchemaNode(kind="primitive", value="null"))
                    else:
                        children.append(self._parse(opt))
                return SchemaNode(kind="union", children=children)

        # Handle allOf
        if "allOf" in schema:
            children = [self._parse(s) for s in schema["allOf"]]
            return SchemaNode(kind="allof", children=children)

        # Handle const
        if "const" in schema:
            return SchemaNode(kind="literal", value=json.dumps(schema["const"]))

        # Handle enum
        if "enum" in schema:
            values = [json.dumps(v) for v in schema["enum"]]
            return SchemaNode(kind="enum", children=values)

        schema_type = schema.get("type")

        # Handle arrays
        if schema_type == "array":
            items = schema.get("items", {})
            item_node = self._parse(items)
            return SchemaNode(kind="array", children=[item_node])

        # Handle objects
        if schema_type == "object":
            properties = schema.get("properties", {})
            required = set(schema.get("required", []))

            if not properties:
                additional = schema.get("additionalProperties")
                if additional and additional is not True:
                    val_node = self._parse(additional)
                    return SchemaNode(kind="dict", children=[val_node])
                return SchemaNode(kind="primitive", value="{...}")

            props = {}
            for prop_name, prop_schema in properties.items():
                prop_node = self._parse(prop_schema)
                props[prop_name] = (prop_node, prop_name in required)
            return SchemaNode(kind="object", props=props)

        # Handle primitive types
        if schema_type in self.TYPE_MAP:
            return SchemaNode(kind="primitive", value=self.TYPE_MAP[schema_type])

        # Handle multiple types
        if isinstance(schema_type, list):
            children = [SchemaNode(kind="primitive", value=self.TYPE_MAP.get(t, t)) for t in schema_type]
            return SchemaNode(kind="union", children=children)

        # Fallback
        return SchemaNode(kind="primitive", value=str(schema_type) if schema_type else "any")

    def _indent_block(self, text: str, indent: str, first_line: bool = False) -> str:
        """Indent all lines of a multi-line string."""
        lines = text.split("\n")
        if first_line:
            return "\n".join(indent + line for line in lines)
        return lines[0] + "\n" + "\n".join(indent + line for line in lines[1:])

    def _render(self, node: SchemaNode, indent_level: int) -> str:
        """Render AST node to string. Returns unindented content."""
        ind = self.INDENT

        if node.kind == "primitive":
            return node.value  # type: ignore

        if node.kind == "literal":
            return node.value  # type: ignore

        if node.kind == "enum":
            single = " | ".join(node.children)
            if len(single) <= self.MAX_LINE_WIDTH:
                return single
            return ("\n" + ind + "| ").join(node.children)

        if node.kind == "union":
            parts = [self._render(c, indent_level) for c in node.children]
            single = " | ".join(parts)
            if len(single) <= self.MAX_LINE_WIDTH and "\n" not in single:
                return single
            # Multi-line union
            result_lines = []
            for i, p in enumerate(parts):
                if i == 0:
                    result_lines.append(p)
                else:
                    if "\n" in p:
                        # Indent continuation lines of multi-line part
                        p_lines = p.split("\n")
                        result_lines.append(f"| {p_lines[0]}")
                        for pl in p_lines[1:]:
                            result_lines.append(f"  {pl}")
                    else:
                        result_lines.append(f"| {p}")
            return "\n".join(result_lines)

        if node.kind == "allof":
            parts = [self._render(c, indent_level) for c in node.children]
            return " & ".join(parts)

        if node.kind == "array":
            item_str = self._render(node.children[0], indent_level)
            single = f"[{item_str}, ...]"
            if len(single) <= self.MAX_LINE_WIDTH and "\n" not in item_str:
                return single
            # Multi-line array - indent item content
            item_lines = item_str.split("\n")
            lines = ["["]
            for il in item_lines:
                lines.append(f"{ind}{il}")
            lines.append(f"{ind}...")
            lines.append("]")
            return "\n".join(lines)

        if node.kind == "dict":
            val_str = self._render(node.children[0], indent_level)
            return f"{{str: {val_str}}}"

        if node.kind == "object":
            # Build property strings
            prop_items = []
            for prop_name, (prop_node, is_required) in node.props.items():
                suffix = "" if is_required else "?"
                prop_val = self._render(prop_node, indent_level)
                prop_items.append((f'"{prop_name}"{suffix}', prop_val))

            # Try single line
            single_parts = [f"{k}: {v}" for k, v in prop_items]
            single = "{" + ", ".join(single_parts) + "}"
            if len(single) <= self.MAX_LINE_WIDTH and "\n" not in single:
                return single

            # Multi-line object
            lines = ["{"]
            for i, (key, val) in enumerate(prop_items):
                comma = "," if i < len(prop_items) - 1 else ""
                if "\n" in val:
                    val_lines = val.split("\n")
                    lines.append(f"{ind}{key}: {val_lines[0]}")
                    for vl in val_lines[1:]:
                        lines.append(f"{ind}{ind}{vl}")
                    if comma:
                        lines[-1] = lines[-1] + comma
                else:
                    lines.append(f"{ind}{key}: {val}{comma}")
            lines.append("}")
            return "\n".join(lines)

        return str(node)


def schema_to_human_readable(schema: Any, defs: Optional[Dict[str, Any]] = None) -> str:
    """Convert a JSON schema to a human-readable format."""
    if not isinstance(schema, dict):
        return str(schema)
    formatter = SchemaFormatter(schema)
    return formatter.format(schema)


async def prompt_for_json(schema_hint: Any, console: Console, schema_display: str = "human") -> Optional[Any]:
    """Prompt the user for JSON input. Empty input means skip."""
    if schema_hint:
        if schema_display == "human":
            display_text = schema_to_human_readable(schema_hint)
            console.print(Panel(display_text, title="Input schema (hint)", border_style="cyan"))
        else:
            # json-schema mode: show full schema without $defs for brevity
            display_schema = schema_hint
            if isinstance(schema_hint, dict) and "$defs" in schema_hint:
                display_schema = {k: v for k, v in schema_hint.items() if k != "$defs"}
            console.print(Panel(pretty_json(display_schema), title="Input schema (hint)", border_style="cyan"))

    while True:
        user_text = await asyncio.to_thread(console.input, "Enter JSON input for the workflow (blank to skip): ")
        if user_text.strip() == "":
            return None
        try:
            return json.loads(user_text)
        except json.JSONDecodeError as exc:
            console.print(f"[red]Invalid JSON[/]: {exc}. Please try again.")


async def start_workflow(
    client: Mistral,
    workflow_name: str,
    workflow_input: BaseModel | None,
    console: Optional[Console] = None,
) -> str:
    response = await client.workflows.execute_workflow_async(
        workflow_identifier=workflow_name,
        input=workflow_input,
        deployment_name="default",
    )
    execution_id = response.execution_id
    start_console = console or Console()
    start_console.print(f"[green]Started workflow[/] '{workflow_name}' with execution id: {execution_id}")
    return execution_id


async def send_update(
    client: Mistral,
    workflow_exec_id: str,
    update_name: str,
    custom_task_id: str,
    user_input: Any,
) -> None:
    await client.workflows.executions.update_workflow_execution_async(
        execution_id=workflow_exec_id,
        name=update_name,
        input=UpdateWorkflowInput(input=user_input, task_id=custom_task_id).model_dump(mode="json"),
    )
    # Keep console clean; rely on live view.


async def stream_workflow(
    client: Mistral,
    workflow_exec_id: str,
    stream: str,
    custom_task_state: CustomTaskState,
    update_name_override: Optional[str] = None,
    dump_raw_events: bool = False,
    schema_display: str = "human",
    console: Optional[Console] = None,
) -> None:
    stream_console = console or Console(force_terminal=True, soft_wrap=True)
    view = EventView(custom_task_state, console=stream_console)

    dump_file = None
    dump_path: Optional[Path] = None
    if dump_raw_events:
        try:
            # ISO 8601 format with seconds, POSIX-safe filename (no colons)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            dump_path = Path.cwd() / f"sse_events_{timestamp}.sse.log"
            dump_file = dump_path.open("w", encoding="utf-8")
            stream_console.print(
                Panel(
                    f"Dumping raw SSE events to [bold]{dump_path}[/]",
                    border_style="green",
                )
            )
        except OSError as exc:  # pragma: no cover - filesystem error handling
            dump_file = None
            dump_path = None
            stream_console.print(f"[red]Failed to create raw event dump file: {exc}. Continuing without dumping.[/]")

    try:
        stream_console.print(
            Panel(
                f"Connected to stream [bold]{stream}[/] for execution [bold]{workflow_exec_id}[/]",
                border_style="blue",
            )
        )

        try:
            event_stream = await client.workflows.events.get_stream_events_async(
                workflow_exec_id=workflow_exec_id,
                stream=stream,
            )
            async with event_stream:
                async for sse_event in event_stream:
                    raw = sse_event.data
                    if raw is None:
                        continue
                    try:
                        payload = translate_model(StreamEventSsePayload, raw)
                    except Exception:
                        continue

                    if dump_file:
                        dump_sse_payload_to_file(payload, dump_file)

                    view.apply_event(payload)
                    stream_console.print(view.render())

                    # Check for terminal workflow events - exit stream when workflow completes
                    event = view.last_event
                    if isinstance(
                        event, (WorkflowExecutionCompleted, WorkflowExecutionFailed, WorkflowExecutionCanceled)
                    ):
                        terminal_status = event.event_type.replace("WORKFLOW_EXECUTION_", "").lower()
                        stream_console.print(
                            Panel(
                                f"[green]Workflow {terminal_status}.[/]",
                                title="Workflow Finished",
                                border_style="green" if terminal_status == "completed" else "yellow",
                            )
                        )
                        break

                    # Check if this is a CustomTaskStarted event using the new protocol
                    if isinstance(event, CustomTaskStarted):
                        attrs = event.attributes
                        custom_task_id = attrs.custom_task_id
                        task_type = attrs.custom_task_type
                        initial_payload = custom_task_state.get_task(custom_task_id).payload or {}

                        if task_type != "wait_for_input":
                            continue

                        update_name = update_name_override or "__submit_input"
                        input_schema = (
                            initial_payload.get("input_schema") if isinstance(initial_payload, dict) else None
                        )
                        user_payload = await prompt_for_json(input_schema, stream_console, schema_display)
                        if user_payload is None:
                            stream_console.print("[yellow]Skipped sending update (empty input).[/]")
                            continue
                        await send_update(
                            client=client,
                            workflow_exec_id=workflow_exec_id,
                            update_name=update_name,
                            custom_task_id=custom_task_id,
                            user_input=user_payload,
                        )
                        stream_console.print(view.render())
        except httpx.RemoteProtocolError as e:
            # Server closed the SSE connection - this typically happens when:
            # - Kong gateway timeout (default 60s read_timeout in scripts/gateway/kong.yaml)
            # - The workflow completed and the stream ended
            # - The server restarted or had an issue
            error_msg = str(e)
            if "peer closed connection" in error_msg or "incomplete chunked read" in error_msg:
                stream_console.print(
                    Panel(
                        "[yellow]Stream connection closed by server.[/]\n"
                        "This is likely due to Kong gateway timeout (60s by default).",
                        title="Stream Ended",
                        border_style="yellow",
                    )
                )
            else:
                stream_console.print(
                    Panel(
                        f"[red]Connection error:[/] {error_msg}",
                        title="Stream Error",
                        border_style="red",
                    )
                )
        except httpx.ReadTimeout:
            stream_console.print(
                Panel(
                    "[yellow]Stream read timeout.[/]\nThe server did not send any data within the timeout period.",
                    title="Stream Timeout",
                    border_style="yellow",
                )
            )
        except asyncio.CancelledError:
            stream_console.print(
                Panel(
                    "[yellow]Stream cancelled.[/]",
                    title="Cancelled",
                    border_style="yellow",
                )
            )
            raise
    finally:
        if dump_file:
            dump_file.close()
            if dump_path:
                stream_console.print(f"[green]Raw SSE events saved to {dump_path}[/]")


async def main_async() -> None:
    args = build_arg_parser().parse_args()
    custom_task_state = CustomTaskState()
    console = Console(force_terminal=True, soft_wrap=True)

    if not args.api_key:
        console.print("[red]Error: MISTRAL_API_KEY not set. Provide --api-key or set MISTRAL_API_KEY env var.[/]")
        return

    # Set up signal handler for clean shutdown
    shutdown_event = asyncio.Event()

    def signal_handler() -> None:
        console.print("\n[yellow]Received interrupt signal, shutting down...[/]")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        async with get_mistral_client(
            server_url=args.base_url,
            api_key=args.api_key,
        ) as client:
            # Create a dynamic model from the input dict
            field_definitions: Dict[str, Any] = {k: (type(v), v) for k, v in args.input.items()}
            DynamicInput = create_model("DynamicInput", **field_definitions)
            execution_id = await start_workflow(
                client=client,
                workflow_name=args.workflow_name,
                workflow_input=DynamicInput(**args.input),
                console=console,
            )

            # Create stream task that can be cancelled
            stream_task = asyncio.create_task(
                stream_workflow(
                    client=client,
                    workflow_exec_id=execution_id,
                    stream=args.stream,
                    custom_task_state=custom_task_state,
                    update_name_override=args.update_name,
                    dump_raw_events=args.dump_raw_events,
                    schema_display=args.schema_display,
                    console=console,
                )
            )

            # Wait for either stream completion or shutdown signal
            shutdown_task = asyncio.create_task(shutdown_event.wait())
            done, pending = await asyncio.wait(
                [stream_task, shutdown_task],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # Cancel pending tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            # Re-raise any exception from the stream task
            if stream_task in done:
                stream_task.result()
    except asyncio.CancelledError:
        console.print("[yellow]Shutdown complete.[/]")
    finally:
        # Remove signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)


def main() -> None:
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        # Fallback for platforms where signal handlers don't work
        pass


if __name__ == "__main__":
    main()
