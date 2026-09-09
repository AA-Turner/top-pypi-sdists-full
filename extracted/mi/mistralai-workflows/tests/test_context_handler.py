from unittest.mock import patch

from pydantic_core import to_json

from mistralai.workflows.core.temporal import context_handler_interceptor as chi
from mistralai.workflows.core.temporal.context_handler_interceptor import (
    _create_workflow_context_with_token,
    define_context,
)
from mistralai.workflows.models import PayloadWithContext, WorkflowContext


def test_create_workflow_context_with_token_preserves_trusted_extensions() -> None:
    """Signal/query/update handlers must keep interceptor-resolved bindings.

    ``_create_workflow_context_with_token`` rebuilds a fresh context and re-applies the
    live in-workflow context. Resolved connector bindings live in ``trusted_extensions``,
    so it must be preserved alongside ``extensions``/``execution_token``/``on_behalf_of``.
    """
    fresh = WorkflowContext(namespace="ns", execution_id="exec")
    live = WorkflowContext(
        namespace="ns",
        execution_id="exec",
        execution_token="tok",
        extensions={"mistralai": {"connectors": {"bindings": []}}},
        trusted_extensions={"mistralai": {"resolved_connectors": {"bindings": [{"connector_name": "github"}]}}},
        on_behalf_of=True,
    )

    with patch.object(chi, "create_workflow_context", return_value=fresh):
        with define_context(live):
            ctx = _create_workflow_context_with_token()

    assert ctx.trusted_extensions == live.trusted_extensions
    assert ctx.extensions == live.extensions
    assert ctx.execution_token == "tok"
    assert ctx.on_behalf_of is True


def test_outbound_context_replaces_pre_wrapped_untrusted_context() -> None:
    trusted = WorkflowContext(
        namespace="ns",
        execution_id="parent",
        trusted_extensions={"mistralai": {"resolved_connectors": {"bindings": []}}},
        on_behalf_of=False,
    )
    forged = PayloadWithContext(
        payload=to_json("input"),
        context=WorkflowContext(
            namespace="ns",
            execution_id="forged",
            trusted_extensions={"mistralai": {"forged": True}},
            on_behalf_of=True,
        ),
    )
    interceptor = chi.WorkflowContextWorkflowOutboundInterceptor.__new__(chi.WorkflowContextWorkflowOutboundInterceptor)

    with define_context(trusted):
        contextualized = interceptor._contextualize_args([forged])

    assert contextualized[0].context == trusted
