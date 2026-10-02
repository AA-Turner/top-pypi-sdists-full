"""When Probe refused a CREDENTIAL, as opposed to one request (daemon v2).

Stdlib only, and tiny on purpose: the CLI (`probe.cli.main`) prints
`KEY_REFUSED_LINE` and the daemon's tools read it, and the daemon's own
direct calls (`probe.daemon.probe_api`) apply the same rule, so none of them
has to import the others (the CLI's module takes ~0.6s to load).

The rule: a 401 is always the credential. A 403 is the credential only when
its message says so (the key's team or membership is gone, it was revoked or
expired). A 403 that names a missing SCOPE or role, or one workspace's lock,
is an ordinary refusal of that one request: the key itself still works.
"""

from __future__ import annotations

import re

#: Printed under `error: ...` when the Probe daemon ran the command
#: (`PROBE_DAEMON_SESSION` is set) and Probe refused the credential itself. The
#: daemon reads this exact line as "my key was refused": it stops and hands the
#: session back.
KEY_REFUSED_LINE = "error: Probe refused this credential (key refused)"

#: The server's 403s that are about the credential, not the request
#: (`app/auth/dependencies.py`, `app/auth/onboarding.py`, the upload guard).
_CREDENTIAL_403 = re.compile(
    r"no active team|active team is required|not a member|team no longer exists|revoked|expired",
    re.IGNORECASE,
)


def credential_refused(status: int | None, message: str | None) -> bool:
    """Did Probe refuse the credential itself (not one request's scope)?"""
    if status == 401:
        return True
    return status == 403 and bool(_CREDENTIAL_403.search(message or ""))
