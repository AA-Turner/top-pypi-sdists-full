"""ask the server to email a failed job's owner, once per distinct failure."""

from __future__ import annotations
import hashlib
import json
import socket
from pathlib import Path


# -- telling the person -------------------------------------------------------
# The funnel above reaches US. Nothing in it reaches the researcher, and a
# detached worker has no terminal to print to: an overnight import that stops at
# 03:00 is invisible until somebody thinks to reopen the import screen. So a
# terminal FAILURE also asks the server to email the account that approved it.
#
# Everything here is best-effort in exactly the sense the funnel is: it runs
# after the job record is already durable, it never raises, and a job that could
# not be reported is still a job whose own record says what happened.


#: How long the worker will wait on the report before giving up and exiting.
#: A failed import is already finished; nobody is served by a worker that lingers
#: on a slow network to send a courtesy email.
_REPORT_TIMEOUT_S = 10.0


def _job_context_name(job: dict) -> str | None:
    """The saved CLI context this job's lane authenticates with.

    The two lanes spell it differently because they pin different things: the
    transcript lane pins a whole account identity it re-verifies before
    uploading, the folder lane pins a destination scope. Neither shape is worth
    changing for a notification, so this reads both.
    """
    payload = job.get("payload")
    if not isinstance(payload, dict):
        return None
    account = payload.get("account")
    if isinstance(account, dict) and isinstance(account.get("context"), str):
        return account["context"]
    return payload.get("context") if isinstance(payload.get("context"), str) else None


def _report_digest(job: dict) -> str:
    """What makes one failure DIFFERENT from the one already reported.

    The attempt number alone is not enough: a job relaunched by recovery can
    fail before `run_worker` ever increments it, and mailing on every one of
    those turns a crash loop into an inbox. The error text alone is not enough
    either: a person who fixed the cause, resumed, and hit the same wall must
    hear about it again.
    """
    canonical = json.dumps(
        [job.get("attempt"), str(job.get("state") or ""), str(job.get("error") or "")],
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode()).hexdigest()[:32]


def _post_failure_report(context: str, job_id: str, body: dict) -> None:
    """One authenticated POST. Its own function so tests can replace it.

    A TRANSPORT rather than a `Client`: this needs one request, and a client
    would also stand up an outbox and a journal for a process that is on its way
    out. Imported inside the call for the reason `_telemetry` documents -- a
    worker replays from a PINNED source tree, and a module that is missing there
    must cost a notification, never the import.
    """
    from ....sdk.settings.settings import resolve
    from ....sdk.delivery.transport.transport import Transport

    transport = Transport(
        resolve(context=context), timeout=_REPORT_TIMEOUT_S, surface="cli", attribution="backfill"
    )
    try:
        transport.post(f"/v1/import-jobs/{job_id}/failure", body, idempotent=True)
    finally:
        transport.close()


def _report_failure(folder: Path, job: dict, *, failure_kind: str | None = None) -> bool:
    """Ask the server to email this job's owner. Never raises.

    Returns whether a report was SENT -- False covers "already reported",
    "no saved context to authenticate with", and every transport failure.

    THE DEDUPE LIVES HERE, not on the server, because this is the only side that
    holds a durable per-job record and can therefore tell a new failure from the
    same failure being observed twice. The server keeps a short in-process window
    as a backstop; it cannot survive a restart and is not the authority.
    """
    try:
        reason = str(job.get("error") or "").strip()
        if not reason:
            return False
        digest = _report_digest(job)
        if job.get("notified") == digest:
            return False
        context = _job_context_name(job)
        if context is None:
            return False
        done, total = None, None
        try:
            from ..progress import counts

            done, total = counts(job)
        except Exception:
            pass
        _post_failure_report(context, job["id"], {
            "kind": str(job.get("kind") or ""),
            "outcome": "launch_failed" if failure_kind in ("reclaim", "launch") else "failed",
            "reason": _clean(reason),
            "failure_kind": failure_kind,
            "attempt": job.get("attempt"),
            "units_done": done,
            "units_total": total,
            "duration_seconds": _elapsed_seconds(job),
            # The researcher's own machine name, so an email that arrives on a
            # phone says WHICH laptop to go back to. Bounded and re-validated
            # server-side; a host that cannot name itself simply omits it.
            "machine": _machine_label(),
        })
    except Exception:
        return False  # a notification must never become the failure
    # Stamped only after the POST returns: a report that never left must be
    # retried by the next observation, not suppressed by this one.
    try:
        _update(folder, notified=digest)
    except Exception:
        pass
    return True


def _machine_label() -> str | None:
    try:
        name = socket.gethostname().split(".")[0].strip()
    except Exception:
        return None
    return name[:64] if name else None
from probe.cli.imports.jobs.store import _clean, _update  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.telemetry import _elapsed_seconds  # noqa: E402 -- pieces need each other; the front door loads this one first
