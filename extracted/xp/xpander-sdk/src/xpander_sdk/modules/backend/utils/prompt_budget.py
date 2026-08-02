"""Read-only attribution of the assembled prompt, logged as one line per build.

The static prefix (system prompt + tool schemas) is re-read on every turn, so it
is the largest recurring cost in a long task. This module answers "which bytes"
without touching them: it analyses the finished ``args`` and logs sizes. It
never mutates, never writes back, and returns nothing.

NEVER log prompt content here - not a preview, not a head, not a truncated
sample. The prompt carries user memories and org data. Sizes and the fixed
section names only.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import OrderedDict
from typing import Any, Dict, List, Mapping, Optional, Tuple

from loguru import logger

from xpander_sdk.core.context_optimizer.constants import PROMPT_BUDGET_ENABLED

# Below this a module-level string is config or a short message, not a prompt block.
MIN_CONSTANT_CHARS = 200

# Blocks assembled at runtime, identified by the XML wrappers they already carry.
TRACKED_TAGS: Tuple[str, ...] = (
    "dynamic_tools",
    "skills",
    "memories",
    "context",
    "prior_tasks",
    "original_user_request",
    "output_formatting",
    "workspace_reality",
    "live_surfaces",
    "markdown_capabilities",
    "agent_identity",
    "expected_output",
    "workspace_access_rules",
    "compacted_context",
    "last_actions",
    "retry_focus",
    "deep_planning",
    "skill_dispatch",
)


# Same chars/4 with a 1.2x margin the context optimizer uses, so every token
# figure in the logs is on one basis.
def _tokens(chars: int) -> int:
    return int(chars / 4 * 1.2)


def collect_prompt_constants(namespace: Mapping[str, Any]) -> Dict[str, str]:
    """Every module-level prompt literal in *namespace*, by reflection.

    Reflection rather than a hand-maintained table: a new constant is picked up
    automatically instead of silently inflating ``unattributed``.
    """
    return {
        name: value
        for name, value in namespace.items()
        if name.isupper()
        and isinstance(value, str)
        and len(value) >= MIN_CONSTANT_CHARS
    }


def _label(name: str) -> str:
    return name.lower().lstrip("_").removesuffix("_instructions")


def _tag_spans(text: str, tag: str) -> List[Tuple[int, int, str]]:
    """Spans of ``<tag ...>...</tag>``, tolerating attributes on the open tag."""
    pattern = re.compile(
        rf"<{re.escape(tag)}(?:\s[^>]*)?>.*?</{re.escape(tag)}>", re.DOTALL
    )
    return [(m.start(), m.end(), tag) for m in pattern.finditer(text)]


def attribute(text: Optional[str], constants: Mapping[str, str]) -> Dict[str, int]:
    """Token counts per identified section, plus a self-closing remainder.

    Claims spans longest-first so a constant nested inside a larger one is not
    counted twice; ``unattributed`` is the arithmetic remainder and can never go
    negative. A section that appears more than once is credited once - the
    repeats fall into the remainder rather than inflating the total.
    """
    if not text:
        return {"total_tok": 0}

    candidates: List[Tuple[int, int, str]] = []
    for name, value in constants.items():
        start = text.find(value)
        if start != -1:
            candidates.append((start, start + len(value), _label(name)))
    for tag in TRACKED_TAGS:
        candidates.extend(_tag_spans(text, tag))

    candidates.sort(key=lambda s: s[1] - s[0], reverse=True)

    claimed: List[Tuple[int, int]] = []
    sections: Dict[str, int] = {}
    for start, end, label in candidates:
        if any(start < c_end and end > c_start for c_start, c_end in claimed):
            continue
        claimed.append((start, end))
        sections[label] = sections.get(label, 0) + (end - start)

    total = len(text)
    accounted = sum(sections.values())
    out = {label: _tokens(chars) for label, chars in sections.items()}
    out["unattributed"] = _tokens(total - accounted)
    out["total_tok"] = _tokens(total)
    return out


def _tool_family(name: str) -> str:
    for prefix, family in (
        ("xpworkspace-", "xpworkspace"),
        ("xpschedule-", "xpschedule"),
        ("xplivesurface-", "xplivesurface"),
        ("xpchatcard-", "xpchatcard"),
        ("xp_", "xp_meta"),
        ("mcp_tool_", "mcp"),
    ):
        if name.startswith(prefix):
            return family
    if name.startswith("xp"):
        return "xp_other"
    return "other"


def _schema_chars(entry: Any) -> List[Tuple[str, int]]:
    """(name, serialized size) for a tool entry - agno Function, toolkit, or callable."""
    functions = getattr(entry, "functions", None)
    if isinstance(functions, dict):
        out: List[Tuple[str, int]] = []
        for fn in functions.values():
            out.extend(_schema_chars(fn))
        return out

    name = getattr(entry, "name", None) or getattr(entry, "__name__", None)
    if not isinstance(name, str):
        return [("_unknown", 0)]
    schema = {
        "name": name,
        "description": getattr(entry, "description", "") or "",
        "parameters": getattr(entry, "parameters", None),
    }
    try:
        size = len(json.dumps(schema, default=str))
    except Exception:
        size = len(str(schema))
    return [(name, size)]


def attribute_tools(tools: Optional[List[Any]]) -> Dict[str, int]:
    families: Dict[str, int] = {}
    count = 0
    for entry in tools or []:
        try:
            measured = _schema_chars(entry)
        except Exception:
            measured = [("_unknown", 0)]
        for name, size in measured:
            families[_tool_family(name)] = families.get(_tool_family(name), 0) + size
            count += 1
    out = {family: _tokens(chars) for family, chars in families.items()}
    out["total_tok"] = _tokens(sum(families.values()))
    out["count"] = count
    return out


def _wire_tool_families(tools: Optional[List[Any]]) -> Dict[str, int]:
    """Per-family sizes of the serialized tool specs actually sent to the provider.

    Handles both wire shapes: Bedrock ``{"toolSpec": {...}}`` and Anthropic's flat
    ``{"name": ..., "input_schema": ...}``. Anything else lands in ``other``.
    """
    families: Dict[str, int] = {}
    count = 0
    for entry in tools or []:
        if not isinstance(entry, dict):
            continue
        spec = (
            entry.get("toolSpec") if isinstance(entry.get("toolSpec"), dict) else entry
        )
        name = spec.get("name")
        if not isinstance(name, str):
            # Breakpoint markers ride the same list and are not tools.
            continue
        try:
            size = len(json.dumps(entry, default=str))
        except Exception:
            size = len(str(entry))
        family = _tool_family(name)
        families[family] = families.get(family, 0) + size
        count += 1
    out = {family: _tokens(chars) for family, chars in families.items()}
    out["total_tok"] = _tokens(sum(families.values()))
    out["count"] = count
    return out


# Fingerprints already logged. The system prefix is identical across a run's turns and
# differs between runs, so this yields one line per run without needing a run id, and
# stays bounded because model instances are process-wide.
_WIRE_SEEN: "OrderedDict[str, None]" = OrderedDict()
_WIRE_SEEN_MAX = 256


def _wire_already_logged(fingerprint: str) -> bool:
    if fingerprint in _WIRE_SEEN:
        return True
    _WIRE_SEEN[fingerprint] = None
    while len(_WIRE_SEEN) > _WIRE_SEEN_MAX:
        _WIRE_SEEN.popitem(last=False)
    return False


def log_wire_budget(
    *,
    provider: str,
    system_text: str,
    tools: Optional[List[Any]] = None,
) -> None:
    """Log what the provider was actually billed for, once per run. Never raises.

    The build-time line measures what the SDK assembled; this measures the request
    itself, so the two reconcile against the turn's cache_write instead of leaving an
    unexplained gap. Sizes only - never prompt content.
    """
    if not PROMPT_BUDGET_ENABLED:
        return
    try:
        from xpander_sdk.modules.backend.frameworks._cache_split import (
            current_prompt_owner,
        )

        text = system_text or ""
        fingerprint = hashlib.md5(f"{provider}|{text}".encode()).hexdigest()
        if _wire_already_logged(fingerprint):
            return
        payload = {
            "owner": current_prompt_owner.get(""),
            "provider": provider,
            "system_tok": _tokens(len(text)),
            "tools": _wire_tool_families(tools),
        }
        payload["total_tok"] = payload["system_tok"] + payload["tools"]["total_tok"]
        logger.info(
            f"[prompt-budget] wire {json.dumps(payload, separators=(',', ':'))}"
        )
    except Exception as exc:
        logger.debug(f"[prompt-budget] wire skipped: {exc}")


def log_prompt_budget(
    args: Mapping[str, Any],
    namespace: Mapping[str, Any],
    task_id: str = "",
    agent_id: str = "",
) -> None:
    """Log the assembled prompt's composition. Read-only; never raises."""
    if not PROMPT_BUDGET_ENABLED:
        return
    try:
        constants = collect_prompt_constants(namespace)
        instructions = attribute(args.get("instructions"), constants)
        additional = attribute(args.get("additional_context"), constants)
        tools = attribute_tools(args.get("tools"))
        payload = {
            "task_id": task_id,
            "agent_id": agent_id,
            "instructions": instructions,
            "additional_context": additional,
            "tools": tools,
            "description_tok": _tokens(len(args.get("description") or "")),
            "expected_output_tok": _tokens(len(args.get("expected_output") or "")),
            "grand_total_tok": (
                instructions.get("total_tok", 0)
                + additional.get("total_tok", 0)
                + tools.get("total_tok", 0)
                + _tokens(len(args.get("description") or ""))
                + _tokens(len(args.get("expected_output") or ""))
            ),
        }
        logger.info(
            f"[prompt-budget] build {json.dumps(payload, separators=(',', ':'))}"
        )
    except Exception as exc:
        logger.debug(f"[prompt-budget] skipped: {exc}")
