"""Per-run state for migrating legacy manual event publishes to the durable batch path.

This is event-migration state, not run configuration: it lives here, in the events layer,
and is held per run by the event interceptor, never recorded in the run's history.
"""

from contextvars import ContextVar


class _ManualPublishState:
    """The run's manual-publish migration counter, shared by the entrypoint and the signal and update handlers."""

    def __init__(self) -> None:
        self.legacy_manual_publish_count = 0


manual_publish_state_var: ContextVar[_ManualPublishState | None] = ContextVar("manual_publish_state", default=None)


def next_legacy_manual_publish_ordinal() -> int:
    """Number the run's manual publishes after a legacy history, starting at 0."""
    state = manual_publish_state_var.get()
    if state is None:
        raise RuntimeError("Manual event publishing requires the event interceptor")
    ordinal = state.legacy_manual_publish_count
    state.legacy_manual_publish_count += 1
    return ordinal
