"""T4 + T12 — Grammar enforcement defaults.

T4: Strict GBNF on tool-call turns.
    Decides whether a given prompt should run with grammar-constrained
    decoding. Heuristic: if the user is asking for a code change ("implement",
    "fix", "add", "refactor") → enforce grammar. Pure questions ("what is",
    "explain") → no grammar so the model can speak naturally.

T12: Project-aware grammar.
    Combines the SAGE protocol grammar with a per-project import grammar
    so the model literally cannot emit imports for symbols that don't
    exist in the project.
"""

from __future__ import annotations

import re
from pathlib import Path

from sage.core.grammar import SAGE_PROTOCOL_GBNF
from sage.core.project_grammar import build_import_grammar, extract_project_symbols

__all__ = ["should_enforce_grammar", "get_combined_grammar_string", "_cache"]


# Per-project cache: project_root → combined grammar string
_cache: dict[str, str] = {}


# Tool-emitting prompt patterns: model is expected to write/edit/run
_TOOL_TURN_PATTERNS = (
    r"\b(implement|build|add|create|write|fix|change|update|modify|refactor|migrate|"
    r"set\s*up|wire|hook\s*up|connect|integrate|delete|remove|rename|extract)\b"
)
_TOOL_TURN_RE = re.compile(_TOOL_TURN_PATTERNS, re.IGNORECASE)

# Pure question / explanation patterns: chat turn, no grammar
_QUESTION_PATTERNS = (
    r"^\s*(what|why|how|when|who|which|tell me|explain|describe|"
    r"show me|can you explain|do you know)\b"
)
_QUESTION_RE = re.compile(_QUESTION_PATTERNS, re.IGNORECASE)


def should_enforce_grammar(prompt: str) -> bool:
    """Heuristic: is this a tool-emitting turn that benefits from GBNF?

    Returns True for prompts that ask for code changes; False for pure
    chat/explanation turns where natural language is the right output.
    """
    if not prompt or not prompt.strip():
        return False
    # Check question first — if it's clearly a question, allow free text
    if _QUESTION_RE.search(prompt) and not _TOOL_TURN_RE.search(prompt):
        return False
    # Otherwise: enforce when we see tool-action verbs
    return bool(_TOOL_TURN_RE.search(prompt))


def get_combined_grammar_string(project_root: Path | None = None) -> str:
    """Combine the SAGE protocol grammar with project-specific import rules.

    Without a project_root: just the protocol grammar.
    With a project_root: protocol + project_grammar.build_import_grammar().
    Cached per project_root for cheap reuse.
    """
    cache_key = str(project_root.resolve()) if project_root else "_protocol_only"
    if cache_key in _cache:
        return _cache[cache_key]

    parts: list[str] = [SAGE_PROTOCOL_GBNF.strip()]
    if project_root is not None and project_root.is_dir():
        try:
            syms = extract_project_symbols(project_root)
            project_gbnf = build_import_grammar(syms)
            parts.append("\n# Project-aware import grammar\n" + project_gbnf.strip())
        except Exception:
            # If extraction fails, fall back to protocol-only
            pass

    combined = "\n\n".join(parts)
    _cache[cache_key] = combined
    return combined
