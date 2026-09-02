"""``source_context`` node — retrieves source context for reviewed files.

Inserts between ``fetch_pr_details`` and ``scaffold_comments`` in the review
graph. Enriches file entries with full content (source and target branch
versions), related test files, resolved imports, and nearby configuration /
documentation files based on configurable context depth and token budget.

Context depth levels:
- ``"minimal"``: Only changed file content (source + target)
- ``"standard"``: Changed files + related test discovery
- ``"deep"``: Changed files + tests + affected imports + related config/docs
"""

from __future__ import annotations

import logging
import math
import subprocess
import time
from enum import StrEnum
from pathlib import Path
from typing import Any

from agentic_devtools.orchestration.review.budget import (
    DEFAULT_CHARS_PER_TOKEN,
    DEFAULT_SAFETY_MARGIN,
    FALLBACK_BUDGET_TOKENS,
)

logger = logging.getLogger(__name__)

# Retrieval statuses that represent an intentional skip (not a retrieval error).
_SKIP_STATUSES: frozenset[str] = frozenset({"skipped_too_large", "skipped_binary"})

_RELATED_CONFIG_DOC_SUFFIXES: frozenset[str] = frozenset(
    {".md", ".mdx", ".rst", ".txt", ".toml", ".yaml", ".yml", ".json", ".ini", ".cfg"}
)
_REPO_ROOT_CONFIG_DOC_FILES: frozenset[str] = frozenset({"README.md", "copilot-instructions.md", "pyproject.toml"})

# Hard upper-bound on supplemental requests per category (tests / imports /
# config-docs) per source file.  The budget-derived cap below further tightens
# this when the configured token budget is small.
_MAX_SUPPLEMENTAL_PER_CATEGORY: int = 50

# Assumed average content size used to estimate how many supplemental files
# can realistically fit within the token budget.  2 KB is a conservative
# lower-bound (many real files are larger, so this errs on the side of
# fetching fewer files rather than over-fetching).
_ASSUMED_CHARS_PER_SUPPLEMENTAL: int = 2_000


class ContextDepth(StrEnum):
    """Configurable context depth level."""

    MINIMAL = "minimal"
    STANDARD = "standard"
    DEEP = "deep"


def _coerce_optional_positive_int(value: Any) -> int | None:
    """Coerce config values to positive int, returning None on invalid input."""
    if value is None:
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _coerce_positive_int_with_default(value: Any, default: int) -> int:
    """Coerce config values to positive int, falling back to default."""
    parsed = _coerce_optional_positive_int(value)
    return parsed if parsed is not None else default


def _collect_candidate_models(review_config: Any, model_config_raw: Any) -> list[str]:
    """Collect configured model candidates for source-context budgeting helpers."""
    candidates: list[str] = []

    def _add(value: Any) -> None:
        if isinstance(value, str) and value.strip():
            candidates.append(value)

    if isinstance(review_config, dict):
        _add(review_config.get("model_id"))
    if isinstance(model_config_raw, dict):
        _add(model_config_raw.get("default-model"))
        rules = model_config_raw.get("rules")
        if isinstance(rules, list):
            for rule in rules:
                if isinstance(rule, dict):
                    _add(rule.get("model"))
    return candidates


def _resolve_budget_model_id(review_config: Any, model_config_raw: Any) -> str | None:
    """Resolve the most constrained configured model across all candidates."""
    from agentic_devtools.orchestration.review.budget import resolve_model_context_window

    candidates = _collect_candidate_models(review_config, model_config_raw)
    if not candidates:
        return None

    most_constrained: str | None = None
    smallest_window: int | None = None
    for model_id in candidates:
        window = resolve_model_context_window(model_id)
        if window is None:
            continue
        if smallest_window is None or window < smallest_window:
            smallest_window = window
            most_constrained = model_id

    if most_constrained is not None:
        return most_constrained
    return candidates[0]


def _get_provider_default_model(config_path: str | None = None) -> str | None:
    """Best-effort extraction of the ``pr_review`` provider's configured default model.

    Mirrors the logic in ``review_files._resolved_provider_default_model`` so
    that ``source_context`` budgets each file against the same model that
    ``review_files_node`` will actually invoke.  Returns ``None`` on any error
    so callers fall back to the ``model_routing`` default.

    Args:
        config_path: Optional absolute path to the LLM provider config file.
            When provided (e.g. from ``state["llm_config_path"]``), the same
            repo-root-resolved config used by the preflight check and the
            ``review_files`` node is used here, avoiding a CWD-relative fallback.
    """
    try:
        from agentic_devtools.orchestration.llm.config import load_config
        from agentic_devtools.orchestration.llm.factory import get_provider

        config_snapshot = load_config(config_path)
        provider = get_provider("review_files", "pr_review", config=config_snapshot)
        model = getattr(provider, "_model", None)
        if isinstance(model, str) and model.strip():
            return model.strip()
        return None
    except Exception:
        return None


def _resolve_file_budget_model_id(
    file_path: str,
    model_config_raw: Any,
    requested_model: str | None = None,
    provider_default_model: str | None = None,
) -> str | None:
    """Resolve the model whose context window should bound one file's prompt.

    Source context is rendered into one LLM prompt per file, so each file must
    be budgeted against the model that will actually review that file.  Uses the
    same per-file routing logic as ``review_files_node._resolve_model()`` so
    that the assembled context never overflows the reviewer's actual window.

    ``provider_default_model`` should be the provider's resolved default model
    (from ``_get_provider_default_model()``), so that the fallback when no
    explicit per-file rule matches is identical to what ``review_files_node``
    will use at invocation time.
    """
    if isinstance(requested_model, str) and requested_model.strip():
        return requested_model.strip()

    try:
        from agentic_devtools.orchestration.review.model_routing import resolve_model_for_file

        resolved_model = resolve_model_for_file(
            file_path,
            model_config_raw if isinstance(model_config_raw, dict) else None,
            default_model=provider_default_model,
        )
        return resolved_model if isinstance(resolved_model, str) and resolved_model.strip() else None
    except ImportError:
        return None


def _extract_positive_line_numbers(raw_lines: Any) -> list[int]:
    """Extract positive integer line numbers from untyped diff-line metadata."""
    if not isinstance(raw_lines, list):
        return []

    positive_lines: list[int] = []
    for line_info in raw_lines:
        if not isinstance(line_info, dict):
            continue
        line_no = line_info.get("line")
        if isinstance(line_no, int) and line_no > 0:
            positive_lines.append(line_no)
    return positive_lines


def _is_config_or_doc_path(path: str) -> bool:
    """Return whether *path* looks like configuration or documentation content."""
    clean_path = path.lstrip("/")
    if not clean_path:
        return False
    candidate = Path(clean_path)
    return candidate.suffix.lower() in _RELATED_CONFIG_DOC_SUFFIXES


def _discover_related_config_docs(source_path: str, files: list[dict[str, Any]]) -> list[str]:
    """Discover nearby changed config/doc files for deep source-context enrichment."""
    clean_source = source_path.lstrip("/")
    if not clean_source or _is_config_or_doc_path(clean_source):
        return []

    source_parts = Path(clean_source).parts
    source_dir_parts = source_parts[:-1]
    ancestor_dirs = {source_dir_parts[:idx] for idx in range(len(source_dir_parts) + 1)}

    related: list[str] = []
    for file_entry in files:
        candidate_path = file_entry.get("path")
        if not isinstance(candidate_path, str):
            continue
        clean_candidate = candidate_path.lstrip("/")
        if clean_candidate == clean_source or not _is_config_or_doc_path(clean_candidate):
            continue

        candidate_parts = Path(clean_candidate).parts
        candidate_dir_parts = candidate_parts[:-1]
        candidate_name = candidate_parts[-1]
        is_same_dir = candidate_dir_parts == source_dir_parts
        is_ancestor_readme = candidate_name.lower() == "readme.md" and candidate_dir_parts in ancestor_dirs
        is_repo_root_config = len(candidate_parts) == 1 and candidate_name in _REPO_ROOT_CONFIG_DOC_FILES
        if is_same_dir or is_ancestor_readme or is_repo_root_config:
            related.append(clean_candidate)

    return sorted(set(related))


def _resolve_verified_repo_root(files: list[dict[str, Any]], commit_hash: str) -> str | None:
    """Return the local repo root only when it matches the reviewed checkout."""
    try:
        from agentic_devtools.cli.azure_devops.pr_review_manifest import resolve_repo_root

        repo_root = resolve_repo_root()
    except Exception:
        return None

    if not isinstance(repo_root, str) or not repo_root.strip():
        return None

    if not isinstance(commit_hash, str) or not commit_hash.strip():
        return None

    try:
        head_result = subprocess.run(
            ["git", "-C", repo_root, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            shell=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    local_head = head_result.stdout.strip() if head_result.returncode == 0 else ""
    commit_hash_is_short = 7 <= len(commit_hash) < len(local_head)
    if not local_head or not (
        local_head == commit_hash or (commit_hash_is_short and local_head.startswith(commit_hash))
    ):
        return None

    root = Path(repo_root)
    for file_entry in files:
        path = file_entry.get("path")
        if isinstance(path, str) and path and (root / path.lstrip("/")).exists():
            return root.as_posix()
        original_path = file_entry.get("originalPath")
        if isinstance(original_path, str) and original_path and (root / original_path.lstrip("/")).exists():
            return root.as_posix()
    return None


def _build_side_failure_reason(side: str, result: Any) -> str:
    """Build a detailed failure reason for one side of retrieval."""
    if result is None:
        return f"{side}: missing_result"
    status = getattr(result, "context_status", "unavailable") or "unavailable"
    reason = getattr(result, "context_status_reason", "")
    if isinstance(reason, str) and reason:
        return f"{side}: {status} ({reason})"
    return f"{side}: {status}"


def source_context_node(state: dict[str, Any]) -> dict[str, Any]:
    """Retrieve source context for all changed files in the PR.

    Respects the ``source_context_enabled`` flag — when disabled, sets
    ``context_status: "disabled"`` on every file entry and returns immediately.

    Args:
        state: Current ``ReviewGraphState``.

    Returns:
        State update dict with enriched ``files`` list.
    """
    start_time = time.time()

    files = state.get("files", [])
    if not files:
        return {"files": []}

    # Check if source context is enabled
    source_context_enabled = state.get("source_context_enabled", True)
    if not source_context_enabled:
        # Pass-through (FR-009): leave each upstream file entry unchanged except
        # for adding context_status="disabled".  Clearing other context fields
        # here would erase data previously populated on a resumed state.
        disabled_files = []
        for file_entry in files:
            updated: dict[str, Any] = {**file_entry, "context_status": "disabled"}
            disabled_files.append(updated)

        logger.info("Source context disabled, skipping retrieval for %d files", len(files))
        return {"files": disabled_files}

    # Resolve configuration
    config = state.get("config", {})
    review_config = config.get("review", {}) if isinstance(config, dict) else {}
    model_config_raw = state.get("model_config_raw", {})
    depth_str = review_config.get("context_depth", "standard") if isinstance(review_config, dict) else "standard"
    try:
        depth = ContextDepth(depth_str)
    except (ValueError, TypeError):
        # ValueError: unrecognised scalar depth string.  TypeError: unhashable
        # value such as a JSON object/list from a malformed repo config (raised by
        # Enum lookup on Python < 3.12).  Both fall back to the default depth.
        depth = ContextDepth.STANDARD

    commit_hash = state.get("commit_hash", "")
    base_commit_hash = state.get("base_commit_hash", "")

    # Import components
    from agentic_devtools.orchestration.review.budget import TokenBudget
    from agentic_devtools.orchestration.review.content_assembler import assemble_context
    from agentic_devtools.orchestration.review.file_retriever import (
        DEFAULT_MAX_CONCURRENCY,
        is_binary_file,
        retrieve_files_concurrent,
    )

    budget_tokens_raw = review_config.get("token_budget") if isinstance(review_config, dict) else None
    budget_tokens = _coerce_optional_positive_int(budget_tokens_raw)

    max_concurrency_raw = review_config.get("max_concurrency") if isinstance(review_config, dict) else None
    max_concurrency = _coerce_positive_int_with_default(max_concurrency_raw, DEFAULT_MAX_CONCURRENCY)

    repo_root = _resolve_verified_repo_root(files, commit_hash if isinstance(commit_hash, str) else "")

    # Prepare retrieval requests
    file_requests: list[tuple[str, str, str]] = []
    skipped_files: dict[str, dict[str, str]] = {}

    for file_entry in files:
        path = file_entry.get("path", "")
        if not path:
            continue

        # Skip binary files
        if is_binary_file(file_entry):
            skipped_files[path] = {
                "context_status": "skipped_binary",
                "context_status_reason": "binary_file_detected",
            }
            continue

        change_type = file_entry.get("changeType", "edit")
        target_path = file_entry.get("originalPath", path) if change_type == "rename" else path
        if not isinstance(target_path, str) or not target_path:
            target_path = path

        # Source side (head/feature branch)
        if commit_hash and change_type not in ("delete",):
            file_requests.append((path, commit_hash, "source"))

        # Target side (base/target branch)
        if base_commit_hash and change_type not in ("add",):
            file_requests.append((target_path, base_commit_hash, "target"))

    # Execute concurrent retrieval
    retrieval_results = retrieve_files_concurrent(
        file_requests,
        state,
        max_concurrency=max_concurrency,
    )

    # Build enriched file entries
    enriched_files: list[dict[str, Any]] = []
    processed_count = 0
    skipped_count = 0
    failed_count = 0
    supplemental_requests: list[tuple[str, str, str]] = []
    supplemental_side_labels: dict[str, dict[str, str]] = {}

    # Compute a budget-derived cap on supplemental file requests *before*
    # scheduling them.  Without this, deep-context discovery on a large PR can
    # enqueue thousands of requests and consume gigabytes of memory even though
    # the assembler will discard almost all retrieved content immediately.
    #
    # The cap is: min(_MAX_SUPPLEMENTAL_PER_CATEGORY, max(1, effective_budget //
    # assumed_tokens_per_file)).  We use the configured (or fallback) token
    # budget with the default safety margin and DEFAULT_CHARS_PER_TOKEN so the
    # estimate is consistent with the assembler.
    _raw_budget = budget_tokens if budget_tokens is not None else FALLBACK_BUDGET_TOKENS
    _effective_budget_for_cap = int(_raw_budget * (1.0 - DEFAULT_SAFETY_MARGIN))
    _tokens_per_supplemental = max(1, math.ceil(_ASSUMED_CHARS_PER_SUPPLEMENTAL / DEFAULT_CHARS_PER_TOKEN))
    _max_supplemental_per_category = min(
        _MAX_SUPPLEMENTAL_PER_CATEGORY,
        max(1, _effective_budget_for_cap // _tokens_per_supplemental),
    )

    for file_entry in files:
        updated = dict(file_entry)
        path = file_entry.get("path", "")
        target_path = file_entry.get("originalPath", path) if file_entry.get("changeType", "edit") == "rename" else path
        if not isinstance(target_path, str) or not target_path:
            target_path = path

        # Handle pre-skipped files (binary)
        if path in skipped_files:
            skip_info = skipped_files[path]
            updated["context_status"] = skip_info["context_status"]
            updated["context_status_reason"] = skip_info["context_status_reason"]
            updated["full_content_source"] = None
            updated["full_content_target"] = None
            updated["related_tests"] = []
            updated["missing_tests"] = False
            updated["truncation_applied"] = False
            updated["estimated_tokens"] = 0
            skipped_count += 1
            enriched_files.append(updated)
            continue

        # Get retrieval results
        source_result = retrieval_results.get((path, "source"))
        target_result = retrieval_results.get((target_path, "target"))

        # Populate content
        updated["full_content_source"] = source_result.content if source_result else None
        updated["full_content_target"] = target_result.content if target_result else None

        # Determine context status
        change_type = file_entry.get("changeType", "edit")
        source_ok = source_result and source_result.context_status == "success" if source_result else False
        target_ok = target_result and target_result.context_status == "success" if target_result else False

        if change_type == "add":
            # New file: branch-asymmetric — it does not exist on the target/base
            # branch, so a successful source retrieval is reported as "partial"
            # with "not_found_on_target" (per spec) rather than "success", which
            # would falsely imply both branch versions were retrieved.
            if source_ok:
                updated["context_status"] = "partial"
                updated["context_status_reason"] = "not_found_on_target"
            elif source_result:
                updated["context_status"] = source_result.context_status
                updated["context_status_reason"] = source_result.context_status_reason
                failed_count += 1
            else:
                updated["context_status"] = "unavailable"
                updated["context_status_reason"] = "no_commit_hash"
                failed_count += 1
        elif change_type == "delete":
            # Deleted file: branch-asymmetric — it does not exist on the
            # source/head branch, so a successful target retrieval is reported as
            # "partial" with "not_found_on_source" rather than "success".
            if target_ok:
                updated["context_status"] = "partial"
                updated["context_status_reason"] = "not_found_on_source"
            elif target_result:
                updated["context_status"] = target_result.context_status
                updated["context_status_reason"] = target_result.context_status_reason
                failed_count += 1
            else:
                updated["context_status"] = "unavailable"
                updated["context_status_reason"] = "no_base_commit_hash"
                failed_count += 1
        else:
            # Edit: both sides expected
            if source_ok and target_ok:
                updated["context_status"] = "success"
                updated["context_status_reason"] = ""
            elif source_ok or target_ok:
                updated["context_status"] = "partial"
                reasons = []
                if not source_ok:
                    reasons.append(_build_side_failure_reason("source", source_result))
                if not target_ok:
                    reasons.append(_build_side_failure_reason("target", target_result))
                updated["context_status_reason"] = ", ".join(reasons)
            else:
                # Both sides failed or were deliberately skipped.  Preserve
                # structured skip statuses so callers can distinguish
                # "skipped_too_large" / "skipped_binary" from retrieval errors.
                source_status = getattr(source_result, "context_status", None) if source_result else None
                target_status = getattr(target_result, "context_status", None) if target_result else None
                both_skipped = source_status in _SKIP_STATUSES and target_status in _SKIP_STATUSES
                if both_skipped:
                    # Use the source-side skip status as the aggregate; it is
                    # never a retrieval failure so do not increment failed_count.
                    # Both results are guaranteed non-None here (both_skipped
                    # requires both statuses to be in _SKIP_STATUSES, which means
                    # neither result can be None).
                    updated["context_status"] = source_status
                    updated["context_status_reason"] = "; ".join(
                        [
                            f"source: {source_result.context_status_reason}",  # type: ignore[union-attr]
                            f"target: {target_result.context_status_reason}",  # type: ignore[union-attr]
                        ]
                    )
                else:
                    updated["context_status"] = "unavailable"
                    reason_parts = []
                    if source_result:
                        reason_parts.append(f"source: {source_result.context_status_reason}")
                    if target_result:
                        reason_parts.append(f"target: {target_result.context_status_reason}")
                    updated["context_status_reason"] = "; ".join(reason_parts) if reason_parts else "retrieval_failed"
                    failed_count += 1

        # Test discovery (standard and deep depth)
        if depth in (ContextDepth.STANDARD, ContextDepth.DEEP):
            from agentic_devtools.orchestration.review.test_discovery import discover_related_tests

            related_source_content_key = "full_content_target" if change_type == "delete" else "full_content_source"
            source_content = updated.get(related_source_content_key)
            test_result = discover_related_tests(
                path,
                repo_root=repo_root,
                source_content=source_content if isinstance(source_content, str) else None,
                auto_detect_repo_root=False,
            )
            updated["related_tests"] = test_result["related_tests"]
            updated["missing_tests"] = test_result["missing_tests"]
        else:
            updated["related_tests"] = []
            updated["missing_tests"] = False
        updated["related_test_contents"] = []

        # Import resolution (deep depth only)
        if depth == ContextDepth.DEEP:
            from agentic_devtools.orchestration.review.import_resolver import resolve_imports

            import_content_key = "full_content_target" if change_type == "delete" else "full_content_source"
            import_line_key = "removedLines" if change_type == "delete" else "addedLines"
            import_content = updated.get(import_content_key)
            diff_line_numbers = None
            positive_lines = _extract_positive_line_numbers(file_entry.get(import_line_key, []))
            if positive_lines:
                diff_line_numbers = positive_lines

            if isinstance(import_content, str) and import_content:
                resolved = resolve_imports(
                    import_content,
                    path,
                    diff_lines=diff_line_numbers,
                    repo_root=repo_root,
                )
                updated["resolved_imports"] = resolved
            else:
                updated["resolved_imports"] = []
            # Config/doc discovery is independent of import-content availability.
            updated["related_config_docs"] = _discover_related_config_docs(path, files)
        else:
            updated["resolved_imports"] = []
            updated["related_config_docs"] = []
        updated["resolved_import_contents"] = []
        updated["related_config_doc_contents"] = []

        supplemental_commit_ref = base_commit_hash if change_type == "delete" else commit_hash
        if isinstance(supplemental_commit_ref, str) and supplemental_commit_ref:
            side_suffix = "target" if change_type == "delete" else "source"
            side_labels = {
                "related_test": f"related_test_{side_suffix}",
                "import": f"import_{side_suffix}",
                "config_doc": f"config_doc_{side_suffix}",
            }
            supplemental_side_labels[path] = side_labels
            for test_path in updated["related_tests"][:_max_supplemental_per_category]:
                if isinstance(test_path, str):
                    supplemental_requests.append((test_path, supplemental_commit_ref, side_labels["related_test"]))
            for import_path in updated["resolved_imports"][:_max_supplemental_per_category]:
                if isinstance(import_path, str):
                    supplemental_requests.append((import_path, supplemental_commit_ref, side_labels["import"]))
            for config_doc_path in updated["related_config_docs"][:_max_supplemental_per_category]:
                if isinstance(config_doc_path, str):
                    supplemental_requests.append((config_doc_path, supplemental_commit_ref, side_labels["config_doc"]))

        updated["truncation_applied"] = False
        updated["estimated_tokens"] = 0
        processed_count += 1
        enriched_files.append(updated)

    supplemental_results = retrieve_files_concurrent(
        supplemental_requests,
        state,
        max_concurrency=max_concurrency,
    )
    api_only_mode = repo_root is None
    for updated in enriched_files:
        file_path = updated.get("path", "")
        side_labels = supplemental_side_labels.get(file_path if isinstance(file_path, str) else "", {})
        related_test_candidates = [p for p in updated.get("related_tests", []) if isinstance(p, str)]
        resolved_import_candidates = [p for p in updated.get("resolved_imports", []) if isinstance(p, str)]
        related_config_doc_candidates = [p for p in updated.get("related_config_docs", []) if isinstance(p, str)]
        related_test_contents: list[dict[str, str]] = []
        verified_related_tests: list[str] = []
        for test_path in related_test_candidates:
            related_test_label = side_labels.get("related_test")
            result = supplemental_results.get((test_path, related_test_label)) if related_test_label else None
            if result and result.context_status == "success" and isinstance(result.content, str):
                related_test_contents.append({"path": test_path, "content": result.content})
                verified_related_tests.append(test_path)
        updated["related_test_contents"] = related_test_contents

        resolved_import_contents: list[dict[str, str]] = []
        verified_resolved_imports: list[str] = []
        for import_path in resolved_import_candidates:
            import_label = side_labels.get("import")
            result = supplemental_results.get((import_path, import_label)) if import_label else None
            if result and result.context_status == "success" and isinstance(result.content, str):
                resolved_import_contents.append({"path": import_path, "content": result.content})
                verified_resolved_imports.append(import_path)
        updated["resolved_import_contents"] = resolved_import_contents

        related_config_doc_contents: list[dict[str, str]] = []
        verified_related_config_docs: list[str] = []
        for config_doc_path in related_config_doc_candidates:
            config_doc_label = side_labels.get("config_doc")
            result = supplemental_results.get((config_doc_path, config_doc_label)) if config_doc_label else None
            if result and result.context_status == "success" and isinstance(result.content, str):
                related_config_doc_contents.append({"path": config_doc_path, "content": result.content})
                verified_related_config_docs.append(config_doc_path)
        updated["related_config_doc_contents"] = related_config_doc_contents

        if api_only_mode:
            updated["related_test_candidates"] = related_test_candidates
            updated["resolved_import_candidates"] = resolved_import_candidates
            updated["related_config_doc_candidates"] = related_config_doc_candidates
            updated["related_tests"] = verified_related_tests
            updated["resolved_imports"] = verified_resolved_imports
            updated["related_config_docs"] = verified_related_config_docs
            if related_test_candidates and not verified_related_tests:
                updated["missing_tests"] = True
            elif verified_related_tests:
                updated["missing_tests"] = False
            else:
                # No candidate paths were discovered in API-only mode. Preserve
                # the discovery-stage ``missing_tests`` signal as-is.
                pass

    # Apply budget-aware content assembly independently per file so each prompt
    # is bounded by the routed review model's context window.  Resolve the
    # provider default model once here so every file uses the same fallback as
    # review_files_node — preventing a context-window mismatch when the
    # fallback synthesis produces a model different from copilot.model_id.
    provider_default_model = _get_provider_default_model(state.get("llm_config_path"))
    requested_model = state.get("requested_model")
    total_budget_consumed = 0
    assembled_files: list[dict[str, Any]] = []
    for updated in enriched_files:
        path = updated.get("path", "")
        model_id = _resolve_file_budget_model_id(
            path if isinstance(path, str) else "",
            model_config_raw,
            requested_model=requested_model if isinstance(requested_model, str) else None,
            provider_default_model=provider_default_model,
        )
        budget = TokenBudget(budget_tokens=budget_tokens, model_id=model_id)
        assembled = assemble_context([updated], budget)
        total_budget_consumed += budget.consumed
        if assembled:
            assembled_files.append(assembled[0])
        else:
            assembled_files.append(updated)
    enriched_files = assembled_files

    elapsed = time.time() - start_time
    logger.info(
        "Source context retrieval complete: %d processed, %d skipped, %d failed, %d tokens consumed, %.2fs elapsed",
        processed_count,
        skipped_count,
        failed_count,
        total_budget_consumed,
        elapsed,
    )

    return {"files": enriched_files}
