"""RFC 8628 device-authorization login for the CLI (browser-assisted).

The wizard's sign-in starts a short-lived request, opens the dashboard so a
signed-in human approves the exact scopes/team, then polls for the minted
``probe_pat``. Mirrors Probe Research ``/auth/device/*`` with mandatory S256 PKCE:
the browser never sees the token, and the PKCE verifier binds the exchange to
this CLI process. Every sign-in asks in the browser: the website's one-time install
codes are retired (install redesign R1).
"""

from __future__ import annotations

import base64
import hashlib
import os
import secrets
import socket
import subprocess
import sys
import time
import webbrowser
from collections.abc import Callable
from contextlib import AbstractContextManager, nullcontext
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import httpx

from ...foundation.tls.tls import ssl_context

_START_PATH = "/auth/device/code"
_TOKEN_PATH = "/auth/device/token"
_SLOW_DOWN_BACKOFF = 5
#: Set (by the Probe service, for a fenced caller's command, D25): the sign-in link is printed and
#: no browser opened, as on a machine without one.
NO_BROWSER_ENV = "PROBE_NO_BROWSER"


@lru_cache(maxsize=1)
def hostname() -> str:
    """This machine's short name, for labelling a minted token.

    Defaults the token name to the host so the dashboard's client list can tell laptops apart.

    PREFER THE CONFIGURED NAME over the network's: `socket.gethostname()` is TRANSIENT on
    macOS (a captive WiFi made a laptop `visitor-10-59-125-182`, written into the
    dashboard). `scutil --get LocalHostName` and `/etc/hostname` do not move; the
    transient name stays the fallback.
    """
    for candidate in _configured_hostnames():
        name = candidate.split(".")[0].strip()
        if name and name.lower() != "not set":
            return name
    try:
        name = socket.gethostname().split(".")[0].strip()  # drop .local / domain
    except OSError:
        name = ""
    return name or "unknown-host"


def _configured_hostnames() -> list[str]:
    """Stable machine names this platform can offer, best first."""
    if sys.platform == "darwin":
        try:
            done = subprocess.run(  # noqa: S603 - fixed argv, no shell
                ["/usr/sbin/scutil", "--get", "LocalHostName"],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return []
        return [done.stdout.strip()] if done.returncode == 0 else []
    try:
        # ValueError too: invalid UTF-8 raises UnicodeDecodeError, which would crash every CLI run on that host.
        return [Path("/etc/hostname").read_text(encoding="utf-8").strip()]
    except (OSError, ValueError):
        return []


class DeviceLoginError(Exception):
    """The device flow could not complete (denied, expired, or a transport error)."""


class OnboardingRequired(DeviceLoginError):
    """The browser account must finish website onboarding before CLI setup."""

    def __init__(self, message: str, *, onboarding_url: str | None = None):
        super().__init__(message)
        self.onboarding_url = onboarding_url


def _login_error(resp: httpx.Response, fallback: str) -> DeviceLoginError:
    code, description = _error_code(resp)
    if code == "onboarding_required":
        detail = resp.json().get("detail", {})
        return OnboardingRequired(
            description or fallback, onboarding_url=detail.get("onboarding_url")
        )
    return DeviceLoginError(description or fallback)


@dataclass
class DevicePrompt:
    """What to show the user while they approve in the browser."""

    user_code: str
    verification_uri: str
    verification_uri_complete: str
    #: Seconds the approval stays open, as the server said (RFC 8628).
    expires_in: int | None = None


#: Told of every browser approval before polling, beside ``on_prompt``: `probe wizard
#: --json` reports it as an event (`probe.core.events`). One process-wide slot, not
#: a context variable, so approvals started on other threads reach it.
_prompt_observer: Callable[[DevicePrompt], None] | None = None


def set_prompt_observer(
    observer: Callable[[DevicePrompt], None] | None,
) -> Callable[[DevicePrompt], None] | None:
    """Install ``observer`` (None removes it) and return the previous one."""
    global _prompt_observer
    previous, _prompt_observer = _prompt_observer, observer
    return previous


#: Wraps the approval wait (token poll, prompt to answer). `probe wizard --json` makes it
#: the one stretch SIGINT can end (`probe.core.events.interruptible`). Process-wide, like the observer.
_approval_wait: Callable[[], AbstractContextManager[None]] = nullcontext


def set_approval_wait(
    wrapper: Callable[[], AbstractContextManager[None]] | None,
) -> Callable[[], AbstractContextManager[None]]:
    """Install ``wrapper`` around every approval's token poll (None: nothing); return the previous one."""
    global _approval_wait
    previous, _approval_wait = _approval_wait, wrapper or nullcontext
    return previous


def _pkce_pair() -> tuple[str, str]:
    """A PKCE (verifier, S256 challenge) pair, unpadded base64url; the verifier is 43 chars from 32 random bytes (the API's pattern)."""
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def _error_code(resp: httpx.Response) -> tuple[str | None, str | None]:
    """Pull ``{detail: {error, error_description}}`` off an error response."""
    try:
        detail = resp.json().get("detail", {})
    except ValueError:
        return None, None
    if isinstance(detail, dict):
        return detail.get("error"), detail.get("error_description")
    return None, str(detail)


def device_authorize(
    base_url: str,
    *,
    scopes: list[str] | None = None,
    grants: list[str] | None = None,
    capture_source: str | None = None,
    capture_sources: list[str] | None = None,
    client_context: dict | None = None,
    token_name: str | None = None,
    device_instance_id: str | None = None,
    bind_device: bool = True,
    open_browser: bool = True,
    on_prompt: Callable[[DevicePrompt], None] | None = None,
    before_exchange: Callable[[], None] | None = None,
    client: httpx.Client | None = None,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
) -> dict:
    """Run the device flow and return the whole mint response (``TokenCreated``).

    ``POST /v1/tokens`` is session-only on purpose (a leaked token must not mint more), so
    a human approves in the browser and the backend mints one ``probe_pat``. Narrow
    exception: an installation's own ``api`` credential may mint that machine's daemon key
    and an agent's capture key (``/v1/client-installations/current/*-credential``,
    ``setup.mint_from_sign_in``).

    The response carries ``token`` (plaintext, shown once) plus ``id``/``name``/
    ``token_prefix``/``scopes``, enough to revoke it later.

    ``scopes=None`` requests read + write + delete; ``admin`` (browser-only) is not in the
    default. Pass e.g. ``["read"]`` for read-only. A token never exceeds the approver's
    role. ``on_prompt`` receives the verification URI/code to print; ``open_browser`` also
    launches it. ``token_name`` defaults to a hostname-labelled name.

    ``before_exchange`` runs once the browser is open and before the first poll, inside the
    approval wait: the poll that succeeds IS the exchange, so work that must precede it runs
    while the person approves instead of delaying the browser (a sign-in's queued writes).

    ``bind_device=False`` sends no ``device_instance_id``: the token is for elsewhere
    (`probe token create` for a pod) and must not take THIS machine's slot. The exchange
    releases a device's credentials when the request names one, so naming this laptop
    revoked its own login (a customer's Mac, 2026-10-23).
    """
    if token_name is None:
        token_name = f"Probe Research CLI · {hostname()}"
    verifier, challenge = _pkce_pair()
    owns_client = client is None
    http = client or httpx.Client(base_url=base_url, timeout=30.0, verify=ssl_context())
    try:
        body: dict = {
            "token_name": token_name,
            "scopes": scopes,
            "code_challenge": challenge,
        }
        # Omitted when None: an older backend would fail validation on `grants: null`.
        if grants is not None:
            body["grants"] = grants
        if capture_source is not None:
            body["capture_source"] = capture_source
        if capture_sources is not None:
            body["capture_sources"] = capture_sources
        # Display-only approval-page context (account this device holds; guided install). Omitted when None for older backends.
        if client_context is not None:
            body["client_context"] = client_context
        # THE MACHINE: re-running setup lands on the same device row, and the exchange can
        # detach this laptop's old credentials without revoking another laptop's PAT.
        # Omitted when no identity persists; old backends ignore it
        # (`DeviceAuthorizationStart` is not extra="forbid").
        if not bind_device:
            device_instance_id = None
        elif device_instance_id is None:
            from .device_identity import device_instance_id as _resolve

            try:
                device_instance_id = _resolve()
            except Exception:  # noqa: BLE001 - identity is never a hard failure
                device_instance_id = None
        if device_instance_id is not None:
            body["device_instance_id"] = device_instance_id
        start = http.post(_START_PATH, json=body)
        if start.status_code != 201:
            raise _login_error(start, f"could not start device login ({start.status_code})")
        data = start.json()

        expires_in = int(data.get("expires_in", 600))
        prompt = DevicePrompt(
            user_code=data["user_code"],
            verification_uri=data["verification_uri"],
            verification_uri_complete=data["verification_uri_complete"],
            expires_in=expires_in,
        )
        if _prompt_observer is not None:
            _prompt_observer(prompt)
        if on_prompt is not None:
            on_prompt(prompt)
        if open_browser and not os.environ.get(NO_BROWSER_ENV):
            try:
                webbrowser.open(prompt.verification_uri_complete)
            except webbrowser.Error:
                pass  # headless: the printed URL is the fallback

        device_code = data["device_code"]
        interval = max(1, int(data.get("interval", 5)))
        deadline = monotonic() + expires_in

        with _approval_wait():
            if before_exchange is not None:
                before_exchange()
            while monotonic() < deadline:
                resp = http.post(
                    _TOKEN_PATH,
                    json={"device_code": device_code, "code_verifier": verifier},
                )
                if resp.status_code == 200:
                    return resp.json()
                code, desc = _error_code(resp)
                if code == "slow_down":
                    interval += _SLOW_DOWN_BACKOFF
                elif code != "authorization_pending":
                    raise _login_error(resp, f"device login failed ({code or resp.status_code})")
                sleep(interval)

        raise DeviceLoginError("device authorization expired before it was approved")
    except httpx.HTTPError as exc:
        raise DeviceLoginError(f"could not reach {base_url}: {exc}") from exc
    finally:
        if owns_client:
            http.close()


def device_login(base_url: str, **kwargs) -> str:
    """Run the device flow and return just the minted ``probe_pat`` secret.

    Use :func:`device_authorize` when you also need the token's id (e.g. to revoke it later).
    """
    return device_authorize(base_url, **kwargs)["token"]


def credentials_by_grant(minted: dict) -> dict[str, dict]:
    """Index a mint response by grant name.

    An older backend returns no ``grants`` (it only minted a PAT), so the ``api`` entry is
    synthesised from the top-level fields, keeping setup working there.
    """
    entries = minted.get("grants") or []
    by_grant = {entry["grant"]: entry for entry in entries if entry.get("grant")}
    if not by_grant and minted.get("token"):
        by_grant["api"] = {
            "grant": "api",
            "token": minted["token"],
            "token_id": minted.get("id"),
        }
    return by_grant


def capture_credentials_by_source(minted: dict) -> dict[str, dict]:
    """Index capture credentials without collapsing a dual-agent approval."""
    entries = minted.get("grants") or []
    captures = [entry for entry in entries if entry.get("grant") == "capture"]
    return {str(entry.get("capture_source") or "claude_code"): entry for entry in captures}
