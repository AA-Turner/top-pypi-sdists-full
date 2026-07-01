"""Reusable ETL helpers for Worlds trajectory datasets."""

from __future__ import annotations

import json
import shlex
from collections import defaultdict
from typing import TYPE_CHECKING, Literal, TypedDict, cast

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from pathlib import Path

    from dreadnode.datasets.dataset import Dataset
    from dreadnode.datasets.local import LocalDataset
    from dreadnode.training.etl.rl import RLPromptRow
    from dreadnode.training.etl.sft import SFTConversation


class AtifCredential(TypedDict, total=False):
    """Credential information in ATIF format."""

    username: str
    password: str
    domain: str
    hash: str


class AtifGoal(TypedDict, total=False):
    """Goal specification in ATIF format."""

    target_type: str
    target_name: str
    description: str


class AtifInitialState(TypedDict, total=False):
    """Initial state information in ATIF format."""

    host: str
    principal: str
    domain: str
    credentials: list[AtifCredential]


class AtifExtra(TypedDict, total=False):
    """Extra metadata in ATIF format."""

    goal: AtifGoal
    initial_state: AtifInitialState


class AtifToolCallArguments(TypedDict, total=False):
    """Arguments for a tool call."""

    command: str


class AtifToolCall(TypedDict):
    """Tool call in ATIF format."""

    tool_call_id: str
    function_name: str
    arguments: AtifToolCallArguments | str


class AtifObservationResult(TypedDict, total=False):
    """Single result from a tool call observation."""

    source_call_id: str
    tool_call_id: str
    content: str
    is_error: bool


class AtifObservation(TypedDict, total=False):
    """Observation containing tool call results."""

    results: list[AtifObservationResult]


class AtifStep(TypedDict, total=False):
    """Single step in an ATIF trajectory."""

    step_id: int
    source: Literal["user", "agent", "system"]
    message: str
    reasoning_content: str
    tool_calls: list[AtifToolCall]
    observation: AtifObservation


class AtifAgentConfig(TypedDict, total=False):
    """Agent configuration in ATIF format."""

    name: str
    version: str
    model_name: str


class AtifTrajectorySummary(TypedDict, total=False):
    """Worlds trajectory summary metadata attached during dataset publish."""

    trajectory_id: str
    seed: int
    success: bool
    termination_reason: str | None
    step_count: int


class AtifTrajectory(TypedDict, total=False):
    """Complete ATIF trajectory with optional Worlds training metadata."""

    schema_version: str
    session_id: str
    agent: AtifAgentConfig
    extra: AtifExtra
    steps: list[AtifStep]
    trajectory_id: str
    seed: int
    success: bool
    termination_reason: str | None
    step_count: int
    worlds_summary: AtifTrajectorySummary


class AgentToolCallFunction(TypedDict):
    """Function payload for an OpenAI-compatible tool call."""

    name: str
    arguments: str


class AgentToolCall(TypedDict, total=False):
    """Tool call emitted by native agent-mode Worlds trajectories."""

    id: str
    type: Literal["function"]
    function: AgentToolCallFunction


class AgentTrainingMessage(TypedDict, total=False):
    """Message record emitted by native agent-mode Worlds training artifacts."""

    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tool_calls: list[AgentToolCall]
    tool_call_id: str


class AgentTrainingRecord(TypedDict, total=False):
    """Training row emitted by native agent-mode Worlds rollouts."""

    messages: list[AgentTrainingMessage]
    tools: list[ToolSchema]
    metadata: dict[str, object]


WorldsTrainingRecord = AtifTrajectory | AgentTrainingRecord


class JsonSchemaPropertyItem(TypedDict, total=False):
    """Schema for items in an array property."""

    type: str


class JsonSchemaAnyOfEntry(TypedDict, total=False):
    """An entry in an anyOf union type."""

    type: str
    additionalProperties: dict[str, str]


class JsonSchemaProperty(TypedDict, total=False):
    """JSON schema property definition."""

    type: str
    description: str
    title: str
    default: str | int | float | bool | None
    items: JsonSchemaPropertyItem
    anyOf: list[JsonSchemaAnyOfEntry]
    additionalProperties: dict[str, str] | bool


class JsonSchemaParameters(TypedDict, total=False):
    """JSON schema parameters object."""

    type: Literal["object"]
    properties: dict[str, JsonSchemaProperty]
    required: list[str]
    additionalProperties: bool


class ToolFunction(TypedDict):
    """Function definition within a tool schema."""

    name: str
    description: str
    parameters: JsonSchemaParameters


class ToolSchema(TypedDict):
    """OpenAI-compatible tool schema."""

    type: Literal["function"]
    function: ToolFunction


class ChatToolCallFunction(TypedDict):
    """Function details in a chat tool call."""

    name: str
    arguments: str


class ChatToolCall(TypedDict):
    """Tool call in chat_template format."""

    id: str
    type: Literal["function"]
    function: ChatToolCallFunction


class OpenAIMessage(TypedDict, total=False):
    """Message in OpenAI chat format."""

    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tool_calls: list[ChatToolCall]
    tool_call_id: str


# Backwards compatibility alias
ChatMessage = OpenAIMessage


class OpenAIConversation(TypedDict):
    """Complete conversation in OpenAI chat format with tool schemas."""

    tools: list[ToolSchema]
    messages: list[OpenAIMessage]


# Backwards compatibility alias
ChatTemplateTrajectory = OpenAIConversation


ToolMode = Literal["command", "per-tool"]

DEFAULT_FINAL_ASSISTANT = (
    "With that, we have achieved full compromise of the domain. Let me know if "
    "there's any post exploitation tasks you need to perform or report you need me "
    "to create."
)


def iter_atif_trajectories_jsonl(
    path: Path,
    *,
    limit: int | None = None,
) -> Iterator[WorldsTrainingRecord]:
    """Yield Worlds training records from a JSONL file."""

    count = 0
    with path.open("r", encoding="utf-8") as infile:
        for line in infile:
            if limit is not None and count >= limit:
                break
            stripped = line.strip()
            if not stripped:
                continue
            count += 1
            yield cast("WorldsTrainingRecord", json.loads(stripped))


def load_atif_trajectories_jsonl(
    path: Path,
    *,
    limit: int | None = None,
) -> list[WorldsTrainingRecord]:
    """Load Worlds training records from a JSONL file."""

    return list(iter_atif_trajectories_jsonl(path, limit=limit))


def load_atif_trajectories_from_dataset(
    dataset: Dataset | LocalDataset,
    *,
    split: str | None = None,
    limit: int | None = None,
) -> list[WorldsTrainingRecord]:
    """Load Worlds training records from a published dataset."""

    table = dataset.load(split=split)
    records = [record for record in table.to_pylist() if isinstance(record, dict)]
    trajectories = [cast("WorldsTrainingRecord", record) for record in records]
    if limit is None:
        return trajectories
    return trajectories[:limit]


def write_openai_conversations_jsonl(
    conversations: Iterable[OpenAIConversation],
    path: Path,
) -> int:
    """Write OpenAI conversations to a JSONL file."""

    count = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as outfile:
        for conversation in conversations:
            outfile.write(json.dumps(conversation, ensure_ascii=False) + "\n")
            count += 1
    return count


# Backwards compatibility alias
write_chat_template_trajectories_jsonl = write_openai_conversations_jsonl


def convert_atif_trajectories_to_openai(
    trajectories: Iterable[AtifTrajectory],
    *,
    tool_mode: ToolMode = "command",
    append_final_assistant: bool = False,
    final_assistant_message: str = DEFAULT_FINAL_ASSISTANT,
) -> list[OpenAIConversation]:
    """Convert multiple ATIF trajectories into OpenAI conversations."""

    return [
        convert_atif_trajectory_to_openai(
            trajectory,
            tool_mode=tool_mode,
            append_final_assistant=append_final_assistant,
            final_assistant_message=final_assistant_message,
        )
        for trajectory in trajectories
    ]


# Backwards compatibility alias
convert_atif_trajectories_to_chat_template = convert_atif_trajectories_to_openai


def load_conversations_from_worlds_dataset(
    dataset: Dataset | LocalDataset,
    *,
    split: str | None = None,
    limit: int | None = None,
    system_prompt: str | None = None,
    tool_mode: ToolMode = "command",
    append_final_assistant: bool = True,
    final_assistant_message: str = DEFAULT_FINAL_ASSISTANT,
) -> list[OpenAIConversation]:
    """Convert a Worlds ATIF dataset into OpenAI conversations.

    Unlike load_sft_conversations_from_worlds_dataset, this preserves tool_calls
    in assistant messages rather than stripping them.
    """

    from dreadnode.training.etl._common import apply_system_prompt

    trajectories = load_atif_trajectories_from_dataset(
        dataset,
        split=split,
        limit=limit,
    )
    conversations: list[OpenAIConversation] = []
    for trajectory in trajectories:
        openai_conv = convert_atif_trajectory_to_openai(
            trajectory,
            tool_mode=tool_mode,
            append_final_assistant=append_final_assistant,
            final_assistant_message=final_assistant_message,
        )
        messages = openai_conv["messages"]
        if not messages:
            continue
        # Apply system prompt by merging into existing system message or prepending
        if system_prompt:
            plain_messages = [
                {
                    "role": str(msg.get("role") or "user"),
                    "content": str(msg.get("content") or ""),
                }
                for msg in messages
            ]
            merged = apply_system_prompt(
                system_prompt=system_prompt,
                messages=plain_messages,
            )
            # Reconstruct OpenAIMessages preserving tool_calls/tool_call_id
            new_messages: list[OpenAIMessage] = []
            for orig, updated in zip(messages, merged, strict=False):
                rebuilt = OpenAIMessage(role=updated["role"], content=updated["content"])
                if "tool_calls" in orig:
                    rebuilt["tool_calls"] = orig["tool_calls"]
                if "tool_call_id" in orig:
                    rebuilt["tool_call_id"] = orig["tool_call_id"]
                new_messages.append(rebuilt)
            # If apply_system_prompt prepended a new system message, merged is longer
            if len(merged) > len(messages):
                new_messages = [
                    OpenAIMessage(role=merged[0]["role"], content=merged[0]["content"]),
                    *new_messages,
                ]
            messages = new_messages
        conversations.append(OpenAIConversation(tools=openai_conv["tools"], messages=messages))
    return conversations


def load_sft_conversations_from_worlds_dataset(
    dataset: Dataset | LocalDataset,
    *,
    split: str | None = None,
    limit: int | None = None,
    system_prompt: str | None = None,
    tool_mode: ToolMode = "command",
    append_final_assistant: bool = True,
    final_assistant_message: str = DEFAULT_FINAL_ASSISTANT,
) -> list[SFTConversation]:
    """Convert a Worlds ATIF dataset into SFT conversations.

    This strips tool_calls for plain SFT use. For tool-aware training,
    use load_conversations_from_worlds_dataset instead.
    """

    from dreadnode.training.etl._common import apply_system_prompt
    from dreadnode.training.etl.sft import SFTConversation

    trajectories = load_atif_trajectories_from_dataset(
        dataset,
        split=split,
        limit=limit,
    )
    conversations: list[SFTConversation] = []
    for trajectory in trajectories:
        if _is_agent_training_record(trajectory):
            messages = _messages_from_agent_training_record(trajectory)
            if not messages:
                continue
            conversations.append(
                SFTConversation(
                    messages=apply_system_prompt(
                        system_prompt=system_prompt,
                        messages=messages,
                    ),
                    metadata=_agent_training_metadata(trajectory),
                )
            )
            continue

        chat_trajectory = convert_atif_trajectory_to_chat_template(
            trajectory,
            tool_mode=tool_mode,
            append_final_assistant=append_final_assistant,
            final_assistant_message=final_assistant_message,
        )
        messages = [
            {
                "role": str(message.get("role") or "user"),
                "content": str(message.get("content") or ""),
            }
            for message in chat_trajectory["messages"]
            if message.get("content") is not None
        ]
        if not messages:
            continue
        normalized_messages = apply_system_prompt(
            system_prompt=system_prompt,
            messages=messages,
        )
        conversations.append(
            SFTConversation(
                messages=normalized_messages,
                metadata={
                    "session_id": trajectory.get("session_id"),
                    "schema_version": trajectory.get("schema_version"),
                    "extra": trajectory.get("extra", {}),
                },
            )
        )
    return conversations


def load_rl_prompt_rows_from_worlds_dataset(
    dataset: Dataset | LocalDataset,
    *,
    split: str | None = None,
    limit: int | None = None,
    system_prompt: str | None = None,
    default_reward: float = 1.0,
) -> list[RLPromptRow]:
    """Convert a Worlds ATIF dataset into offline-RL prompt rows.

    Each assistant step becomes one prompt row:
    - `messages` is the trace prefix before that assistant step
    - `expected_output` is the recorded assistant action text
    - `reward` is derived from trajectory outcome metadata when available and is
      typically paired with the trajectory-imitation reward recipe
    """

    trajectories = load_atif_trajectories_from_dataset(
        dataset,
        split=split,
    )
    prompt_rows: list[RLPromptRow] = []
    for trajectory in trajectories:
        if _is_agent_training_record(trajectory):
            prompt_rows.extend(
                convert_agent_training_record_to_rl_prompt_rows(
                    trajectory,
                    system_prompt=system_prompt,
                    default_reward=default_reward,
                )
            )
        else:
            prompt_rows.extend(
                convert_atif_trajectory_to_rl_prompt_rows(
                    trajectory,
                    system_prompt=system_prompt,
                    default_reward=default_reward,
                )
            )
        if limit is not None and len(prompt_rows) >= limit:
            return prompt_rows[:limit]
    return prompt_rows


def build_worlds_system_prompt(extra: AtifExtra) -> str:
    """Build a system prompt from Worlds ATIF metadata."""

    goal = extra.get("goal", {})
    initial_state = extra.get("initial_state", {})

    credentials = initial_state.get("credentials", [])
    if credentials:
        credentials_str = ", ".join(
            f"{credential.get('username', 'unknown')} "
            f"(password: {credential.get('password', 'unknown')})"
            for credential in credentials
        )
    else:
        credentials_str = "None"

    return (
        "You are a network security assessment agent. Your task is to achieve the "
        "specified goal using available tools.\n\n"
        f"Goal: {goal.get('target_type', 'unknown')} - {goal.get('target_name', 'unknown')}\n\n"
        "Starting Position:\n"
        f"- Host: {initial_state.get('host', 'unknown')}\n"
        f"- Principal: {initial_state.get('principal', 'unknown')}\n"
        f"- Domain: {initial_state.get('domain', 'unknown')}\n"
        f"- Credentials: {credentials_str}\n\n"
        "You have access to tools for network reconnaissance and exploitation."
    )


def convert_atif_trajectory_to_rl_prompt_rows(
    trajectory: AtifTrajectory,
    *,
    system_prompt: str | None = None,
    default_reward: float = 1.0,
) -> list[RLPromptRow]:
    """Convert one ATIF trajectory into offline-RL prompt rows."""

    from dreadnode.training.etl._common import apply_system_prompt, normalize_optional_string
    from dreadnode.training.etl.rl import RLPromptRow

    prefix_messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": build_worlds_system_prompt(trajectory.get("extra", {})),
        }
    ]
    template_context = _build_worlds_template_context(trajectory)
    reward = _reward_from_worlds_summary(
        trajectory=trajectory,
        default_reward=default_reward,
    )
    rows: list[RLPromptRow] = []
    for step in trajectory.get("steps", []):
        source = normalize_optional_string(step.get("source")) or "user"
        if source == "agent":
            assistant_content = _linearize_assistant_step(step)
            if assistant_content:
                rows.append(
                    RLPromptRow(
                        prompt=None,
                        messages=apply_system_prompt(
                            system_prompt=system_prompt,
                            messages=list(prefix_messages),
                        ),
                        expected_output=assistant_content,
                        template_context=dict(template_context),
                        metadata={
                            "session_id": trajectory.get("session_id"),
                            "trajectory_id": trajectory.get("trajectory_id")
                            or trajectory.get("session_id"),
                            "schema_version": trajectory.get("schema_version"),
                            "step_id": step.get("step_id"),
                            "extra": trajectory.get("extra", {}),
                            "worlds_summary": trajectory.get("worlds_summary", {}),
                            "success": trajectory.get("success"),
                            "termination_reason": trajectory.get("termination_reason"),
                            "step_count": trajectory.get("step_count"),
                        },
                        reward=reward,
                    )
                )
                prefix_messages.append({"role": "assistant", "content": assistant_content})
            prefix_messages.extend(_observation_messages_from_step(step))
            continue

        if source in {"user", "system"}:
            message = normalize_optional_string(step.get("message"))
            if message:
                prefix_messages.append({"role": source, "content": message})
    return rows


def convert_agent_training_record_to_rl_prompt_rows(
    trajectory: AgentTrainingRecord,
    *,
    system_prompt: str | None = None,
    default_reward: float = 1.0,
) -> list[RLPromptRow]:
    """Convert one native agent-mode Worlds trajectory into offline-RL prompt rows."""

    from dreadnode.training.etl._common import apply_system_prompt
    from dreadnode.training.etl.rl import RLPromptRow

    prefix_messages: list[dict[str, str]] = []
    metadata = _get_agent_training_metadata(trajectory)
    template_context = _build_worlds_template_context_from_metadata(metadata)
    reward = _reward_from_agent_metadata(
        metadata=metadata,
        default_reward=default_reward,
    )
    rows: list[RLPromptRow] = []
    for index, message in enumerate(trajectory.get("messages", [])):
        if not isinstance(message, dict):
            continue
        role = _normalize_agent_message_role(message)
        if role == "assistant":
            assistant_content = _linearize_agent_training_assistant_message(message)
            if assistant_content:
                rows.append(
                    RLPromptRow(
                        prompt=None,
                        messages=apply_system_prompt(
                            system_prompt=system_prompt,
                            messages=list(prefix_messages),
                        ),
                        expected_output=assistant_content,
                        template_context=dict(template_context),
                        metadata={
                            **metadata,
                            "message_index": index,
                        },
                        reward=reward,
                    )
                )
                prefix_messages.append({"role": "assistant", "content": assistant_content})
            continue

        content = _linearize_agent_training_non_assistant_message(message)
        if content is None:
            continue
        prefix_messages.append({"role": role, "content": content})
    return rows


def build_command_tool_schema() -> ToolSchema:
    """Return the single command-tool schema used by the harness."""

    nullable_string: list[JsonSchemaAnyOfEntry] = [
        JsonSchemaAnyOfEntry(type="string"),
        JsonSchemaAnyOfEntry(type="null"),
    ]
    nullable_env: list[JsonSchemaAnyOfEntry] = [
        JsonSchemaAnyOfEntry(type="object", additionalProperties={"type": "string"}),
        JsonSchemaAnyOfEntry(type="null"),
    ]

    return ToolSchema(
        type="function",
        function=ToolFunction(
            name="command",
            description=(
                "Execute a shell command.\n\n"
                "## Best Practices\n"
                "- Argument Format: Command and arguments must be a list of strings.\n"
                "- No Shell Syntax: Does not use a shell (no pipes, redirection, var expansion, etc.).\n"
                "- Error on Failure: Raises RuntimeError for non-zero exit codes.\n"
                "- Use input Parameter: Send data to the command's standard input to avoid hanging.\n\n"
                "Args:\n"
                "    cmd: The command to execute as a list of strings.\n"
                "    timeout: Maximum execution time in seconds.\n"
                "    cwd: The working directory for the command.\n"
                "    env: Environment variables for the command.\n"
                "    input: Optional string to send to the command's standard input."
            ),
            parameters=JsonSchemaParameters(
                type="object",
                properties={
                    "cmd": JsonSchemaProperty(
                        items=JsonSchemaPropertyItem(type="string"),
                        title="Cmd",
                        type="array",
                    ),
                    "timeout": JsonSchemaProperty(
                        default=120,
                        title="Timeout",
                        type="integer",
                    ),
                    "cwd": JsonSchemaProperty(anyOf=nullable_string, default=None, title="Cwd"),
                    "env": JsonSchemaProperty(anyOf=nullable_env, default=None, title="Env"),
                    "input": JsonSchemaProperty(
                        anyOf=nullable_string,
                        default=None,
                        title="Input",
                    ),
                },
                required=["cmd"],
                additionalProperties=False,
            ),
        ),
    )


def _build_worlds_template_context(
    trajectory: AtifTrajectory,
) -> dict[str, str | int | None]:
    extra = trajectory.get("extra", {})
    goal = extra.get("goal", {})
    initial_state = extra.get("initial_state", {})
    return {
        "session_id": trajectory.get("session_id"),
        "trajectory_id": trajectory.get("trajectory_id") or trajectory.get("session_id"),
        "target_type": goal.get("target_type"),
        "target_name": goal.get("target_name"),
        "target_description": goal.get("description"),
        "host": initial_state.get("host"),
        "principal": initial_state.get("principal"),
        "domain": initial_state.get("domain"),
    }


def _build_worlds_template_context_from_metadata(
    metadata: dict[str, object],
) -> dict[str, str | int | None]:
    worlds_summary = metadata.get("worlds_summary")
    summary = worlds_summary if isinstance(worlds_summary, dict) else {}
    return {
        "session_id": _string_or_none(metadata.get("session_id")),
        "trajectory_id": _string_or_none(metadata.get("trajectory_id"))
        or _string_or_none(summary.get("trajectory_id")),
        "goal": _string_or_none(metadata.get("goal")),
        "seed": _int_or_none(metadata.get("seed")),
        "step_count": _int_or_none(metadata.get("step_count"))
        or _int_or_none(summary.get("step_count")),
        "termination_reason": _string_or_none(metadata.get("termination_reason"))
        or _string_or_none(summary.get("termination_reason")),
    }


def _reward_from_worlds_summary(
    *,
    trajectory: AtifTrajectory,
    default_reward: float,
) -> float:
    success = trajectory.get("success")
    if isinstance(success, bool):
        return 1.0 if success else 0.0
    summary = trajectory.get("worlds_summary")
    if isinstance(summary, dict):
        summary_success = summary.get("success")
        if isinstance(summary_success, bool):
            return 1.0 if summary_success else 0.0
    return default_reward


def _reward_from_agent_metadata(
    *,
    metadata: dict[str, object],
    default_reward: float,
) -> float:
    success = metadata.get("success")
    if isinstance(success, bool):
        return 1.0 if success else 0.0
    worlds_summary = metadata.get("worlds_summary")
    if isinstance(worlds_summary, dict):
        summary_success = worlds_summary.get("success")
        if isinstance(summary_success, bool):
            return 1.0 if summary_success else 0.0
    return default_reward


def _is_agent_training_record(record: WorldsTrainingRecord) -> bool:
    return isinstance(record, dict) and isinstance(record.get("messages"), list)


def _messages_from_agent_training_record(
    record: AgentTrainingRecord,
) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for item in record.get("messages", []):
        if not isinstance(item, dict):
            continue
        role = _normalize_agent_message_role(item)
        content = (
            _linearize_agent_training_assistant_message(item)
            if role == "assistant"
            else _linearize_agent_training_non_assistant_message(item)
        )
        if content is None:
            continue
        messages.append({"role": role, "content": content})
    return messages


def _agent_training_metadata(record: AgentTrainingRecord) -> dict[str, object]:
    metadata = _get_agent_training_metadata(record)
    tools = record.get("tools")
    if isinstance(tools, list):
        return {**metadata, "tools": tools}
    return metadata


def _get_agent_training_metadata(record: AgentTrainingRecord) -> dict[str, object]:
    metadata = record.get("metadata")
    if isinstance(metadata, dict):
        return dict(metadata)
    return {}


def _normalize_agent_message_role(message: AgentTrainingMessage) -> str:
    from dreadnode.training.etl._common import normalize_optional_string

    return normalize_optional_string(message.get("role")) or "user"


def _linearize_agent_training_assistant_message(
    message: AgentTrainingMessage,
) -> str | None:
    from dreadnode.training.etl._common import normalize_optional_string

    parts: list[str] = []
    content = normalize_optional_string(message.get("content"))
    if content:
        parts.append(content)
    tool_calls = message.get("tool_calls")
    if isinstance(tool_calls, list):
        serialized_tool_calls = [
            rendered
            for tool_call in tool_calls
            if isinstance(tool_call, dict)
            for rendered in [_render_agent_tool_call_for_content(tool_call)]
            if rendered is not None
        ]
        if serialized_tool_calls:
            parts.append("\n".join(serialized_tool_calls))
    if not parts:
        return None
    return "\n\n".join(parts).strip()


def _linearize_agent_training_non_assistant_message(
    message: AgentTrainingMessage,
) -> str | None:
    from dreadnode.training.etl._common import normalize_optional_string

    role = _normalize_agent_message_role(message)
    content = normalize_optional_string(message.get("content"))
    if content is None:
        return None
    if role == "tool":
        tool_call_id = normalize_optional_string(message.get("tool_call_id"))
        if tool_call_id:
            return f"[Tool Result from {tool_call_id}]\n{content}"
    return content


def _render_agent_tool_call_for_content(tool_call: AgentToolCall) -> str | None:
    function = tool_call.get("function")
    if not isinstance(function, dict):
        return None
    function_name = function.get("name")
    if not isinstance(function_name, str) or not function_name:
        return None
    arguments = function.get("arguments")
    rendered_arguments = arguments if isinstance(arguments, str) else json.dumps(arguments)
    return f'<tool_call name="{function_name}">{rendered_arguments}</tool_call>'


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None


def _int_or_none(value: object) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    return None


def _linearize_assistant_step(step: AtifStep) -> str | None:
    from dreadnode.training.etl._common import normalize_optional_string

    parts: list[str] = []
    reasoning_content = normalize_optional_string(step.get("reasoning_content"))
    if reasoning_content:
        parts.append(f"<think>{reasoning_content}</think>")
    message = normalize_optional_string(step.get("message"))
    if message:
        parts.append(message)
    tool_calls = step.get("tool_calls")
    if isinstance(tool_calls, list):
        serialized_tool_calls = [
            rendered
            for tool_call in tool_calls
            if isinstance(tool_call, dict)
            for rendered in [_render_tool_call_for_content(cast("AtifToolCall", tool_call))]
            if rendered is not None
        ]
        if serialized_tool_calls:
            parts.append("\n".join(serialized_tool_calls))
    if not parts:
        return None
    return "\n\n".join(parts).strip()


def _render_tool_call_for_content(tool_call: AtifToolCall) -> str | None:
    function_name = tool_call.get("function_name")
    if not isinstance(function_name, str) or not function_name:
        return None
    arguments = tool_call.get("arguments", {})
    if isinstance(arguments, str):
        rendered_arguments = arguments
    else:
        rendered_arguments = json.dumps(
            normalize_atif_arguments(arguments),
            ensure_ascii=False,
            sort_keys=True,
        )
    return f'<tool_call name="{function_name}">{rendered_arguments}</tool_call>'


def _observation_messages_from_step(step: AtifStep) -> list[dict[str, str]]:
    from dreadnode.training.etl._common import normalize_optional_string

    observation = step.get("observation")
    if not isinstance(observation, dict):
        return []
    results = observation.get("results")
    if not isinstance(results, list):
        return []
    messages: list[dict[str, str]] = []
    for result in results:
        if not isinstance(result, dict):
            continue
        content = normalize_optional_string(result.get("content"))
        if content is None:
            continue
        if result.get("is_error") is True:
            content = f"[error] {content}"
        messages.append({"role": "tool", "content": content})
    return messages


def normalize_atif_arguments(arguments: AtifToolCallArguments | str) -> dict[str, str]:
    """Normalize ATIF tool call arguments to a string-keyed mapping."""

    if isinstance(arguments, str):
        return {"command": arguments}
    return {key: str(value) if value is not None else "" for key, value in arguments.items()}


def command_from_arguments(function_name: str, arguments: AtifToolCallArguments | str) -> str:
    """Build a shellish command string from an ATIF tool call."""

    if isinstance(arguments, str):
        return arguments
    command = arguments.get("command")
    if command and command.strip():
        return command
    return f"{function_name} {json.dumps(arguments, ensure_ascii=False)}"


def command_to_cmd_list(function_name: str, arguments: AtifToolCallArguments | str) -> list[str]:
    """Convert ATIF tool arguments into a command argv list."""

    command_str = command_from_arguments(function_name, arguments)
    try:
        return shlex.split(command_str)
    except ValueError:
        return command_str.split()


def iter_tool_calls(trajectory: AtifTrajectory) -> Iterable[AtifToolCall]:
    """Iterate all tool calls contained in a trajectory."""

    for step in trajectory.get("steps", []):
        yield from step.get("tool_calls", [])


def build_tool_schemas_per_tool(tool_calls: Iterable[AtifToolCall]) -> list[ToolSchema]:
    """Build one tool schema per unique ATIF function name."""

    tool_keys: dict[str, set[str]] = defaultdict(set)
    tool_required: dict[str, set[str]] = {}

    for tool_call in tool_calls:
        name = tool_call["function_name"]
        keys = set(normalize_atif_arguments(tool_call.get("arguments", {})).keys())
        tool_keys[name].update(keys)
        if name not in tool_required:
            tool_required[name] = set(keys)
        else:
            tool_required[name].intersection_update(keys)

    schemas: list[ToolSchema] = []
    for name in sorted(tool_keys):
        properties = {key: JsonSchemaProperty(type="string") for key in sorted(tool_keys[name])}
        schemas.append(
            ToolSchema(
                type="function",
                function=ToolFunction(
                    name=name,
                    description=f"Execute {name} in the assessment environment.",
                    parameters=JsonSchemaParameters(
                        type="object",
                        properties=properties,
                        required=sorted(tool_required.get(name, set())),
                    ),
                ),
            )
        )
    return schemas


def convert_atif_tool_call(tool_call: AtifToolCall, tool_mode: ToolMode) -> ChatToolCall:
    """Convert an ATIF tool call into chat_template tool-call format."""

    if tool_mode == "command":
        serialized_args = json.dumps(
            {"cmd": command_to_cmd_list(tool_call["function_name"], tool_call["arguments"])},
            ensure_ascii=False,
        )
        tool_name = "command"
    else:
        serialized_args = json.dumps(
            normalize_atif_arguments(tool_call.get("arguments", {})),
            ensure_ascii=False,
        )
        tool_name = tool_call["function_name"]

    return ChatToolCall(
        id=tool_call.get("tool_call_id") or "",
        type="function",
        function=ChatToolCallFunction(name=tool_name, arguments=serialized_args),
    )


def convert_atif_trajectory_to_openai(
    trajectory: AtifTrajectory,
    *,
    tool_mode: ToolMode = "command",
    append_final_assistant: bool = False,
    final_assistant_message: str = DEFAULT_FINAL_ASSISTANT,
) -> OpenAIConversation:
    """Convert a single ATIF trajectory into OpenAI conversation format."""

    messages: list[OpenAIMessage] = [
        OpenAIMessage(
            role="system", content=build_worlds_system_prompt(trajectory.get("extra", {}))
        )
    ]

    for step in trajectory.get("steps", []):
        source = step.get("source")
        if source == "user":
            messages.append(OpenAIMessage(role="user", content=step.get("message", "")))
            continue
        if source != "agent":
            continue

        tool_calls = step.get("tool_calls", [])
        content_parts: list[str] = []
        reasoning = step.get("reasoning_content", "")
        if reasoning and reasoning.strip():
            content_parts.append(f"<think>{reasoning.strip()}</think>")
        message = step.get("message", "")
        if message and message.strip():
            content_parts.append(message.strip())

        assistant_message = OpenAIMessage(
            role="assistant",
            content="\n".join(content_parts) if content_parts else "",
        )
        if tool_calls:
            assistant_message["tool_calls"] = [
                convert_atif_tool_call(tool_call, tool_mode) for tool_call in tool_calls
            ]
        messages.append(assistant_message)

        messages.extend(
            [
                OpenAIMessage(
                    role="tool",
                    tool_call_id=result.get("source_call_id") or result.get("tool_call_id") or "",
                    content=result.get("content", ""),
                )
                for result in step.get("observation", {}).get("results", [])
            ]
        )

    tools = (
        [build_command_tool_schema()]
        if tool_mode == "command"
        else build_tool_schemas_per_tool(iter_tool_calls(trajectory))
    )

    if append_final_assistant and messages:
        last_message = messages[-1]
        last_role = last_message.get("role")
        if last_role == "tool" or (
            last_role == "assistant" and bool(last_message.get("tool_calls"))
        ):
            messages.append(OpenAIMessage(role="assistant", content=final_assistant_message))

    return OpenAIConversation(tools=tools, messages=messages)


# Backwards compatibility alias
convert_atif_trajectory_to_chat_template = convert_atif_trajectory_to_openai


__all__ = [
    "DEFAULT_FINAL_ASSISTANT",
    "AtifAgentConfig",
    "AtifCredential",
    "AtifExtra",
    "AtifGoal",
    "AtifInitialState",
    "AtifObservation",
    "AtifObservationResult",
    "AtifStep",
    "AtifToolCall",
    "AtifToolCallArguments",
    "AtifTrajectory",
    "ChatMessage",
    "ChatTemplateTrajectory",
    "OpenAIConversation",
    "OpenAIMessage",
    "ToolMode",
    "ToolSchema",
    "build_worlds_system_prompt",
    "convert_atif_tool_call",
    "convert_atif_trajectories_to_chat_template",
    "convert_atif_trajectories_to_openai",
    "convert_atif_trajectory_to_chat_template",
    "convert_atif_trajectory_to_openai",
    "iter_atif_trajectories_jsonl",
    "load_atif_trajectories_from_dataset",
    "load_atif_trajectories_jsonl",
    "load_conversations_from_worlds_dataset",
    "load_sft_conversations_from_worlds_dataset",
    "write_chat_template_trajectories_jsonl",
    "write_openai_conversations_jsonl",
]
