"""
Reflector agent: build prompts, call LLM, parse output.

Mirrors: packages/memory/src/processors/observational-memory/reflector-agent.ts
"""

from __future__ import annotations

import re
import textwrap
from typing import Optional

from .constants import (
    COMPRESSION_GUIDANCE,
    OBSERVER_EXTRACTION_INSTRUCTIONS,
    REFLECTOR_PERSONA,
    REFLECTOR_RULES,
)
from .types import ModelConfig, ReflectorResult


# ---------------------------------------------------------------------------
# System prompt construction
# ---------------------------------------------------------------------------

def build_reflector_system_prompt(instruction: Optional[str] = None) -> str:
    """
    Build the reflector system prompt.
    
    The Reflector is given the same extraction instructions as the Observer
    so it understands exactly how observations were created and how to preserve
    the intent of each entry while condensing them.
    """
    sections = [
        REFLECTOR_PERSONA,
        "",
        "## Observation Format Reference",
        "(You created observations following these rules — use them to guide compression)",
        "",
        OBSERVER_EXTRACTION_INSTRUCTIONS,
        "",
        REFLECTOR_RULES,
        "",
        _REFLECTOR_OUTPUT_FORMAT,
    ]

    if instruction:
        sections.append(f"\n## Additional Instructions\n{instruction}")

    return "\n".join(sections)


_REFLECTOR_OUTPUT_FORMAT = textwrap.dedent("""\
    ## Output Format

    Respond ONLY with the refined observations block. Same format as input.
    Do not include any explanation, preamble, or text outside the observations.

    <observations>
    Date: Month Day, Year
    * 🔴 (HH:MM) [compressed observation]
      * -> [essential supporting detail only]
    </observations>

    <current-task>
    Updated current task (if different from source)
    </current-task>

    <suggested-response>
    Updated response hint (if different from source)
    </suggested-response>
""")


# ---------------------------------------------------------------------------
# Task prompt construction
# ---------------------------------------------------------------------------

def build_reflector_prompt(
    observations: str,
    current_task: Optional[str] = None,
    manual_prompt: Optional[str] = None,
    compression_level: int = 0,
) -> str:
    """
    Build the user-turn prompt for the Reflector LLM.
    
    Args:
        observations: The full current observation text to compress.
        current_task: Current task context from the OM record.
        manual_prompt: Optional override instruction from config.
        compression_level: 0-4. Higher = more aggressive compression.
    """
    parts: list[str] = []

    if current_task:
        parts.append(f"## Current Task Context\n{current_task}\n")

    parts.append("## Observations to Compress\n")
    parts.append(observations)

    guidance = COMPRESSION_GUIDANCE.get(compression_level, "")
    if guidance:
        parts.append(f"\n## Compression Guidance\n{guidance}")

    if manual_prompt:
        parts.append(f"\n## Additional Instructions\n{manual_prompt}")

    parts.append(
        "\n## Your Task\n"
        "Compress and reorganize the observations above while preserving all important "
        "information. Output ONLY the refined <observations> block (and optionally "
        "updated <current-task> and <suggested-response>)."
    )

    return "\n".join(parts)


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


def parse_reflector_output(
    output: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> Optional[ReflectorResult]:
    """
    Parse the XML output from the Reflector LLM.
    
    Returns None if the output lacks an <observations> block or is degenerate.
    """
    from .observer_agent import detect_degenerate_repetition, sanitize_observation_lines

    obs_match = _OBSERVATIONS_RE.search(output)
    if not obs_match:
        return None

    reflections = obs_match.group(1).strip()

    if detect_degenerate_repetition(reflections):
        return None

    reflections = sanitize_observation_lines(reflections)

    return ReflectorResult(
        reflections=reflections,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )


# ---------------------------------------------------------------------------
# Compression validation
# ---------------------------------------------------------------------------

def validate_compression(
    reflected_tokens: int,
    target_threshold: int,
    tolerance: float = 1.05,
) -> bool:
    """
    Check if the reflection actually compressed below the target threshold.
    
    Args:
        reflected_tokens: Token count of the reflector output.
        target_threshold: The observationTokens threshold we're trying to go below.
        tolerance: Allow up to 5% over threshold (default) to account for counting imprecision.
    
    Returns:
        True if compression achieved the target.
    """
    return reflected_tokens <= round(target_threshold * tolerance)


# ---------------------------------------------------------------------------
# LLM call wrapper with retry + escalating compression
# ---------------------------------------------------------------------------

async def run_reflector(
    model_config: ModelConfig,
    observations: str,
    current_task: Optional[str],
    target_threshold: int,
    count_tokens_fn,
    llm_call_fn,
    instruction: Optional[str] = None,
    max_compression_levels: int = 4,
) -> ReflectorResult:
    """
    Run the Reflector LLM with escalating compression levels until the output
    fits within the target_threshold.
    
    Args:
        model_config: Model settings.
        observations: Current observation text to compress.
        current_task: Current task for context.
        target_threshold: Token target for the output (observationTokens threshold).
        count_tokens_fn: Callable(str) -> int.
        llm_call_fn: Async callable(model, messages, temperature, max_tokens) → str.
        instruction: Optional additional instruction from config.
        max_compression_levels: How many compression levels to try (0 through N).
    
    Returns:
        ReflectorResult (raises ValueError if all levels failed).
    """
    system_prompt = build_reflector_system_prompt(instruction)

    for level in range(max_compression_levels + 1):
        user_prompt = build_reflector_prompt(
            observations=observations,
            current_task=current_task,
            manual_prompt=instruction,
            compression_level=level,
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        raw_output = await llm_call_fn(
            model=model_config.model,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
        )

        result = parse_reflector_output(raw_output)
        if result is None:
            continue

        token_count = count_tokens_fn(result.reflections)
        result = ReflectorResult(
            reflections=result.reflections,
            input_tokens=result.input_tokens,
            output_tokens=token_count,
        )

        if validate_compression(token_count, target_threshold):
            return result

        # Compression level escalates on next iteration

    raise ValueError(
        f"Reflector failed to compress observations below {target_threshold} tokens "
        f"after {max_compression_levels + 1} attempts."
    )
