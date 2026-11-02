# File: matrx_rag/db/managers/rag/kg_edges.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_orm import BaseManager, BaseDTO, ModelView, build_output_schema
from matrx_rag.db.models_rag import KgEdges


# ---------------------------------------------------------------------------
# ModelView (new) — opt-in projection layer.
# Stores results flat on the model instance; no duplication, no nesting.
# To activate: set view_class = KgEdgesView on your manager subclass,
# or pass view_class=KgEdgesView to super().__init__().
# When active, the DTO path below is skipped automatically.
# ---------------------------------------------------------------------------

class KgEdgesView(ModelView[KgEdges]):
    """
    Declarative view for KgEdges.

    Configure what gets fetched and shaped automatically on every load:

      prefetch    — relation names to fetch concurrently (FK / IFK / M2M)
      exclude     — model field names to omit from to_dict() output
      inline_fk   — replace FK id columns with the full related object
                    e.g. {"customer_id": "customer"}

    Add async methods (no leading underscore) for computed fields:

        async def display_name(self, model: KgEdges) -> str:
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
#   - JSON Schema generation: KgEdgesSchema.model_json_schema()
#   - Typed API responses: KgEdgesSchema.model_validate(item.to_dict())
#
# Usage example:
#   @app.get("/{id}", response_model=KgEdgesSchema)
#   async def get_kg_edges(id: str):
#       item = await kg_edges_manager_instance.load_by_id(id)
#       return item.to_dict()
# ---------------------------------------------------------------------------

try:
    KgEdgesSchema = build_output_schema(KgEdges)
except ImportError:
    KgEdgesSchema = None  # type: ignore[assignment]  # pydantic not installed


# ---------------------------------------------------------------------------
# BaseDTO (default) — active by default, fully backward compatible.
# Extend _process_core_data / _process_metadata with your business logic.
# When you are ready to migrate to the View above, set view_class on your
# manager subclass and this DTO will be bypassed automatically.
# ---------------------------------------------------------------------------

@dataclass
class KgEdgesDTO(BaseDTO[KgEdges]):
    id: str

    async def _initialize_dto(self, model: KgEdges) -> None:
        '''Override to populate DTO fields from the model.'''
        self.id = model.get_cache_key()
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True

    async def _process_core_data(self, model: KgEdges) -> None:
        '''Process core data from the model item.'''
        pass

    async def _process_metadata(self, model: KgEdges) -> None:
        '''Process metadata from the model item.'''
        pass

    async def _initial_validation(self, model: KgEdges) -> None:
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
#   1. Quick: set view_class = KgEdgesView  (replaces DTO automatically)
#   2. Explicit: super().__init__(KgEdges, view_class=KgEdgesView)
# ---------------------------------------------------------------------------

class KgEdgesBase(BaseManager[KgEdges]):
    view_class = None  # DTO is used by default; set to KgEdgesView to opt in

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
            KgEdges,
            dto_class=dto_class or KgEdgesDTO,
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self) -> None:
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgEdges) -> None:
        pass

    async def create_kg_edges(self, **data: Any) -> KgEdges:
        return await self.create_item(**data)

    async def delete_kg_edges(self, id: Any) -> bool:
        return await self.delete_item(id)

    async def get_kg_edges_with_all_related(self, id: Any) -> tuple[KgEdges, Any]:
        return await self.get_item_with_all_related(id)

    async def load_kg_edges_by_id(self, id: Any) -> KgEdges:
        return await self.load_by_id(id)

    async def load_kg_edges(self, use_cache: bool = True, **kwargs: Any) -> KgEdges:
        return await self.load_item(use_cache, **kwargs)

    async def update_kg_edges(self, id: Any, **updates: Any) -> KgEdges:
        return await self.update_item(id, **updates)

    async def load_all_kg_edges(self, **kwargs: Any) -> list[KgEdges]:
        return await self.load_items(**kwargs)

    async def filter_all_kg_edges(self, **kwargs: Any) -> list[KgEdges]:
        return await self.filter_items(**kwargs)

    async def get_or_create_kg_edges(self, defaults: dict[str, Any] | None = None, **kwargs: Any) -> KgEdges | None:
        return await self.get_or_create(defaults, **kwargs)

    async def get_kg_edges_with_kg_entities(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_entities')

    async def get_all_kg_edges_with_kg_entities(self) -> list[Any]:
        return await self.get_items_with_related('kg_entities')

    async def get_kg_edges_with_iam_organizations(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.organizations')

    async def get_all_kg_edges_with_iam_organizations(self) -> list[Any]:
        return await self.get_items_with_related('iam.organizations')

    async def get_kg_edges_with_kg_chunks(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_chunks')

    async def get_all_kg_edges_with_kg_chunks(self) -> list[Any]:
        return await self.get_items_with_related('kg_chunks')

    async def load_all_kg_edges_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.load_items(organization_id=organization_id)

    async def filter_all_kg_edges_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.filter_items(organization_id=organization_id)

    async def load_all_kg_edges_by_src_id(self, src_id: Any) -> list[Any]:
        return await self.load_items(src_id=src_id)

    async def filter_all_kg_edges_by_src_id(self, src_id: Any) -> list[Any]:
        return await self.filter_items(src_id=src_id)

    async def load_all_kg_edges_by_dst_id(self, dst_id: Any) -> list[Any]:
        return await self.load_items(dst_id=dst_id)

    async def filter_all_kg_edges_by_dst_id(self, dst_id: Any) -> list[Any]:
        return await self.filter_items(dst_id=dst_id)

    async def load_all_kg_edges_by_source_chunk_id(self, source_chunk_id: Any) -> list[Any]:
        return await self.load_items(source_chunk_id=source_chunk_id)

    async def filter_all_kg_edges_by_source_chunk_id(self, source_chunk_id: Any) -> list[Any]:
        return await self.filter_items(source_chunk_id=source_chunk_id)

    async def load_all_kg_edges_by_ids(self, ids: list[Any]) -> list[Any]:
        return await self.load_items_by_ids(ids)

    def add_computed_field(self, field: str) -> None:
        super().add_computed_field(field)

    def add_relation_field(self, field: str) -> None:
        super().add_relation_field(field)

    @property
    def active_kg_edges_ids(self) -> set[Any]:
        return self.active_item_ids



class KgEdgesManager(KgEdgesBase):
    _instance: KgEdgesManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> KgEdgesManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: KgEdges) -> None:
        pass

kg_edges_manager_instance = KgEdgesManager()