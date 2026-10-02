"""RFC 8628 device-authorization login for the CLI (browser-assisted).

The wizard's sign-in starts a short-lived request, opens the dashboard so a
signed-in human approves the exact scopes/team, then polls for the minted
``probe_pat``. Mirrors Probe Research ``/auth/device/*`` with mandatory S256 PKCE:
the browser never sees the token, and the PKCE verifier binds the exchange to
this CLI process. A one-time website install code pre-approves the same flow via
``/auth/device/install-token``; its resulting credentials use the same PKCE exchange.
"""

from __future__ import annotations

import base64
import hashlib
import re
import secrets
import socket
import subprocess
import sys
import time
import webbrowser
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import httpx

from .tls import ssl_context

_START_PATH = "/auth/device/code"
_INSTALL_PATH = "/auth/device/install-token"
_TOKEN_PATH = "/auth/device/token"
_SLOW_DOWN_BACKOFF = 5


@lru_cache(maxsize=1)
def hostname() -> str:
    """This machine's short name, for labelling a minted token.

    The token name is the only way to tell one client apart from another in the
    dashboard's client list, so default it to the host — three laptops otherwise
    show up as three identical rows and "revoke that one" is guesswork.

    PREFER THE NAME THE MACHINE WAS GIVEN over the one the network is calling it
    today. `socket.gethostname()` returns the TRANSIENT name, which on macOS
    follows the DHCP lease: joining a captive WiFi renamed a laptop to
    `visitor-10-59-125-182`, and that string is what got written into the
    dashboard as the machine's name — unrecognisable, and different again on the
    next network. `scutil --get LocalHostName` and `/etc/hostname` are the
    configured names, and they do not move. The transient name remains the
    fallback, so a platform offering neither is exactly as well off as before.
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
        # ValueError as well as OSError: `read_text` raises UnicodeDecodeError
        # (a ValueError) on a file that is not valid UTF-8, and letting that
        # escape would crash every CLI invocation on that host rather than
        # falling back to the transient name the way this function promises.
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


def _pkce_pair() -> tuple[str, str]:
    """A PKCE (verifier, S256 challenge) pair as unpadded base64url. The verifier
    is 43 chars from 32 random bytes, matching the API's challenge pattern."""
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
    install_code: str | None = None,
    open_browser: bool = True,
    on_prompt: Callable[[DevicePrompt], None] | None = None,
    client: httpx.Client | None = None,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
) -> dict:
    """Run the device flow and return the whole mint response (``TokenCreated``).

    This is the CLI's only way to mint a token: ``POST /v1/tokens`` is session-only
    on purpose ("a leaked token must not be able to mint more tokens"), so a human
    approves in the browser and the backend mints exactly one ``probe_pat`` here.

    The response carries ``token`` (the plaintext secret, shown exactly once) plus
    ``id``/``name``/``token_prefix``/``scopes`` — the identifying fields a caller
    needs in order to later revoke it without ever re-reading the secret.

    ``scopes=None`` requests read + write + delete — "full access" for the CLI means
    research data, so ``admin`` (browser-only team administration) is deliberately not
    in the default. Pass e.g. ``["read"]`` for a read-only token. Whatever is
    requested, the minted token can never exceed the scopes the approver's role
    confers. ``on_prompt`` receives the verification URI/code so the caller can print
    it; ``open_browser`` also launches it. ``token_name`` defaults to a
    hostname-labelled name so the token is identifiable in the dashboard's client list.

    ``install_code`` redeems the website's short-lived 10-character code instead
    of requesting another browser approval. The selected grants are still
    explicit, and the long-lived secrets return only through the PKCE exchange.
    """
    if install_code is not None and not re.fullmatch(r"[A-Z0-9]{10}", install_code):
        raise DeviceLoginError(
            "the sign-in code must contain exactly 10 uppercase letters or digits"
        )
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
        # Omitted entirely when None, so an older backend that has never heard of
        # grants still sees the request shape it has always seen. Sending
        # `grants: null` would fail validation there.
        if grants is not None:
            body["grants"] = grants
        if capture_source is not None:
            body["capture_source"] = capture_source
        if capture_sources is not None:
            body["capture_sources"] = capture_sources
        # Display-only context for the approval page — the CLI's claim about
        # the account this device currently holds, and whether this approval
        # is a guided install the page should wait out. Omitted when None so
        # older backends see the request shape they have always seen.
        if client_context is not None:
            body["client_context"] = client_context
        # THE MACHINE. This is what makes re-running setup land on the same
        # device row instead of minting another one, and what lets the exchange
        # detach this laptop's old credentials without revoking a PAT another
        # laptop is still using.
        #
        # Omitted when we could not persist an identity, and harmlessly ignored
        # by a backend that predates it (`DeviceAuthorizationStart` is not
        # extra="forbid"), so a new CLI keeps working against an old server.
        if device_instance_id is None:
            from .device_identity import device_instance_id as _resolve

            try:
                device_instance_id = _resolve()
            except Exception:  # noqa: BLE001 - identity is never a hard failure
                device_instance_id = None
        if device_instance_id is not None:
            body["device_instance_id"] = device_instance_id
        if install_code is not None:
            body["code"] = install_code
            start = http.post(_INSTALL_PATH, json=body)
        else:
            start = http.post(_START_PATH, json=body)
        accepted = (200, 201) if install_code is not None else (201,)
        if start.status_code not in accepted:
            raise _login_error(start, f"could not start device login ({start.status_code})")
        data = start.json()

        prompt = DevicePrompt(
            user_code=data["user_code"],
            verification_uri=data["verification_uri"],
            verification_uri_complete=data["verification_uri_complete"],
        )
        if install_code is None and on_prompt is not None:
            on_prompt(prompt)
        if install_code is None and open_browser:
            try:
                webbrowser.open(prompt.verification_uri_complete)
            except webbrowser.Error:
                pass  # headless: the printed URL is the fallback

        device_code = data["device_code"]
        interval = max(1, int(data.get("interval", 5)))
        deadline = monotonic() + int(data.get("expires_in", 600))

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

    The login path only ever needs the secret; use :func:`device_authorize` when you
    also need the token's id (e.g. to print what to revoke later).
    """
    return device_authorize(base_url, **kwargs)["token"]


def credentials_by_grant(minted: dict) -> dict[str, dict]:
    """Index a mint response by grant name.

    An older backend returns no ``grants`` array at all -- it only ever minted a
    PAT -- so synthesise the ``api`` entry from the top-level fields. That keeps
    the wizard's setup working against a backend that predates grants instead of
    silently finding nothing and reporting success.
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
