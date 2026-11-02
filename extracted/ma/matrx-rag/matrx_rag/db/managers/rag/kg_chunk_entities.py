# File: matrx_rag/db/managers/rag/kg_chunk_entities.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_orm import BaseManager, BaseDTO, ModelView, build_output_schema
from matrx_rag.db.models_rag import KgChunkEntities


# ---------------------------------------------------------------------------
# ModelView (new) — opt-in projection layer.
# Stores results flat on the model instance; no duplication, no nesting.
# To activate: set view_class = KgChunkEntitiesView on your manager subclass,
# or pass view_class=KgChunkEntitiesView to super().__init__().
# When active, the DTO path below is skipped automatically.
# ---------------------------------------------------------------------------

class KgChunkEntitiesView(ModelView[KgChunkEntities]):
    """
    Declarative view for KgChunkEntities.

    Configure what gets fetched and shaped automatically on every load:

      prefetch    — relation names to fetch concurrently (FK / IFK / M2M)
      exclude     — model field names to omit from to_dict() output
      inline_fk   — replace FK id columns with the full related object
                    e.g. {"customer_id": "customer"}

    Add async methods (no leading underscore) for computed fields:

        async def display_name(self, model: KgChunkEntities) -> str:
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
#   - JSON Schema generation: KgChunkEntitiesSchema.model_json_schema()
#   - Typed API responses: KgChunkEntitiesSchema.model_validate(item.to_dict())
#
# Usage example:
#   @app.get("/{id}", response_model=KgChunkEntitiesSchema)
#   async def get_kg_chunk_entities(id: str):
#       item = await kg_chunk_entities_manager_instance.load_by_id(id)
#       return item.to_dict()
# ---------------------------------------------------------------------------

try:
    KgChunkEntitiesSchema = build_output_schema(KgChunkEntities)
except ImportError:
    KgChunkEntitiesSchema = None  # type: ignore[assignment]  # pydantic not installed


# ---------------------------------------------------------------------------
# BaseDTO (default) — active by default, fully backward compatible.
# Extend _process_core_data / _process_metadata with your business logic.
# When you are ready to migrate to the View above, set view_class on your
# manager subclass and this DTO will be bypassed automatically.
# ---------------------------------------------------------------------------

@dataclass
class KgChunkEntitiesDTO(BaseDTO[KgChunkEntities]):
    id: str

    async def _initialize_dto(self, model: KgChunkEntities) -> None:
        '''Override to populate DTO fields from the model.'''
        self.id = model.get_cache_key()
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True

    async def _process_core_data(self, model: KgChunkEntities) -> None:
        '''Process core data from the model item.'''
        pass

    async def _process_metadata(self, model: KgChunkEntities) -> None:
        '''Process metadata from the model item.'''
        pass

    async def _initial_validation(self, model: KgChunkEntities) -> None:
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
#   1. Quick: set view_class = KgChunkEntitiesView  (replaces DTO automatically)
#   2. Explicit: super().__init__(KgChunkEntities, view_class=KgChunkEntitiesView)
# ---------------------------------------------------------------------------

class KgChunkEntitiesBase(BaseManager[KgChunkEntities]):
    view_class = None  # DTO is used by default; set to KgChunkEntitiesView to opt in

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
            KgChunkEntities,
            dto_class=dto_class or KgChunkEntitiesDTO,
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self) -> None:
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgChunkEntities) -> None:
        pass

    async def create_kg_chunk_entities(self, **data: Any) -> KgChunkEntities:
        return await self.create_item(**data)

    async def delete_kg_chunk_entities(self, id: Any) -> bool:
        return await self.delete_item(id)

    async def get_kg_chunk_entities_with_all_related(self, id: Any) -> tuple[KgChunkEntities, Any]:
        return await self.get_item_with_all_related(id)

    async def load_kg_chunk_entities_by_id(self, id: Any) -> KgChunkEntities:
        return await self.load_by_id(id)

    async def load_kg_chunk_entities(self, use_cache: bool = True, **kwargs: Any) -> KgChunkEntities:
        return await self.load_item(use_cache, **kwargs)

    async def update_kg_chunk_entities(self, id: Any, **updates: Any) -> KgChunkEntities:
        return await self.update_item(id, **updates)

    async def load_all_kg_chunk_entities(self, **kwargs: Any) -> list[KgChunkEntities]:
        return await self.load_items(**kwargs)

    async def filter_all_kg_chunk_entities(self, **kwargs: Any) -> list[KgChunkEntities]:
        return await self.filter_items(**kwargs)

    async def get_or_create_kg_chunk_entities(self, defaults: dict[str, Any] | None = None, **kwargs: Any) -> KgChunkEntities | None:
        return await self.get_or_create(defaults, **kwargs)

    async def get_kg_chunk_entities_with_kg_entity_aliases(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_entity_aliases')

    async def get_all_kg_chunk_entities_with_kg_entity_aliases(self) -> list[Any]:
        return await self.get_items_with_related('kg_entity_aliases')

    async def get_kg_chunk_entities_with_kg_chunks(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_chunks')

    async def get_all_kg_chunk_entities_with_kg_chunks(self) -> list[Any]:
        return await self.get_items_with_related('kg_chunks')

    async def get_kg_chunk_entities_with_kg_entities(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_entities')

    async def get_all_kg_chunk_entities_with_kg_entities(self) -> list[Any]:
        return await self.get_items_with_related('kg_entities')

    async def get_kg_chunk_entities_with_iam_organizations(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.organizations')

    async def get_all_kg_chunk_entities_with_iam_organizations(self) -> list[Any]:
        return await self.get_items_with_related('iam.organizations')

    async def get_kg_chunk_entities_with_scope_association_suggestions(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'scope_association_suggestions')

    async def get_all_kg_chunk_entities_with_scope_association_suggestions(self) -> list[Any]:
        return await self.get_items_with_related('scope_association_suggestions')

    async def load_all_kg_chunk_entities_by_chunk_id(self, chunk_id: Any) -> list[Any]:
        return await self.load_items(chunk_id=chunk_id)

    async def filter_all_kg_chunk_entities_by_chunk_id(self, chunk_id: Any) -> list[Any]:
        return await self.filter_items(chunk_id=chunk_id)

    async def load_all_kg_chunk_entities_by_entity_id(self, entity_id: Any) -> list[Any]:
        return await self.load_items(entity_id=entity_id)

    async def filter_all_kg_chunk_entities_by_entity_id(self, entity_id: Any) -> list[Any]:
        return await self.filter_items(entity_id=entity_id)

    async def load_all_kg_chunk_entities_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.load_items(organization_id=organization_id)

    async def filter_all_kg_chunk_entities_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.filter_items(organization_id=organization_id)

    async def load_all_kg_chunk_entities_by_alias_id(self, alias_id: Any) -> list[Any]:
        return await self.load_items(alias_id=alias_id)

    async def filter_all_kg_chunk_entities_by_alias_id(self, alias_id: Any) -> list[Any]:
        return await self.filter_items(alias_id=alias_id)

    async def load_all_kg_chunk_entities_by_ids(self, ids: list[Any]) -> list[Any]:
        return await self.load_items_by_ids(ids)

    def add_computed_field(self, field: str) -> None:
        super().add_computed_field(field)

    def add_relation_field(self, field: str) -> None:
        super().add_relation_field(field)

    @property
    def active_kg_chunk_entities_ids(self) -> set[Any]:
        return self.active_item_ids



class KgChunkEntitiesManager(KgChunkEntitiesBase):
    _instance: KgChunkEntitiesManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> KgChunkEntitiesManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: KgChunkEntities) -> None:
        pass

kg_chunk_entities_manager_instance = KgChunkEntitiesManager()