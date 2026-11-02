"""drain the outbox, waiting out a dropped connection rather than failing the import."""

from __future__ import annotations
import os


class _TransientFlush(RuntimeError):
    """A drain that failed for a reason worth waiting out."""


#: Flush attempts before a foreground import stops waiting for the connection.
#: With the shared 2s->5min backoff the waits are 2+4+8+16+32+64 = just over two
#: minutes, which covers a laptop moving between networks. Longer than that
#: belongs to a background job, which has a supervisor; a foreground process
#: that sits for an hour is one nobody can tell from a hang.
FLUSH_ATTEMPTS = 7

#: Set to 1 to stop waiting at all. A known-offline machine wants that, and so
#: does a test suite pointed at an unroutable host -- otherwise every drain in
#: it is a genuine transient failure and every flush costs the full backoff.
FLUSH_ATTEMPTS_ENV = "PROBE_FLUSH_ATTEMPTS"


def flush_attempts() -> int:
    raw = os.environ.get(FLUSH_ATTEMPTS_ENV)
    if raw:
        try:
            return max(1, min(int(raw), 12))
        except ValueError:
            pass
    return FLUSH_ATTEMPTS


def _flush_uploads(client, *, retry_network: bool, report=None, progress=None,
                   on_delivered=None) -> None:
    """Drain the outbox, waiting out a dropped connection rather than failing.

    The outbox worker has had patient backoff since it was written. The import
    never used it: a Wi-Fi blip during the upload raised straight through
    `execute`, and a multi-hour run ended with "Backfill could not finish" even
    though every byte was already staged and resumable. Nothing was lost, but
    nothing continued either, and a person had to be there to re-run it.

    A background job keeps deferring to its own supervisor -- that worker owns
    the schedule and can wait far longer than a foreground process should. This
    only changes what happens when there is no supervisor.
    """
    from .....foundation.durable import durable
    from ...jobs.errors import RetryableJobError, is_retryable_error

    attempts = flush_attempts()

    if retry_network:
        def on_error(exc):
            if is_retryable_error(exc):
                raise RetryableJobError(
                    "The upload connection is unavailable. Completed uploads are saved."
                ) from None

        client.flush(on_error=on_error, on_delivered=on_delivered)
        return

    def attempt():
        """Drain once. Returns the report, or None when it could not run at all.

        `Client.flush` returns a DELIVERED COUNT and never raises on a network
        failure -- the drain classifies transport errors itself, parks the
        operation and returns -- so an exception-shaped retry around it waits
        for something that cannot happen. The drain's own report is the signal,
        and `stopped_transient` is the precise half of it: work merely left
        QUEUED is the normal state of an import with no drainer attached, and
        sleeping through the backoff for that would add two minutes to every
        ordinary partial run.
        """
        from .....sdk.delivery.outbox.drain.drain import drain

        try:
            return drain(client.journal, client_factory=client._outbox_client_factory(),
                         on_delivered=on_delivered)
        except Exception as exc:
            if not is_retryable_error(exc):
                raise
            return None

    def waiting(attempt_number, outcome):
        if attempt_number >= attempts or (outcome is not None
                                                and not outcome.stopped_transient):
            return
        message = "The upload connection is unavailable; waiting to retry. Completed uploads are saved."
        if progress:
            progress(message)
        elif report is not None:
            report.add(message)

    def settled(outcome) -> bool:
        """Anything but a transient stop. A parked queue is what we wait out."""
        return outcome is not None and not outcome.stopped_transient

    result = durable.retry(attempt, attempts=attempts, accept=settled, on_retry=waiting)
    if not settled(result) and report is not None:
        remaining = result.remaining if result is not None else len(client.journal.pending())
        report.add(
            f"{remaining:,} upload(s) are still queued after waiting for the connection. "
            "Re-running resumes them; nothing needs to be reviewed again."
        )
