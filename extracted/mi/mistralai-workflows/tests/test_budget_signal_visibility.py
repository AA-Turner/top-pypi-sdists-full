from mistralai.workflows.core.execution.child_start_budget import ChildStartBudget
from mistralai.workflows.core.temporal.context_handler_interceptor import (
    WorkflowContextWorkflowInboundInterceptor,
)


class _StubNext:
    """Minimal next-interceptor stand-in so the inbound interceptor can be constructed
    outside a Temporal runtime."""

    def init(self, outbound) -> None:  # noqa: ANN001
        pass


def test_child_start_budget_shared_across_handlers():
    """The per-run budget must be a single shared instance across execute_workflow,
    handle_signal, and handle_update_handler. Each handler runs in its own asyncio
    task with a copied context, so a ContextVar set only in execute_workflow reads None
    in handle_signal (cursor[bot] r3840649037). The interceptor stores one budget per
    run and re-sets it into the ContextVar in every handler — verify the sharing."""
    interceptor = WorkflowContextWorkflowInboundInterceptor(_StubNext())

    first = interceptor._get_child_start_budget()
    second = interceptor._get_child_start_budget()

    assert isinstance(first, ChildStartBudget)
    assert first is second, "handle_signal/handle_update_handler must see the same budget as execute_workflow"
