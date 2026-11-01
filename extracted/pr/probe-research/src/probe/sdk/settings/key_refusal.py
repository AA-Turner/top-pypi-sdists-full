"""When Probe refused a CREDENTIAL, as opposed to one request (daemon v2).

Stdlib only and tiny: the CLI prints `KEY_REFUSED_LINE`, the daemon's tools read it and
`probe.daemon.session.probe_api` applies the same rule, with no imports between them (the CLI
module takes ~0.6s to load).

Rule: a 401 is always the credential. A 403 is the credential only when its message says
so (team or membership gone, revoked, expired); a missing SCOPE or role, or one
workspace's lock, is an ordinary refusal and the key still works.
"""

from __future__ import annotations

import re

#: Printed under `error: ...` when the daemon ran the command (`PROBE_DAEMON_SESSION`
#: set) and Probe refused the credential. The daemon reads this exact line as "my key
#: was refused", stops and hands the session back.
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
