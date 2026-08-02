"""On-disk store for Auth0 tokens, keyed by environment.

Tokens are written to ``pysae-api-tokens.json`` in the XDG data dir with ``0600``
permissions — the same plaintext-under-home model as ``~/.aws/credentials`` or
``~/.config/gh/hosts.yml``. The file is never committed and must not be copied
across machines.

The store keeps one :class:`TokenSet` per environment (``dev`` / ``prod``) so a
single machine can stay logged into both at once.
"""

import json
import os
import shutil
import time
from dataclasses import asdict, dataclass

from ....config import CONFIG_DIR
from .config import TOKENS_PATH

# Historical location (persistent auth state mis-filed under the config dir).
_LEGACY_PATH = CONFIG_DIR / "pysae-api-tokens.json"


def migrate_legacy() -> None:
    """Move the token store from the config dir to the data dir, once. ``shutil.move`` preserves the
    0600 perms of the existing file, so no re-login is forced. Best-effort and idempotent."""
    try:
        if _LEGACY_PATH.exists() and not TOKENS_PATH.exists():
            TOKENS_PATH.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(_LEGACY_PATH), str(TOKENS_PATH))
    except OSError:
        pass


# Refresh a little before the real expiry to avoid races on slow calls.
EXPIRY_SKEW_SECONDS = 60


def _to_float(value: object) -> float:
    if isinstance(value, (int, float, str)):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
    return 0.0


@dataclass
class TokenSet:
    """A set of Auth0 tokens for one environment."""

    access_token: str
    refresh_token: str = ""
    id_token: str = ""
    token_type: str = "Bearer"
    scope: str = ""
    # Absolute epoch seconds at which ``access_token`` stops being valid.
    expires_at: float = 0.0

    @classmethod
    def from_response(cls, payload: dict[str, object], *, previous: "TokenSet | None" = None) -> "TokenSet":
        """Build a token set from an Auth0 ``/oauth/token`` response.

        With rotating refresh tokens the response usually carries a fresh
        ``refresh_token``; when it does not (some refresh responses omit it),
        we keep the previous one.
        """
        expires_in = _to_float(payload.get("expires_in"))
        refresh = str(payload.get("refresh_token", "") or "")
        if not refresh and previous is not None:
            refresh = previous.refresh_token
        return cls(
            access_token=str(payload.get("access_token", "") or ""),
            refresh_token=refresh,
            id_token=str(payload.get("id_token", "") or ""),
            token_type=str(payload.get("token_type", "Bearer") or "Bearer"),
            scope=str(payload.get("scope", "") or ""),
            expires_at=time.time() + expires_in,
        )

    def is_expired(self, *, skew: int = EXPIRY_SKEW_SECONDS) -> bool:
        return time.time() >= (self.expires_at - skew)

    def seconds_remaining(self) -> int:
        return max(0, int(self.expires_at - time.time()))


def _load_all() -> dict[str, dict[str, object]]:
    try:
        raw = TOKENS_PATH.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _save_all(data: dict[str, dict[str, object]]) -> None:
    TOKENS_PATH.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(TOKENS_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def load(env: str) -> TokenSet | None:
    """Return the stored token set for ``env`` or ``None``."""
    entry = _load_all().get(env)
    if not isinstance(entry, dict) or not entry.get("access_token"):
        return None
    return TokenSet(
        access_token=str(entry.get("access_token", "")),
        refresh_token=str(entry.get("refresh_token", "")),
        id_token=str(entry.get("id_token", "")),
        token_type=str(entry.get("token_type", "Bearer")),
        scope=str(entry.get("scope", "")),
        expires_at=_to_float(entry.get("expires_at")),
    )


def save(env: str, tokens: TokenSet) -> None:
    """Upsert the token set for ``env``."""
    data = _load_all()
    data[env] = asdict(tokens)
    _save_all(data)


def clear(env: str | None = None) -> None:
    """Drop tokens for ``env``, or the whole file when ``env`` is ``None``."""
    if env is None:
        try:
            TOKENS_PATH.unlink()
        except FileNotFoundError:
            pass
        return
    data = _load_all()
    if env in data:
        del data[env]
        _save_all(data)
