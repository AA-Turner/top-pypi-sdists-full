"""Settings accessor — read/write scoped key-value settings via MongoDB."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .constants import SETTINGS_KEY_FIELD
from .db import get_active_identity

if TYPE_CHECKING:
    from .app import App
    from .db import Collection


class SettingsAccessor:
    """Central ``app.settings.get(key)`` / ``app.settings.set(key, value)`` API.

    Backed by a reserved ``_settings`` Mongo collection.  Scope filters are
    resolved from the headers the runner injects on each request
    (user_id / owner_id), matching the pattern used by ``ScopedCollection``.
    """

    def __init__(self, app: App) -> None:
        self._app = app
        self._collection: Collection | None = None
        self._user_id: str = ""
        self._owner_id: str = ""

    def _bind(self, collection: Collection) -> None:
        self._collection = collection

    def _set_identity(self, user_id: str, owner_id: str) -> None:
        self._user_id = user_id
        self._owner_id = owner_id

    def _require_collection(self) -> Collection:
        if self._collection is None:
            raise RuntimeError("Settings are not available yet — the app has not booted.")
        return self._collection

    def _scope_filter(self, key: str) -> dict[str, str]:
        decl = self._app._settings.get(key)
        if decl is None:
            return {}
        identity = get_active_identity()
        if identity is not None:
            user = getattr(identity, "user", None)
            user_id = getattr(user, "id", "") if user else ""
            owner_id = getattr(user, "owner_id", "") if user else ""
        else:
            user_id = self._user_id
            owner_id = self._owner_id
        return decl.scope_filter(
            user_id=user_id,
            owner_id=owner_id,
        )

    async def get(self, key: str) -> Any:
        """Read a setting value.  Returns the declared default if not yet set."""
        col = self._require_collection()
        decl = self._app._settings.get(key)
        filt = {SETTINGS_KEY_FIELD: key, **self._scope_filter(key)}
        doc = await col.find_one(filt)
        if doc is not None:
            return doc.get("value", decl.default if decl else None)
        return decl.default if decl else None

    async def set(self, key: str, value: Any) -> None:
        """Write a setting value (upsert)."""
        col = self._require_collection()
        filt = {SETTINGS_KEY_FIELD: key, **self._scope_filter(key)}
        await col.update_one(filt, {"$set": {"value": value, **filt}})

    async def get_all(self, keys: list[str] | None = None) -> dict[str, Any]:
        """Bulk-read all declared settings, returning ``{key: value}``."""
        self._require_collection()
        targets = keys or list(self._app._settings.keys())
        result: dict[str, Any] = {}
        for key in targets:
            result[key] = await self.get(key)
        return result
