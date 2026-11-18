"""What the server tells a team API key (`probe_svc_`), said plainly: a route a key may not call, the read
budget, and a key whose creator left the team (twin: app/accounts/auth/principals/scopes.py, D10)."""

from __future__ import annotations

import threading
import warnings
from collections.abc import Mapping

from ... import errors

#: Every answer to a key names whose view it reads (`creator` | `team-default`).
READS_AS_HEADER = "Probe-Key-Reads-As"
#: The key's creator left the team: it reads only what every member sees.
TEAM_DEFAULT = "team-default"
#: The server's 403 for a route a key may not call (scopes.py).
KEY_REFUSED_DETAIL = "this route is not available to service tokens"
#: The server's 429 code past a key's read budget (key_budget.py).
RATE_LIMITED_CODE = "rate_limited"


class KeyReadsAsTeamWarning(UserWarning):
    """A team API key whose creator left the team: it now reads only what every member can see."""


_warned = threading.Event()


def warn_if_team_default(headers: Mapping[str, str]) -> None:
    """Warn once per process when a key's answers read as the team default, never silently fewer rows."""
    if _warned.is_set() or (headers.get(READS_AS_HEADER) or "").strip().lower() != TEAM_DEFAULT:
        return
    _warned.set()
    warnings.warn(
        "this team API key's creator is no longer in the team, so it reads only what every member can see; "
        "an admin can make a new key under Settings -> Access",
        KeyReadsAsTeamWarning,
        stacklevel=2,
    )


def explain_key_refusal(error: errors.RosError, method: str, path: str) -> errors.RosError:
    """A key's 403 on a withheld route names the route and why; other errors pass through unchanged."""
    if error.status != 403 or error.detail != KEY_REFUSED_DETAIL:
        return error
    explained = errors.ScopeError(
        f"{method} {path} is not open to team API keys: a key reads the team's research data, but never "
        "people, access controls, credentials, connector or workspace admin, or one person's own settings. "
        "Use a personal token for this call",
        status=403,
        detail=error.detail,
    )
    explained.server_message = error.server_message
    explained.retry_after = error.retry_after
    return explained
