"""Send one telemetry batch: hand it to the Probe service, else POST it."""

from __future__ import annotations
from probe.analytics import core as core
from probe.foundation.tls.tls import ssl_context


def _post_batch(entries: list[dict]) -> None:
    """The core's wire shape over the SDK's TLS trust, so telemetry and SDK writes agree
    on a proxy's certificate (plan item (l)).

    A running Probe service takes the batch when it can (plan Q5, `service_handoff.telemetry`;
    not with proxy or certificate settings, which its sender lacks), so an exiting training
    process never waits on PostHog; it answers within 0.25 s or this POSTs. Each entry gets a
    `uuid` first, so a batch both send counts once."""
    from probe.sdk.delivery.outbox.drainers import service_handoff

    service_handoff.stamp(entries)
    if service_handoff.telemetry(entries):
        return
    core.post_batch(entries, context=ssl_context())
