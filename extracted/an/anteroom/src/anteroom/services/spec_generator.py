"""LLM-assisted spec generation from prompts and GitHub issues (#1165).

Follows the ``compile_from_prompt()`` pattern in ``mission_compiler.py``:
builds a system prompt, calls ``ai_service.complete()`` (non-streaming),
parses the JSON response, and converts to spec YAML.
"""

from __future__ import annotations

import json
import logging
import subprocess
from typing import Any

from .spec_schema import (
    SPEC_GENERATION_SCHEMA,
    SpecContent,
    SpecMode,
    SpecTask,
    serialize_spec_content,
)

logger = logging.getLogger(__name__)

_SPEC_SYSTEM_PROMPT = """\
You are a software specification author. Given a user request, output a JSON object \
matching this schema:

{schema}

Rules:
- requirements: a clear description of what the feature must do.
- design: a technical description of how to implement it.
- tasks: a list of implementation tasks with unique IDs (short, snake_case).
- depends_on references other tasks' id values within the same spec.
- Output ONLY valid JSON, no markdown fences, no commentary.
"""


async def generate_spec_from_prompt(
    prompt: str,
    *,
    ai_service: Any,
    namespace: str,
    name: str,
) -> str:
    """Generate spec YAML from a natural-language prompt via LLM.

    Returns YAML string on success, or raw LLM output with a WARNING header
    on parse failure.
    """
    system = _SPEC_SYSTEM_PROMPT.format(schema=json.dumps(SPEC_GENERATION_SCHEMA, indent=2))
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    raw = await ai_service.complete(messages, max_completion_tokens=2000)

    if not raw:
        return _fallback_raw("LLM returned empty response")

    return _parse_and_convert(raw)


async def generate_spec_from_issue(
    issue_number: int,
    *,
    ai_service: Any,
    namespace: str,
    name: str,
) -> str:
    """Fetch a GitHub issue and generate spec YAML from its content.

    Uses ``gh issue view`` to retrieve the issue, then delegates to
    :func:`generate_spec_from_prompt`.

    Raises ``ValueError`` on subprocess failure.
    """
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_number), "--json", "title,body,labels"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValueError(f"Timed out fetching issue #{issue_number}") from exc
    except FileNotFoundError as exc:
        raise ValueError("GitHub CLI (gh) not found — install it to use --from-issue") from exc

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise ValueError(f"Failed to fetch issue #{issue_number}: {stderr}")

    try:
        issue_data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not parse gh output for issue #{issue_number}") from exc

    title = issue_data.get("title", "")
    body = issue_data.get("body", "")
    labels = issue_data.get("labels") or []
    label_names = [lb.get("name", "") if isinstance(lb, dict) else str(lb) for lb in labels]

    prompt_parts = [f"Title: {title}"]
    if body:
        prompt_parts.append(f"Description:\n{body}")
    if label_names:
        prompt_parts.append(f"Labels: {', '.join(label_names)}")

    prompt = "\n\n".join(prompt_parts)
    return await generate_spec_from_prompt(
        prompt,
        ai_service=ai_service,
        namespace=namespace,
        name=name,
    )


def _parse_and_convert(raw: str) -> str:
    """Parse LLM JSON output and convert to spec YAML."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("LLM returned invalid JSON for spec generation")
        return _fallback_raw(raw)

    if not isinstance(data, dict):
        return _fallback_raw(raw)

    requirements = data.get("requirements")
    design = data.get("design")
    raw_tasks = data.get("tasks")

    if not isinstance(requirements, str) or not requirements.strip():
        return _fallback_raw(raw)
    if not isinstance(design, str) or not design.strip():
        return _fallback_raw(raw)
    if not isinstance(raw_tasks, list):
        return _fallback_raw(raw)

    tasks: list[SpecTask] = []
    for item in raw_tasks:
        if not isinstance(item, dict):
            return _fallback_raw(raw)
        task_id = str(item.get("id", f"t{len(tasks) + 1}"))
        summary = str(item.get("summary", ""))
        depends_on = item.get("depends_on", [])
        if not isinstance(depends_on, list):
            depends_on = []
        depends_on = [str(d) for d in depends_on]
        tasks.append(SpecTask(id=task_id, summary=summary, depends_on=depends_on))

    if not tasks:
        return _fallback_raw(raw)

    spec = SpecContent(
        requirements=requirements,
        design=design,
        tasks=tasks,
        mode=SpecMode.FEATURE,
    )
    return serialize_spec_content(spec)


def _fallback_raw(raw: str) -> str:
    """Return raw output with a warning header when parsing fails."""
    return f"# WARNING: Could not parse LLM output — review and fix manually\n{raw}"
