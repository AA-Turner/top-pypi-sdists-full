"""ORM-backed model manager impl — importing THIS module requires DB config.

The public ``AiModelManager`` facade (``ai_model_manager.py``) constructs
``OrmAiModelManager`` lazily on the first ORM-path call; a client host with an
injected model catalog never imports this module at all.
"""

from __future__ import annotations

import uuid as _uuid
from typing import Any

from .ai_model_base import AiModelBase


class OrmAiModelManager(AiModelBase):
    """Read surface over the AI model catalog (host table: ai.model_definition).

    The consumed API is deliberately tiny — load_model / load_all_models /
    load_model_get_string_uuid — everything else goes through the generic
    BaseManager vocabulary (load_items / load_by_id), NEVER through the host
    base's table-name-derived methods (those renamed with ai.model →
    ai.model_definition and will rename again if the table ever moves).
    Catalog routing/controls/pricing resolution lives in matrx_ai.catalog.
    """

    _instance: OrmAiModelManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> OrmAiModelManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__(
            fetch_on_init_limit=300,
            fetch_on_init_with_warnings_off=(
                "YES_I_KNOW_WHAT_IM_DOING_TURN_OFF_WARNINGS_FOR_LIMIT_300"
            ),
        )

    async def _initialize_runtime_data(self, item: Any) -> None:
        pass

    async def load_all_models(self) -> list[Any]:
        # Soft-deleted rows must never surface as models. The catalog engine
        # path filters deleted_at itself (catalog/manager.py reload); this ORM
        # fallback (validators/scripts) must match, or deleted models resurface
        # as phantom "NO OFFERING" findings.
        return [m for m in await self.load_items() if getattr(m, "deleted_at", None) is None]

    async def load_model(self, id_or_name: str) -> Any | None:
        """UUID → id lookup, anything else → name lookup. None when missing —
        callers own their typed "model not found" errors."""
        try:
            _uuid.UUID(str(id_or_name))
        except (ValueError, AttributeError, TypeError):
            models = await self.load_items(name=id_or_name)
            return models[0] if models else None

        # lazy: matrx-orm is host-injected. The manager's @handle_errors wraps
        # DoesNotExist in AppError (error["type"] carries the inner class name);
        # ONLY that maps to None — any real DB failure still raises.
        from matrx_orm import DoesNotExist
        from matrx_orm.extended.app_error_handler import AppError

        try:
            return await self.load_by_id(id_or_name)
        except DoesNotExist:
            return None
        except AppError as exc:
            if exc.error.get("type") == "DoesNotExist":
                return None
            raise

    async def load_model_get_string_uuid(self, id_or_name: str) -> str | None:
        model = await self.load_model(id_or_name)
        return str(model.id) if model else None
