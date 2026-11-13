"""
Shared primitives for issuing a server-side statement cancellation on Stop.

Imports standard library only -- ``logging``, ``sys``, ``threading`` and ``typing`` -- because it
is imported from the vendored Redshift Data API dialect as well as from ``utils/athena_v4.py``,
and must not create an import cycle back into ``sql_engine`` or ``sqlutils``.
"""

import logging
import sys
import threading
from typing import Callable

logger = logging.getLogger(__name__)

# The bound on a cancellation attempt. Read as a module attribute at call time so a test
# can patch it.
CANCEL_TIMEOUT_SECONDS: float = 5.0


def run_bounded(fn: Callable[[], None], description: str) -> bool:
    """
    Run ``fn`` on a daemon thread, wait up to ``CANCEL_TIMEOUT_SECONDS``, and log the outcome.

    Never raises: a cancellation attempt must not replace the user's interrupt, and must not
    hold it for longer than the bound. A failure of ``fn``, a failure to start the thread, and
    expiry of the bound are all logged and swallowed.

    The one exception that may leave this function is a fresh ``KeyboardInterrupt`` delivered
    while waiting (a second Stop click); it propagates, and the abandoned worker is a daemon
    thread that finishes on its own or dies with the process.

    Args:
        fn: The cancellation call to make. Takes no arguments and its return value is ignored.
        description: What is being cancelled, for the log records.

    Returns:
        True when ``fn`` returned without raising inside the bound; False when it raised, could
        not be started, or had not finished when the bound expired. The return value is for
        reporting only -- callers must not change their control flow on a False, because the
        user's interrupt is what has to propagate either way.
    """
    completed = threading.Event()
    succeeded = False

    def _worker() -> None:
        nonlocal succeeded
        try:
            fn()
            succeeded = True
            logger.info("%s: cancellation request succeeded", description)
        except Exception:
            logger.warning("%s: cancellation request failed", description, exc_info=True)
        finally:
            completed.set()

    try:
        # `except Exception`, not `except BaseException`: the failure guarded here is
        # `RuntimeError: can't start new thread`. A KeyboardInterrupt arriving during start()
        # must propagate rather than be swallowed.
        threading.Thread(target=_worker, name="statement-cancel", daemon=True).start()
    except Exception:
        logger.warning("%s: could not start cancellation thread", description, exc_info=True)
        return False

    timeout = CANCEL_TIMEOUT_SECONDS
    if not completed.wait(timeout):
        logger.warning("%s: cancellation abandoned after %.1fs", description, timeout)
        return False

    # Read after the worker has set `completed`, so this is the worker's own outcome.
    return succeeded


def report_cancelled(target: str, accepted: bool) -> None:
    """
    Write one user-facing line about the cancellation to stderr, for display in the cell.

    ipykernel replaces ``sys.stderr`` with a stream that forwards to the notebook, so this
    reaches the cell output above the ``KeyboardInterrupt`` traceback. ``sys.stderr`` is read
    at call time rather than captured at import, because that replacement happens after import.

    "Accepted" means the service took the cancellation request, not that the statement has
    stopped -- a request can be accepted and still leave the query running, so the wording
    deliberately does not promise more than was observed.

    Never raises: a closed or broken stderr must not turn into a second failure on a path that
    is already unwinding an interrupt.

    Args:
        target: The service the cancellation was sent to, e.g. "Redshift" or "Athena".
        accepted: The outcome from ``run_bounded``.
    """
    if accepted:
        message = f"Query cancelled; cancel request accepted by {target}."
    else:
        message = (
            f"Stop requested. The cancel request to {target} did not complete; "
            f"the query may still be running."
        )
    try:
        print(message, file=sys.stderr)
    except Exception:
        logger.warning("could not write the cancellation notice to stderr", exc_info=True)
