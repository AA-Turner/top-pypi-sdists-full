"""Send one telemetry batch: a client hands it to the Probe service (`telemetry.send`, plan D10); only a
process the service runs (`handoff.is_under_service`) POSTs it itself."""

from __future__ import annotations
from probe.analytics import core as core
from probe.foundation.tls.tls import ssl_context


def _post_batch(entries: list[dict]) -> None:
    """The core's wire shape over the SDK's TLS trust (plan item (l)), from a process under the
    service; anywhere else the service takes the batch (starting where none runs), and a batch
    it cannot take is dropped: telemetry never opens a connection from a client. Each entry gets
    a `uuid` first, so a batch resent after a lost answer counts once."""
    from probe.foundation.service_api import handoff

    handoff.stamp(entries)
    if handoff.is_under_service():
        core.post_batch(entries, context=ssl_context())
        return
    handoff.telemetry(entries)
