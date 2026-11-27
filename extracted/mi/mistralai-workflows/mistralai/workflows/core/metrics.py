"""Worker metrics.

The workflows collector drops names outside the `mistral_` prefix and attribute keys outside its
`keep_keys` allowlist, so both are constrained here.
"""

from opentelemetry import metrics
from opentelemetry.metrics import Counter

_METER_NAME = "mistralai.workflows"

_counters: dict[str, Counter] = {}


def _get_counter(name: str, description: str) -> Counter:
    # Created on first use so the meter resolves after the worker has installed its provider.
    counter = _counters.get(name)
    if counter is None:
        counter = metrics.get_meter(_METER_NAME).create_counter(name, description=description)
        _counters[name] = counter
    return counter


def record_event_publish_retry(event_count: int) -> None:
    _get_counter(
        "mistral_workflows_event_publish_retries",
        "Workflow events whose publish attempt failed transiently and will be retried.",
    ).add(event_count)


def record_event_dropped_too_large() -> None:
    _get_counter(
        "mistral_workflows_events_dropped_too_large",
        "Workflow events dropped because the events API rejected them as too large.",
    ).add(1)
