"""`last-stop.json`: why the last Probe service in this machine's folder stopped, written by that service on its way out
(the machine service's and the SDK's delivery service's `stop`). A crash or a kill writes none, which is how the next
service and the update guard tell a stop on purpose from a crash. Moved here from `service/guard.py` (public: the SDK
writes it too); `guard` re-exports these names for one release (`load_last_stop` as its old `last_stop`)."""

from __future__ import annotations

import contextlib
import json
import os
import time

from . import paths

#: Why the last service stopped (`record_stop`, written by the service itself
#: on its way out): a crash or a kill writes none.
LAST_STOP_NAME = "last-stop.json"


def record_stop(reason: str, version: str) -> None:
    """The service is stopping on purpose (`server.stop`): say so, for a guard
    watching it. Never raises."""
    from . import procid

    target = paths.service_dir() / LAST_STOP_NAME
    temp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    try:
        with open(os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
            json.dump({"pid": os.getpid(), "start": procid.start_time(os.getpid()), "reason": reason,
                       "version": version, "at": time.time()}, handle)
        os.replace(temp, target)
    except OSError:
        pass
    finally:
        with contextlib.suppress(OSError):
            os.unlink(temp)


def load_last_stop() -> dict | None:
    try:
        data = json.loads((paths.service_dir() / LAST_STOP_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None
