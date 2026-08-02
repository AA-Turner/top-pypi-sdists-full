"""On-disk cache for expensive env-var resolutions.

Some resolvers (notably the interactive OAuth flow for ``SLACK_USER_TOKEN``)
are expensive to re-run on every invocation. For env vars whose
:class:`~pysae_ai_tools.env.config.EnvVarSpec` sets ``cache=True``, the
resolver writes the value to ``env-cache.json`` in the XDG cache dir
after a successful resolution and reads back from it on the next call.

Security model: the cache file stores secrets in plaintext under the
user's home directory, protected by POSIX 0600 permissions (and by the
default NTFS ACL on Windows). Same model as ``~/.aws/credentials``,
``~/.config/gh/hosts.yml``, ``~/.config/argocd/config``. The file is
never committed and must not be copied across machines.
"""

import json
import os
import shutil

from ..config import CACHE_DIR, CONFIG_DIR

CACHE_PATH = CACHE_DIR / "env-cache.json"

# Historical location (a resolved-secrets cache mis-filed under the config dir).
_LEGACY_PATH = CONFIG_DIR / "env-cache.json"


def migrate_legacy() -> None:
    """Move the env-cache from the config dir to the cache dir, once. ``shutil.move`` preserves the
    0600 perms of the existing file. Best-effort and idempotent."""
    try:
        if _LEGACY_PATH.exists() and not CACHE_PATH.exists():
            CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(_LEGACY_PATH), str(CACHE_PATH))
    except OSError:
        pass


def _load() -> dict[str, str]:
    """Load the cache file, returning an empty dict on any failure."""
    try:
        raw = CACHE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return {k: v for k, v in data.items() if isinstance(k, str) and isinstance(v, str)}


def _save(data: dict[str, str]) -> None:
    """Atomically write the cache file with 0o600 perms."""
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Open with O_CREAT|O_TRUNC + mode=0o600 so new files get the tight perms
    # from the start. Existing perms are preserved if the file already exists.
    fd = os.open(CACHE_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def read(var: str) -> str | None:
    """Return the cached value for ``var``, or ``None`` if missing."""
    value = _load().get(var, "")
    return value if value else None


def write(var: str, value: str) -> None:
    """Upsert ``var=value`` in the cache."""
    data = _load()
    data[var] = value
    _save(data)


def clear(var: str | None = None) -> None:
    """Remove ``var`` from the cache, or drop the whole file when ``None``."""
    if var is None:
        try:
            CACHE_PATH.unlink()
        except FileNotFoundError:
            pass
        return
    data = _load()
    if var in data:
        del data[var]
        _save(data)
