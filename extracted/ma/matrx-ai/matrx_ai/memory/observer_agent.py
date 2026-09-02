"""
Observer agent: build prompts, call LLM, parse output.

Mirrors: packages/memory/src/processors/observational-memory/observer-agent.ts
"""

from __future__ import annotations

import re
import textwrap
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from .constants import (
    OBSERVER_EXTRACTION_INSTRUCTIONS,
    OBSERVER_GUIDELINES,
    OBSERVER_PERSONA,
)
from .types import Message, MessageRole, ModelConfig, ObserverResult


# ---------------------------------------------------------------------------
# System prompt construction
# ---------------------------------------------------------------------------

def build_observer_system_prompt(
    multi_thread: bool = False,
    instruction: Optional[str] = None,
    include_thread_title: bool = False,
) -> str:
    """
    Build the observer system prompt.
    
    Args:
        multi_thread: If True, include instructions for batched multi-thread observation.
        instruction: Optional extra instruction appended at the end.
        include_thread_title: Whether the observer should suggest a thread title.
    """
    sections = [
        OBSERVER_PERSONA,
        "",
        OBSERVER_EXTRACTION_INSTRUCTIONS,
        "",
        OBSERVER_GUIDELINES,
        "",
        build_observer_output_format(include_thread_title),
    ]

    if multi_thread:
        sections.append(
            "\n## Multi-Thread Mode\n"
            "You will be given multiple conversations. Process each independently.\n"
            "Wrap each response in <thread id=\"THREAD_ID\">...</thread> tags."
        )

    if instruction:
        sections.append(f"\n## Additional Instructions\n{instruction}")

    return "\n".join(sections)


def build_observer_output_format(include_thread_title: bool = False) -> str:
    """Return the XML output format specification for the Observer."""
    title_section = ""
    if include_thread_title:
        title_section = """
<thread-title>
A short descriptive title for this conversation (5-8 words)
</thread-title>"""

    return textwrap.dedent(f"""\
        ## Output Format

        Respond ONLY with the following XML structure. Do not include any text outside these tags.

        <observations>
        Date: Month Day, Year
        * [EMOJI] (HH:MM) [observation text]
          * -> [supporting detail or tool call result]
          * -> [another detail]
        * [EMOJI] (HH:MM) [another observation]
        </observations>

        <current-task>
        What the agent is currently focused on (1-3 sentences)
        </current-task>

        <suggested-response>
        A brief hint for what the agent should do or say next
        </suggested-response>{title_section}

        Priority emojis: 🔴 high | 🟡 medium | 🟢 low | ✅ completed
        Sub-bullets use "  * ->" prefix (two spaces, asterisk, right-arrow)
    """)


# ---------------------------------------------------------------------------
# User/task prompt construction
# ---------------------------------------------------------------------------

def build_observer_prompt(
    existing_observations: Optional[str],
    messages: list[Message],
    timezone: str = "UTC",
    current_task: Optional[str] = None,
    previous_response_hint: Optional[str] = None,
    resource_id: Optional[str] = None,
    thread_id: Optional[str] = None,
) -> str:
    """
    Build the user-turn prompt for the Observer LLM.
    
    Args:
        existing_observations: Current observation text the Observer should extend (not replace).
        messages: New unobserved messages to process.
        timezone: Timezone for formatting timestamps.
        current_task: Prior `current_task` value (passed for context).
        previous_response_hint: Prior `suggested_response` value.
    """
    parts: list[str] = []

    if existing_observations:
        parts.append("## Existing Observations (DO NOT repeat these — only ADD new ones)\n")
        parts.append(existing_observations)
        parts.append("")

    if current_task:
        parts.append(f"## Current Task\n{current_task}\n")

    if previous_response_hint:
        parts.append(f"## Pending Response Hint\n{previous_response_hint}\n")

    parts.append("## New Messages to Observe\n")
    parts.append(format_messages_for_observer(messages, timezone))

    parts.append(
        "\n## Your Task\n"
        "Extract observations from the new messages above. "
        "Append them to the existing observations (do not duplicate existing ones). "
        "Update <current-task> and <suggested-response> to reflect the current state."
    )

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Message formatting for Observer (text representation of the conversation)
# ---------------------------------------------------------------------------

def format_messages_for_observer(
    messages: list[Message],
    timezone: str = "UTC",
) -> str:
    """
    Format a list of messages as readable text for the Observer LLM.
    
    Output:
        Dec 4 2025:
        User (2:30 PM): Hello
        Assistant (2:31 PM): Hi there!
        Tool Call my_tool (2:31 PM):
        {"arg": "value"}
        Tool Result my_tool (2:31 PM): result content
    """
    tz = ZoneInfo(timezone)
    lines: list[str] = []
    last_date: Optional[str] = None

    for msg in messages:
        ts = msg.created_at.astimezone(tz)
        date_str = ts.strftime("%b %-d %Y")
        time_str = ts.strftime("%-I:%M %p")

        if date_str != last_date:
            if lines:
                lines.append("")
            lines.append(f"{date_str}:")
            last_date = date_str

        role = msg.role
        content = msg.content

        if isinstance(content, str):
            if role == MessageRole.USER:
                lines.append(f"User ({time_str}): {content}")
            elif role == MessageRole.ASSISTANT:
                lines.append(f"Assistant ({time_str}): {content}")
            elif role == MessageRole.SYSTEM:
                lines.append(f"System ({time_str}): {content}")
        elif isinstance(content, list):
            from .types import TextPart, ToolCallPart, ToolResultPart, ImagePart
            import json

            role_label = {
                MessageRole.USER: "User",
                MessageRole.ASSISTANT: "Assistant",
                MessageRole.SYSTEM: "System",
                MessageRole.TOOL: "Tool",
            }.get(role, str(role))

            text_parts = []
            for part in content:
                if isinstance(part, TextPart):
                    text_parts.append(part.text)
                elif isinstance(part, ToolCallPart):
                    if text_parts:
                        lines.append(f"{role_label} ({time_str}): {''.join(text_parts)}")
                        text_parts = []
                    args_str = json.dumps(part.args, indent=2)
                    lines.append(f"Tool Call {part.tool_name} ({time_str}):")
                    lines.append(args_str)
                elif isinstance(part, ToolResultPart):
                    result_str = (
                        json.dumps(part.result, indent=2)
                        if isinstance(part.result, (dict, list))
                        else str(part.result)
                    )
                    # Truncate very long tool results
                    if len(result_str) > 4000:
                        result_str = result_str[:4000] + "\n... [truncated]"
                    lines.append(f"Tool Result {part.tool_name} ({time_str}): {result_str}")
                elif isinstance(part, ImagePart):
                    fname = part.filename or "image"
                    lines.append(f"{role_label} ({time_str}): [Image: {fname}]")

            if text_parts:
                lines.append(f"{role_label} ({time_str}): {''.join(text_parts)}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output parsing
# ---------------------------------------------------------------------------

_OBSERVATIONS_RE = re.compile(
    r"<observations>(.*?)</observations>",
    re.DOTALL | re.IGNORECASE,
)
_CURRENT_TASK_RE = re.compile(
    r"<current-task>(.*?)</current-task>",
    re.DOTALL | re.IGNORECASE,
)
_SUGGESTED_RESPONSE_RE = re.compile(
    r"<suggested-response>(.*?)</suggested-response>",
    re.DOTALL | re.IGNORECASE,
)
_THREAD_TITLE_RE = re.compile(
    r"<thread-title>(.*?)</thread-title>",
    re.DOTALL | re.IGNORECASE,
)


def parse_observer_output(
    output: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> Optional[ObserverResult]:
    """
    Parse the XML output from the Observer LLM.
    
    Returns None if the output lacks an <observations> block (failed/malformed).
    """
    obs_match = _OBSERVATIONS_RE.search(output)
    if not obs_match:
        return None

    observations = obs_match.group(1).strip()

    # Guard: detect degenerate repetition (LLM got stuck in a loop)
    if detect_degenerate_repetition(observations):
        return None

    # Sanitize lines
    observations = sanitize_observation_lines(observations)

    task_match = _CURRENT_TASK_RE.search(output)
    current_task = task_match.group(1).strip() if task_match else None

    hint_match = _SUGGESTED_RESPONSE_RE.search(output)
    suggested_response = hint_match.group(1).strip() if hint_match else None

    title_match = _THREAD_TITLE_RE.search(output)
    thread_title = title_match.group(1).strip() if title_match else None

    return ObserverResult(
        observations=observations,
        current_task=current_task,
        suggested_response=suggested_response,
        thread_title=thread_title,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )


# ---------------------------------------------------------------------------
# Multi-thread output parsing
# ---------------------------------------------------------------------------

_THREAD_BLOCK_RE = re.compile(
    r'<thread\s+id="([^"]+)">(.*?)</thread>',
    re.DOTALL | re.IGNORECASE,
)


def parse_multi_thread_observer_output(
    output: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> dict[str, ObserverResult]:
    """
    Parse batched multi-thread observer output.
    
    Returns a dict mapping thread_id → ObserverResult.
    """
    results: dict[str, ObserverResult] = {}
    for match in _THREAD_BLOCK_RE.finditer(output):
        thread_id = match.group(1)
        block_content = match.group(2)
        result = parse_observer_output(block_content, input_tokens, output_tokens)
        if result is not None:
            results[thread_id] = result
    return results


# ---------------------------------------------------------------------------
# Context optimization (strip visual markers before injecting into Actor)
# ---------------------------------------------------------------------------

_MEDIUM_LOW_EMOJI_RE = re.compile(r"[🟡🟢]")
_SEMANTIC_TAG_RE = re.compile(r"\[[\w\s,]+\]")
_ARROW_RE = re.compile(r"\s*->\s*")


def optimize_observations_for_context(observations: str) -> str:
    """
    Strip visual clutter from observations before injecting into the Actor's context.
    
    - Remove 🟡 and 🟢 emojis (keep 🔴 and ✅)
    - Remove [semantic-tag, tag] markers
    - Remove arrow indicators (-> becomes a space)
    - Collapse multiple spaces/blank lines
    """
    text = _MEDIUM_LOW_EMOJI_RE.sub("", observations)
    text = _SEMANTIC_TAG_RE.sub("", text)
    text = _ARROW_RE.sub(" ", text)
    # Collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)
    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Observation truncation for Observer context (preserve important observations)
# ---------------------------------------------------------------------------

_RED_PRIORITY_RE = re.compile(r"^\s*\*\s*🔴")


def truncate_observations_for_observer(
    observations: str,
    token_budget: int,
    count_tokens_fn,
) -> str:
    """
    Truncate prior observations to fit within a token budget for the Observer prompt.
    
    Strategy:
    1. Keep as much raw tail (recent observations) as possible.
    2. If still over budget, rescue 🔴-priority lines from the truncated head.
    3. Add a "[N observations truncated here]" marker at the gap.
    4. Ensure at least 50% of kept observations are raw tail.
    """
    if count_tokens_fn(observations) <= token_budget:
        return observations

    lines = observations.split("\n")
    total_lines = len(lines)

    # Walk from the end, accumulate lines until we hit 80% of budget
    tail_budget = int(token_budget * 0.8)
    tail_lines: list[str] = []
    tail_tokens = 0
    cutoff_idx = total_lines  # index from which we start keeping lines

    for i in range(total_lines - 1, -1, -1):
        line_tokens = count_tokens_fn(lines[i])
        if tail_tokens + line_tokens > tail_budget:
            cutoff_idx = i + 1
            break
        tail_lines.insert(0, lines[i])
        tail_tokens += line_tokens

    if cutoff_idx == 0:
        # Nothing was truncated
        return observations

    head_lines = lines[:cutoff_idx]
    truncated_count = len(head_lines)

    # Rescue 🔴 lines from head within remaining 20% budget
    rescue_budget = token_budget - tail_tokens
    rescued: list[str] = []
    rescued_tokens = 0
    # Go newest-first within the head
    for line in reversed(head_lines):
        if _RED_PRIORITY_RE.match(line):
            lt = count_tokens_fn(line)
            if rescued_tokens + lt <= rescue_budget:
                rescued.insert(0, line)
                rescued_tokens += lt

    marker = f"[{truncated_count} observations truncated]"
    if rescued:
        result_parts = rescued + [marker] + tail_lines
    else:
        result_parts = [marker] + tail_lines

    return "\n".join(result_parts)


# ---------------------------------------------------------------------------
# Degenerate repetition detection
# ---------------------------------------------------------------------------

def detect_degenerate_repetition(text: str, threshold: float = 0.4) -> bool:
    """
    Detect if an LLM output is stuck in a repetition loop.
    
    Algorithm:
    - Sample ~50 windows of 200 chars across the entire text
    - If >threshold (40%) of windows are duplicates → degenerate
    - Also flag single lines >50,000 chars
    """
    if not text:
        return False

    # Check for absurdly long lines
    for line in text.split("\n"):
        if len(line) > 50_000:
            return True

    window_size = 200
    if len(text) < window_size * 2:
        return False

    # Sample 50 windows uniformly
    num_samples = min(50, len(text) // window_size)
    step = max(1, (len(text) - window_size) // num_samples)
    windows = set()
    duplicate_count = 0

    for i in range(0, len(text) - window_size, step):
        window = text[i : i + window_size]
        if window in windows:
            duplicate_count += 1
        else:
            windows.add(window)

    ratio = duplicate_count / max(1, num_samples)
    return ratio > threshold


# ---------------------------------------------------------------------------
# Observation line sanitization
# ---------------------------------------------------------------------------

def sanitize_observation_lines(observations: str, max_line_length: int = 10_000) -> str:
    """
    Truncate any single observation line that exceeds max_line_length characters.
    This guards against edge cases where the LLM copies huge content verbatim.
    """
    lines = observations.split("\n")
    sanitized = []
    for line in lines:
        if len(line) > max_line_length:
            line = line[:max_line_length] + "… [truncated]"
        sanitized.append(line)
    return "\n".join(sanitized)


# ---------------------------------------------------------------------------
# LLM call wrapper (bring-your-own client)
# ---------------------------------------------------------------------------

async def run_observer(
    model_config: ModelConfig,
    system_prompt: str,
    user_prompt: str,
    llm_call_fn,
) -> ObserverResult:
    """
    Run the Observer LLM and parse its output.
    
    Args:
        model_config: Model, temperature, max_tokens settings.
        system_prompt: Built via build_observer_system_prompt().
        user_prompt: Built via build_observer_prompt().
        llm_call_fn: Async callable(model, messages, temperature, max_tokens) → str.
            You must provide this — it wraps your preferred LLM SDK.
            
    Returns:
        ObserverResult (raises ValueError if output couldn't be parsed after 2 attempts).
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    for attempt in range(2):
        raw_output = await llm_call_fn(
            model=model_config.model,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
        )

        result = parse_observer_output(raw_output)
        if result is not None:
            return result

        if attempt == 0:
            # Retry with a nudge
            messages.append({"role": "assistant", "content": raw_output})
            messages.append({
                "role": "user",
                "content": (
                    "Your response was missing the required <observations> block or contained "
                    "degenerate repetition. Please try again with just the XML output."
                ),
            })

    raise ValueError("Observer LLM failed to produce valid output after 2 attempts.")
