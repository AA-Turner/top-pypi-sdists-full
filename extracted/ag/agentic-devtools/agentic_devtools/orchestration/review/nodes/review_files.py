"""``review_files`` node — LLM-powered per-file code review.

Satisfies FR-003 (structured output per file) and FR-005 (atomic state
persistence after each file review).  Uses NFR-004 retry via the
LLM error normalizer.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import asdict
from typing import Any

from ..state import FileReviewOutput, FileReviewResult


def review_files_node(state: dict[str, Any], *, provider_factory: Any = None) -> dict[str, Any]:
    """Review each changed file using an LLM.

    Iterates over ``state["files"]``, invokes the LLM with the file diff
    (and optional source context), parses structured output into
    ``FileReviewResult`` objects, and atomically updates
    ``review-state.json`` after each file.

    Args:
        state: Current ``ReviewGraphState``.
        provider_factory: Optional pre-built provider factory injected via
            node closure by :func:`build_review_graph`.  Kept outside graph
            state to prevent credentials from being captured by the
            LangGraph checkpointer or returned in the final graph result.

    Returns:
        State update dict with ``file_results``.
    """
    files = state.get("files", [])
    pr_id = state.get("pr_id")
    config = state.get("config", {})
    source_context_enabled = state.get("source_context_enabled", True)
    model_config_raw = state.get("model_config_raw", {})

    if not files:
        return {"file_results": [], "errors": []}

    results: list[dict[str, Any]] = []
    errors: list[str] = []

    # Only resolve the provider when at least one file actually needs review.
    # Pathless entries are always skipped; calling get_provider() before this
    # check would raise authentication/configuration errors even when the loop
    # would immediately return an empty result — contradicting the
    # established contract of test_skips_files_without_path.
    if not any(f.get("path") for f in files):
        return {"file_results": [], "errors": []}

    # Resolve provider and node config once before looping.
    # This prevents recording false per-file "request-changes" verdicts for
    # provider-wide failures and ensures provider/model routing are aligned.
    if provider_factory is not None and hasattr(provider_factory, "get_provider"):
        provider = provider_factory.get_provider("review_files", "pr_review")
    else:
        # Load config from the repo-root path stored in state so this node uses
        # the same snapshot as the preflight check in runner.py regardless of CWD.
        from agentic_devtools.orchestration.llm.config import load_config
        from agentic_devtools.orchestration.llm.factory import get_provider

        llm_config_path = state.get("llm_config_path")
        config_snapshot = load_config(llm_config_path)
        provider = get_provider("review_files", "pr_review", config=config_snapshot)
    provider_default_model = _resolved_provider_default_model(provider)

    for file_info in files:
        file_path = file_info.get("path", "")
        if not file_path:
            continue

        try:
            result = _review_single_file(
                file_path=file_path,
                file_info=file_info,
                config=config,
                source_context_enabled=source_context_enabled,
                model_config_raw=model_config_raw,
                state=state,
                provider=provider,
                provider_default_model=provider_default_model,
                requested_model=state.get("requested_model"),
            )
            results.append(asdict(result))

            # Atomic state persistence (FR-005)
            if pr_id:
                _update_review_state_for_file(int(pr_id), file_path, result)

        except Exception as exc:
            # Provider-wide failures (e.g., invalid credentials) must abort the
            # whole node; treating them as per-file review failures yields
            # misleading "request-changes" results for every file.
            if _is_provider_wide_failure(exc):
                raise
            # Log full exception details to stderr only — provider-specific error
            # messages (e.g. HTTP responses, token info) must NOT be persisted to
            # state artifacts such as review-state.json or PR comments.
            print(
                f"review_files: error reviewing {file_path}: {exc}",
                file=sys.stderr,
            )
            # Sanitized label: no exception text so sensitive details stay out of state
            sanitized_label = f"review_files: failed to review {file_path}"
            errors.append(sanitized_label)

            # Record error result so the file isn't silently skipped
            error_result = FileReviewResult(
                file_path=file_path,
                outcome="request-changes",
                summary="Review failed: see error log for details",
                model_id=None,
                tokens_used=None,
            )
            results.append(asdict(error_result))
            if pr_id:
                _update_review_state_for_file(int(pr_id), file_path, error_result)

    return {"file_results": results, "errors": errors}


def _review_single_file(
    *,
    file_path: str,
    file_info: dict[str, Any],
    config: dict[str, Any],
    source_context_enabled: bool,
    model_config_raw: dict[str, Any],
    state: dict[str, Any],
    provider: Any | None = None,
    provider_default_model: str | None = None,
    requested_model: str | None = None,
) -> FileReviewResult:
    """Review a single file using the LLM.

    Args:
        file_path: Repository-relative path of the file.
        file_info: ADO file change metadata.
        config: Repo configuration.
        source_context_enabled: Whether source context enrichment is on.
        model_config_raw: Model routing configuration.
        state: Full graph state for context.
        provider: Pre-resolved provider instance, when available.
        provider_default_model: Provider's resolved default model.
        requested_model: Explicit CLI ``--model`` override.

    Returns:
        ``FileReviewResult`` with the LLM's verdict.
    """
    from ..llm_error_normalizer import TransientLLMError, normalize_llm_error

    # Resolve model for this file (FR-009)
    model_id = _resolve_model(
        file_path,
        model_config_raw,
        requested_model=requested_model,
        provider_default_model=provider_default_model,
    )

    # Build the review prompt
    prompt = _build_review_prompt(
        file_path=file_path,
        file_info=file_info,
        config=config,
        source_context_enabled=source_context_enabled,
        state=state,
    )

    # Invoke LLM with structured output
    max_retries = 3
    tokens_used: int | None = None
    attempt = 0

    while True:
        try:
            with normalize_llm_error():
                output, tokens, effective_model, provider_type, latency_ms, finish_reason = _invoke_llm(
                    prompt, model_id, provider=provider
                )
                tokens_used = tokens

                return FileReviewResult(
                    file_path=file_path,
                    outcome=output.outcome,
                    summary=output.summary,
                    suggestions=[s.model_dump() for s in output.suggestions],
                    model_id=effective_model or model_id,
                    provider_type=provider_type,
                    latency_ms=latency_ms,
                    finish_reason=finish_reason,
                    tokens_used=tokens_used,
                )
        except TransientLLMError:
            if attempt < max_retries - 1:
                delay = 2**attempt
                time.sleep(delay)
                attempt += 1
                continue
            raise
        except Exception:
            # Non-transient error — fail immediately
            raise


def _resolve_model(
    file_path: str,
    model_config_raw: dict[str, Any],
    *,
    requested_model: str | None = None,
    provider_default_model: str | None = None,
) -> str:
    """Resolve the LLM model to use for a given file.

    Delegates to the model_routing module if available, otherwise uses
    the default model from config or falls back to a sensible default.
    """
    if isinstance(requested_model, str) and requested_model.strip():
        return requested_model.strip()

    try:
        from ..model_routing import resolve_model_for_file

        return resolve_model_for_file(
            file_path,
            model_config_raw,
            default_model=provider_default_model,
        )
    except ImportError:
        pass

    default_model = model_config_raw.get("default-model", "")
    if default_model:
        return default_model
    if provider_default_model:
        return provider_default_model

    from agentic_devtools.state import get_value

    return get_value("copilot.model_id") or "gpt-4o"


def _format_numbered_file_content(file_content: str) -> str:
    """Format full-file fallback content with 1-based line numbers."""
    lines = file_content.splitlines()
    return "\n".join(f"{n:>4} | {line}" for n, line in enumerate(lines, start=1))


def _build_pre_enriched_context(
    file_info: dict[str, Any],
    *,
    content_key: str,
    line_key: str,
    bound_fallback_context: Any,
    extract_surrounding_context: Any,
) -> str:
    """Build a prompt-ready context block from pre-enriched file content."""
    full_content = file_info.get(content_key)
    if not isinstance(full_content, str) or not full_content:
        return ""

    diff_ranges: list[tuple[int, int]] = []
    line_entries = file_info.get(line_key, [])
    if not isinstance(line_entries, list):
        line_entries = []
    for entry in line_entries:
        if not isinstance(entry, dict):
            continue
        ln = entry.get("line")
        if isinstance(ln, int) and ln > 0:
            diff_ranges.append((ln, ln))

    if diff_ranges:
        # When this side's content was smart-truncated by the budget assembler,
        # its line 1 no longer corresponds to original line 1, so the original
        # diff line anchors cannot be interpreted against it.  Render the
        # already-bounded excerpt directly instead.
        if file_info.get(f"{content_key}_truncated", False):
            return bound_fallback_context(full_content)
        available_lines = len(full_content.splitlines())
        max_diff_line = max(ln for ln, _ in diff_ranges)
        if max_diff_line <= available_lines:
            return full_content
        if file_info.get("truncation_applied", False):
            return bound_fallback_context(full_content)
        return ""

    return bound_fallback_context(full_content)


_MAX_PATH_FALLBACK = 20  # Maximum paths to list when content is unavailable


def _render_related_file_sections(
    *,
    parts: list[str],
    section_title: str,
    paths: Any,
    content_items: Any,
    omitted_count: Any,
    max_fallback_paths: int = _MAX_PATH_FALLBACK,
) -> None:
    """Render related-file content, or path-only fallbacks when content is unavailable."""
    rendered_items: list[str] = []
    if isinstance(content_items, list) and content_items:
        for item in content_items:
            if not isinstance(item, dict):
                continue
            path = item.get("path")
            content = item.get("content")
            if not isinstance(path, str) or not isinstance(content, str):
                continue
            rendered_items.extend(
                [
                    f"### {path}\n",
                    "```",
                    content.rstrip(),
                    "```",
                    "",
                ]
            )

    if rendered_items:
        parts.append(f"## {section_title}\n")
        parts.extend(rendered_items)
        if isinstance(omitted_count, int) and omitted_count > 0:
            parts.append("")
            parts.append(f"{omitted_count} file(s) were omitted or truncated to stay within the token budget.")
            parts.append("")
        return

    if isinstance(paths, list) and paths:
        valid_paths = [p for p in paths if isinstance(p, str)]
        shown_paths = valid_paths[:max_fallback_paths]
        hidden_paths = len(valid_paths) - len(shown_paths)
        parts.append(f"## {section_title}\n")
        parts.append("\n".join(f"- {path}" for path in shown_paths))
        total_omitted = (omitted_count if isinstance(omitted_count, int) else 0) + hidden_paths
        if total_omitted > 0:
            parts.append("")
            parts.append(f"{total_omitted} file(s) were omitted or truncated to stay within the token budget.")
        parts.append("")


def _build_review_prompt(
    *,
    file_path: str,
    file_info: dict[str, Any],
    config: dict[str, Any],
    source_context_enabled: bool,
    state: dict[str, Any],
) -> str:
    """Build the LLM prompt for reviewing a single file."""
    parts: list[str] = []
    parts.append("Review the following file change and provide a structured verdict.\n")
    parts.append(f"File: {file_path}")
    parts.append(f"Change type: {file_info.get('changeType', 'edit')}\n")
    # Prefer the budget-limited excerpt when the assembler produced one.  An
    # explicitly-set excerpt (including an intentionally empty string for a
    # zero-token allocation) must take precedence over the full patch so the
    # configured token budget is respected; only fall back to the full patch
    # when no excerpt key is present.
    if "patch_budget_excerpt" in file_info:
        patch = file_info.get("patch_budget_excerpt")
    else:
        patch = file_info.get("patch")
    if isinstance(patch, str) and patch.strip():
        parts.append("## Patch\n")
        parts.append("```diff")
        parts.append(patch.rstrip())
        parts.append("```")
        parts.append("")
    else:
        parts.append(
            "## Patch unavailable\n"
            "No diff payload was provided for this file. "
            "If source context is available below, use it cautiously — "
            "you cannot determine exactly what changed. Do not approve the file "
            "unless the available context clearly proves the change is correct. "
            "Treat 'request-changes' as the default outcome and explain that the "
            "review is blocked by the missing diff.\n"
        )

    # Add source context if enabled and the file is not binary.
    # Binary files produce garbage or very large text when decoded, so skip enrichment.
    is_binary = file_info.get("isBinary", False)
    if source_context_enabled and not is_binary:
        context_content = ""
        target_context_content = ""

        try:
            from ..source_context import (
                bound_fallback_context,
                extract_surrounding_context,
                fetch_source_context,
            )

            context_content = _build_pre_enriched_context(
                file_info,
                content_key="full_content_source",
                line_key="addedLines",
                bound_fallback_context=bound_fallback_context,
                extract_surrounding_context=extract_surrounding_context,
            )
            target_context_content = _build_pre_enriched_context(
                file_info,
                content_key="full_content_target",
                line_key="removedLines",
                bound_fallback_context=bound_fallback_context,
                extract_surrounding_context=extract_surrounding_context,
            )

            # Only attempt a live fetch when the source_context node did NOT run for
            # this file.  The node stamps every file entry it processes with a
            # ``context_status`` and has already made a budget-aware retrieval decision
            # (including known failures, target-only results, and deleted files).  When
            # ``context_status`` is present, re-fetching here would either inject content
            # never charged to the PR-wide TokenBudget or redundantly repeat a request
            # that already failed, so the legacy fallback is skipped.  A missing
            # ``context_status`` means the node did not run (e.g. disabled at an older
            # revision), so a bounded live fetch is safe.
            node_ran = "context_status" in file_info
            if not node_ran and not context_content and not file_info.get("truncation_applied", False):
                full_content = fetch_source_context(
                    file_path=file_path,
                    state=state,
                )
                if full_content:
                    # Build diff line ranges from the added-line numbers in the *new* file so
                    # we only inject the context that is relevant to the review, avoiding
                    # blowing the model's context budget on large files.
                    # Note: removedLines carry base-file line numbers and must NOT be used
                    # here because we fetched full_content from the source (new) commit.
                    added_lines = file_info.get("addedLines", [])
                    diff_ranges = []
                    for entry in added_lines:
                        ln = entry.get("line", 0)
                        if ln:
                            diff_ranges.append((ln, ln))

                    if diff_ranges:
                        context_content = extract_surrounding_context(full_content, diff_ranges)
                    else:
                        # No line information available (e.g. diff enrichment failed);
                        # fall back to the file content bounded to a max character budget
                        # so large files don't blow the LLM context window.
                        context_content = bound_fallback_context(_format_numbered_file_content(full_content))

            if context_content:
                parts.append("## Source Context\n")
                parts.append(context_content)
                parts.append("")
            if target_context_content:
                parts.append("## Target/Base Context\n")
                parts.append(target_context_content)
                parts.append("")

        except ImportError:
            pass
        except Exception as exc:
            print(
                f"Warning: source context enrichment skipped for {file_path}: {exc}",
                file=sys.stderr,
            )

        _render_related_file_sections(
            parts=parts,
            section_title="Related Test Files",
            paths=file_info.get("related_tests", []),
            content_items=file_info.get("related_test_contents", []),
            omitted_count=file_info.get("related_tests_omitted_count"),
            max_fallback_paths=file_info.get("related_tests_paths_display_cap", _MAX_PATH_FALLBACK),
        )
        _render_related_file_sections(
            parts=parts,
            section_title="Resolved First-Party Imports",
            paths=file_info.get("resolved_imports", []),
            content_items=file_info.get("resolved_import_contents", []),
            omitted_count=file_info.get("resolved_imports_omitted_count"),
            max_fallback_paths=file_info.get("resolved_imports_paths_display_cap", _MAX_PATH_FALLBACK),
        )
        _render_related_file_sections(
            parts=parts,
            section_title="Related Config/Documentation Files",
            paths=file_info.get("related_config_docs", []),
            content_items=file_info.get("related_config_doc_contents", []),
            omitted_count=file_info.get("related_config_docs_omitted_count"),
            max_fallback_paths=file_info.get("related_config_docs_paths_display_cap", _MAX_PATH_FALLBACK),
        )

    # Add focus areas from repo config
    review_config = config.get("review", {})
    if isinstance(review_config, dict):
        focus_areas_file = review_config.get("focus-areas-file")
        if focus_areas_file:
            from agentic_devtools.cli.azure_devops.pr_review_manifest import resolve_repo_root
            from agentic_devtools.config import load_review_focus_areas

            try:
                repo_root = resolve_repo_root()
                focus_areas = load_review_focus_areas(repo_root)
            except (FileNotFoundError, RuntimeError) as exc:
                print(f"Warning: failed to load review focus areas: {exc}", file=sys.stderr)
                focus_areas = None

            if isinstance(focus_areas, str) and focus_areas.strip():
                parts.append("\n## Review Focus Areas\n")
                parts.append(focus_areas.strip())
                parts.append("")

    parts.append(
        "\nProvide your review as structured output with:\n"
        "- outcome: 'approve', 'request-changes', or 'request-changes-with-suggestion'\n"
        "- summary: 1-3 sentence rationale\n"
        "- suggestions: list of findings with severity, content, and optional replacement_code\n"
        "\nIMPORTANT: `line` and `endLine` in suggestions must be 1-based line numbers in the "
        "**file** (not diff/patch-relative line numbers). These anchors are used to post inline "
        "comments on specific lines in the actual source file."
    )

    return "\n".join(parts)


def _invoke_llm(
    prompt: str,
    model_id: str,
    *,
    provider: Any | None = None,
) -> tuple[FileReviewOutput, int | None, str | None, str | None, int | None, str | None]:
    """Invoke the LLM and parse structured output.

    Resolves a configured ``LLMProvider`` for the ``"review_files"`` node in
    the ``"pr_review"`` workflow via ``get_provider()``, then wraps it in an
    ``ExecutionContext`` so the ``ReasoningAdapter`` can forward the call to
    the provider.  The resolved ``model_id`` is passed as a model override so
    per-file routing (FR-009) takes precedence over the provider's default.

    Returns:
        Tuple of (parsed FileReviewOutput, tokens used, effective model ID,
        provider type, latency in milliseconds, finish reason).
    """
    from agentic_devtools.orchestration.execution.context_factory import build_execution_context
    from agentic_devtools.orchestration.llm.factory import get_provider

    if provider is None:
        provider = get_provider("review_files", "pr_review")

    ctx = build_execution_context(provider=provider)
    response = ctx.reasoning.invoke(
        prompt,
        output_schema=FileReviewOutput,
        model=model_id,
    )

    tokens: int | None = None
    if response.usage is not None:
        tokens = response.usage.total_tokens

    # Prefer the already-validated structured output when the provider returned
    # it via the schema-parsing path; only fall back to raw-text parsing when
    # parsed_output is absent.
    if isinstance(response.parsed_output, FileReviewOutput):
        return (
            response.parsed_output,
            tokens,
            getattr(response, "model", None),
            getattr(response, "provider_type", None),
            getattr(response, "latency_ms", None),
            getattr(response, "finish_reason", None),
        )

    # Fall back: parse raw_text as JSON (provider returned plain text).
    try:
        output = FileReviewOutput.model_validate_json(response.raw_text)
    except Exception:
        # Second fallback: try constructing from a plain dict
        try:
            data = json.loads(response.raw_text)
            output = FileReviewOutput(**data)
        except Exception as parse_exc:
            raise ValueError(f"Failed to parse LLM output as FileReviewOutput: {parse_exc}") from parse_exc

    return (
        output,
        tokens,
        getattr(response, "model", None),
        getattr(response, "provider_type", None),
        getattr(response, "latency_ms", None),
        getattr(response, "finish_reason", None),
    )


def _is_provider_wide_failure(exc: Exception) -> bool:
    """Return whether ``exc`` represents a provider-wide failure.

    Returns ``True`` for:

    - Authentication / configuration failures (401, 403, 404, ``AuthenticationError``,
      ``ProviderNotConfiguredError``) — the provider is unusable for this
      invocation. HTTP 404 covers model-not-found (OpenAI) and
      deployment-not-found (Azure) errors that indicate a misconfigured endpoint.
    """
    from agentic_devtools.orchestration.llm.errors import (
        AuthenticationError,
        ModelNotAvailableError,
        ProviderNotConfiguredError,
    )

    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if isinstance(
            current,
            (AuthenticationError, ProviderNotConfiguredError),
        ):
            return True
        if isinstance(current, ModelNotAvailableError):
            return True
        status_code = _status_code_from_exception(current)
        if status_code in {401, 403, 404}:
            return True
        current = current.__cause__ or current.__context__
    return False


def _status_code_from_exception(exc: BaseException) -> int | None:
    """Extract HTTP status code from common SDK exception shapes."""
    code = getattr(exc, "status_code", None)
    if isinstance(code, int):
        return code
    response = getattr(exc, "response", None)
    if response is not None:
        response_code = getattr(response, "status_code", None)
        if isinstance(response_code, int):
            return response_code
    return None


def _resolved_provider_default_model(provider: Any) -> str | None:
    """Best-effort extraction of the provider's configured default model."""
    model = getattr(provider, "_model", None)
    if isinstance(model, str) and model.strip():
        return model
    return None


def _update_review_state_for_file(pr_id: int, file_path: str, result: FileReviewResult) -> None:
    """Atomically update review-state.json with the result for a single file.

    Holds an exclusive lock for the entire load → mutate → save cycle via
    ``read_modify_write_review_state`` so concurrent callers cannot interleave
    reads and writes.  Satisfies FR-005: atomic persistence after each file review.

    Draft suggestions are persisted with ``threadId=0`` and ``commentId=0`` as
    placeholder sentinels indicating the finding has not yet been posted to ADO.
    ``post_results`` replaces these draft entries with real ``SuggestionEntry``
    objects (carrying actual thread/comment IDs) once threads are successfully
    created.  This ensures LLM findings are not lost if the pipeline is
    interrupted between the ``review_files`` and ``post_results`` nodes.
    """
    from agentic_devtools.cli.azure_devops.review_state import (
        ReviewStatus,
        SuggestionEntry,
        normalize_file_path,
        read_modify_write_review_state,
    )

    # Map outcome to review status
    status_map = {
        "approve": ReviewStatus.APPROVED.value,
        "request-changes": ReviewStatus.NEEDS_WORK.value,
        "request-changes-with-suggestion": ReviewStatus.NEEDS_WORK.value,
    }

    try:
        with read_modify_write_review_state(pr_id) as review_state:
            normalized_path = normalize_file_path(file_path)
            if normalized_path in review_state.files:
                entry = review_state.files[normalized_path]
                entry.status = status_map.get(result.outcome, ReviewStatus.NEEDS_WORK.value)
                entry.summary = result.summary
                entry.modelId = result.model_id
                entry.providerType = result.provider_type
                entry.latencyMs = result.latency_ms
                entry.finishReason = result.finish_reason
                entry.tokensUsed = result.tokens_used

                # Build draft SuggestionEntry objects for each LLM finding.
                # threadId=0 / commentId=0 are sentinels meaning "pending ADO post";
                # post_results will clear and replace them with real ADO IDs.
                draft_suggestions: list[SuggestionEntry] = []
                for s in result.suggestions:
                    if isinstance(s, dict):
                        line: int = s.get("line", 1)
                        end_line = s.get("endLine")
                        severity: str = s.get("severity", "low")
                        content: str = s.get("content", "")
                        out_of_scope: bool = bool(s.get("out_of_scope", False))
                        replacement_code = s.get("replacement_code")
                    else:
                        line = getattr(s, "line", 1)
                        end_line = getattr(s, "endLine", None)
                        severity = getattr(s, "severity", "low")
                        content = getattr(s, "content", "")
                        out_of_scope = bool(getattr(s, "out_of_scope", False))
                        replacement_code = getattr(s, "replacement_code", None)

                    draft_suggestions.append(
                        SuggestionEntry(
                            threadId=0,
                            commentId=0,
                            line=line,
                            endLine=end_line if isinstance(end_line, int) else line,
                            severity=severity,
                            outOfScope=out_of_scope,
                            linkText="",  # populated after posting to ADO
                            content=content,
                            replacement_code=replacement_code if isinstance(replacement_code, str) else None,
                        )
                    )
                entry.suggestions = draft_suggestions
    except Exception as exc:
        print(f"Warning: failed to save review state: {exc}", file=sys.stderr)
