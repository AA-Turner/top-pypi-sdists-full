"""PR review graph nodes — LangGraph node implementations.

Provides ``review_file_node`` which uses ``ExecutionContext`` for LLM calls
and tool invocations during automated PR file review.
"""

from __future__ import annotations

from typing import Any, cast

from agentic_devtools.orchestration.execution.context import ExecutionContext
from agentic_devtools.orchestration.execution.types import JSONValue


def review_file_node(state: dict[str, Any], *, context: ExecutionContext) -> dict[str, Any]:
    """Review a single file using LLM reasoning and tool invocation.

    Uses ``context.reasoning.invoke()`` to get a structured review verdict,
    validates the response, and invokes the appropriate tool action.

    Args:
        state: Current graph state containing file info and review context.
        context: Injected execution context with reasoning, tools, and tracer.

    Returns:
        Updated state dict with review outcome.
    """
    from agentic_devtools.orchestration.schemas._validation import (
        SchemaValidationError,
        validate_llm_output,
    )
    from agentic_devtools.orchestration.tools.review_bindings import (
        APPROVE_FILE,
        REQUEST_CHANGES,
        REQUEST_CHANGES_WITH_SUGGESTION,
    )

    # Prefer the explicit file-path key; fall back to file_key for backward
    # compatibility.  Note: current_file_key is a slug+hash in the v2 review
    # pipeline and is NOT a valid repo path — callers should populate
    # current_file_path with the actual repo-relative path instead.
    file_path = state.get("current_file_path")
    file_key = state.get("current_file_key", "")
    if not file_path and isinstance(file_key, str) and ("/" in file_key or "\\" in file_key):
        file_path = file_key
    file_diff = state.get("current_file_diff", "")
    review_prompt = state.get("review_prompt", "")

    if not isinstance(file_path, str) or not file_path.strip():
        return {
            "status": "failed",
            "error": {
                "type": "missing_input",
                "message": "No current_file_path or current_file_key in state",
            },
        }

    # Build the prompt
    prompt = review_prompt or f"Review the following file diff and provide a verdict:\n\n{file_diff}"

    # Call the LLM for a structured verdict
    from agentic_devtools.orchestration.schemas.review import ReviewVerdict

    response = context.reasoning.invoke(
        prompt,
        output_schema=ReviewVerdict,
    )

    # Validate the LLM output against the schema
    try:
        verdict = validate_llm_output(ReviewVerdict, response.raw_text)
    except SchemaValidationError as exc:
        return {
            "status": "failed",
            "error": {
                "type": "schema_validation_failed",
                "message": str(exc),
            },
        }

    # Determine which tool to invoke based on the verdict
    outcome = verdict.outcome if hasattr(verdict, "outcome") else "approve"

    summary = verdict.summary if hasattr(verdict, "summary") else ""
    tool_kwargs: dict[str, JSONValue] = {"file_path": file_path}

    tool_name = ""
    if outcome == "approve":
        tool_kwargs["summary"] = summary
        tool_name = APPROVE_FILE
    elif outcome == "request-changes":
        tool_kwargs["summary"] = summary
        tool_kwargs["suggestions"] = []
        tool_name = REQUEST_CHANGES
    elif outcome == "request-changes-with-suggestion":
        tool_kwargs["summary"] = summary
        raw_suggestions = verdict.suggestions if hasattr(verdict, "suggestions") else []
        # Convert Pydantic model instances to plain dicts so jsonschema validation
        # in ToolExecutor passes (it expects {"type": "object"} items, not BaseModel).
        serialized_suggestions: list[dict[str, Any]] = [
            s.model_dump(exclude_none=True) if hasattr(s, "model_dump") else cast(dict[str, Any], s)
            for s in raw_suggestions
        ]
        tool_kwargs["suggestions"] = cast(JSONValue, serialized_suggestions)
        tool_name = REQUEST_CHANGES_WITH_SUGGESTION
    else:
        return {
            "status": "failed",
            "error": {
                "type": "unrecognized_outcome",
                "message": f"Unrecognized LLM outcome: {outcome!r}",
            },
        }

    try:
        tool_result = context.tools.invoke(tool_name, node_name="review_file_node", **tool_kwargs)
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "failed",
            "error": {
                "type": "tool_invoke_exception",
                "tool": tool_name,
                "message": str(exc),
            },
        }

    if isinstance(tool_result, dict) and tool_result.get("success") is False:
        error_message = tool_result.get("error_message") or tool_result.get("error")
        return {
            "status": "failed",
            "error": {
                "type": "tool_invoke_failed",
                "tool": tool_name,
                "message": str(error_message or "Tool returned success=false"),
            },
        }

    # Surface the submission_item so the orchestration caller can submit it
    # through the durable engine (the tool binding only builds the item; it
    # does not persist it to the v2 ledger or post it to the PR).
    submission_item = None
    if isinstance(tool_result, dict):
        submission_item = tool_result.get("submission_item")
        output = tool_result.get("output")
        if submission_item is None and isinstance(output, dict):
            submission_item = output.get("submission_item")

    completed: dict[str, Any] = {
        "status": "completed",
        "current_file_outcome": outcome,
        "current_file_summary": summary,
    }
    if submission_item is not None:
        completed["current_file_submission_item"] = submission_item
    return completed
