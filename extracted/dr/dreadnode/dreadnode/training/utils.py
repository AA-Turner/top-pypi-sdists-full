#!/usr/bin/env python3
"""Augment ATIF trajectories with thinking traces using Kimi-K2.5.

Processes trajectories in parallel at the trajectory level, but sequentially
within each trajectory to maintain causal consistency of thinking traces.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import shlex
import sys
import time
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

from dreadnode.generators.models import XMLModel, element


@dataclass
class AugmentArgs:
    """Typed arguments for augmentation."""

    input_file: Path
    output: Path
    limit: int | None
    model: str
    concurrency: int


class ThinkingOutput(XMLModel):
    """Structured output for thinking trace generation."""

    scratchpad: str = element(tag="scratchpad")
    reasoning: str = element(tag="reasoning")


# Available tools in the harness (from trajectories_v2)
AVAILABLE_TOOLS = [
    "nmap",
    "nslookup",
    "ldapsearch",
    "netexec",
    "certipy",
    "GetNPUsers.py",
    "GetUserSPNs.py",
    "hashcat",
    "bloodyAD",
    "dacledit.py",
    "owneredit.py",
    "changepasswd.py",
    "secretsdump.py",
]

TOOLS_LIST = ", ".join(AVAILABLE_TOOLS)

# Create example for the prompt - grounded in previous observation
THINKING_EXAMPLE = ThinkingOutput(
    scratchpad="The nmap scan revealed LDAP (389) and Kerberos (88) on 10.0.0.12, confirming it is a domain controller. I have credentials for dallen. My goal is Domain Admins membership, so I need to enumerate AD relationships to find a privilege escalation path.",
    reasoning="The nmap results show 10.0.0.12 is running LDAP and Kerberos - that's a domain controller. I should query it for AD group memberships and trust relationships using ldapsearch with dallen's credentials. Enumerating users and group nesting should reveal whether there's a path from my current access to Domain Admins.",
)


THINKING_PROMPT = f"""You are a penetration testing agent with access to a "command" tool that executes shell commands. You need to decide what to do next based on your observations so far.

CURRENT ASSESSMENT:
- Goal: {{goal}}
- Host: {{host}} | Principal: {{principal}} | Domain: {{domain}}
- Credentials: {{credentials}}

AVAILABLE TOOLS (via the command tool): {TOOLS_LIST}

ACTIONS AND RESULTS SO FAR:
{{history}}

Based on the observations above, decide what to do next.

Respond ONLY with {ThinkingOutput.xml_tags()} containing:
- <scratchpad>: Your internal analysis - what did the previous output tell you? What information is actionable? (this is discarded)
- <reasoning>: 2-4 sentences explaining what you learned from recent results and what you'll do next. Your reasoning MUST reference specific information from previous command output that motivates your next action (IPs discovered, credentials found, services identified, errors encountered, etc).

RULES:
- Ground your reasoning in the actual output from previous steps - cite specific IPs, usernames, hashes, ports, or errors you observed
- Explain the logical chain: "The previous output showed X, which means Y, so I should do Z"
- Use prospective language for next actions ("I need to...", "I'll use the command tool to...", "This should reveal...")
- Be specific: mention actual IPs, hostnames, credentials, and protocols from the trajectory
- No XML tags inside <reasoning> - just plain text
- No markdown formatting
- Do NOT write meta-commentary about what to write - just write the reasoning directly

Example:
{THINKING_EXAMPLE.to_pretty_xml()}

Your response:"""


def build_history_text(steps: list[AtifStep], current_idx: int) -> str:
    """Build a summary of actions taken before the current step.

    Full observations are included for the last 2 agent steps to ground
    reasoning in recent results. Earlier steps get brief summaries.
    """
    if current_idx == 0:
        return "None yet - this is the first action."

    # Collect agent step indices
    agent_indices: list[int] = []
    for i, step in enumerate(steps[:current_idx]):
        if step.get("source") != "agent" or not step.get("tool_calls"):
            continue
        agent_indices.append(i)

    if not agent_indices:
        return "None yet."

    # Last 2 agent steps get full observations
    recent_set = set(agent_indices[-2:])

    lines: list[str] = []
    for i in agent_indices:
        step = steps[i]
        tool_calls = step.get("tool_calls", [])

        for tc in tool_calls:
            func_name = tc.get("function_name", "unknown")
            args = tc.get("arguments", {})
            command = args.get("command", str(args)) if isinstance(args, dict) else str(args)
            lines.append(f"{i + 1}. {func_name}: {command}")

            observation = step.get("observation", {})
            results = observation.get("results", [])
            for result in results:
                content = result.get("content", "")
                if not content:
                    continue

                if i in recent_set:
                    # Full output for recent steps (cap at 4000 chars to stay in context)
                    output = content[:4000] + "..." if len(content) > 4000 else content
                    lines.append(f"   OUTPUT:\n{output}")
                else:
                    # Brief summary for older steps
                    summary = content[:200] + "..." if len(content) > 200 else content
                    summary = summary.replace("\n", " ")
                    lines.append(f"   → {summary}")

    return "\n".join(lines)


def extract_goal_info(extra: AtifExtra) -> dict[str, str]:
    """Extract goal and initial state info from ATIF extra field."""
    goal = extra.get("goal", {})
    initial_state = extra.get("initial_state", {})

    creds = initial_state.get("credentials", [])
    if creds:
        creds_str = ", ".join(
            f"{c.get('username', 'unknown')} (password: {c.get('password', 'unknown')})"
            for c in creds
        )
    else:
        creds_str = "None"

    return {
        "goal": f"{goal.get('target_type', 'unknown')} - {goal.get('target_name', 'unknown')}",
        "host": initial_state.get("host", "unknown"),
        "principal": initial_state.get("principal", "unknown"),
        "domain": initial_state.get("domain", "unknown"),
        "credentials": creds_str,
    }


MIN_REASONING_LENGTH = 40

META_COMMENTARY_PATTERNS = re.compile(
    r"(?:first person explanation|explain(?:ing)? (?:why|how|what)|"
    r"description of (?:why|reasoning)|write (?:a |the )?reason|"
    r"the (?:agent|user) (?:should|would|could))",
    re.IGNORECASE,
)

XML_TAG_PATTERN = re.compile(r"</?(?:thinking-output|scratchpad|reasoning)>")


def validate_reasoning(reasoning: str) -> str | None:
    """Validate reasoning quality. Returns an error message if invalid, None if valid."""
    if len(reasoning) < MIN_REASONING_LENGTH:
        return f"Reasoning is too short ({len(reasoning)} chars). Write 2-4 detailed sentences."

    if META_COMMENTARY_PATTERNS.search(reasoning):
        return (
            "Reasoning contains meta-commentary. Write the actual reasoning in first person "
            '(e.g. "I am scanning..."), not a description of what to write.'
        )

    if XML_TAG_PATTERN.search(reasoning):
        return "Reasoning contains XML tags. Write plain text only inside <reasoning>."

    return None


async def generate_thinking_for_step(
    generator: rg.Generator,
    trajectory: AtifTrajectory,
    step_idx: int,
) -> str | None:
    """Generate thinking trace for a single step."""
    steps = trajectory.get("steps", [])
    step = steps[step_idx]

    # Only process agent steps with tool calls
    if step.get("source") != "agent":
        return None

    tool_calls = step.get("tool_calls", [])
    if not tool_calls:
        return None

    # Build context
    goal_info = extract_goal_info(trajectory.get("extra", {}))
    history = build_history_text(steps, step_idx)

    prompt = THINKING_PROMPT.format(
        goal=goal_info["goal"],
        host=goal_info["host"],
        principal=goal_info["principal"],
        domain=goal_info["domain"],
        credentials=goal_info["credentials"],
        history=history,
    )

    format_retry = f"""Your response was not in the correct XML format. Respond ONLY with:

{THINKING_EXAMPLE.to_pretty_xml()}

Replace the example content with your actual reasoning about what to do next, grounded in the previous command output."""

    max_retries = 5

    try:
        chat = await generator.chat([rg.Message("user", prompt)]).run()

        for _attempt in range(max_retries):
            output = chat.last.try_parse(ThinkingOutput)

            if not output:
                # Parse failed - ask to fix format
                chat = await chat.continue_(format_retry).run()
                continue

            reasoning = output.reasoning.strip()
            validation_error = validate_reasoning(reasoning)

            if validation_error is None:
                return reasoning

            # Validation failed - ask to fix content
            content_retry = (
                f"Problem with your <reasoning>: {validation_error}\n\n"
                f"Rewrite the reasoning. Ground it in the specific output from previous steps - "
                f"what did you learn and what should you do next?\n"
                f"Respond with the full {ThinkingOutput.xml_tags()} structure again."
            )
            chat = await chat.continue_(content_retry).run()

        print(
            f"Warning: Failed to generate valid reasoning for step {step_idx} after {max_retries} attempts",
            file=sys.stderr,
        )
        return None
    except Exception as e:
        print(f"Error generating thinking for step {step_idx}: {e}", file=sys.stderr)
        return None


async def augment_trajectory(
    generator: rg.Generator,
    trajectory: AtifTrajectory,
    trajectory_idx: int,
) -> AtifTrajectory:
    """Augment a single trajectory with thinking traces."""
    steps = trajectory.get("steps", [])

    # Process steps sequentially to maintain causal consistency
    for step_idx, step in enumerate(steps):
        if step.get("source") != "agent":
            continue

        thinking = await generate_thinking_for_step(generator, trajectory, step_idx)
        if thinking:
            step["reasoning_content"] = thinking

    print(f"Augmented trajectory {trajectory_idx + 1}", file=sys.stderr)
    return trajectory


def _count_existing_lines(path: Path) -> int:
    """Count non-empty lines in an existing output file for resume support."""
    if not path.exists():
        return 0
    count = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1
    return count


def _format_duration(seconds: float) -> str:
    """Format seconds into a human-readable duration."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f}m"
    hours = minutes / 60
    return f"{hours:.1f}h"


async def process_trajectories(
    input_path: Path,
    output_path: Path,
    model: str,
    limit: int | None,
    concurrency: int,
) -> tuple[int, int]:
    """Process all trajectories with parallel augmentation.

    Supports resuming: if the output file already exists, completed
    trajectories are skipped and new results are appended.
    """
    # Initialize generator
    generator = rg.get_generator(model)
    generator.params.temperature = 0.7

    # Check for existing progress
    already_done = _count_existing_lines(output_path)

    # Read trajectories
    all_trajectories: list[AtifTrajectory] = []
    with input_path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if limit and len(all_trajectories) >= limit:
                break
            line = line.strip()
            if not line:
                continue
            try:
                all_trajectories.append(cast("AtifTrajectory", json.loads(line)))
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}", file=sys.stderr)

    total = len(all_trajectories)

    if already_done >= total:
        print(f"All {total} trajectories already processed in {output_path}", file=sys.stderr)
        return already_done, 0

    if already_done > 0:
        print(
            f"Resuming: {already_done}/{total} already done, processing remaining {total - already_done}",
            file=sys.stderr,
        )

    # Skip already-processed trajectories
    trajectories = all_trajectories[already_done:]
    print(f"Processing {len(trajectories)} trajectories (of {total} total)", file=sys.stderr)

    # Shared state for progress and file writes
    write_lock = asyncio.Lock()
    completed = 0
    errors = 0
    start_time = time.monotonic()

    async def process_and_write(idx: int, traj: AtifTrajectory) -> None:
        nonlocal completed, errors

        global_idx = already_done + idx
        try:
            result = await augment_trajectory(generator, traj, global_idx)
        except Exception as e:
            print(f"Error processing trajectory {global_idx + 1}: {e}", file=sys.stderr)
            result = traj  # Write original on error
            errors += 1

        # Write immediately under lock
        async with write_lock:
            with output_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
            completed += 1

            # Progress update
            total_done = already_done + completed
            elapsed = time.monotonic() - start_time
            rate_per_sec = completed / elapsed if elapsed > 0 else 0
            rate_per_min = rate_per_sec * 60
            remaining = len(trajectories) - completed
            eta_seconds = remaining / rate_per_sec if rate_per_sec > 0 else 0
            print(
                f"[{total_done}/{total}] {total_done / total * 100:.1f}% | "
                f"{rate_per_min:.1f} traj/min | "
                f"ETA {_format_duration(eta_seconds)} | "
                f"{errors} errors",
                file=sys.stderr,
            )

    # Process with concurrency control
    semaphore = asyncio.Semaphore(concurrency)

    async def bounded_process(idx: int, traj: AtifTrajectory) -> None:
        async with semaphore:
            await process_and_write(idx, traj)

    # Run all augmentations
    tasks = [bounded_process(i, traj) for i, traj in enumerate(trajectories)]
    await asyncio.gather(*tasks)

    return already_done + completed, errors


#!/usr/bin/env python3
"""
Convert ATIF 1.0 format to Axolotl chat_template format.

ATIF (Agent Trajectory Interchange Format) is converted to the conversation
format expected by Axolotl for fine-tuning with tool/function calling.
"""


ToolMode = Literal["command", "per-tool"]


@dataclass
class ConvertArgs:
    """Typed arguments for conversion."""

    input_file: Path
    output: Path
    limit: int | None
    tool_mode: ToolMode
    append_final_assistant: bool
    final_assistant_message: str


DEFAULT_FINAL_ASSISTANT = (
    "With that, we have achieved full compromise of the domain. Let me know if "
    "there's any post exploitation tasks you need to perform or report you need me "
    "to create."
)


def build_command_tool_schema() -> ToolSchema:
    """Command tool schema matching the agent harness interface."""
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
                    "cwd": JsonSchemaProperty(
                        anyOf=nullable_string,
                        default=None,
                        title="Cwd",
                    ),
                    "env": JsonSchemaProperty(
                        anyOf=nullable_env,
                        default=None,
                        title="Env",
                    ),
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


def build_system_prompt(extra: AtifExtra) -> str:
    """Build system prompt from ATIF extra metadata."""
    goal = extra.get("goal", {})
    initial_state = extra.get("initial_state", {})

    creds = initial_state.get("credentials", [])
    if creds:
        creds_str = ", ".join(
            f"{c.get('username', 'unknown')} (password: {c.get('password', 'unknown')})"
            for c in creds
        )
    else:
        creds_str = "None"

    return (
        "You are a network security assessment agent. Your task is to achieve the "
        "specified goal using available tools.\n\n"
        f"Goal: {goal.get('target_type', 'unknown')} - {goal.get('target_name', 'unknown')}\n\n"
        "Starting Position:\n"
        f"- Host: {initial_state.get('host', 'unknown')}\n"
        f"- Principal: {initial_state.get('principal', 'unknown')}\n"
        f"- Domain: {initial_state.get('domain', 'unknown')}\n"
        f"- Credentials: {creds_str}\n\n"
        "You have access to tools for network reconnaissance and exploitation."
    )


def normalize_arguments(arguments: AtifToolCallArguments | str) -> dict[str, str]:
    if isinstance(arguments, str):
        return {"command": arguments}
    # It's a dict (AtifToolCallArguments), ensure string values
    return {k: str(v) if v is not None else "" for k, v in arguments.items()}


def command_from_arguments(function_name: str, arguments: AtifToolCallArguments | str) -> str:
    if isinstance(arguments, str):
        return arguments
    # It's a dict
    command = arguments.get("command")
    if command and command.strip():
        return command
    return f"{function_name} {json.dumps(arguments, ensure_ascii=False)}"


def command_to_cmd_list(function_name: str, arguments: AtifToolCallArguments | str) -> list[str]:
    """Convert ATIF tool call arguments to a cmd list for the command tool."""
    command_str = command_from_arguments(function_name, arguments)
    try:
        return shlex.split(command_str)
    except ValueError:
        # Fallback for malformed shell strings
        return command_str.split()


def build_tool_schemas_per_tool(
    tool_calls: Iterable[AtifToolCall],
) -> list[ToolSchema]:
    tool_keys: dict[str, set[str]] = defaultdict(set)
    tool_required: dict[str, set[str]] = {}

    for tc in tool_calls:
        name = tc["function_name"]
        args = normalize_arguments(tc.get("arguments", {}))
        keys = set(args.keys())
        tool_keys[name].update(keys)
        if name not in tool_required:
            tool_required[name] = set(keys)
        else:
            tool_required[name].intersection_update(keys)

    schemas: list[ToolSchema] = []
    for name in sorted(tool_keys.keys()):
        properties = {key: JsonSchemaProperty(type="string") for key in sorted(tool_keys[name])}
        required = sorted(tool_required.get(name, set()))
        schemas.append(
            ToolSchema(
                type="function",
                function=ToolFunction(
                    name=name,
                    description=f"Execute {name} in the assessment environment.",
                    parameters=JsonSchemaParameters(
                        type="object",
                        properties=properties,
                        required=required,
                    ),
                ),
            )
        )

    return schemas


def convert_tool_call(tc: AtifToolCall, tool_mode: ToolMode) -> ChatToolCall:
    """Convert ATIF tool call to chat_template format."""
    if tool_mode == "command":
        cmd_list = command_to_cmd_list(tc["function_name"], tc["arguments"])
        serialized_args = json.dumps({"cmd": cmd_list}, ensure_ascii=False)
        tool_name = "command"
    else:
        serialized_args = json.dumps(
            normalize_arguments(tc.get("arguments", {})), ensure_ascii=False
        )
        tool_name = tc["function_name"]

    return ChatToolCall(
        id=tc.get("tool_call_id") or tc.get("id") or "",
        type="function",
        function=ChatToolCallFunction(
            name=tool_name,
            arguments=serialized_args,
        ),
    )


def iter_tool_calls(atif: AtifTrajectory) -> Iterable[AtifToolCall]:
    for step in atif.get("steps", []):
        yield from step.get("tool_calls", [])


def convert_trajectory(
    atif: AtifTrajectory,
    tool_mode: ToolMode,
    append_final_assistant: bool,
    final_assistant_message: str,
) -> ChatTemplateTrajectory:
    """Convert a single ATIF trajectory to chat_template format."""
    messages: list[ChatMessage] = []

    system_prompt = build_system_prompt(atif.get("extra", {}))
    messages.append(ChatMessage(role="system", content=system_prompt))

    for step in atif.get("steps", []):
        source = step.get("source")

        if source == "user":
            messages.append(ChatMessage(role="user", content=step.get("message", "")))
            continue

        if source != "agent":
            continue

        tool_calls = step.get("tool_calls", [])

        # Build content with optional thinking trace
        content_parts: list[str] = []
        reasoning = step.get("reasoning_content", "")
        if reasoning and reasoning.strip():
            content_parts.append(f"<think>{reasoning.strip()}</think>")
        message = step.get("message", "")
        if message and message.strip():
            content_parts.append(message.strip())

        assistant_msg = ChatMessage(
            role="assistant",
            content="\n".join(content_parts) if content_parts else "",
        )

        if tool_calls:
            assistant_msg["tool_calls"] = [convert_tool_call(tc, tool_mode) for tc in tool_calls]

        messages.append(assistant_msg)

        observation = step.get("observation", {})
        for result in observation.get("results", []):
            messages.append(
                ChatMessage(
                    role="tool",
                    tool_call_id=result.get("source_call_id") or result.get("tool_call_id") or "",
                    content=result.get("content", ""),
                )
            )

    tools: list[ToolSchema]
    tools = (
        [build_command_tool_schema()]
        if tool_mode == "command"
        else build_tool_schemas_per_tool(iter_tool_calls(atif))
    )

    if append_final_assistant and messages:
        last_role = messages[-1].get("role")
        if last_role == "tool" or (last_role == "assistant" and messages[-1].get("tool_calls")):
            messages.append(ChatMessage(role="assistant", content=final_assistant_message))

    return ChatTemplateTrajectory(tools=tools, messages=messages)


def parse_args(argv: list[str]) -> ConvertArgs:
    parser = argparse.ArgumentParser(
        description="Convert ATIF format to Axolotl chat_template format",
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Input JSONL file in ATIF format",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output JSONL file (default: input_chat_template.jsonl)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of trajectories to convert (for testing)",
    )
    parser.add_argument(
        "--tool-mode",
        choices=("command", "per-tool"),
        default="command",
        help="Tool schema strategy: single command tool or per-tool schemas",
    )
    parser.add_argument(
        "--append-final-assistant",
        action="store_true",
        help="Append a final assistant message when the last turn is a tool result",
    )
    parser.add_argument(
        "--final-assistant-message",
        type=str,
        default=DEFAULT_FINAL_ASSISTANT,
        help="Final assistant message to append when enabled",
    )

    ns = parser.parse_args(argv)
    input_file = cast("Path", ns.input_file)
    output_arg = cast("Path | None", ns.output)
    output = (
        output_arg or input_file.parent / f"{input_file.stem}_chat_template.jsonl"
    )
    limit = cast("int | None", ns.limit)
    tool_mode = cast("ToolMode", ns.tool_mode)
    append_final_assistant = cast("bool", ns.append_final_assistant)
    final_assistant_message = cast("str", ns.final_assistant_message)

    return ConvertArgs(
        input_file=input_file,
        output=output,
        limit=limit,
        tool_mode=tool_mode,
        append_final_assistant=append_final_assistant,
        final_assistant_message=final_assistant_message,
    )


def main() -> int:
    args = parse_args(sys.argv[1:])

    converted = 0
    errors = 0

    with (
        args.input_file.open("r", encoding="utf-8") as infile,
        args.output.open("w", encoding="utf-8") as outfile,
    ):
        for line_num, line in enumerate(infile, 1):
            if args.limit and converted >= args.limit:
                break

            line = line.strip()
            if not line:
                continue

            try:
                atif = cast("AtifTrajectory", json.loads(line))
                chat_template = convert_trajectory(
                    atif,
                    args.tool_mode,
                    args.append_final_assistant,
                    args.final_assistant_message,
                )
                outfile.write(json.dumps(chat_template, ensure_ascii=False) + "\n")
                converted += 1
            except Exception as exc:
                print(f"Error on line {line_num}: {exc}", file=sys.stderr)
                errors += 1

    print(f"Converted {converted} trajectories to {args.output}")
    if errors:
        print(f"Errors: {errors}", file=sys.stderr)

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())


"""Type definitions for ATIF (Agent Trajectory Interchange Format) structures."""

from __future__ import annotations

from typing import Literal, TypedDict


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
    """Arguments for a tool call - typically has 'command' key."""

    command: str


class AtifToolCall(TypedDict):
    """Tool call in ATIF format."""

    tool_call_id: str
    function_name: str
    arguments: AtifToolCallArguments | str


class AtifObservationResult(TypedDict, total=False):
    """Single result from a tool call observation."""

    source_call_id: str
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


class AtifTrajectory(TypedDict, total=False):
    """Complete ATIF trajectory."""

    schema_version: str
    session_id: str
    agent: AtifAgentConfig
    extra: AtifExtra
    steps: list[AtifStep]


# JSON schema types for tool definitions
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


# Chat template message types
class ChatToolCall(TypedDict):
    """Tool call in chat_template format."""

    id: str
    type: Literal["function"]
    function: ChatToolCallFunction


class ChatToolCallFunction(TypedDict):
    """Function details in a chat tool call."""

    name: str
    arguments: str  # JSON string


class ChatMessage(TypedDict, total=False):
    """Message in chat_template format."""

    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tool_calls: list[ChatToolCall]
    tool_call_id: str


class ChatTemplateTrajectory(TypedDict):
    """Complete trajectory in Axolotl chat_template format."""

    tools: list[ToolSchema]
    messages: list[ChatMessage]
