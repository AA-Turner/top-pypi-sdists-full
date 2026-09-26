"""
Reflector agent: build prompts, call LLM, parse output.

Mirrors: packages/memory/src/processors/observational-memory/reflector-agent.ts
"""

from __future__ import annotations

import re
from typing import Optional

from .constants import COMPRESSION_LEVELS
from .types import ModelConfig, ReflectorResult


# The Reflector's system prompt (persona, observation format reference, rules,
# output format) is the memory.reflector mandate Holder's (2026-09-25) — seeded
# verbatim from what used to be assembled here.


# ---------------------------------------------------------------------------
# Task prompt construction
# ---------------------------------------------------------------------------

def build_reflector_variables(
    observations: str,
    current_task: Optional[str] = None,
    manual_prompt: Optional[str] = None,
    compression_level: int = 0,
) -> dict[str, str]:
    """
    Build what the Reflector's Holder receives (memory.reflector).

    The instruction text — the compression guidance for each level and the
    "## Your Task" statement — is the Holder's own user turn (2026-09-25
    residue pass). This offers only the material, the config's own extra
    instruction, and which level's guidance applies: every OTHER level's
    ``compression_guidance_level_N`` is sent empty, so only the run's level
    keeps the Holder's text (level 0 = none).

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

    variables: dict[str, str] = {
        f"compression_guidance_level_{level}": ""
        for level in COMPRESSION_LEVELS
        if level != compression_level
    }
    variables["additional_instructions"] = (
        f"\n\n## Additional Instructions\n{manual_prompt}" if manual_prompt else ""
    )
    variables["material"] = "\n".join(parts)
    return variables


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
        llm_call_fn: Async callable(mandate_key=, messages=, model=, variables=) → str.
        instruction: Optional additional instruction from config.
        max_compression_levels: How many compression levels to try (0 through N).
    
    Returns:
        ReflectorResult (raises ValueError if all levels failed).
    """
    for level in range(max_compression_levels + 1):
        raw_output = await llm_call_fn(
            mandate_key=model_config.mandate_key,
            messages=[],
            model=model_config.model,
            variables=build_reflector_variables(
                observations=observations,
                current_task=current_task,
                manual_prompt=instruction,
                compression_level=level,
            ),
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
