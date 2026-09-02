"""AiModelManager — catalog-aware facade over the model read surface.

Resolution order for every lookup:
1. **Runtime models** (``matrx_ai.catalog.register_runtime_model``) — synthetic
   process-local entries (matrx-local's connected llama-server). Checked in
   BOTH hosts so a runtime model shadows nothing but always resolves.
2. **Host-injected model catalog** (``matrx_ai.configure(model_catalog=...)``)
   — a client host's model source (server API payload, offline baseline, …).
   In catalog mode the ORM base is NEVER constructed: no matrx-orm, no DB.
3. **ORM path** (``_ai_model_manager_orm.OrmAiModelManager``) — the unchanged
   server behavior, constructed lazily on the first ORM-path call
   (constructing it eagerly would fire ``get_model("AiModel")`` and the
   fetch-on-init read, which requires full host DB config).

Importing this module is safe in an unconfigured environment — config errors
surface at CALL time, never import time.

Anything beyond load_model / load_all_models / load_model_get_string_uuid
(the generic BaseManager vocabulary: load_items, load_by_id, …) is forwarded
to the ORM manager via ``__getattr__`` — in catalog mode that forwarding
raises DBNotConfiguredError loudly, because the catalog protocol deliberately
does not cover arbitrary ORM queries.
"""

from __future__ import annotations

from typing import Any


class AiModelManager:
    _instance: AiModelManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> AiModelManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Singleton __init__ re-runs on every AiModelManager() call — keep it
        # idempotent and side-effect free.
        if not hasattr(self, "_orm"):
            self._orm: Any | None = None

    # ------------------------------------------------------------------
    # Backend resolution
    # ------------------------------------------------------------------

    def _orm_manager(self) -> Any:
        if self._orm is None:
            from ._ai_model_manager_orm import OrmAiModelManager

            self._orm = OrmAiModelManager()
        return self._orm

    @staticmethod
    def _catalog() -> Any | None:
        from matrx_ai.catalog.host_catalog import get_model_catalog

        return get_model_catalog()

    # ------------------------------------------------------------------
    # Public read surface
    # ------------------------------------------------------------------

    async def load_all_models(self) -> list[Any]:
        from matrx_ai.catalog.host_catalog import CatalogModel, list_runtime_models

        catalog = self._catalog()
        if catalog is not None:
            models: list[Any] = [CatalogModel(d) for d in await catalog.list_models()]
            models.extend(list_runtime_models())
            return models
        base = await self._orm_manager().load_all_models()
        runtime = list_runtime_models()
        return list(base) + runtime if runtime else base

    async def load_model(self, id_or_name: str) -> Any | None:
        from matrx_ai.catalog.host_catalog import CatalogModel, get_runtime_model

        runtime = get_runtime_model(id_or_name)
        if runtime is not None:
            return runtime
        catalog = self._catalog()
        if catalog is not None:
            data = await catalog.get_model(id_or_name)
            return CatalogModel(data) if data is not None else None

        # ── THE ONE name-routing funnel (server hosts) ──────────────────
        # EVERY inbound model ref — id, name, or ai.model_alias alias —
        # resolves through ai_catalog_manager.resolve_model_ref before the
        # ORM read, so every entry path (chat/agents/conversations/workflows/
        # realtime/persistence) honors aliases without its own resolution
        # logic. Client hosts have no DB-backed catalog: the ref passes
        # through unchanged (DBNotConfiguredError). Retry routing grows on
        # resolve_model_ref, never here.
        resolved_ref = id_or_name
        from matrx_ai.db._registry import DBNotConfiguredError

        try:
            from matrx_ai.catalog.manager import ai_catalog_manager

            await ai_catalog_manager.ensure_loaded()
            resolved_ref = ai_catalog_manager.resolve_model_ref(id_or_name)
        except DBNotConfiguredError:
            pass

        model = await self._orm_manager().load_model(resolved_ref)
        if model is None and resolved_ref != id_or_name:
            model = await self._orm_manager().load_model(id_or_name)
        return model

    async def load_model_get_string_uuid(self, id_or_name: str) -> str | None:
        model = await self.load_model(id_or_name)
        return str(model.id) if model else None

    async def refresh(self) -> int:
        """Refetch every model row from the DB, busting the ORM model cache.

        The admin catalog-reload seam (paired with ai_catalog_manager.reload()
        in aidream/services/ai_catalog/reload.py) — model-level fields like
        retry_max_attempts / retry_fallback_id take effect without a restart.
        Returns the number of model rows now served.
        """
        catalog = self._catalog()
        if catalog is not None:
            # Catalog host: the injected catalog is the source of truth and
            # holds no ORM cache to bust — a fresh list IS the refresh.
            return len(await self.load_all_models())

        from matrx_ai.db._registry import get_model
        from matrx_orm import StateManager

        try:
            await StateManager.clear_cache(get_model("AiModel"))
        except KeyError:
            pass  # no cache state exists yet — nothing to bust
        return len(await self._orm_manager().load_all_models())

    # ------------------------------------------------------------------
    # ORM vocabulary passthrough (server hosts)
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        return getattr(self._orm_manager(), name)


ai_model_manager_instance = AiModelManager()
