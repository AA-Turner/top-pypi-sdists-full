from __future__ import annotations

from typing import Any

from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

VALID_COMPONENT_TYPES = {
    "dropdown",
    "checkboxes",
    "radio",
    "toggle",
    "slider",
    "input",
    "textarea",
}


async def interaction_ask(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    introduction = args.get("introduction", "")
    if introduction and not isinstance(introduction, str):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation", message="'introduction' must be a string."
            ),
        )

    questions = args.get("questions")
    if not isinstance(questions, list) or not questions:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation", message="'questions' must be a non-empty list."
            ),
        )

    for idx, q in enumerate(questions):
        if not isinstance(q, dict):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Question at index {idx} must be an object.",
                ),
            )

        for field in ("id", "prompt", "component_type"):
            if field not in q or not isinstance(q[field], str):
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="validation",
                        message=f"Question {idx}: '{field}' must be a string.",
                    ),
                )

        if q["component_type"] not in VALID_COMPONENT_TYPES:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Question {idx}: 'component_type' must be one of {VALID_COMPONENT_TYPES}.",
                ),
            )

        if "options" in q:
            if not isinstance(q["options"], list):
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="validation",
                        message=f"Question {idx}: 'options' must be a list.",
                    ),
                )
            if (
                q["component_type"] in {"dropdown", "checkboxes", "radio"}
                and not q["options"]
            ):
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="validation",
                        message=f"Question {idx}: 'options' cannot be empty for {q['component_type']}.",
                    ),
                )
            for opt_idx, opt in enumerate(q["options"]):
                if not isinstance(opt, str):
                    return ToolResult(
                        success=False,
                        error=ToolError(
                            error_type="validation",
                            message=f"Question {idx}: option {opt_idx} must be a string.",
                        ),
                    )

        if "allow_other" in q and not isinstance(q["allow_other"], bool):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Question {idx}: 'allow_other' must be a boolean.",
                ),
            )

    from matrx_connect.context.data_types import QuestionnaireDisplayData

    frontend_payload = QuestionnaireDisplayData(
        introduction=introduction,
        questions=questions,
    )

    emitter = ctx.emitter
    if emitter is not None:
        try:
            if hasattr(emitter, "send_tool_event"):
                await emitter.send_tool_event(
                    {
                        "event": "tool_step",
                        "call_id": ctx.call_id,
                        "tool_name": ctx.tool_name,
                        "message": "Displaying questionnaire",
                        "data": frontend_payload.model_dump(),
                    }
                )
            else:
                await emitter.send_data(frontend_payload)

            return ToolResult(
                success=True,
                output={
                    "message": "Questionnaire sent to frontend successfully.",
                    "questions_sent": len(questions),
                },
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=ToolError.from_exception(
                    e,
                    error_type="execution", message=f"Failed to send questionnaire: {e}"
                ),
            )
    else:
        return ToolResult(
            success=True,
            output={
                "message": "Questionnaire validated (no stream handler available).",
                "data": frontend_payload.model_dump(),
            },
        )
