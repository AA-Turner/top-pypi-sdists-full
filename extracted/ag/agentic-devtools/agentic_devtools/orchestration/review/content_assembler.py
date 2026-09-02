"""Priority-based content assembly and truncation for source context.

Combines full file content, test content, import content, and related
configuration/documentation content according to priority tiers, applying
truncation when the token budget is exceeded.

Priority tiers (FR-005):
1. Diff hunks (changed regions) — always included
2. Unchanged regions of changed files (full_content_source/target)
3. Related test files
4. Imported modules
5. Related configuration/documentation files
"""

from __future__ import annotations

import logging
import re
from typing import Any

from agentic_devtools.orchestration.review.budget import TokenBudget, estimate_tokens

logger = logging.getLogger(__name__)

# Priority tier constants
PRIORITY_DIFF = 1
PRIORITY_FULL_CONTENT = 2
PRIORITY_TESTS = 3
PRIORITY_IMPORTS = 4
PRIORITY_CONFIG_DOCS = 5

# Maximum number of path strings to consider when building fallback path-only
# sections (i.e. when content was budget-dropped or retrieval failed).  The
# same value is used both here (for budget allocation in priority 6) and in the
# ``_render_related_file_sections`` renderer.
_MAX_FALLBACK_PATHS: int = 20

# Generous upper bound on the token cost of a single fallback section heading
# (e.g. ``"## Related Test Files\n"``).  Used in the Priority-6 loop so the
# renderer never exceeds the configured budget via heading-only text.
_FALLBACK_HEADING_TOKENS: int = 5


def _extract_diff_lines_for_content_key(entry: dict[str, Any], content_key: str) -> list[int]:
    """Extract positive diff line numbers relevant to a content side."""
    # In this review pipeline, "source" means the head/new file version and
    # "target" means the base/old file version.
    line_key = "addedLines" if content_key == "full_content_source" else "removedLines"
    raw_lines = entry.get(line_key, [])
    if not isinstance(raw_lines, list):
        return []

    line_numbers: list[int] = []
    for line_info in raw_lines:
        if not isinstance(line_info, dict):
            continue
        line_no = line_info.get("line")
        if isinstance(line_no, int) and line_no > 0:
            line_numbers.append(line_no)
    return line_numbers


def _diff_priority(entry: dict[str, Any]) -> int:
    """Estimate a file's relative diff size for same-tier ordering."""
    added = len(_extract_diff_lines_for_content_key(entry, "full_content_source"))
    removed = len(_extract_diff_lines_for_content_key(entry, "full_content_target"))
    if added or removed:
        return added + removed
    patch = entry.get("patch", "")
    return estimate_tokens(patch) if isinstance(patch, str) else 0


def _normalize_content_items(value: Any) -> list[dict[str, str]]:
    """Normalize related-file content items into ``{path, content}`` dicts."""
    if not isinstance(value, list):
        return []

    items: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        content = item.get("content")
        if isinstance(path, str) and isinstance(content, str):
            items.append({"path": path, "content": content})
    return items


def _serialize_content_item(item: dict[str, str]) -> str:
    """Serialize a related-file content item for token estimation."""
    return f"{item['path']}\n{item['content']}"


def _truncate_content_item(item: dict[str, str], *, max_chars: int) -> dict[str, str] | None:
    """Truncate a related-file content item to fit the remaining character budget."""
    if max_chars <= 0:
        return None

    prefix = f"{item['path']}\n"
    if max_chars <= len(prefix):
        return None

    return {
        "path": item["path"],
        "content": item["content"][: max_chars - len(prefix)],
    }


def _consume_related_content_items(
    updated: dict[str, Any],
    *,
    content_key: str,
    omitted_count_key: str,
    budget: TokenBudget,
) -> int:
    """Consume budget for related-file content lists, truncating or omitting as needed."""
    items = _normalize_content_items(updated.get(content_key, []))
    if not items:
        updated[content_key] = []
        updated[omitted_count_key] = 0
        return 0

    kept: list[dict[str, str]] = []
    consumed = 0

    for index, item in enumerate(items):
        serialized = _serialize_content_item(item)
        tokens = estimate_tokens(serialized, budget.chars_per_token)
        if budget.can_accommodate(tokens):
            budget.record_consumption(tokens)
            consumed += tokens
            kept.append(item)
            continue

        remaining = budget.remaining
        omitted = len(items) - len(kept)
        if remaining > 0:
            truncated = _truncate_content_item(item, max_chars=int(remaining * budget.chars_per_token))
            if truncated is not None and truncated["content"]:
                kept.append(truncated)
                budget.record_consumption(remaining)
                consumed += remaining
                omitted = len(items) - index
                updated["truncation_applied"] = True
        updated[content_key] = kept
        updated[omitted_count_key] = omitted
        return consumed

    updated[content_key] = kept
    updated[omitted_count_key] = 0
    return consumed


_PATCH_TRUNCATION_MARKER = "\n[... diff truncated — budget exceeded ...]"
_HUNK_HEADER_PREFIX = "@@ "


def _truncate_patch_at_hunk_boundary(patch: str, *, max_chars: int) -> str:
    """Truncate a unified diff at the last complete hunk boundary within *max_chars*.

    Searches backwards from *max_chars* for the start of the most recent hunk
    header (``@@ ... @@``) so that the cut never falls inside a hunk.  An
    explicit truncation marker is appended so that the LLM knows the diff is
    incomplete.  If no hunk boundary can be found within *max_chars* the patch
    is truncated at the character boundary as a last resort (still with the
    marker).

    Args:
        patch: Raw unified diff text.
        max_chars: Maximum number of characters to retain (excluding the marker).

    Returns:
        Truncated patch string ending with the truncation marker.
    """
    if len(patch) <= max_chars:
        return patch

    marker = _PATCH_TRUNCATION_MARKER
    # Leave room for the marker in the final output.
    body_budget = max_chars - len(marker)
    if body_budget <= 0:
        # Budget too small to include any patch content; emit a marker
        # truncated to max_chars so we never exceed the configured limit.
        return marker[:max_chars] if max_chars > 0 else ""

    window = patch[:body_budget]
    # Find hunk headers at line starts so we can avoid dropping the only hunk.
    hunk_positions = [match.start() for match in re.finditer(r"(?m)^@@ ", window)]
    if hunk_positions:
        if len(hunk_positions) >= 2:
            # Keep everything up to (but not including) that last hunk — the
            # hunk that starts there is incomplete so we stop before it.
            cut = window[: hunk_positions[-1]]
        else:
            # We are truncating inside the first hunk. Preserve a bounded
            # prefix so changed lines remain visible instead of dropping the
            # entire hunk.
            cut = window
    else:
        # No hunk boundary found; fall back to a clean character cut.
        cut = window

    return cut + marker


def _truncate_around_changed_region(content: str, *, max_chars: int, diff_lines: list[int]) -> str:
    """Truncate content to fit budget while preserving changed-region context."""
    if max_chars <= 0:
        return ""
    if len(content) <= max_chars:
        return content
    if not diff_lines:
        return content[:max_chars]

    lines = content.splitlines()
    bounded = [line for line in diff_lines if 1 <= line <= len(lines)]
    if not bounded:
        return content[:max_chars]

    min_idx = min(bounded) - 1
    max_idx = max(bounded) - 1

    def _window_text(start: int, end: int) -> str:
        return "\n".join(lines[start : end + 1])

    # Reserve space for omission markers when surrounding lines are excluded.
    marker_prefix = "[... lines omitted before changed region ...]\n"
    marker_suffix = "\n[... lines omitted after changed region ...]"
    body_budget = max_chars - len(marker_prefix) - len(marker_suffix)
    if body_budget <= 0:
        return content[:max_chars]

    window_start = min_idx
    window_end = max_idx
    window = _window_text(window_start, window_end)

    if len(window) > body_budget:
        # Even changed lines alone exceed budget: keep a prefix at the first
        # changed line while preserving explicit omission markers.
        tail_window = "\n".join(lines[min_idx:])
        omitted_before = min_idx > 0
        omitted_after = len(tail_window) > body_budget
        prefix = marker_prefix if omitted_before else ""
        suffix = marker_suffix if omitted_after else ""
        available_for_window = max_chars - len(prefix) - len(suffix)
        truncated_window = tail_window[:available_for_window]
        return prefix + truncated_window + suffix

    # Expand around changed region while staying within body budget.
    while True:
        expanded = False
        if window_start > 0:
            candidate = _window_text(window_start - 1, window_end)
            if len(candidate) <= body_budget:
                window_start -= 1
                window = candidate
                expanded = True
        if window_end < len(lines) - 1:
            candidate = _window_text(window_start, window_end + 1)
            if len(candidate) <= body_budget:
                window_end += 1
                window = candidate
                expanded = True
        if not expanded:
            break

    omitted_before = window_start > 0
    omitted_after = window_end < len(lines) - 1
    truncated = (marker_prefix if omitted_before else "") + window + (marker_suffix if omitted_after else "")
    return truncated


def assemble_context(
    file_entries: list[dict[str, Any]],
    budget: TokenBudget,
) -> list[dict[str, Any]]:
    """Assemble source context for all file entries within budget.

    Processes files in priority tiers.  Within the diff (Priority 1) tier,
    patch tokens are allocated *proportionally* across all files so that no
    single large diff can starve later files of any patch content.  If total
    patch demand fits within the remaining budget, each file receives its full
    patch; otherwise each file receives a truncated slice proportional to its
    share of the total patch demand.  Files are processed in descending
    diff-size order (highest-priority first), so larger diffs benefit first
    when the budget cannot be divided equally.  When the total budget is
    smaller than the number of patched files some later files may receive an
    empty patch and are marked with ``truncation_applied=True``.  Subsequent
    tiers (full content, tests, imports, config/docs) then consume whatever
    budget remains.

    Patch truncation is done at hunk boundaries (``@@ ... @@`` lines) when
    possible so that the LLM never receives a partial hunk without a diff header.
    A ``[... diff truncated ...]`` marker is appended to make the omission
    explicit.

    After Priority 5, ``related_tests_retained``,
    ``resolved_imports_retained``, and ``related_config_docs_retained`` path
    lists are populated with the paths for which content was actually kept.
    The original ``related_tests`` / ``resolved_imports`` /
    ``related_config_docs`` path lists are preserved intact so that
    graceful-degradation renderers can still reference the identity of
    budget-dropped or retrieval-failed files.

    Sets ``truncation_applied`` on file entries where any content was truncated
    or dropped to fit.

    Args:
        file_entries: List of file entry dicts with content fields populated.
        budget: Token budget to enforce.

    Returns:
        Updated file entries with ``truncation_applied``, ``estimated_tokens``,
        ``related_tests_retained``, ``resolved_imports_retained``, and
        ``related_config_docs_retained`` fields set.
    """
    if not file_entries:
        return []

    result = [
        {
            **entry,
            "related_test_contents": _normalize_content_items(entry.get("related_test_contents", [])),
            "resolved_import_contents": _normalize_content_items(entry.get("resolved_import_contents", [])),
            "related_config_doc_contents": _normalize_content_items(entry.get("related_config_doc_contents", [])),
            "related_tests_omitted_count": 0,
            "resolved_imports_omitted_count": 0,
            "related_config_docs_omitted_count": 0,
            # Fallback-path caps: capped to ``_MAX_FALLBACK_PATHS`` by default;
            # updated in Priority 6 when the remaining budget is smaller.
            "related_tests_paths_display_cap": _MAX_FALLBACK_PATHS,
            "resolved_imports_paths_display_cap": _MAX_FALLBACK_PATHS,
            "related_config_docs_paths_display_cap": _MAX_FALLBACK_PATHS,
            "truncation_applied": False,
            "estimated_tokens": 0,
        }
        for entry in file_entries
    ]
    priority_order = sorted(range(len(result)), key=lambda idx: _diff_priority(result[idx]), reverse=True)

    # Priority 1: Diff — guaranteed slice for every file.
    #
    # To prevent high-priority large diffs from starving lower-priority files of
    # any patch content (which causes the LLM to receive an empty diff and emit a
    # false "request-changes" verdict), we use proportional allocation:
    #
    # 1. Compute the token demand for every file's patch.
    # 2. If total demand fits in the available budget → allocate greedily (no
    #    truncation, all files get their full patch).
    # 3. If total demand exceeds the budget → each file gets a share proportional
    #    to its demand, with a minimum of 1 token per file that has a patch, so
    #    that no file is left with an empty diff.
    #
    # Files processed in priority order so that when rounding leads to a residual
    # token, the highest-priority file benefits.
    available_for_patches = budget.remaining
    patch_demands: dict[int, int] = {}
    for idx in priority_order:
        patch = result[idx].get("patch", "")
        patch_demands[idx] = estimate_tokens(patch, budget.chars_per_token) if patch else 0

    total_patch_demand = sum(patch_demands.values())

    if total_patch_demand <= available_for_patches:
        # All patches fit — allocate in full; no truncation needed.
        for idx in priority_order:
            demand = patch_demands[idx]
            if demand > 0:
                budget.record_consumption(demand)
                result[idx]["estimated_tokens"] += demand
    else:
        # Proportional allocation: give each file a fraction of the available
        # budget proportional to its share of the total demand, with a minimum
        # of 1 allocated token per file that has a patch so that no file receives
        # an empty diff.
        patched_idxs = [idx for idx in priority_order if patch_demands[idx] > 0]
        for idx in patched_idxs:
            demand = patch_demands[idx]
            # Floor-divide first; the priority loop order means the first
            # (highest-priority) files benefit from any rounding residual.
            alloc = max(1, int(available_for_patches * demand // total_patch_demand))
            alloc = min(alloc, budget.remaining)
            if alloc <= 0:
                # No budget remains for this file's diff.  Set an explicit empty
                # excerpt (distinct from an absent key) so the prompt builder
                # renders no patch instead of falling back to the full patch and
                # overflowing the configured budget.
                result[idx]["patch_budget_excerpt"] = ""
                result[idx]["truncation_applied"] = True
                continue
            patch = result[idx].get("patch", "")
            max_chars = int(alloc * budget.chars_per_token)
            if len(patch) > max_chars:
                result[idx]["patch_budget_excerpt"] = _truncate_patch_at_hunk_boundary(patch, max_chars=max_chars)
                result[idx]["truncation_applied"] = True
            budget.record_consumption(alloc)
            result[idx]["estimated_tokens"] += alloc

    # Priority 2: Full content (source and target)
    for idx in priority_order:
        updated = result[idx]
        for content_key in ("full_content_source", "full_content_target"):
            content = updated.get(content_key)
            if content:
                tokens = estimate_tokens(content, budget.chars_per_token)
                if budget.can_accommodate(tokens):
                    budget.record_consumption(tokens)
                    updated["estimated_tokens"] += tokens
                else:
                    remaining = budget.remaining
                    if remaining > 0:
                        max_chars = int(remaining * budget.chars_per_token)
                        diff_lines = _extract_diff_lines_for_content_key(updated, content_key)
                        updated[content_key] = _truncate_around_changed_region(
                            content,
                            max_chars=max_chars,
                            diff_lines=diff_lines,
                        )
                        budget.record_consumption(remaining)
                        updated["estimated_tokens"] += remaining
                        updated["truncation_applied"] = True
                        # Record per-side truncation so the prompt builder renders
                        # the excerpt directly instead of re-anchoring original
                        # diff line numbers against shifted content.
                        updated[f"{content_key}_truncated"] = True
                    else:
                        updated[content_key] = None
                        updated["truncation_applied"] = True

    # Priority 3: Related test file content
    for idx in priority_order:
        updated = result[idx]
        updated["estimated_tokens"] += _consume_related_content_items(
            updated,
            content_key="related_test_contents",
            omitted_count_key="related_tests_omitted_count",
            budget=budget,
        )
        if updated["related_tests_omitted_count"] > 0:
            updated["truncation_applied"] = True

    # Priority 4: Imported module content
    for idx in priority_order:
        updated = result[idx]
        updated["estimated_tokens"] += _consume_related_content_items(
            updated,
            content_key="resolved_import_contents",
            omitted_count_key="resolved_imports_omitted_count",
            budget=budget,
        )
        if updated["resolved_imports_omitted_count"] > 0:
            updated["truncation_applied"] = True

    # Priority 5: Related configuration/documentation content
    for idx in priority_order:
        updated = result[idx]
        updated["estimated_tokens"] += _consume_related_content_items(
            updated,
            content_key="related_config_doc_contents",
            omitted_count_key="related_config_docs_omitted_count",
            budget=budget,
        )
        if updated["related_config_docs_omitted_count"] > 0:
            updated["truncation_applied"] = True

    # Populate retained-path lists for renderers that need to distinguish between
    # "content available" and "discovered but budget-dropped / retrieval-failed".
    # The original ``related_tests`` / ``resolved_imports`` /
    # ``related_config_docs`` path lists are preserved intact so that
    # graceful-degradation renderers can still show the identity of related
    # files even when their content was not fetched.
    for idx in priority_order:
        updated = result[idx]
        updated["related_tests_retained"] = [item["path"] for item in updated.get("related_test_contents", [])]
        updated["resolved_imports_retained"] = [item["path"] for item in updated.get("resolved_import_contents", [])]
        updated["related_config_docs_retained"] = [
            item["path"] for item in updated.get("related_config_doc_contents", [])
        ]

    # Priority 6: Fallback path-only sections (charged when content is absent).
    #
    # When the assembler drops all content for a tier (budget exhausted or
    # retrieval failed), the renderer falls back to a bullet-list of discovered
    # paths.  Those strings still consume LLM context window space and must be
    # allocated against the same budget so that a low configured budget is not
    # substantially exceeded (FR-008).
    #
    # For each category, this step:
    #   1. Skips the category when content items ARE present (renderer shows
    #      content, not paths).
    #   2. Charges the section heading + one line per path until budget is
    #      exhausted, recording how many paths were approved.
    #   3. Writes ``*_paths_display_cap`` — the renderer must not show more paths
    #      than this value.
    for idx in priority_order:
        updated = result[idx]
        for content_key, paths_key, cap_key in (
            ("related_test_contents", "related_tests", "related_tests_paths_display_cap"),
            ("resolved_import_contents", "resolved_imports", "resolved_imports_paths_display_cap"),
            ("related_config_doc_contents", "related_config_docs", "related_config_docs_paths_display_cap"),
        ):
            # If content items are present the fallback section is suppressed.
            if updated.get(content_key):
                continue
            raw_paths = updated.get(paths_key)
            candidate_paths = [p for p in (raw_paths if isinstance(raw_paths, list) else []) if isinstance(p, str)]
            if not candidate_paths:
                updated[cap_key] = 0
                continue

            # Charge the section heading first.
            if not budget.can_accommodate(_FALLBACK_HEADING_TOKENS):
                updated[cap_key] = 0
                updated["truncation_applied"] = True
                continue
            budget.record_consumption(_FALLBACK_HEADING_TOKENS)
            updated["estimated_tokens"] += _FALLBACK_HEADING_TOKENS

            # Charge paths one by one up to _MAX_FALLBACK_PATHS.
            approved = 0
            for path in candidate_paths[:_MAX_FALLBACK_PATHS]:
                line_tokens = estimate_tokens(f"- {path}\n", budget.chars_per_token)
                if budget.can_accommodate(line_tokens):
                    budget.record_consumption(line_tokens)
                    updated["estimated_tokens"] += line_tokens
                    approved += 1
                else:
                    updated["truncation_applied"] = True
                    break
            updated[cap_key] = approved
            if approved < len(candidate_paths):
                updated["truncation_applied"] = True

    logger.info(
        "Content assembly complete: %d files, %d tokens consumed, %d remaining",
        len(result),
        budget.consumed,
        budget.remaining,
    )

    return result
