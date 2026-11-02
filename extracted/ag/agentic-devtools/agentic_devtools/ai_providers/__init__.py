from typing import Any

from .agent_tasks_payload import (
    AGENT_TASKS_API_VERSION,
    AGENT_TASKS_ENDPOINT_TEMPLATE,
    AGENT_TASKS_HTTP_METHOD,
    AGENT_TASKS_VALIDATION_ORDER,
    REQUIRED_CUSTOM_AGENT,
    AgentTasksPayload,
    assert_headers_equal_redacted,
    build_agent_tasks_payload,
    get_agent_tasks_headers,
    redact_authorization_header,
    validate_agent_tasks_payload,
)
from .copilot import CopilotProvider, CopilotProviderConfig
from .dispatch_policy import (
    MAX_DISPATCHES_PER_SHA,
    DispatchInputError,
    DispatchLimitError,
    DispatchLimitReached,
    DispatchMarker,
    DispatchPolicyError,
    DispatchReconciliationRequired,
    DispatchStateError,
    ReconciliationRequired,
    build_dispatch_marker,
    claim_dispatch_ordinal,
    parse_dispatch_marker,
    reconcile_dispatch_state,
)
from .errors import ProviderError
from .http import DeliveryState, HttpResponse, HttpTransport, RequestsHttpTransport, TransportError
from .models import (
    AgentTaskSpec,
    FailureEnvelope,
    ModelRecord,
    TaskHandle,
    TaskRequest,
    TaskState,
)
from .priors import DEFAULT_PRIOR_SET, DEFAULT_PRIORS, PRIORS_VERSION, PriorSet, PriorValidationError, resolve_prior
from .promotion import DraftManager, PromotionManifest
from .provider import AIProvider, ModelDiscovery
from .serialization import (
    JsonMapping,
    JsonSequence,
    JsonValue,
    freeze_json,
    freeze_json_verbatim,
    redact_credentials,
    thaw_json,
)
from .tier_selector import (
    EXCLUDED_MODELS,
    TIER_LADDER,
    ModelCostError,
    ModelSelection,
    NoSelection,
    resolve_model_cost,
    select_model_for_dispatch,
)

__all__ = [
    "ProviderError",
    "AGENT_TASKS_API_VERSION",
    "AGENT_TASKS_ENDPOINT_TEMPLATE",
    "AGENT_TASKS_HTTP_METHOD",
    "AGENT_TASKS_VALIDATION_ORDER",
    "REQUIRED_CUSTOM_AGENT",
    "AgentTasksPayload",
    "assert_headers_equal_redacted",
    "build_agent_tasks_payload",
    "get_agent_tasks_headers",
    "redact_authorization_header",
    "validate_agent_tasks_payload",
    "ModelRecord",
    "TaskRequest",
    "AgentTaskSpec",
    "TaskHandle",
    "TaskState",
    "FailureEnvelope",
    "AIProvider",
    "ModelDiscovery",
    "CopilotProvider",
    "CopilotProviderConfig",
    "HttpTransport",
    "HttpResponse",
    "DeliveryState",
    "TransportError",
    "RequestsHttpTransport",
    "DEFAULT_MODEL_MATRIX",
    "DEFAULT_AVAILABILITY_MATRIX",
    "ProbeObservation",
    "ProbeOutcome",
    "ProbeResult",
    "build_default_matrix",
    "canonicalize_matrix",
    "classify_probe_response",
    "classify_response",
    "curate_availability_matrix",
    "infer_validation_surface",
    "render_canonical_body",
    "render_adoption_note",
    "assert_task_snapshot_invariant",
    "validate_task_snapshot",
    "freeze_json",
    "freeze_json_verbatim",
    "thaw_json",
    "redact_credentials",
    "JsonMapping",
    "JsonSequence",
    "JsonValue",
    "DraftManager",
    "PromotionManifest",
    "TIER_LADDER",
    "EXCLUDED_MODELS",
    "ModelCostError",
    "ModelSelection",
    "NoSelection",
    "resolve_model_cost",
    "select_model_for_dispatch",
    "DEFAULT_PRIOR_SET",
    "DEFAULT_PRIORS",
    "PRIORS_VERSION",
    "PriorSet",
    "PriorValidationError",
    "resolve_prior",
    "DispatchInputError",
    "DispatchLimitError",
    "DispatchLimitReached",
    "DispatchMarker",
    "DispatchPolicyError",
    "DispatchReconciliationRequired",
    "DispatchStateError",
    "MAX_DISPATCHES_PER_SHA",
    "ReconciliationRequired",
    "build_dispatch_marker",
    "claim_dispatch_ordinal",
    "parse_dispatch_marker",
    "reconcile_dispatch_state",
]

# `.availability` is also a runnable script
# (``python -m agentic_devtools.ai_providers.availability``). Importing it
# eagerly above would populate ``sys.modules`` with the module before runpy
# executes it as ``__main__``, which triggers a ``RuntimeWarning`` (module
# "found in sys.modules ... may result in unpredictable behaviour") and
# re-runs its module-level initialization a second time. Deferring the
# import to first attribute access via PEP 562 avoids that double-import
# while keeping these names available as ``agentic_devtools.ai_providers.*``.
_AVAILABILITY_EXPORTS = frozenset(
    {
        "DEFAULT_AVAILABILITY_MATRIX",
        "DEFAULT_MODEL_MATRIX",
        "ProbeObservation",
        "ProbeOutcome",
        "ProbeResult",
        "assert_task_snapshot_invariant",
        "build_default_matrix",
        "canonicalize_matrix",
        "classify_probe_response",
        "classify_response",
        "curate_availability_matrix",
        "infer_validation_surface",
        "render_adoption_note",
        "render_canonical_body",
        "validate_task_snapshot",
    }
)


def __getattr__(name: str) -> Any:
    if name in _AVAILABILITY_EXPORTS:
        from . import availability

        return getattr(availability, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(__all__) | set(globals()))
