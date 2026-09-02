"""Anthropic's compiled-grammar budget — detection and the shed ladder's vocabulary.

WHY THIS EXISTS — measured live 2026-08-24 against ``claude-sonnet-5``.

When a request carries BOTH ``output_config.format`` (a bound structured-output
schema) and ``tools``, Anthropic compiles them into ONE grammar and rejects the
request when that grammar is too large::

    invalid_request: The compiled grammar is too large, which would cause
    performance issues. Simplify your tool schemas or reduce the number of
    strict tools.

The budget is SHARED between the two. The Study Pack ``flashcards`` node proved
it three times in production (runs 5ec2e0bb / 5b8ada58 / c9686dbb, definition
3bd1960c): the ``flashcard_set`` binding compiles CLEANLY on its own, and fails
the moment even ONE tool is attached — while its siblings ``quiz_set`` (1,038
bytes) and ``study_notes`` (2,309 bytes) pass with all six tools attached.

    flashcard_set + 0 tools  -> PASS
    flashcard_set + 1 tool   -> compiled grammar too large
    flashcard_set + 6 tools  -> compiled grammar too large

THE MEASUREMENTS THAT RULED OUT THE OBVIOUS FIXES. None of these is the lever;
every one was tried against the live compiler before this module was written:

* Byte size is NOT the metric. ``seo_keyword_relationship_research_result``
  compiles at 7,494 bytes while ``flashcard_set`` fails at 4,929; stripping
  every ``description`` took flashcard_set to 3,849 bytes and it STILL failed.
* The ``required`` encoding is NOT the lever. Anthropic accepts a PARTIAL
  ``required`` list (contrary to what ``schema/lint.py`` asserts), but the
  registry's own leaner ``required`` (4,573 bytes) fails too, and the
  OpenAI-documented ``["<type>","null"]`` optional encoding is WORSE — it fails
  even with zero tools.
* Inlining ``$defs`` does not help: refs are already expanded by the compiler,
  so inlining only duplicates what it was going to duplicate anyway.

What actually costs is STRUCTURE — a union of large object variants inside an
array, each carrying a nested envelope with its own array of objects. There is
no lossless transform of the bound copy that buys headroom, which is why the
platform sheds TOOLS (a request-time concern) instead of quietly mutilating the
declared kind (the user's actual contract). The kind stays whole, ``__kind``
stays first, and streaming pre-recognition keeps working.

A sweep of all 417 registered kinds on 2026-08-24 found **16** whose binding is
already over budget alongside the six ambient user-data tools — this is a
platform-wide class, not one bad schema. ``scripts/check_kind_grammar_budget.py``
is the standing guard that re-measures it.
"""

from __future__ import annotations

from typing import Any

#: The substring Anthropic puts in the ``invalid_request`` message. Matched on
#: the MESSAGE rather than a code because the provider gives this rejection no
#: distinct code — it arrives as a generic 400 ``invalid_request_error``.
GRAMMAR_TOO_LARGE_MARKER = "compiled grammar is too large"


def binds_structured_output(response_format: Any) -> bool:
    """True when a ``response_format`` carries a REAL bound json_schema.

    The signal a caller needs before deciding whether this turn has to share
    the provider's compiled-grammar budget. A bare ``{"type": "json_schema"}``
    placeholder does NOT count — the frontend sends that to mean "use the
    agent's schema", so it is a request for hydration, not evidence of a
    binding. ``json_object`` is a format hint with no schema and no grammar.
    """
    if not isinstance(response_format, dict) or response_format.get("type") != "json_schema":
        return False
    inner = response_format.get("json_schema")
    if isinstance(inner, dict):
        return isinstance(inner.get("schema"), dict) or bool(
            {"type", "properties", "items"} & inner.keys()
        )
    return isinstance(response_format.get("schema"), dict)


def is_grammar_too_large(error: Any) -> bool:
    """True when ``error`` is Anthropic's compiled-grammar-too-large rejection.

    Accepts an exception or a message string. Deliberately narrow: this must
    never swallow an unrelated 400, because the caller's response to a True is
    to RETRY with capability removed.
    """
    if error is None:
        return False
    text = error if isinstance(error, str) else str(error)
    return GRAMMAR_TOO_LARGE_MARKER in text


__all__ = ["GRAMMAR_TOO_LARGE_MARKER", "binds_structured_output", "is_grammar_too_large"]
