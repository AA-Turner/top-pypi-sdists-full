"""
`seq login`'s sign-in on this machine: the session the platform signed in for you, kept per
platform address in the config directory's sequences/login.json (0600), refreshed through the platform when it is
about to lapse, never printed.

In one sentence: `seq login` saves {access token, refresh token, when it lapses, your email} under the platform's
address → a command with no key finds it (seq/_account.credential) → each request asks it for its token (`token()`),
which refreshes it - under a file lock, so two `seq` running at once refresh it once - when under two minutes are
left → `seq logout` ends it and removes it.

WHY a robot never uses it: it is you, not a robot. connect(), teleop() and planner() take a key alone (Transport's
`login` stays off for them), so a robot on a machine where someone ran `seq login` cannot act as that person.
WHY no token is ever printed or put in an error: whoever holds the refresh token is you until you sign out.
"""
from __future__ import annotations

import contextlib
import json
import os
import time
from pathlib import Path
from typing import Any, Iterator

import httpx

from sequence_ai.errors import AuthError, Unavailable, from_response


PERSON_REFUSAL = "this needs you signed in: seq login - a key cannot make keys, pay or change the account"
ENDED = "this sign-in has ended - run seq login"
EARLY_S = 120


def path() -> Path:
    """Where the sign-ins live: %APPDATA%\\sequences on Windows, else $XDG_CONFIG_HOME/sequences or ~/.config/sequences."""
    if os.name == "nt" and os.environ.get("APPDATA"):
        root = Path(os.environ["APPDATA"])
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return root / "sequences" / "login.json"


@contextlib.contextmanager
def _locked() -> Iterator[None]:
    """This machine's seq processes one at a time over the file (an flock on its .lock beside it)."""
    p = path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with contextlib.suppress(OSError):
        os.chmod(p.parent, 0o700)
    fd = os.open(f"{p}.lock", os.O_RDWR | os.O_CREAT, 0o600)
    try:
        try:
            import fcntl

            fcntl.flock(fd, fcntl.LOCK_EX)
        except ImportError:
            pass
        yield
    finally:
        os.close(fd)


def _read() -> dict:
    try:
        data = json.loads(path().read_text())
    except (OSError, ValueError):
        return {}
    logins = data.get("logins") if isinstance(data, dict) else None
    return logins if isinstance(logins, dict) else {}


def _write(logins: dict) -> None:
    p = path()
    tmp = p.with_name(p.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump({"version": 1, "logins": logins}, f)
    os.replace(tmp, p)
    with contextlib.suppress(OSError):
        os.chmod(p, 0o600)


def _key(base: str) -> str:
    return base.rstrip("/")


def saved(base: str) -> dict | None:
    """The sign-in kept for the platform at `base`, or None."""
    entry = _read().get(_key(base))
    return entry if isinstance(entry, dict) and entry.get("refresh_token") else None


def save(base: str, entry: dict) -> None:
    with _locked():
        logins = _read()
        logins[_key(base)] = entry
        _write(logins)


def keep(base: str, **fields: Any) -> None:
    """`fields` kept beside the sign-in for `base` (your time zone and clock: seq/person_cli.remember), read and written
    under the lock a refresh takes - a token another `seq` refreshed meanwhile is never written back older. Nothing when
    no one is signed in there."""
    with _locked():
        logins = _read()
        entry = logins.get(_key(base))
        if isinstance(entry, dict) and entry.get("refresh_token") and any(entry.get(k) != v for k, v in fields.items()):
            logins[_key(base)] = {**entry, **fields}
            _write(logins)


def drop(base: str) -> dict | None:
    """The sign-in kept for `base` removed from this machine; what it was, or None."""
    with _locked():
        logins = _read()
        gone = logins.pop(_key(base), None)
        if gone is not None:
            _write(logins)
        return gone


def _client() -> httpx.Client:
    from sequence_ai._core.transport import _version

    return httpx.Client(timeout=30, headers={"User-Agent": f"sequence-ai-python/{_version()}"})


def _refresh(base: str, refresh_token: str) -> dict | None:
    """Fresh tokens for a sign-in, from the platform; None when it has ended there."""
    try:
        with _client() as c:
            r = c.post(f"{base}/v1/login/refresh", json={"refresh_token": refresh_token})
    except httpx.TransportError as exc:
        raise Unavailable(f"could not reach {base} to refresh your sign-in ({type(exc).__name__})") from None
    if r.status_code == 401:
        return None
    if r.status_code != 200:
        try:
            said = r.json()
        except ValueError:
            said = None
        raise from_response(r.status_code, said, text=r.text, headers=r.headers)
    body = r.json()
    return {k: body[k] for k in ("access_token", "refresh_token", "expires_at")}


def _fresh(entry: dict) -> bool:
    try:
        return float(entry.get("expires_at") or 0) - time.time() > EARLY_S
    except (TypeError, ValueError):
        return False


class Login:
    """You, signed in on this machine to the platform at `base`."""

    def __init__(self, base: str) -> None:
        self.base = _key(base)

    @property
    def entry(self) -> dict:
        return saved(self.base) or {}

    def token(self, *, force: bool = False) -> str:
        """The access token to send now - refreshed first when it has under EARLY_S left (or `force`). AuthError(ENDED)
        once the platform says the sign-in has ended; it is removed from this machine then."""
        entry = saved(self.base)
        if entry is None:
            raise AuthError(ENDED)
        if not force and _fresh(entry):
            return entry["access_token"]
        with _locked():
            entry = _read().get(self.base)
            if not isinstance(entry, dict) or not entry.get("refresh_token"):
                raise AuthError(ENDED)
            if not force and _fresh(entry):
                return entry["access_token"]
            fresh = _refresh(self.base, entry["refresh_token"])
            logins = _read()
            if fresh is None:
                logins.pop(self.base, None)
                _write(logins)
                raise AuthError(ENDED)
            entry = {**entry, **fresh}
            logins[self.base] = entry
            _write(logins)
            return entry["access_token"]


def login_for(base: str) -> Login | None:
    """Your sign-in to the platform at `base` on this machine, or None."""
    return Login(base) if saved(base) else None


class LoginAuth(httpx.Auth):
    """A Transport's requests sent as you: each one carries the token in force when it goes out, and one answered 401
    goes once more with a refreshed token."""

    def __init__(self, login: Login) -> None:
        self._login = login

    def auth_flow(self, request: httpx.Request):
        request.headers["Authorization"] = f"Bearer {self._login.token()}"
        response = yield request
        if response.status_code == 401:
            request.headers["Authorization"] = f"Bearer {self._login.token(force=True)}"
            yield request
