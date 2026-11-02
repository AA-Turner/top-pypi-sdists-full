# File: matrx_rag/db/managers/rag/kg_alerts.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_orm import BaseManager, BaseDTO, ModelView, build_output_schema
from matrx_rag.db.models_rag import KgAlerts


# ---------------------------------------------------------------------------
# ModelView (new) — opt-in projection layer.
# Stores results flat on the model instance; no duplication, no nesting.
# To activate: set view_class = KgAlertsView on your manager subclass,
# or pass view_class=KgAlertsView to super().__init__().
# When active, the DTO path below is skipped automatically.
# ---------------------------------------------------------------------------

class KgAlertsView(ModelView[KgAlerts]):
    """
    Declarative view for KgAlerts.

    Configure what gets fetched and shaped automatically on every load:

      prefetch    — relation names to fetch concurrently (FK / IFK / M2M)
      exclude     — model field names to omit from to_dict() output
      inline_fk   — replace FK id columns with the full related object
                    e.g. {"customer_id": "customer"}

    Add async methods (no leading underscore) for computed fields:

        async def display_name(self, model: KgAlerts) -> str:
            return model.name.title()
    """

    prefetch: list[str] = []
    exclude: list[str] = []
    inline_fk: dict[str, str] = {}

    # ------------------------------------------------------------------ #
    # Computed fields — add async methods below.                          #
    # Each method receives the model instance and returns a plain value.  #
    # Errors in computed fields are logged and stored as None —           #
    # they never abort the load.                                          #
    # ------------------------------------------------------------------ #


# ---------------------------------------------------------------------------
# Pydantic output schema (optional, requires pydantic v2).
# Auto-generated from the model's field definitions.  Useful for:
#   - FastAPI response_model type annotation
#   - JSON Schema generation: KgAlertsSchema.model_json_schema()
#   - Typed API responses: KgAlertsSchema.model_validate(item.to_dict())
#
# Usage example:
#   @app.get("/{id}", response_model=KgAlertsSchema)
#   async def get_kg_alerts(id: str):
#       item = await kg_alerts_manager_instance.load_by_id(id)
#       return item.to_dict()
# ---------------------------------------------------------------------------

try:
    KgAlertsSchema = build_output_schema(KgAlerts)
except ImportError:
    KgAlertsSchema = None  # type: ignore[assignment]  # pydantic not installed


# ---------------------------------------------------------------------------
# BaseDTO (default) — active by default, fully backward compatible.
# Extend _process_core_data / _process_metadata with your business logic.
# When you are ready to migrate to the View above, set view_class on your
# manager subclass and this DTO will be bypassed automatically.
# ---------------------------------------------------------------------------

@dataclass
class KgAlertsDTO(BaseDTO[KgAlerts]):
    id: str

    async def _initialize_dto(self, model: KgAlerts) -> None:
        '''Override to populate DTO fields from the model.'''
        self.id = model.get_cache_key()
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True

    async def _process_core_data(self, model: KgAlerts) -> None:
        '''Process core data from the model item.'''
        pass

    async def _process_metadata(self, model: KgAlerts) -> None:
        '''Process metadata from the model item.'''
        pass

    async def _initial_validation(self, model: KgAlerts) -> None:
        '''Validate fields from the model item.'''
        pass

    async def _final_validation(self) -> bool:
        '''Final validation of the model item.'''
        return True

    async def get_validated_dict(self) -> dict[str, Any]:
        '''Get the validated dictionary.'''
        await self._final_validation()
        return self.to_dict()


# ---------------------------------------------------------------------------
# Manager — DTO is active by default for full backward compatibility.
# To switch to the View (opt-in):
#   1. Quick: set view_class = KgAlertsView  (replaces DTO automatically)
#   2. Explicit: super().__init__(KgAlerts, view_class=KgAlertsView)
# ---------------------------------------------------------------------------

class KgAlertsBase(BaseManager[KgAlerts]):
    view_class = None  # DTO is used by default; set to KgAlertsView to opt in

    def __init__(
        self,
        dto_class: type[Any] | None = None,
        view_class: type[Any] | None = None,
        fetch_on_init_limit: int = 0,
        fetch_on_init_with_warnings_off: str | None = None,
    ) -> None:
        if view_class is not None:
            self.view_class = view_class
        super().__init__(
            KgAlerts,
            dto_class=dto_class or KgAlertsDTO,
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self) -> None:
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgAlerts) -> None:
        pass

    async def create_kg_alerts(self, **data: Any) -> KgAlerts:
        return await self.create_item(**data)

    async def delete_kg_alerts(self, id: Any) -> bool:
        return await self.delete_item(id)

    async def get_kg_alerts_with_all_related(self, id: Any) -> tuple[KgAlerts, Any]:
        return await self.get_item_with_all_related(id)

    async def load_kg_alerts_by_id(self, id: Any) -> KgAlerts:
        return await self.load_by_id(id)

    async def load_kg_alerts(self, use_cache: bool = True, **kwargs: Any) -> KgAlerts:
        return await self.load_item(use_cache, **kwargs)

    async def update_kg_alerts(self, id: Any, **updates: Any) -> KgAlerts:
        return await self.update_item(id, **updates)

    async def load_all_kg_alerts(self, **kwargs: Any) -> list[KgAlerts]:
        return await self.load_items(**kwargs)

    async def filter_all_kg_alerts(self, **kwargs: Any) -> list[KgAlerts]:
        return await self.filter_items(**kwargs)

    async def get_or_create_kg_alerts(self, defaults: dict[str, Any] | None = None, **kwargs: Any) -> KgAlerts | None:
        return await self.get_or_create(defaults, **kwargs)

    async def get_kg_alerts_with_iam_users(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.users')

    async def get_all_kg_alerts_with_iam_users(self) -> list[Any]:
        return await self.get_items_with_related('iam.users')

    async def get_kg_alerts_with_iam_organizations(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.organizations')

    async def get_all_kg_alerts_with_iam_organizations(self) -> list[Any]:
        return await self.get_items_with_related('iam.organizations')

    async def load_all_kg_alerts_by_user_id(self, user_id: Any) -> list[Any]:
        return await self.load_items(user_id=user_id)

    async def filter_all_kg_alerts_by_user_id(self, user_id: Any) -> list[Any]:
        return await self.filter_items(user_id=user_id)

    async def load_all_kg_alerts_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.load_items(organization_id=organization_id)

    async def filter_all_kg_alerts_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.filter_items(organization_id=organization_id)

    async def load_all_kg_alerts_by_created_by(self, created_by: Any) -> list[Any]:
        return await self.load_items(created_by=created_by)

    async def filter_all_kg_alerts_by_created_by(self, created_by: Any) -> list[Any]:
        return await self.filter_items(created_by=created_by)

    async def load_all_kg_alerts_by_updated_by(self, updated_by: Any) -> list[Any]:
        return await self.load_items(updated_by=updated_by)

    async def filter_all_kg_alerts_by_updated_by(self, updated_by: Any) -> list[Any]:
        return await self.filter_items(updated_by=updated_by)

    async def load_all_kg_alerts_by_shown_to(self, shown_to: Any) -> list[Any]:
        return await self.load_items(shown_to=shown_to)

    async def filter_all_kg_alerts_by_shown_to(self, shown_to: Any) -> list[Any]:
        return await self.filter_items(shown_to=shown_to)

    async def load_all_kg_alerts_by_ids(self, ids: list[Any]) -> list[Any]:
        return await self.load_items_by_ids(ids)

    def add_computed_field(self, field: str) -> None:
        super().add_computed_field(field)

    def add_relation_field(self, field: str) -> None:
        super().add_relation_field(field)

    @property
    def active_kg_alerts_ids(self) -> set[Any]:
        return self.active_item_ids



class KgAlertsManager(KgAlertsBase):
    _instance: KgAlertsManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> KgAlertsManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: KgAlerts) -> None:
        pass

kg_alerts_manager_instance = KgAlertsManager()