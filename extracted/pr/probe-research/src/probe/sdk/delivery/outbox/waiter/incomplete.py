"""DeliveryIncomplete: `finish()` (or `probe run end`) could not confirm a run's writes reached the
server. Raised only for loss or a definite stall, never for slowness; the writes stay on disk."""

from __future__ import annotations

from probe.sdk import errors
from probe.sdk.delivery.outbox.waiter.outcome import WaitOutcome, WaitResult

#: What to do next, per outcome (the message's last sentence).
_NEXT = {
    WaitOutcome.REFUSED: "see `probe outbox status`; fix the cause, then `probe outbox retry`",
    WaitOutcome.LOGIN_REFUSED: "sign in again (`probe login`); the writes go out on their own then",
    WaitOutcome.PAUSED: "`probe outbox resume` sends them",
    WaitOutcome.STALLED: "they are retried every hour; `probe outbox retry` tries them now",
    WaitOutcome.UNREACHABLE: "the background worker keeps trying for a day; `probe outbox status` shows them",
    WaitOutcome.WORKER_CRASH_LOOP: "see the outbox's drainer.log; `probe outbox drain` sends them in the foreground",
    WaitOutcome.NO_SENDER: "no Probe service could start here; `probe outbox drain` sends them once one can",
    WaitOutcome.KEY_NOT_HANDED: (
        "before this container or job exits, run `PROBE_TOKEN=<that key> probe outbox drain` with "
        "PROBE_OUTBOX_DIR={outbox} (`probe sync` for runs recorded offline)"
    ),
    WaitOutcome.OLD_WORKER: "an older probe-research is sending this outbox; upgrade it or stop it",
    WaitOutcome.NEEDS_NEWER_SERVICE: "{newer_service_advice}; they wait, in order, until then",
    WaitOutcome.CLOSE_UNRECORDED: "free space next to the outbox (`probe outbox status`); the server closes the run when it goes quiet",
    WaitOutcome.DATA_REFUSED: "`probe run get {run}` lists them under `ingest.refusals`",
}

_WHY = {
    WaitOutcome.REFUSED: "the server refused {failed} of them for good",
    WaitOutcome.LOGIN_REFUSED: "the server refused this machine's credential",
    WaitOutcome.PAUSED: "the outbox is paused",
    WaitOutcome.STALLED: "{held} kept failing and were set aside",
    WaitOutcome.UNREACHABLE: "the server could not be reached for {minutes} minutes",
    WaitOutcome.WORKER_CRASH_LOOP: "the background worker kept dying without delivering",
    WaitOutcome.NO_SENDER: "the Probe service could not be reached to send them",
    WaitOutcome.KEY_NOT_HANDED: (
        "the API key passed in code never reached the Probe service (it could not start), so nothing here can send them"
    ),
    WaitOutcome.OLD_WORKER: "an older worker ({holder}) holds the outbox and did not step aside",
    WaitOutcome.NEEDS_NEWER_SERVICE: (
        "a write of this run is of a newer outbox format than the Probe service here ({service_version}) reads"
    ),
    WaitOutcome.CLOSE_UNRECORDED: "the close itself could not be sent nor saved to the outbox",
}


class DeliveryIncomplete(errors.RosError):
    """Some of a run's writes did not reach the server. ``result`` says where they stand:
    ``outcome`` (why), ``pending``, ``held``, ``failed``. Nothing is lost: they stay on disk."""

    def __init__(self, result: WaitResult, *, minutes: int = 10) -> None:
        self.result = result
        self.outcome = result.outcome
        self.run_ref = result.run_ref
        super().__init__(describe(result, minutes=minutes))


def describe(result: WaitResult, *, minutes: int = 10) -> str:
    """One plain sentence a researcher can act on."""
    if result.outcome == WaitOutcome.DATA_REFUSED:
        return _describe_refusals(result)
    left = result.pending + result.held + result.failed
    why = _WHY.get(result.outcome, str(result.outcome)).format(
        failed=result.failed, held=result.held, minutes=minutes, holder=result.holder or "?",
        service_version=result.service_version or "unknown version",
    )
    error = f" (first error: {result.first_error[:200]})" if result.first_error else ""
    return (
        f"run {result.run_ref}: {left} write(s) not delivered: {why}{error}. "
        f"They are kept on disk; "
        f"{_NEXT.get(result.outcome, 'see `probe outbox status`').format(outbox=result.outbox or '<the outbox>', newer_service_advice=_get_newer_service_advice())}."
    )


def _describe_refusals(result: WaitResult) -> str:
    """Which kinds of refusal the server recorded, in its own words (I15d)."""
    points = sum(int(r.get("points") or 0) for r in result.refusals)
    reasons = []
    for refusal in result.refusals:
        text = (refusal.get("message") or {}).get("text") or str(refusal.get("kind") or "refused")
        if text not in reasons:
            reasons.append(text)
    return (
        f"run {result.run_ref}: the server accepted {points:,} point(s) and then did not store them "
        f"({'; '.join(reasons)}). {_NEXT[WaitOutcome.DATA_REFUSED].format(run=result.run_ref)}."
    )


def _get_newer_service_advice() -> str:
    """How to get a Probe service that reads newer writes: the CLI's update where this machine has a
    CLI install; on a pip-only box, the package in the environment that started the older service."""
    try:
        from probe.foundation.service_api.start import get_cli_python

        has_cli = get_cli_python() is not None
    except Exception:  # noqa: BLE001 -- unknown: the CLI's advice
        has_cli = True
    if has_cli:
        return "update Probe on this machine (`probe update`)"
    return "upgrade probe-research in the environment that started the older Probe service (`pip install -U probe-research`)"
