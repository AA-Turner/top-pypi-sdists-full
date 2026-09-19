"""HTTP client for the login console API - the only network surface of `plato vault`.

The CLI is a THIN client over the console's ``/api/logins`` routes. Every safety
gate lives inside those routes (the exit ban check, the 2FA widening, the
single-worker launch lock and its fail-closed in-flight check), so going over
HTTP inherits all of them for free. Never talk to 1Password or Chronos-launch directly: a second
process launching bakes sits outside the console's in-process guard.

The console has no auth boundary of its own (it is Tailscale-gated), so the only
credential here is the base URL.
"""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import quote

import httpx

ENV_VAR = "PLATO_VAULT_URL"

# Named in the "unset" error only as a hint. There is deliberately NO default:
# guessing a host would silently talk to the wrong console.
DEFAULT_CONSOLE_HINT = "http://jerry-dev-machine:8003"

# The console's own browser_mode values (logins.py: POST bake browser_mode
# Literal), keyed by the CLI's operator-facing names.
MODES: dict[str, str] = {
    "on-vm": "chrome",
    "browser": "browserbase",
    "vm-to-browser": "browserbase_via_vm",
}


class VaultConsoleError(Exception):
    """Anything that stops a vault command. Exit code 1 unless specialised."""

    exit_code = 1


class ConsoleUnreachable(VaultConsoleError):
    """The console did not answer (DNS, connect, timeout, 5xx)."""

    exit_code = 2


# The console waits up to 120 s for Chronos to accept a launch (expd chronos_client),
# so the bake POST must outlast that or a slow-but-successful launch reads as a failure.
BAKE_TIMEOUT_S = 150.0


class BakeOutcomeUnknown(ConsoleUnreachable):
    """The bake POST got no answer. The launch may still have gone through."""


class GateRefused(VaultConsoleError):
    """The console refused on purpose: 409 a bake is already running, or a 403
    gate (today the only 403 is the human-bake-only list, which is empty)."""

    exit_code = 3


class NotFound(VaultConsoleError):
    """No such login/account."""

    exit_code = 4


def resolve_base_url(override: str | None = None) -> str:
    """The console base URL, from --console-url or the environment."""
    base = override or os.environ.get(ENV_VAR)
    if not base:
        raise VaultConsoleError(
            f"{ENV_VAR} is not set. Point it at the login console backend, for example {DEFAULT_CONSOLE_HINT}"
        )
    return base.rstrip("/")


def translate_mode(mode: str | None) -> str | None:
    """CLI mode name -> the console's ``browser_mode``. Both spellings accepted."""
    if not mode:
        return None
    if mode in MODES:
        return MODES[mode]
    if mode in MODES.values():
        return mode
    accepted = ", ".join(list(MODES) + list(MODES.values()))
    raise VaultConsoleError(f"unknown mode {mode!r}; accepted: {accepted}")


class VaultConsoleClient:
    """One httpx client over the login console. Never logs a request body."""

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout)

    def __enter__(self) -> VaultConsoleClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            resp = self._client.request(method, path, **kwargs)
        except httpx.HTTPError as e:
            raise ConsoleUnreachable(f"cannot reach the login console at {self.base_url}: {e}") from e
        if resp.status_code in (403, 409):
            raise GateRefused(f"{resp.status_code} refused by the console: {_detail(resp)}")
        if resp.status_code == 404:
            raise NotFound(_detail(resp))
        if resp.status_code >= 500:
            raise ConsoleUnreachable(f"{resp.status_code} from the login console: {_detail(resp)}")
        if resp.status_code >= 400:
            raise VaultConsoleError(f"{resp.status_code} from the login console: {_detail(resp)}")
        # Anything left that is not a JSON 2xx is not the console answering: a
        # 3xx (httpx does not follow redirects), or an HTML body from a base URL
        # pointed at the frontend. Typed, so a driver gets the documented exit
        # code and a JSON error object instead of a JSONDecodeError traceback.
        try:
            if resp.is_success:
                return resp.json()
        except ValueError:
            pass
        raise ConsoleUnreachable(
            f"{self.base_url}{path} did not answer with JSON "
            f"({resp.status_code} {resp.headers.get('content-type') or 'no content-type'})"
        )

    def list_logins(self, include_archived: bool = False) -> dict:
        """GET /api/logins - inventory grouped by login_key."""
        return self._request("GET", "/api/logins", params={"include_archived": include_archived})

    def get_login_detail(self, login_key: str, account: str) -> dict:
        """GET /api/logins/{login_key}/{account} - one login record."""
        return self._request("GET", f"/api/logins/{quote_segment(login_key)}/{quote_segment(account)}")

    def bake_login(self, login_key: str, account: str, browser_mode: str | None = None) -> dict:
        """POST /api/logins/{login_key}/{account}/bake - launches a REAL paid session."""
        params = {"browser_mode": browser_mode} if browser_mode else None
        try:
            return self._request(
                "POST",
                f"/api/logins/{quote_segment(login_key)}/{quote_segment(account)}/bake",
                params=params,
                timeout=BAKE_TIMEOUT_S,
            )
        except ConsoleUnreachable as e:
            if not isinstance(e.__cause__, httpx.HTTPError):
                raise
            raise BakeOutcomeUnknown(
                f"{e} - the bake MAY have launched anyway: run `plato vault status {login_key} --account {account}` "
                "before retrying (a retry while one is in flight is refused with 409)"
            ) from e

    def get_bake_live(self, login_key: str, account: str) -> dict:
        """GET /api/logins/{login_key}/{account}/bake-live - watch links for an in-flight bake."""
        return self._request("GET", f"/api/logins/{quote_segment(login_key)}/{quote_segment(account)}/bake-live")


def quote_segment(value: str) -> str:
    """One path segment. An id is data, never URL syntax: an unquoted `..` or `?`
    would silently retarget a bake at a different account or route."""
    return quote(str(value), safe="")


def _detail(resp: httpx.Response) -> str:
    """The console's ``detail`` string, falling back to the status line."""
    try:
        body = resp.json()
    except ValueError:
        return resp.reason_phrase or str(resp.status_code)
    if isinstance(body, dict) and body.get("detail"):
        return str(body["detail"])
    return resp.reason_phrase or str(resp.status_code)
