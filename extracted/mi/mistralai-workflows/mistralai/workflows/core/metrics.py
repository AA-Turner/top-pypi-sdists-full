"""Worker metrics.

The workflows collector drops names outside the `mistral_` prefix and attribute keys outside its
`keep_keys` allowlist, so both are constrained here.
"""

from enum import StrEnum

from opentelemetry import metrics
from opentelemetry.metrics import Counter

_METER_NAME = "mistralai.workflows"

_counters: dict[str, Counter] = {}


class EventRouteFallbackReason(StrEnum):
    """Why a v2-configured worker published over v1 instead."""

    ROUTE_UNAVAILABLE = "route_unavailable"
    TOKEN_SERVICE_UNAVAILABLE = "token_service_unavailable"
    TOKEN_REQUIRED = "token_required"


def _get_counter(name: str, description: str) -> Counter:
    # Created on first use so the meter resolves after the worker has installed its provider.
    counter = _counters.get(name)
    if counter is None:
        counter = metrics.get_meter(_METER_NAME).create_counter(name, description=description)
        _counters[name] = counter
    return counter


def record_event_route_v1_fallback(reason: EventRouteFallbackReason) -> None:
    _get_counter(
        "mistral_workflows_event_route_v1_fallback",
        "Times a v2-configured worker fell back to the v1 event route.",
    ).add(1, {"reason": reason.value})
