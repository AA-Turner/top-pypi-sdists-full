"""The router's store: route_log (one row per call through the router) and its API
keys (hugpy-wrapper's KeyAuth with the router's own settings).

Backends: the pure router (no central) keeps hugpy-wrapper's SQLite Store in its own
directory; central (hugpy-core 0.4.3) hands over its Postgres-backed store through
`configure` so the route log and the keys live in the core database with everything
else. `STORE` and `KEYS` are read through the module (they are swapped, not copied).
"""
from __future__ import annotations

import json
import os
import time
from typing import Optional

from hugpy_core.lifted.key_auth import KeyAuth

from hugpy_core.router.imports import constants as C
from hugpy_core.router.imports import functions as F


def home() -> str:
    explicit = os.environ.get(C.ENV_HOME, "").strip()
    if explicit:
        return os.path.abspath(os.path.expanduser(explicit))
    state = os.environ.get("STATE_DIRECTORY", "").strip()
    return state.split(":")[0] if state else F.data_dir()


class _Lazy:
    """The default SQLite store, opened on first use (central never opens it)."""
    def __init__(self):
        self._store = None

    def _real(self):
        if self._store is None:
            from hugpy_core.lifted.sqlite_store import Store
            self._store = Store(home, "hugpy_core.router.observability", C.STORE_FILENAME, mode_env=C.ENV_STORE_MODE)
        return self._store

    def __getattr__(self, name):
        return getattr(self._real(), name)

    def close(self):
        if self._store is not None:
            self._store.close()
            self._store = None


STORE = _Lazy()
KEYS = KeyAuth(STORE, C.ENV_KEY, C.ENV_REQUIRE_KEY, C.ENV_TRUSTED_NETS, C.ENV_TRUSTED_PROXIES)


def configure(store) -> None:
    """A supplied central store replaces the default router store."""
    global STORE, KEYS
    STORE = store
    KEYS = KeyAuth(store, C.ENV_KEY, C.ENV_REQUIRE_KEY, C.ENV_TRUSTED_NETS, C.ENV_TRUSTED_PROXIES)


def open_call(request_id: str, route: str, model: str, options: Optional[str], pin: Optional[str],
              client: str) -> None:
    STORE.write("INSERT INTO route_log (request_id, received_at, route, model, options, pin, client) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)", (request_id, time.time(), route, model, options, pin, client))


def update_call(request_id: str, **cols) -> None:
    if not cols:
        return
    vals = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in cols.values()]
    STORE.write(f"UPDATE route_log SET {', '.join(f'{k} = ?' for k in cols)} WHERE request_id = ?",
                (*vals, request_id))
