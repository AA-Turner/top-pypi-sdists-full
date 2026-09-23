"""What a worker can learn about itself from its own launch, and its platform session.

Two things live here, and they are together because both answer the same question --
*what was this container handed when it started?* -- from the same place:

* :func:`resolve_action_id` reads the launch environment and ``sys.argv``. No I/O, no
  session, no credentials.
* :func:`open_session` and :func:`get_session` turn the container's credentials into a
  ``matrice_common`` session, which is the handle every call in :mod:`.transport` needs.

**Everything here raises :class:`~.response.CallFailure` and nothing else.** This package
is an import leaf: ``matrice_common`` and the standard library only, never
``matrice_analytics.runtime``. ``matrice_common`` itself is imported *lazily*, inside the
function that needs it, so this module still imports cleanly in an image built without the
platform SDK -- the same thing ``PostProcessingConfigClient`` does, and the reason an
analytics-only container can import the package at all.
"""

from __future__ import annotations

import os
import re
import sys
import threading
from typing import Any, Mapping, Optional, Sequence

from .response import CallFailure

ENV_ACTION_ID = "MATRICE_ACTION_ID"
#: The bare name the Go services and the ENV_ID_ACTIONS images read. py_compute's
#: k8s lane has always emitted both; its docker lane emitted only the MATRICE_ one
#: for the ACTION_SCRIPTS class, so the id was reachable under one name in one lane
#: and the other name in the other. Accepting both here fixes every already-running
#: pod on its next SDK pull, without waiting on a py_compute redeploy.
ENV_ACTION_ID_BARE = "ACTION_ID"

#: A 24-hex Mongo ObjectId. Used to recognise an action id in ``sys.argv``.
_OBJECT_ID_RE = re.compile(r"^[0-9a-f]{24}$")

#: Guards :func:`get_session`'s memo. A module-level lock rather than a per-call one so that
#: two threads racing on a cold process build one session between them, not two.
_SESSION_LOCK = threading.Lock()

#: The process's session once :func:`get_session` has built it. ``None`` means "not yet",
#: never "could not" -- a failure raises and is not remembered, so the next caller retries.
_SESSION: Any = None


def resolve_action_id(
    env: Optional[Mapping[str, str]] = None, argv: Optional[Sequence[str]] = None
) -> Optional[str]:
    """The action record id for this worker, if it can be determined locally.

    Three sources, no I/O. ``$MATRICE_ACTION_ID`` first, because an operator setting it means it,
    then ``$ACTION_ID`` -- the bare name the Go services and the ENV_ID_ACTIONS images read, and the
    only one some py_compute launch paths emitted. Then ``sys.argv``: py_compute launches every
    action container as ``python3 <entrypoint>.py <action_record_id> <port>``, so the id is the
    first argument that looks like an ObjectId. Matching on shape rather than position keeps this
    from mistaking a port or a flag for an id.

    A malformed value in either env var falls through rather than erroring, so a truncated id does
    not mask a good one in argv.
    """
    environ = os.environ if env is None else env
    for name in (ENV_ACTION_ID, ENV_ACTION_ID_BARE):
        explicit = (environ.get(name) or "").strip()
        if _OBJECT_ID_RE.match(explicit.lower()):
            return explicit.lower()

    for arg in list(argv if argv is not None else sys.argv)[1:]:
        candidate = str(arg).strip().lower()
        if _OBJECT_ID_RE.match(candidate):
            return candidate
    return None


def open_session(what: str) -> Any:
    """A ``matrice_common`` session from the container's own credentials.

    Imported lazily, exactly as ``PostProcessingConfigClient.__init__`` does, so this module stays
    importable in an image with no platform SDK.

    Opens a **new** session every call. Callers that want one session for the life of the process
    use :func:`get_session` instead; this one stays uncached so that a caller who needs a session
    independent of anyone else's -- or a test that needs two -- can still get one.

    Credentials come from ``matrice_common.resolve_credentials``, which is the same three-tier
    order ``Session.__init__`` itself applies: an explicit argument, then the SDK's in-process
    registry, then the environment. Reading ``os.environ`` directly -- as this did until now --
    sees only the last of the three, so a container whose credentials were published to the
    registry by an SDK entry point was refused for want of variables it never needed to export.
    That is reachable rather than theoretical: ``Session`` used to copy explicit keys back into
    ``os.environ`` and deliberately stopped, because the environment is inherited by every
    subprocess and captured by most crash reporters.
    """
    try:
        from matrice_common import resolve_credentials
        from matrice_common.session import Session
    except Exception as exc:
        raise CallFailure(
            f"Cannot resolve {what}: matrice_common is not importable ({exc})."
        ) from exc

    access_key, secret_key = resolve_credentials()
    if not access_key or not secret_key:
        raise CallFailure(
            f"Cannot resolve {what}: no Matrice credentials in this process -- neither an SDK "
            f"entry point nor MATRICE_ACCESS_KEY_ID / MATRICE_SECRET_ACCESS_KEY supplied them."
        )
    try:
        return Session(
            access_key=access_key,
            secret_key=secret_key,
            account_number=os.getenv("MATRICE_ACCOUNT_NUMBER", "") or "",
        )
    except Exception as exc:
        raise CallFailure(f"Could not open a Matrice session to resolve {what}: {exc}") from exc


def get_session(what: str = "the platform session") -> Any:
    """The process's one ``matrice_common`` session, built on first use.

    Lazy because a container that never needs the platform should never pay for a session, and
    should not fail at import time for want of credentials it does not use. Memoised per
    *process*, not per caller: sessions are built from the same two environment variables
    wherever they are opened, so a second one is the same handle at the cost of another
    credential exchange.

    Thread-safe under the double-checked pattern -- the fast path is a bare read once the
    session exists, and the lock is taken only while the process is still cold.

    A failure is **not** memoised: ``_SESSION`` is assigned only on success, so a container that
    starts before its credentials are mounted recovers on the next call instead of being stuck
    with the first error for its lifetime.
    """
    global _SESSION

    if _SESSION is not None:
        return _SESSION

    with _SESSION_LOCK:
        # Re-checked inside the lock: another thread may have built it while this one waited.
        if _SESSION is None:
            _SESSION = open_session(what)
        return _SESSION
