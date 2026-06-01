from contextvars import ContextVar, Token
from typing import Any, Tuple

from mistralai.workflows.models import PayloadWithContext, WorkflowContext


def reset_contextvar(var: ContextVar, token: Token) -> None:
    """
    Safely reset a ContextVar with a token.

    During workflow eviction (when a workflow is reset), Temporal execute
    some code in a different asyncio context than where the variable was set.
    This leads to a ValueError: 'Token was created in a different Context'.
    We catch and ignore this error as the context is being destroyed anyway.
    """
    try:
        var.reset(token)
    except ValueError:
        pass


def unwrap_contextual_result(result: Any) -> tuple[WorkflowContext | None, Any]:
    if isinstance(result, PayloadWithContext):
        return result.context, result.payload
    return None, result


def unwrap_contextual_args(args: Tuple[Any, ...]) -> Tuple[WorkflowContext | None, Tuple[Any, ...]]:
    workflow_context: WorkflowContext | None = None
    new_args_list = []

    for arg in args:
        if isinstance(arg, PayloadWithContext):
            workflow_context = arg.context
            new_args_list.append(arg.payload)
        else:
            new_args_list.append(arg)

    new_args = tuple(new_args_list)  # Convert back to a tuple

    return workflow_context, new_args
