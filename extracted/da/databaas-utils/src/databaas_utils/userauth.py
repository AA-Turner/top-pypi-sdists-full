"""Interactive login as the user's own Zitadel identity.

Two flows, both ending in a refresh token: Authorization Code + PKCE through a
browser and a loopback redirect (interactive desktop use), and the OAuth2
Device Authorization Grant (SSH / headless, where nothing can reach a
loopback redirect). After the first login, ``auth_header()`` renews silently
from the refresh token; an interactive login only happens again once that
refresh token itself has expired or been revoked.

Mirrors the double-checked, expiry-aware caching in ``settings.py``'s
``OAuthClientCredentials``/``ServiceAccountKey``, but with two extra layers:
the cache is cross-process (the token store), and refreshing must be
serialised across processes too, since Zitadel rotates the refresh token on
every use.
"""

from __future__ import annotations

import base64
import contextlib
import hashlib
import http.server
import os
import secrets
import sys
import threading
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass, field
from typing import Any

import requests

from databaas_utils.errors import AuthenticationError, ConfigurationError
from databaas_utils.profiles import Profile, oidc_metadata
from databaas_utils.tokenstore import TokenStore, default_store, store_lock

TOKEN_TIMEOUT = 30
# Refresh this many seconds before actual expiry, matching settings.py.
_EXPIRY_MARGIN = 60
_DEVICE_DEFAULT_TIMEOUT = 300
_BROWSER_LOGIN_TIMEOUT = 300
_JWT_PARTS = 3
_HTTP_OK = 200


@dataclass
class UserLogin:
    """A ``TokenProvider`` backed by a user's own interactive Zitadel login.

    Built from a saved profile via ``UserLogin.from_profile`` — see
    ``LakehouseSettings.from_profile``, the normal entry point. ``auth_header()``
    serves a cached token, refreshes silently when a stored refresh token is
    still good, and — only when ``interactive`` is true — falls back to an
    interactive login when there is none.
    """

    issuer: str
    client_id: str
    project_id: str
    store_key: str
    interactive: bool = True
    # "auto" | "browser" | "device"
    flow: str = "auto"
    redirect_port: int = 0
    store: TokenStore = field(default_factory=default_store)

    _token: str | None = field(default=None, init=False, repr=False, compare=False)
    _expires_at: float = field(default=0.0, init=False, repr=False, compare=False)
    _lock: threading.Lock = field(
        default_factory=threading.Lock, init=False, repr=False, compare=False
    )

    @classmethod
    def from_profile(cls, profile: Profile, **overrides: Any) -> UserLogin:
        """Build from a saved :class:`~databaas_utils.Profile`.

        Args:
            profile: The profile to log in with.
            **overrides: Other fields, e.g. ``interactive=False``, ``flow="device"``
                or ``store=...``.
        """
        redirect_port = overrides.pop("redirect_port", profile.redirect_port)
        return cls(
            issuer=profile.issuer,
            client_id=profile.client_id,
            project_id=profile.project_id,
            store_key=f"{profile.name}@{profile.issuer}",
            redirect_port=redirect_port,
            **overrides,
        )

    @property
    def scope(self) -> str:
        """The OAuth scope requested at login."""
        scope = "openid profile email offline_access"
        if not self.project_id:
            # Zitadel puts the app's own project in the audience by default.
            return scope
        return f"{scope} urn:zitadel:iam:org:project:id:{self.project_id}:aud"

    def auth_header(self) -> str:
        """``Bearer <token>``, refreshing or logging in first if needed.

        Raises:
            AuthenticationError: If there is no usable session and
                ``interactive`` is false, or the login fails.
        """
        now = time.monotonic()
        if self._token and now < self._expires_at:
            return f"Bearer {self._token}"
        with self._lock:
            now = time.monotonic()
            if self._token and now < self._expires_at:
                return f"Bearer {self._token}"
            self._token, self._expires_at = self._ensure_token()
            return f"Bearer {self._token}"

    def invalidate(self) -> None:
        """Drop the in-memory access token only. Used by 401-retry logic."""
        with self._lock:
            self._token = None
            self._expires_at = 0.0

    def _ensure_token(self) -> tuple[str, float]:
        with store_lock(self.store_key):
            cached = self.store.load(self.store_key)
            wall_now = time.time()
            if (
                cached
                and cached.get("access_token")
                and cached.get("expires_at", 0.0) > wall_now + _EXPIRY_MARGIN
            ):
                return str(cached["access_token"]), self._monotonic_deadline(
                    float(cached["expires_at"])
                )
            refresh_token = cached.get("refresh_token") if cached else None
            if refresh_token:
                try:
                    return self._apply_bundle(self._refresh(refresh_token))
                except AuthenticationError:
                    pass  # refresh token expired/revoked — fall through to login
            if not self.interactive:
                profile_name = self.store_key.split("@", 1)[0]
                raise AuthenticationError(
                    f"no valid login for {self.store_key!r} — run "
                    f"`databaas login --profile {profile_name}`"
                )
            return self._apply_bundle(self._login())

    def _monotonic_deadline(self, wall_expires_at: float) -> float:
        return time.monotonic() + max(wall_expires_at - time.time(), 0.0)

    def _apply_bundle(self, bundle: dict[str, Any]) -> tuple[str, float]:
        """Persist a fetched token bundle and return (token, monotonic deadline).

        Caller holds the store lock. A bundle without a fresh refresh_token
        (some IdPs omit it when unrotated) keeps whatever was already stored.
        """
        access_token = str(bundle["access_token"])
        expires_in = float(bundle.get("expires_in", 300))
        wall_expires_at = time.time() + expires_in
        payload: dict[str, Any] = {
            "access_token": access_token,
            "expires_at": wall_expires_at,
        }
        refresh_token = bundle.get("refresh_token")
        if refresh_token:
            payload["refresh_token"] = refresh_token
        else:
            existing = self.store.load(self.store_key) or {}
            if existing.get("refresh_token"):
                payload["refresh_token"] = existing["refresh_token"]
        self.store.save(self.store_key, payload)
        return access_token, time.monotonic() + max(expires_in - _EXPIRY_MARGIN, 0.0)

    # -- explicit login/logout -----------------------------------------

    def login(self) -> None:
        """Run an interactive login now, regardless of any cached token."""
        with store_lock(self.store_key), self._lock:
            self._token, self._expires_at = self._apply_bundle(self._login())

    def logout(self) -> None:
        """Revoke the stored refresh token (best effort) and forget it."""
        with store_lock(self.store_key):
            cached = self.store.load(self.store_key)
            self.store.delete(self.store_key)
        self.invalidate()
        if cached and cached.get("refresh_token"):
            self._revoke(str(cached["refresh_token"]))

    def claims(self) -> dict[str, Any]:
        """Decode the current access token's payload, unverified.

        The server has already verified it; this is only for local display
        (``databaas whoami``), never for authorisation decisions.
        """
        import json

        self.auth_header()  # populates self._token
        assert self._token is not None
        parts = self._token.split(".")
        if len(parts) != _JWT_PARTS:
            return {}
        padded = parts[1] + "=" * (-len(parts[1]) % 4)
        return dict(json.loads(base64.urlsafe_b64decode(padded)))

    def userinfo(self) -> dict[str, Any]:
        """The signed-in user's profile (``email``, ``name``) from the issuer.

        Zitadel puts the email in the ID token and the userinfo response, not
        in the access token that :meth:`claims` decodes. Only for display;
        returns ``{}`` when the issuer has no userinfo endpoint or refuses.
        """
        endpoint = self._metadata().get("userinfo_endpoint")
        if not endpoint:
            return {}
        response = requests.get(
            endpoint,
            headers={"Authorization": self.auth_header()},
            timeout=TOKEN_TIMEOUT,
        )
        if response.status_code != _HTTP_OK:
            return {}
        return dict(response.json())

    # -- flows ------------------------------------------------------------

    def _metadata(self) -> dict[str, Any]:
        return oidc_metadata(self.issuer)

    def _login(self) -> dict[str, Any]:
        flow = self.flow
        if flow == "auto":
            flow = "device" if _headless() else "browser"
        if flow == "browser":
            return self._browser_login()
        if flow == "device":
            return self._device_login()
        raise ConfigurationError(f"unknown login flow {self.flow!r}")

    def _browser_login(self) -> dict[str, Any]:
        meta = self._metadata()
        verifier = _generate_verifier()
        challenge = _code_challenge(verifier)
        state = secrets.token_urlsafe(24)

        server = _RedirectServer(("127.0.0.1", self.redirect_port), "/callback")
        try:
            port = server.server_address[1]
            redirect_uri = f"http://127.0.0.1:{port}/callback"
            params = {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": redirect_uri,
                "scope": self.scope,
                "state": state,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
            }
            url = f"{meta['authorization_endpoint']}?{urllib.parse.urlencode(params)}"
            print(
                f"\nOpening your browser to sign in. If it does not open, visit:\n"
                f"    {url}\n",
                flush=True,
            )
            webbrowser.open(url)
            code = server.wait_for_code(
                expected_state=state, timeout=_BROWSER_LOGIN_TIMEOUT
            )
        finally:
            server.server_close()

        return self._token_request(
            {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": self.client_id,
                "code_verifier": verifier,
            },
            meta,
        )

    def _device_login(self) -> dict[str, Any]:
        meta = self._metadata()
        device_endpoint = meta.get("device_authorization_endpoint")
        if not device_endpoint:
            raise ConfigurationError(
                f"issuer {self.issuer!r} does not advertise a "
                "device_authorization_endpoint — device login is unavailable"
            )
        try:
            response = requests.post(
                device_endpoint,
                data={"client_id": self.client_id, "scope": self.scope},
                timeout=TOKEN_TIMEOUT,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise AuthenticationError(
                f"device-authorization request to {device_endpoint} failed: {exc}"
            ) from exc
        device = response.json()

        verification_uri = (
            device.get("verification_uri_complete") or device["verification_uri"]
        )
        print(f"\nTo sign in, visit:\n    {verification_uri}", flush=True)
        if not device.get("verification_uri_complete"):
            print(f"and enter code: {device['user_code']}", flush=True)

        interval = float(device.get("interval", 5))
        deadline = time.monotonic() + float(
            device.get("expires_in", _DEVICE_DEFAULT_TIMEOUT)
        )
        token_url = meta["token_endpoint"]
        while time.monotonic() < deadline:
            time.sleep(interval)
            try:
                response = requests.post(
                    token_url,
                    data={
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                        "device_code": device["device_code"],
                        "client_id": self.client_id,
                    },
                    timeout=TOKEN_TIMEOUT,
                )
            except requests.RequestException as exc:
                raise AuthenticationError(
                    f"device-code poll to {token_url} failed: {exc}"
                ) from exc
            payload = response.json()
            if response.status_code == _HTTP_OK:
                return dict(payload)
            error = payload.get("error")
            if error == "slow_down":
                interval += 5
                continue
            if error == "authorization_pending":
                continue
            raise AuthenticationError(f"device login failed: {error or payload}")
        raise AuthenticationError("device login timed out waiting for approval")

    def _refresh(self, refresh_token: str) -> dict[str, Any]:
        return self._token_request(
            {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "scope": self.scope,
            },
            self._metadata(),
        )

    def _token_request(
        self, data: dict[str, str], meta: dict[str, Any]
    ) -> dict[str, Any]:
        token_url = meta["token_endpoint"]
        try:
            response = requests.post(token_url, data=data, timeout=TOKEN_TIMEOUT)
        except requests.RequestException as exc:
            raise AuthenticationError(
                f"token request to {token_url} failed: {exc}"
            ) from exc
        if response.status_code != _HTTP_OK:
            raise AuthenticationError(
                f"token endpoint {token_url} returned HTTP {response.status_code}: "
                f"{response.text}"
            )
        return dict(response.json())

    def _revoke(self, refresh_token: str) -> None:
        with contextlib.suppress(requests.RequestException, ValueError):
            endpoint = self._metadata().get("revocation_endpoint")
            if not endpoint:
                return
            requests.post(
                endpoint,
                data={
                    "token": refresh_token,
                    "token_type_hint": "refresh_token",
                    "client_id": self.client_id,
                },
                timeout=TOKEN_TIMEOUT,
            )


def login(profile: str | None = None, **overrides: Any) -> UserLogin:
    """Log in interactively and return a live ``UserLogin`` bound to the profile.

    Convenience for notebooks: opens a browser (or prints a device code),
    persists the session, and returns something ``LakehouseSettings`` can be
    built from directly — or just call ``LakehouseSettings.from_profile()``
    afterwards, which reuses the cache this writes.

    Args:
        profile: Profile name; the default profile if omitted.
        **overrides: Passed to :meth:`UserLogin.from_profile`.

    Raises:
        ConfigurationError: If no such profile exists.
    """
    from databaas_utils.profiles import load_profile

    resolved = load_profile(profile)
    session = UserLogin.from_profile(resolved, **overrides)
    session.login()
    return session


def _headless() -> bool:
    """Best-effort guess at whether a browser can actually be opened here."""
    if os.environ.get("SSH_CONNECTION") and not os.environ.get("DISPLAY"):
        return True
    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
        return True
    return False


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        server: _RedirectServer = self.server  # type: ignore[assignment]
        if parsed.path != server.expected_path:
            self.send_response(404)
            self.end_headers()
            return
        server.result = params
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body>Signed in. You can close this tab.</body></html>")

    def log_message(self, *args: object) -> None:  # silence default stderr logging
        pass


class _RedirectServer(http.server.HTTPServer):
    def __init__(self, address: tuple[str, int], expected_path: str) -> None:
        super().__init__(address, _CallbackHandler)
        self.expected_path = expected_path
        self.result: dict[str, list[str]] | None = None

    def wait_for_code(self, *, expected_state: str, timeout: float) -> str:
        thread = threading.Thread(target=self.handle_request, daemon=True)
        thread.start()
        thread.join(timeout=timeout)
        if self.result is None:
            raise AuthenticationError("timed out waiting for the browser login redirect")
        if "error" in self.result:
            raise AuthenticationError(f"login was denied: {self.result['error'][0]}")
        if self.result.get("state", [None])[0] != expected_state:
            raise AuthenticationError("redirect state did not match — possible CSRF")
        codes = self.result.get("code")
        if not codes:
            raise AuthenticationError("redirect carried no authorization code")
        return codes[0]


def _generate_verifier() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
