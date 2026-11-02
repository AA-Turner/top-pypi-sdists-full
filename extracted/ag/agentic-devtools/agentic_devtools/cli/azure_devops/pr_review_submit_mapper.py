"""Explicit answer → submission-item mapper for the v2 PR review (P3, §15.6).

The orchestrator's ``agdt-pr-review-submit`` reads accepted answers from the
ledger and must hand each one to the durable submit engine
(:func:`agentic_devtools.submission_processor.process_submission`). That engine
consumes the **same** ``file_path`` / ``outcome`` / ``summary`` / ``suggestions``
shape the legacy file-review path produced, and it does **not** wrap
``replacement_code`` itself. This module is the single, explicit translation
layer between the two schemas (plan §15.6):

* canonicalize the answer's ``filePath`` to the engine's ``file_path``;
* transform ``replacement_code`` into the Azure DevOps ```suggestion``` fence
  (exactly as ``request_changes_with_suggestion`` did) so the engine posts an
  applyable suggestion thread;
* preserve optional ``endLine`` / ``out_of_scope`` / ``link_text`` anchoring;
* reject line-anchored suggestions for ``binary`` / ``deleted`` /
  ``metadata-only`` review modes (they have no diff line to anchor to); and
* skip out-of-scope observations that carry no line (the engine can only post
  line-anchored threads) without losing the rest of the verdict.

The mapper never performs I/O — it is a pure transformation, validated by the
P2 schema upstream and re-validated for freshness by submit.
"""

from __future__ import annotations

from typing import Any

from .pr_review_write import LINE_ANCHOR_FORBIDDEN_MODES, VALID_OUTCOMES

_APPROVE_OUTCOME = "approve"


class MapperError(ValueError):
    """Raised when an answer or suggestion cannot be mapped to a submission item."""


def transform_replacement_code(content: str, replacement_code: str | None) -> str:
    """Append an Azure DevOps ```suggestion``` fence when *replacement_code* is set.

    Mirrors ``request_changes_with_suggestion``: the reviewer supplies plain
    ``replacement_code`` and the submit path wraps it in fences so the agent
    never has to author fence syntax. A missing or blank ``replacement_code``
    leaves *content* unchanged.

    Args:
        content: The human-readable suggestion comment body.
        replacement_code: The replacement code to fence, or ``None``.

    Returns:
        *content*, optionally followed by a fenced ```suggestion``` block.
    """
    if replacement_code and replacement_code.strip():
        return f"{content}\n\n```suggestion\n{replacement_code}\n```"
    return content


def map_suggestion(suggestion: dict[str, Any], review_mode: str) -> dict[str, Any] | None:
    """Map one answer suggestion to the engine's suggestion shape.

    Args:
        suggestion: A suggestion entry from the answer schema (plan §9).
        review_mode: The answer's review mode (``diff``, ``binary``, ...).

    Returns:
        The engine suggestion dict (``line`` / ``end_line`` / ``severity`` /
        ``content`` / ``out_of_scope`` and optional ``link_text``), or ``None``
        when the suggestion is an out-of-scope note with no anchorable line (it
        is skipped rather than posted).

    Raises:
        MapperError: When a line is required but missing, or a line-anchored
            suggestion targets a non-anchorable review mode.
    """
    out_of_scope = bool(suggestion.get("out_of_scope", False))
    line = suggestion.get("line")

    if line is None:
        if out_of_scope:
            # Out-of-scope observation with no diff line — the engine can only
            # post line-anchored threads, so skip it (reported as skipped).
            return None
        raise MapperError("suggestion is missing 'line' and is not out_of_scope")

    if review_mode in LINE_ANCHOR_FORBIDDEN_MODES and not out_of_scope:
        raise MapperError(f"line-anchored suggestion is not allowed for reviewMode {review_mode!r}")

    end_line = suggestion.get("endLine")
    if end_line is None:
        end_line = line

    mapped: dict[str, Any] = {
        "line": line,
        "end_line": end_line,
        "severity": suggestion.get("severity"),
        "content": transform_replacement_code(suggestion.get("content", ""), suggestion.get("replacement_code")),
        "out_of_scope": out_of_scope,
    }
    link_text = suggestion.get("link_text")
    if link_text is not None:
        if not isinstance(link_text, str):
            raise MapperError("suggestion field 'link_text' must be a string when provided")
        if link_text.strip():
            mapped["link_text"] = link_text
    return mapped


def map_answer_to_submission_item(answer: dict[str, Any]) -> dict[str, Any]:
    """Map a complete accepted answer to a submit-engine item.

    Args:
        answer: An accepted answer (plan §9 schema, status ``complete``).

    Returns:
        ``{"file_path", "outcome", "summary", "suggestions"}`` where
        ``suggestions`` is ``None`` for ``approve`` outcomes and otherwise the
        list of mapped, anchorable suggestions (out-of-scope notes without a
        line are dropped).

    Raises:
        MapperError: When ``filePath`` is missing/blank, the outcome is
            unrecognized, or a suggestion cannot be mapped.
    """
    file_path = answer.get("filePath")
    if not isinstance(file_path, str) or not file_path.strip():
        raise MapperError("answer is missing a non-empty 'filePath'")

    outcome = answer.get("outcome")
    if outcome not in VALID_OUTCOMES:
        raise MapperError(f"answer has an invalid outcome {outcome!r}")

    summary = answer.get("summary") or ""

    if outcome == _APPROVE_OUTCOME:
        return {"file_path": file_path, "outcome": outcome, "summary": summary, "suggestions": None}

    review_mode = answer.get("reviewMode", "diff")
    mapped_suggestions: list[dict[str, Any]] = []
    for suggestion in answer.get("suggestions", []):
        mapped = map_suggestion(suggestion, review_mode)
        if mapped is not None:
            mapped_suggestions.append(mapped)

    return {
        "file_path": file_path,
        "outcome": outcome,
        "summary": summary,
        "suggestions": mapped_suggestions or None,
    }
