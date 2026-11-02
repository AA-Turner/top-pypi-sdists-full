# File: matrx_rag/db/managers/rag/kg_entities.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_orm import BaseManager, BaseDTO, ModelView, build_output_schema
from matrx_rag.db.models_rag import KgEntities


# ---------------------------------------------------------------------------
# ModelView (new) — opt-in projection layer.
# Stores results flat on the model instance; no duplication, no nesting.
# To activate: set view_class = KgEntitiesView on your manager subclass,
# or pass view_class=KgEntitiesView to super().__init__().
# When active, the DTO path below is skipped automatically.
# ---------------------------------------------------------------------------

class KgEntitiesView(ModelView[KgEntities]):
    """
    Declarative view for KgEntities.

    Configure what gets fetched and shaped automatically on every load:

      prefetch    — relation names to fetch concurrently (FK / IFK / M2M)
      exclude     — model field names to omit from to_dict() output
      inline_fk   — replace FK id columns with the full related object
                    e.g. {"customer_id": "customer"}

    Add async methods (no leading underscore) for computed fields:

        async def display_name(self, model: KgEntities) -> str:
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
#   - JSON Schema generation: KgEntitiesSchema.model_json_schema()
#   - Typed API responses: KgEntitiesSchema.model_validate(item.to_dict())
#
# Usage example:
#   @app.get("/{id}", response_model=KgEntitiesSchema)
#   async def get_kg_entities(id: str):
#       item = await kg_entities_manager_instance.load_by_id(id)
#       return item.to_dict()
# ---------------------------------------------------------------------------

try:
    KgEntitiesSchema = build_output_schema(KgEntities)
except ImportError:
    KgEntitiesSchema = None  # type: ignore[assignment]  # pydantic not installed


# ---------------------------------------------------------------------------
# BaseDTO (default) — active by default, fully backward compatible.
# Extend _process_core_data / _process_metadata with your business logic.
# When you are ready to migrate to the View above, set view_class on your
# manager subclass and this DTO will be bypassed automatically.
# ---------------------------------------------------------------------------

@dataclass
class KgEntitiesDTO(BaseDTO[KgEntities]):
    id: str

    async def _initialize_dto(self, model: KgEntities) -> None:
        '''Override to populate DTO fields from the model.'''
        self.id = model.get_cache_key()
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True

    async def _process_core_data(self, model: KgEntities) -> None:
        '''Process core data from the model item.'''
        pass

    async def _process_metadata(self, model: KgEntities) -> None:
        '''Process metadata from the model item.'''
        pass

    async def _initial_validation(self, model: KgEntities) -> None:
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
#   1. Quick: set view_class = KgEntitiesView  (replaces DTO automatically)
#   2. Explicit: super().__init__(KgEntities, view_class=KgEntitiesView)
# ---------------------------------------------------------------------------

class KgEntitiesBase(BaseManager[KgEntities]):
    view_class = None  # DTO is used by default; set to KgEntitiesView to opt in

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
            KgEntities,
            dto_class=dto_class or KgEntitiesDTO,
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self) -> None:
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgEntities) -> None:
        pass

    async def create_kg_entities(self, **data: Any) -> KgEntities:
        return await self.create_item(**data)

    async def delete_kg_entities(self, id: Any) -> bool:
        return await self.delete_item(id)

    async def get_kg_entities_with_all_related(self, id: Any) -> tuple[KgEntities, Any]:
        return await self.get_item_with_all_related(id)

    async def load_kg_entities_by_id(self, id: Any) -> KgEntities:
        return await self.load_by_id(id)

    async def load_kg_entities(self, use_cache: bool = True, **kwargs: Any) -> KgEntities:
        return await self.load_item(use_cache, **kwargs)

    async def update_kg_entities(self, id: Any, **updates: Any) -> KgEntities:
        return await self.update_item(id, **updates)

    async def load_all_kg_entities(self, **kwargs: Any) -> list[KgEntities]:
        return await self.load_items(**kwargs)

    async def filter_all_kg_entities(self, **kwargs: Any) -> list[KgEntities]:
        return await self.filter_items(**kwargs)

    async def get_or_create_kg_entities(self, defaults: dict[str, Any] | None = None, **kwargs: Any) -> KgEntities | None:
        return await self.get_or_create(defaults, **kwargs)

    async def get_kg_entities_with_kg_clusters(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_clusters')

    async def get_all_kg_entities_with_kg_clusters(self) -> list[Any]:
        return await self.get_items_with_related('kg_clusters')

    async def get_kg_entities_with_iam_organizations(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.organizations')

    async def get_all_kg_entities_with_iam_organizations(self) -> list[Any]:
        return await self.get_items_with_related('iam.organizations')

    async def get_kg_entities_with_iam_users(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.users')

    async def get_all_kg_entities_with_iam_users(self) -> list[Any]:
        return await self.get_items_with_related('iam.users')

    async def get_kg_entities_with_kg_chunk_entities(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_chunk_entities')

    async def get_all_kg_entities_with_kg_chunk_entities(self) -> list[Any]:
        return await self.get_items_with_related('kg_chunk_entities')

    async def get_kg_entities_with_kg_edges(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_edges')

    async def get_all_kg_entities_with_kg_edges(self) -> list[Any]:
        return await self.get_items_with_related('kg_edges')

    async def get_kg_entities_with_kg_entity_aliases(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_entity_aliases')

    async def get_all_kg_entities_with_kg_entity_aliases(self) -> list[Any]:
        return await self.get_items_with_related('kg_entity_aliases')

    async def get_kg_entities_with_scope_association_suggestions(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'scope_association_suggestions')

    async def get_all_kg_entities_with_scope_association_suggestions(self) -> list[Any]:
        return await self.get_items_with_related('scope_association_suggestions')

    async def get_kg_entities_with_scope_item_value_suggestions(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'scope_item_value_suggestions')

    async def get_all_kg_entities_with_scope_item_value_suggestions(self) -> list[Any]:
        return await self.get_items_with_related('scope_item_value_suggestions')

    async def load_all_kg_entities_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.load_items(organization_id=organization_id)

    async def filter_all_kg_entities_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.filter_items(organization_id=organization_id)

    async def load_all_kg_entities_by_cluster_id(self, cluster_id: Any) -> list[Any]:
        return await self.load_items(cluster_id=cluster_id)

    async def filter_all_kg_entities_by_cluster_id(self, cluster_id: Any) -> list[Any]:
        return await self.filter_items(cluster_id=cluster_id)

    async def load_all_kg_entities_by_created_by(self, created_by: Any) -> list[Any]:
        return await self.load_items(created_by=created_by)

    async def filter_all_kg_entities_by_created_by(self, created_by: Any) -> list[Any]:
        return await self.filter_items(created_by=created_by)

    async def load_all_kg_entities_by_updated_by(self, updated_by: Any) -> list[Any]:
        return await self.load_items(updated_by=updated_by)

    async def filter_all_kg_entities_by_updated_by(self, updated_by: Any) -> list[Any]:
        return await self.filter_items(updated_by=updated_by)

    async def load_all_kg_entities_by_ids(self, ids: list[Any]) -> list[Any]:
        return await self.load_items_by_ids(ids)

    def add_computed_field(self, field: str) -> None:
        super().add_computed_field(field)

    def add_relation_field(self, field: str) -> None:
        super().add_relation_field(field)

    @property
    def active_kg_entities_ids(self) -> set[Any]:
        return self.active_item_ids



class KgEntitiesManager(KgEntitiesBase):
    _instance: KgEntitiesManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> KgEntitiesManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: KgEntities) -> None:
        pass

kg_entities_manager_instance = KgEntitiesManager()