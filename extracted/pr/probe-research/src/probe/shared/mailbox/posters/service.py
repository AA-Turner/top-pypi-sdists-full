"""post through the Probe service (`mailbox.post`) within a deadline, then stay quiet after a stall."""

from __future__ import annotations
import os
import time
from dataclasses import asdict
from probe.daemon.host import runctx


#: `PROBE_MAILBOX_SERVICE=off`: never post through the Probe service (a test,
#: a fault being chased).
SERVICE_ENV = "PROBE_MAILBOX_SERVICE"
#: A post through the service must be done by this long after it is sent...
POST_WAIT_S = 1.0
#: ...and its answer may come this much later; past both, the post is written
#: here (the service never writes past the deadline it was given).
POST_GRACE_S = 0.5
#: After a call that got no answer in time (a stalled service), this process
#: asks the service nothing for this long: the worker's loop must not pay the
#: wait on every message.
SERVICE_BREAK_S = 30.0
_service_quiet_until = 0.0
#: The run's own in the daemon host: one session's stalled call quiets only its own posts.
_quiet_until = runctx.Shared(globals(), "_service_quiet_until", float)


def service_call(method: str, params: dict, *, wait: float) -> "dict | None":
    """`method` on the Probe service, its answer within `wait` (plus the
    grace), or None: no service, an older one, a refusal (a sandbox), an
    error, or no answer in time. Never from the service itself (`rooted`)."""
    if getattr(_ROOTED, "root", None) is not None or os.environ.get(SERVICE_ENV) == "off" or os.name != "posix":
        return None
    if time.monotonic() < _quiet_until.get():
        return None
    try:
        from probe import __version__
        from probe.foundation import service_api as client
    except Exception:  # noqa: BLE001 -- the file is written here instead
        return None
    sent = None
    try:
        with client.Connection.open(0.3) as conn:
            conn.hello("cli", str(__version__))
            conn.sock.settimeout(wait + POST_GRACE_S)
            sent = time.monotonic()
            answer = conn.call(method, {**params, "deadline": time.time() + wait, "budget": wait})
    except client.ServiceError:
        return None  # an answer: it did nothing (busy, refused, an older service)
    except Exception:  # noqa: BLE001 -- no answer: written here, past the deadline
        if sent is not None:
            # It may have been at work: never write before its deadline passed.
            time.sleep(max(0.0, sent + wait + POST_GRACE_S - time.monotonic()))
            _quiet_until.set(time.monotonic() + SERVICE_BREAK_S)
        return None
    return answer if isinstance(answer, dict) else None


def post_via_service(msg: Message) -> bool:
    """Post `msg` through the Probe service (`mailbox.post`): True once its
    file is written. False and nothing written by the service, so the caller
    writes it here: no service answered, it refused, or its deadline passed
    (it never writes after that, and the caller only writes once it has)."""
    answer = service_call("mailbox.post", {"sid": msg.session, "state_dir": str(root().parent.absolute()),
                                            "message": asdict(msg)}, wait=POST_WAIT_S)
    return bool(answer and answer.get("posted"))
from probe.shared.mailbox.layout import _ROOTED, root  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.mailbox import Message  # noqa: E402 -- pieces need each other; the front door loads this one first
