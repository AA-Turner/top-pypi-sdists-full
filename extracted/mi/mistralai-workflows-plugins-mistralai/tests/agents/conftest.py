from typing import Any

from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.plugins.mistralai.connectors.constants import (
    MISTRALAI_PLUGIN_KEY,
    RESOLVED_CONNECTORS_KEY,
)


def make_context(bindings: list[dict[str, Any]] | None = None) -> WorkflowContext:
    """Create a WorkflowContext with interceptor-resolved bindings in the trusted channel."""
    trusted_extensions: dict[str, Any] = {}
    if bindings is not None:
        trusted_extensions[MISTRALAI_PLUGIN_KEY] = {RESOLVED_CONNECTORS_KEY: {"bindings": bindings}}
    return WorkflowContext(
        namespace="default",
        execution_id="test-exec-id",
        trusted_extensions=trusted_extensions,
    )
