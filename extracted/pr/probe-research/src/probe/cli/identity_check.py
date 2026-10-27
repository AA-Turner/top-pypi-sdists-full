"""Identity first: every credential on this machine belongs to the account signed in (plan clean-uninstall-reinstall R-T4).

Before an install's workers start (the service restart, the daemon), read
who is signed in (`/v1/me` with the saved API token), then hold every other
credential this machine uses to it:

    the daemon key     (`companion_token`) of another account or team, or one
                       the server refuses: released (revoked on the server
                       where it still answers), dropped, and approved afresh
                       when daemon mode is in use and someone can approve it;
                       an earlier sign-in's key stayed and the daemon wrote to
                       the OLD team (R5: `save_context` merges, and a key was
                       minted only when none was held)
    env overrides      `PROBE_TOKEN`, `PROBE_MCP_TOKEN`, `PROBE_INGEST_TOKEN`,
                       `PROBE_DAEMON_KEY`, the agents' capture-token variables
                       and `PROBE_BASE_URL` outrank the sign-in (R7): one that
                       disagrees with it makes the install INCOMPLETE, the
                       variable named -- a warning alone let a stale shell
                       profile win every time. (`PROBE_SERVICE_TOKEN` is no
                       person's sign-in: `/v1/me` refuses it by design, and it
                       never outranks one.)

`drain_before_switch` sends what is queued under the credential about to be
replaced BEFORE the device-authorization exchange, which releases this
device's old credentials on the server (`app/auth/device_router.py`, during
the exchange): queued writes are stamped with the credential that queued them,
and were stranded (R8).
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

#: The SDK's and the daemon's own credential variables (`sdk/config.resolve`,
#: `daemon/model.py`).
TOKEN_VARIABLES = ("PROBE_TOKEN", "PROBE_MCP_TOKEN", "PROBE_INGEST_TOKEN",
                   "PROBE_DAEMON_KEY")
BASE_URL_VARIABLE = "PROBE_BASE_URL"
#: How long a switch waits for the old credential's queue to send.
DRAIN_BUDGET_S = 60.0


@dataclass
class IdentityReport:
    #: `(customer_id, user_id)` of the sign-in, or None (not signed in, unreachable).
    account: tuple[str, str] | None = None
    email: str | None = None
    lines: list[str] = field(default_factory=list)
    #: What keeps the install INCOMPLETE, the variable or credential named.
    problems: list[str] = field(default_factory=list)


def override_variables() -> tuple[str, ...]:
    """Every credential variable that outranks the sign-in, once each."""
    return tuple(dict.fromkeys((*TOKEN_VARIABLES, *capture_variables())))


def capture_variables() -> tuple[str, ...]:
    """Every coding agent's capture-token variable (the harness registry)."""
    try:
        from probe.harness.registry import get_registry

        return tuple(dict.fromkeys(h.capture.token_env for h in get_registry().all() if h.capture is not None))
    except Exception:  # noqa: BLE001
        return ("PROBE_INGEST_TOKEN", "PRBE_CODEX_TAP_TOKEN", "PROBE_PI_TAP_TOKEN", "PROBE_KIMI_TAP_TOKEN")


def whoami(token: str, base_url: str) -> tuple[str, dict | None]:
    """`(state, /v1/me)` for `token`: `ok`, `rejected` (401/403) or `unreachable`."""
    from probe.sdk import errors
    from probe.sdk.client import Client
    from probe.sdk.config import Settings
    from probe.sdk.surface import Surface

    try:
        with Client(settings=Settings(base_url=base_url, token=token), async_writes=False,
                    surface=Surface.CLI.value) as client:
            return "ok", client.me()
    except (errors.AuthError, errors.ScopeError):
        return "rejected", None
    except Exception:  # noqa: BLE001 -- offline, a server error: unknown, never "another account"
        return "unreachable", None


def _account(me: dict | None) -> tuple[str, str] | None:
    if not isinstance(me, dict):
        return None
    customer, user = me.get("customer_id"), me.get("user_id")
    return (str(customer), str(user)) if customer and user else None


def _same_url(a: str | None, b: str | None) -> bool:
    return (a or "").rstrip("/").lower() == (b or "").rstrip("/").lower()


def _daemon_in_use() -> bool:
    try:
        from probe.sdk import session_marker

        from . import setup as wizard

        return any(session_marker.recorder(source) == session_marker.RECORDER_DAEMON
                   for source in wizard.RECORDER_SOURCES)
    except Exception:  # noqa: BLE001
        return False


def _interactive() -> bool:
    try:
        from . import setup as wizard

        return wizard.interactive()
    except Exception:  # noqa: BLE001
        return False


#: `reconcile_once`'s answer for this process: a wizard pass over several
#: agents asks the server once.
_once: tuple[tuple, IdentityReport] | None = None


def _credentials_now() -> tuple:
    """What `reconcile` holds to the sign-in, as it is now: the saved
    credentials and the variables that outrank them."""
    try:
        from probe.sdk.config import load_context

        stored = load_context() or {}
    except Exception:  # noqa: BLE001
        stored = {}
    saved = tuple(str(stored.get(key) or "") for key in ("base_url", "token", "companion_token"))
    return saved + tuple(os.environ.get(name, "") for name in (*override_variables(), BASE_URL_VARIABLE))


def reconcile_once() -> IdentityReport:
    """`reconcile`, once per wizard pass over its agents: asked again only
    when the credentials changed since (a sign-in in between), and asking the
    server only when there is something to hold to the sign-in (a daemon key,
    a credential variable)."""
    global _once
    now = _credentials_now()
    if _once is None or _once[0] != now:
        report = reconcile(only_when_needed=True)
        _once = (_credentials_now(), report)
    return _once[1]


def reconcile(*, base_url: str | None = None, mint=None, network: bool = True,
              only_when_needed: bool = False) -> IdentityReport:
    """Hold every credential to the signed-in account (see the module
    docstring). `mint(base_url) -> lines` approves a new daemon key (default:
    the wizard's companion approval, only when someone can approve it).
    `only_when_needed`: no server call when no daemon key is saved and no
    credential variable is set (the sign-in itself is the wizard's to check).
    Never raises."""
    from probe.sdk.config import load_context, save_context

    report = IdentityReport()
    try:
        stored = load_context() or {}
    except Exception as exc:  # noqa: BLE001
        report.problems.append(f"the saved sign-in could not be read: {exc}")
        return report
    url = str(stored.get("base_url") or base_url or "")
    token = str(stored.get("token") or "")
    env_url = os.environ.get(BASE_URL_VARIABLE)
    if env_url and url and not _same_url(env_url, url):
        report.problems.append(
            f"{BASE_URL_VARIABLE}={env_url} in this environment outranks the sign-in's {url}: every `probe` "
            f"started from here talks to another server. Unset {BASE_URL_VARIABLE} (or sign in at {env_url})")
    url = url or env_url or base_url or ""
    if not token or not url:
        for name in override_variables():
            if os.environ.get(name):
                report.lines.append(f"{name} is set in this environment and there is no saved sign-in: it is the "
                                    "credential in use")
        return report
    if not network:
        return report
    if only_when_needed and not stored.get("companion_token") and not any(
            os.environ.get(name) for name in override_variables()):
        return report
    state, me = whoami(token, url)
    report.account, report.email = _account(me), (me or {}).get("email")
    if state == "rejected":
        report.problems.append("the saved sign-in is refused by the server: sign in again (`probe wizard` > Account)")
        return report
    if report.account is None:
        report.lines.append("who is signed in could not be read (offline?); the daemon key and the environment's "
                            "credentials were not checked")
        return report

    # Environment overrides that disagree with the sign-in.
    for name in override_variables():
        value = os.environ.get(name)
        if not value or value in {str(stored.get(k) or "") for k in
                                  ("token", "mcp_token", "ingest_token", "service_token", "companion_token")}:
            continue
        found, theirs = whoami(value, url)
        if found == "ok" and _account(theirs) == report.account:
            continue
        why = ("is refused by the server" if found == "rejected"
               else "could not be checked" if found == "unreachable"
               else f"belongs to {(theirs or {}).get('email') or 'another account'} "
                    f"(team {(_account(theirs) or ('?',))[0]})")
        if found == "unreachable":
            report.lines.append(f"{name} in this environment {why}; it outranks the sign-in")
            continue
        report.problems.append(
            f"{name} in this environment {why}, and it outranks the sign-in "
            f"({report.email or report.account[1]}, team {report.account[0]}): unset {name}")

    # The daemon key.
    key = str(stored.get("companion_token") or "")
    if key:
        found, theirs = whoami(key, url)
        if found == "ok" and _account(theirs) == report.account:
            return report
        if found == "unreachable":
            report.lines.append("the daemon key could not be checked (offline?)")
            return report
        owner = "refused by the server" if found == "rejected" else (
            f"of team {(_account(theirs) or ('?',))[0]}, not {report.account[0]}")
        if found == "ok":
            from . import setup as wizard

            report.lines.extend(wizard._revoke(key, base_url=url, what="the daemon key of the other account"))  # noqa: SLF001
        save_context({"companion_token": None})
        report.lines.append(f"dropped the daemon key: it was {owner}")
        if _daemon_in_use():
            minted = None
            if mint is not None:
                minted = mint(url)
            elif _interactive():
                from .main import _authorize_companion

                minted = _authorize_companion(url, open_browser=True)
            if minted is not None:
                report.lines.extend(minted)
            from . import setup as wizard

            if not wizard.companion_token_held():
                report.problems.append("daemon mode has no key for this account: approve one with `probe wizard` > "
                                       "Who records (Enter on the daemon)")
    return report


def drain_before_switch(*, seconds: float = DRAIN_BUDGET_S) -> list[str]:
    """Send what is queued under the credential about to be replaced, before
    the exchange that releases it (R8). Bounded by `seconds`; what is left is
    said, never dropped. Lines to show (none when nothing was queued)."""
    try:
        from probe.sdk import transport
        from probe.sdk.journal import Journal, drain

        journal = Journal()
        queued = sum(1 for queue in journal.namespaces() for _ in queue.pending())
        if not queued:
            return []
        with transport.deadline_scope(time.monotonic() + seconds):
            report = drain(journal, lock_timeout=5.0)
    except Exception as exc:  # noqa: BLE001 -- the sign-in goes on; what is queued stays queued
        return [f"! {type(exc).__name__} while sending what is queued under the current sign-in: {exc}"[:300]]
    lines = [f"sent {report.delivered} queued write(s) under the current sign-in before switching"]
    if report.remaining:
        lines.append(f"! {report.remaining} queued write(s) could not be sent yet; they stay queued and send once "
                     "this account is signed in again (`probe outbox status`)")
    return lines
