"""Public inventory of telemetry surfaces."""

from .runtime import (
    APPROVAL_FAMILY,
    DELIVERY_FAMILY,
    EXECUTION_FAMILY,
    FAILURE_FAMILY,
    KRN_REQUIRED_EVENTS,
    LIFECYCLE_FAMILY,
    OPS_REQUIRED_EVENTS,
    SEC_REQUIRED_EVENTS,
)

TELEMETRY_FAMILIES = (
    LIFECYCLE_FAMILY,
    EXECUTION_FAMILY,
    APPROVAL_FAMILY,
    DELIVERY_FAMILY,
    FAILURE_FAMILY,
)

TELEMETRY_SURFACES = (
    "TelemetryMetadata",
    "LifecycleTelemetryEvent",
    "ExecutionTelemetryEvent",
    "ApprovalTelemetryEvent",
    "DeliveryTelemetryEvent",
    "FailureTelemetryEvent",
    "TelemetrySink",
    "emit_event",
    "emit_lifecycle_event",
    "emit_execution_event",
    "emit_approval_event",
    "emit_delivery_event",
    "emit_failure_event",
)

TELEMETRY_REQUIRED_EVENTS = {
    "KRN-1": KRN_REQUIRED_EVENTS,
    "SEC-1": SEC_REQUIRED_EVENTS,
    "OPS-2": OPS_REQUIRED_EVENTS,
}
