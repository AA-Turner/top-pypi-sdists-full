"""T3 — Bounded regenerate context.

When a write fails validation or tests, regeneration must NOT receive the
full conversation history. The Novellia incident: a tiny model was given
its own previous garbled output as context, and re-emitted it almost
verbatim into the next "fix attempt". The feedback bomb compounds.

This module builds a minimal regenerate prompt:
    1. The single failing file path + content
    2. The error tail (last N lines)
    3. Up to 3 RAG chunks of relevant context
    4. NO planning markers, NO previous-turn history
"""

from __future__ import annotations

import re

__all__ = ["build_regenerate_prompt", "scrub_protocol_markers"]


# Patterns that should never appear in a regenerate prompt — they leak
# planning state from prior turns and tend to make small models echo them.
_PROTOCOL_PATTERNS = (
    re.compile(r"^\s*## (STEP|TASK|NEXT STEPS|CURRENT PLAN|LOGIC REQUIRED|EDGE CASES|NEXT ACTION|SESSION CONTEXT)\b.*$", re.MULTILINE),
    re.compile(r"^---\s*END OF PREVIOUS FINDINGS\s*---.*$", re.MULTILINE),
    re.compile(r"^Plan ID:\s*\S.*$", re.MULTILINE),
)


def scrub_protocol_markers(text: str) -> str:
    """Strip planning-protocol noise from a chunk of text. Idempotent."""
    out = text
    for pattern in _PROTOCOL_PATTERNS:
        out = pattern.sub("", out)
    # Collapse runs of blank lines
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def build_regenerate_prompt(
    *,
    failing_file: str,
    failing_content: str,
    error_tail: str,
    rag_chunks: list[tuple[str, str]] | None = None,
    max_chars: int = 4000,
) -> str:
    """Construct the prompt fed to the model when a write fails validation.

    Args:
        failing_file:    relative path of the file that needs fixing
        failing_content: the actual content that just failed
        error_tail:      stderr/stdout tail from the failing test/lint
        rag_chunks:      optional list of (path, snippet) for context
        max_chars:       hard upper bound on output length

    Returns: a focused prompt with just enough context to fix the bug.
    """
    rag_chunks = rag_chunks or []

    # Scrub each input independently before assembly
    safe_content = scrub_protocol_markers(failing_content)
    safe_error = scrub_protocol_markers(error_tail)

    # Headers + content are kept short; truncate body if needed
    error_budget = max(200, max_chars // 4)
    if len(safe_error) > error_budget:
        safe_error = safe_error[-error_budget:]   # tail of error matters most

    # File-content budget = remaining after headers + error
    header_overhead = 400
    content_budget = max_chars - header_overhead - len(safe_error)
    content_budget = max(200, content_budget)
    if len(safe_content) > content_budget:
        # Keep the first half + the last half so we see both definitions and
        # the area near the syntax error
        head = safe_content[: content_budget // 2]
        tail = safe_content[-(content_budget // 2):]
        safe_content = head + "\n... [truncated] ...\n" + tail

    sections: list[str] = [
        f"FIX TASK — file: {failing_file}",
        "",
        "## CURRENT FILE CONTENT",
        "```",
        safe_content,
        "```",
        "",
        "## ERROR / TEST OUTPUT",
        safe_error or "(no error output captured)",
    ]

    if rag_chunks:
        sections.extend(["", "## RELEVANT PROJECT CONTEXT (real symbols, real paths)"])
        chunk_budget = max(200, max_chars - sum(len(s) for s in sections) - 200)
        used = 0
        for path, snippet in rag_chunks:
            block = f"\n— {path}\n```\n{snippet}\n```"
            if used + len(block) > chunk_budget:
                break
            sections.append(block)
            used += len(block)

    sections.extend([
        "",
        "## INSTRUCTIONS",
        "Emit ONLY a corrected FILE: block for the file above. "
        "Do not include planning, headings, or commentary. "
        "Use only real symbols and paths from the project context.",
    ])

    out = "\n".join(sections)
    if len(out) > max_chars:
        out = out[:max_chars]
    return out
