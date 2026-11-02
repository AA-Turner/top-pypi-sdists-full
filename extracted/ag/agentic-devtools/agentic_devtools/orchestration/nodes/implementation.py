"""Implementation node: TDD RED/GREEN cycle for each checklist item.

Iterates over incomplete checklist items, performing for each:
1. RED: Generate a failing test via LLM
2. GREEN: Generate implementation code via LLM
3. VERIFY: Run tests to confirm they pass

Uses repository context discovery to inform LLM prompts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentic_devtools.orchestration.execution.context_factory import _run_async
from agentic_devtools.orchestration.nodes._helpers import (
    _to_nonneg_int,
    detect_test_conventions,
    read_file_content,
    resolve_repo_root,
    run_command,
    scan_directory_structure,
    utc_now,
)
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


def implementation_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Execute TDD cycle for each incomplete checklist item.

    Iterates over checklist items, generating tests (RED) and implementation
    (GREEN) for each. Verifies with ``agdt-test-pattern``. When ``dry_run`` is
    active, local file writes and test execution are simulated by marking
    incomplete checklist items complete in returned graph state only.
    """
    checklist_items = state.get("checklist_items", [])
    if not isinstance(checklist_items, list):
        checklist_items = []

    raw_log = state.get("implementation_log", [])
    implementation_log: list[dict[str, Any]] = raw_log if isinstance(raw_log, list) else []
    raw_paths = state.get("affected_paths", [])
    affected_paths: list[str] = (
        [str(p) for p in raw_paths if not isinstance(p, bool)] if isinstance(raw_paths, list) else []
    )
    dry_run = state.get("dry_run") is True
    error_message: str | None = None
    accumulated_prompt = 0
    accumulated_completion = 0

    if dry_run:
        simulated_items = list(checklist_items)
        for i, item in enumerate(simulated_items):
            if not isinstance(item, dict) or item.get("is_complete"):
                continue
            simulated_items[i] = {**item, "is_complete": True}
            implementation_log.append(
                {
                    "item_index": i,
                    "status": "dry_run",
                    "affected_paths": [],
                    "timestamp": utc_now(),
                }
            )
        dict_items = [item for item in simulated_items if isinstance(item, dict)]
        all_complete = bool(dict_items) and all(item.get("is_complete", False) for item in dict_items)
        if not dict_items:
            error_message = "No valid checklist items to implement; cannot mark implementation complete."
        return {
            "step": "implementation",
            "error": error_message if not all_complete and error_message else None,
            "checklist_items": simulated_items,
            "checklist_complete": all_complete,
            "implementation_log": implementation_log,
            "affected_paths": affected_paths,
            "dry_run_skipped": True,
            "token_usage_prompt": _to_nonneg_int(state.get("token_usage_prompt")),
            "token_usage_completion": _to_nonneg_int(state.get("token_usage_completion")),
            "events": [
                {
                    "event": "implementation_completed" if all_complete else "implementation_partial",
                    "timestamp": utc_now(),
                    "signals": {
                        "checklist_complete": all_complete,
                        "error": error_message,
                        "action": "skipped_dry_run",
                    },
                }
            ],
        }

    # Process each incomplete item
    for i, item in enumerate(checklist_items):
        if not isinstance(item, dict):
            continue
        if item.get("is_complete"):
            continue

        try:
            result = _implement_checklist_item(item, i, state)
        except Exception as exc:
            error_message = f"Implementation failed for item {i}: {exc}"
            implementation_log.append(
                {
                    "item_index": i,
                    "status": "failed",
                    "error": str(exc),
                    "timestamp": utc_now(),
                }
            )
            break

        accumulated_prompt += _to_nonneg_int(result.get("token_usage_prompt"))
        accumulated_completion += _to_nonneg_int(result.get("token_usage_completion"))

        if result.get("error"):
            error_message = result["error"]
            implementation_log.append(
                {
                    "item_index": i,
                    "status": "failed",
                    "error": error_message,
                    "timestamp": utc_now(),
                }
            )
            break

        # Mark item as complete
        checklist_items[i] = {**item, "is_complete": True}
        affected_paths.extend(result.get("affected_paths", []))
        implementation_log.append(
            {
                "item_index": i,
                "status": "completed",
                "affected_paths": result.get("affected_paths", []),
                "timestamp": utc_now(),
            }
        )

    # Determine if all items are complete. A checklist with no valid (dict) items —
    # an empty list, a non-list value coerced to [], or only corrupted non-dict
    # entries — must NOT be treated as complete: ``all(...)`` over an empty
    # generator returns True, which would let the workflow skip implementation
    # entirely and proceed as if the work were done.
    dict_items = [item for item in checklist_items if isinstance(item, dict)]
    all_complete = bool(dict_items) and all(item.get("is_complete", False) for item in dict_items)
    if not dict_items:
        error_message = "No valid checklist items to implement; cannot mark implementation complete."

    return {
        "step": "implementation",
        "error": error_message if not all_complete and error_message else None,
        "checklist_items": checklist_items,
        "checklist_complete": all_complete,
        "implementation_log": implementation_log,
        "affected_paths": affected_paths,
        "token_usage_prompt": _to_nonneg_int(state.get("token_usage_prompt")) + accumulated_prompt,
        "token_usage_completion": _to_nonneg_int(state.get("token_usage_completion")) + accumulated_completion,
        "events": [
            {
                "event": "implementation_completed" if all_complete else "implementation_partial",
                "timestamp": utc_now(),
                "signals": {"checklist_complete": all_complete, "error": error_message},
            }
        ],
    }


def _implement_checklist_item(
    item: dict[str, Any],
    index: int,
    state: WorkOnIssueState,
) -> dict[str, Any]:
    """Implement a single checklist item using TDD cycle.

    Returns dict with affected_paths list, accumulated token usage counts,
    or an error string.
    """
    issue_key = state.get("issue_key", "")
    plan = state.get("plan", "")
    description = item.get("description", "")

    # Discover repository context
    repo_root = _get_repo_root(state)
    if repo_root is None:
        return {"error": "Cannot determine repository root"}

    context = _build_context(repo_root)
    prompt_tokens = 0
    completion_tokens = 0

    # RED phase: generate failing test
    test_result = _generate_test(description, plan, context, issue_key, repo_root)
    test_usage = test_result.get("token_usage", {})
    prompt_tokens += _to_nonneg_int(test_usage.get("prompt_tokens"))
    completion_tokens += _to_nonneg_int(test_usage.get("completion_tokens"))
    if test_result.get("error"):
        return {
            "error": f"RED phase failed: {test_result['error']}",
            "token_usage_prompt": prompt_tokens,
            "token_usage_completion": completion_tokens,
        }

    test_path = test_result.get("path", "")
    affected = [test_path] if test_path else []

    # RED verification: confirm the generated test actually fails before writing implementation.
    # A test that immediately passes either has no real assertions or the behavior already exists.
    # pytest exit code 1 means "tests ran and at least one failed" — the expected outcome for a
    # properly-written RED-phase test.  Any other non-zero code (2 = usage/syntax error,
    # 3 = internal error, 4/5 = no tests collected) indicates a broken test file.
    if test_path:
        red_verify = run_command(
            ["agdt-test-pattern", test_path, "-v", "-o", "addopts="],
            timeout=120,
            cwd=str(repo_root),
        )
        if red_verify.returncode == 0:
            return {
                "error": (
                    f"RED phase failed: generated test already passes before implementation; "
                    f"the behavior may already exist or the test has no real assertions ({test_path})"
                ),
                "token_usage_prompt": prompt_tokens,
                "token_usage_completion": completion_tokens,
            }
        if red_verify.returncode != 1:
            # Not a clean test failure — exit codes 2+ indicate broken generated test
            # (2 = usage/syntax error, 3 = internal error, 4 = pytest usage error, 5 = no tests collected).
            return {
                "error": (
                    f"RED phase failed: generated test is invalid "
                    f"(pytest exit {red_verify.returncode}); "
                    f"expected exit code 1 (test failures) but got a collection or syntax error. "
                    f"Output: {red_verify.stderr[:500]}"
                ),
                "token_usage_prompt": prompt_tokens,
                "token_usage_completion": completion_tokens,
            }

    # GREEN phase: generate implementation
    impl_result = _generate_implementation(description, plan, context, test_path, issue_key, repo_root)
    impl_usage = impl_result.get("token_usage", {})
    prompt_tokens += _to_nonneg_int(impl_usage.get("prompt_tokens"))
    completion_tokens += _to_nonneg_int(impl_usage.get("completion_tokens"))
    if impl_result.get("error"):
        return {
            "error": f"GREEN phase failed: {impl_result['error']}",
            "token_usage_prompt": prompt_tokens,
            "token_usage_completion": completion_tokens,
        }

    impl_path = impl_result.get("path", "")
    if impl_path:
        affected.append(impl_path)

    # VERIFY: run tests
    if test_path:
        verify_result = run_command(
            ["agdt-test-pattern", test_path, "-v", "-o", "addopts="],
            timeout=120,
            cwd=str(repo_root),
        )
        if verify_result.returncode != 0:
            return {
                "error": f"VERIFY phase failed: tests did not pass\n{verify_result.stdout}\n{verify_result.stderr}",
                "token_usage_prompt": prompt_tokens,
                "token_usage_completion": completion_tokens,
            }

    return {
        "affected_paths": affected,
        "token_usage_prompt": prompt_tokens,
        "token_usage_completion": completion_tokens,
    }


def _get_repo_root(state: WorkOnIssueState | None = None) -> Path | None:
    """Get the repository root path, preferring the setup worktree when available."""
    return resolve_repo_root(state)


def _build_context(repo_root: Path) -> dict[str, Any]:
    """Build repository context for LLM prompts."""
    structure = scan_directory_structure(repo_root, max_depth=2)
    conventions = detect_test_conventions(repo_root)
    return {
        "structure": structure[:100],  # Limit to avoid token overflow
        "conventions": conventions,
    }


def _resolve_output_path(repo_root: Path, file_path: str) -> Path:
    """Resolve an LLM-provided output path within repository bounds."""
    candidate = Path(file_path)
    if candidate.is_absolute():
        raise ValueError(f"Absolute paths are not allowed: {file_path}")

    resolved = (repo_root / candidate).resolve()
    repo_root_resolved = repo_root.resolve()

    try:
        resolved.relative_to(repo_root_resolved)
    except ValueError as exc:
        raise ValueError(f"Path traversal is not allowed: {file_path}") from exc

    return resolved


def _generate_test(
    description: str,
    plan: str,
    context: dict[str, Any],
    issue_key: str,
    repo_root: Path,
) -> dict[str, Any]:
    """Generate a failing test file via LLM (RED phase)."""
    from agentic_devtools.orchestration.llm.factory import ProviderFactory

    factory = ProviderFactory()
    provider = factory.get_provider("implementation", "work_on_issue")

    conventions = context.get("conventions", {})
    test_layout = conventions.get("test_layout", "1:1:1")

    system_prompt = (
        "You are a test-driven development assistant. Generate a Python test file "
        "that will initially FAIL (RED phase of TDD). The test should verify the "
        "expected behavior described in the checklist item.\n\n"
        f"Test layout convention: {test_layout}\n"
        "Follow pytest conventions. Include only the test code, no explanations.\n"
        'Respond with JSON: {"file_path": "relative/path.py", "content": "..."}'
    )

    user_prompt = f"Issue: {issue_key}\nChecklist item: {description}\nPlan context: {plan[:2000]}"

    async def _call():
        from agentic_devtools.orchestration.llm.types import LLMMessage

        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt),
        ]
        return await provider.complete(messages)

    token_usage: dict[str, int] = {}
    try:
        response = _run_async(_call())
        if response.usage:
            token_usage = {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
            }
        parsed = json.loads(response.text)
        if not isinstance(parsed, dict):
            return {"error": "LLM did not produce valid test file output", "token_usage": token_usage}
        file_path = parsed.get("file_path", "")
        content = parsed.get("content", "")

        if file_path and content:
            full_path = _resolve_output_path(repo_root, file_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            return {"path": file_path, "token_usage": token_usage}

        return {"error": "LLM did not produce valid test file output", "token_usage": token_usage}
    except Exception as exc:
        return {"error": str(exc), "token_usage": token_usage}


def _generate_implementation(
    description: str,
    plan: str,
    context: dict[str, Any],
    test_path: str,
    issue_key: str,
    repo_root: Path,
) -> dict[str, Any]:
    """Generate implementation code via LLM (GREEN phase)."""
    from agentic_devtools.orchestration.llm.factory import ProviderFactory

    factory = ProviderFactory()
    provider = factory.get_provider("implementation", "work_on_issue")

    # Read the test file for context
    test_content = ""
    if test_path:
        test_full_path = repo_root / test_path
        if test_full_path.exists():
            test_content = read_file_content(test_full_path)

    system_prompt = (
        "You are an implementation assistant. Generate Python source code that makes "
        "the provided failing test pass (GREEN phase of TDD). Write minimal code "
        "to satisfy the test assertions.\n\n"
        'Respond with JSON: {"file_path": "relative/path.py", "content": "..."}'
    )

    user_prompt = (
        f"Issue: {issue_key}\n"
        f"Checklist item: {description}\n"
        f"Test file ({test_path}):\n{test_content}\n"
        f"Plan context: {plan[:1000]}"
    )

    async def _call():
        from agentic_devtools.orchestration.llm.types import LLMMessage

        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt),
        ]
        return await provider.complete(messages)

    token_usage: dict[str, int] = {}
    try:
        response = _run_async(_call())
        if response.usage:
            token_usage = {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
            }
        parsed = json.loads(response.text)
        if not isinstance(parsed, dict):
            return {"error": "LLM did not produce valid implementation output", "token_usage": token_usage}
        file_path = parsed.get("file_path", "")
        content = parsed.get("content", "")

        if file_path and content:
            full_path = _resolve_output_path(repo_root, file_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            return {"path": file_path, "token_usage": token_usage}

        return {"error": "LLM did not produce valid implementation output", "token_usage": token_usage}
    except Exception as exc:
        return {"error": str(exc), "token_usage": token_usage}
