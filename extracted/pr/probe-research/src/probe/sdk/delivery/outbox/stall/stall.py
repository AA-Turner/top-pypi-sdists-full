"""Tell the server a run's delivery stalled (D5): `POST /v1/runs/{run_ref}/delivery-stalled`, once
per run and cause. Best-effort; an older server's 404/405/422 is the expected answer, not an error."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from typing import Any

from probe.foundation.compat.compat import StrEnum

log = logging.getLogger(__name__)

#: The whole report's budget: it rides the worker loop, between two passes.
_REPORT_SECONDS = 5.0
#: An older server that has no such route, or a body it does not take: nothing to tell.
_OLDER_SERVER = frozenset({404, 405, 422})
_ERROR_CHARS = 300


class DeliveryStallCause(StrEnum):
    """Why a run's writes could not all be delivered (the server's `delivery_stalled` notice)."""

    #: The server refused a write for good (4xx); it is in failed/.
    REFUSED = "refused"
    #: The server refused the credential; writes wait for a new sign-in.
    LOGIN_REFUSED = "login_refused"
    #: No progress for the stall window while a write kept failing; it was set aside to held/.
    STALLED = "stalled"
    #: The worker kept dying with no progress.
    WORKER_CRASH_LOOP = "worker_crash_loop"
    #: Nothing answered for the outage window.
    UNREACHABLE = "unreachable"


@dataclass(frozen=True)
class StallReport:
    """The body of one report, named as the server reads it."""

    cause: str
    held: int
    failed: int
    op_count: int
    first_error: str | None

    def to_body(self) -> dict:
        body = asdict(self)
        body["first_error"] = (self.first_error or "")[:_ERROR_CHARS] or None
        return body


def send_stall_report(run_ref: str, report: StallReport, context: dict | None) -> bool:
    """POST the report with the credential that queued the run's writes. True when the server
    took it or cannot (an older one): either way, no second try. Never raises."""
    try:
        return _post(run_ref, report, context)
    except Exception as exc:  # noqa: BLE001 -- a report never stops delivery
        log.debug("outbox: stall report for run %s not sent: %s", run_ref, type(exc).__name__)
        return False


def _post(run_ref: str, report: StallReport, context: dict | None) -> bool:
    import time

    from probe.sdk import errors
    from probe.sdk.delivery.ops.ops import delivery_client
    from probe.sdk.delivery.outbox.drain.credentials import _settings_for_op
    from probe.sdk.delivery.transport.deadlines import fresh_deadline_scope

    settings = _settings_for_op(context)
    if not (settings.token or settings.ingest_token):
        return False
    client: Any = delivery_client()(settings=settings, async_writes=False)
    try:
        with fresh_deadline_scope(time.monotonic() + _REPORT_SECONDS):
            client.transport.request(
                "POST", f"/v1/runs/{run_ref}/delivery-stalled", json_body=report.to_body()
            )
        return True
    except errors.RosError as exc:
        return getattr(exc, "status", None) in _OLDER_SERVER
    finally:
        try:
            client.close()
        except Exception:  # noqa: BLE001
            pass
