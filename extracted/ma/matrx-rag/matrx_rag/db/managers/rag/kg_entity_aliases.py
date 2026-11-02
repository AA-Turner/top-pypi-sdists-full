# File: matrx_rag/db/managers/rag/kg_entity_aliases.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_orm import BaseManager, BaseDTO, ModelView, build_output_schema
from matrx_rag.db.models_rag import KgEntityAliases


# ---------------------------------------------------------------------------
# ModelView (new) — opt-in projection layer.
# Stores results flat on the model instance; no duplication, no nesting.
# To activate: set view_class = KgEntityAliasesView on your manager subclass,
# or pass view_class=KgEntityAliasesView to super().__init__().
# When active, the DTO path below is skipped automatically.
# ---------------------------------------------------------------------------

class KgEntityAliasesView(ModelView[KgEntityAliases]):
    """
    Declarative view for KgEntityAliases.

    Configure what gets fetched and shaped automatically on every load:

      prefetch    — relation names to fetch concurrently (FK / IFK / M2M)
      exclude     — model field names to omit from to_dict() output
      inline_fk   — replace FK id columns with the full related object
                    e.g. {"customer_id": "customer"}

    Add async methods (no leading underscore) for computed fields:

        async def display_name(self, model: KgEntityAliases) -> str:
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
#   - JSON Schema generation: KgEntityAliasesSchema.model_json_schema()
#   - Typed API responses: KgEntityAliasesSchema.model_validate(item.to_dict())
#
# Usage example:
#   @app.get("/{id}", response_model=KgEntityAliasesSchema)
#   async def get_kg_entity_aliases(id: str):
#       item = await kg_entity_aliases_manager_instance.load_by_id(id)
#       return item.to_dict()
# ---------------------------------------------------------------------------

try:
    KgEntityAliasesSchema = build_output_schema(KgEntityAliases)
except ImportError:
    KgEntityAliasesSchema = None  # type: ignore[assignment]  # pydantic not installed


# ---------------------------------------------------------------------------
# BaseDTO (default) — active by default, fully backward compatible.
# Extend _process_core_data / _process_metadata with your business logic.
# When you are ready to migrate to the View above, set view_class on your
# manager subclass and this DTO will be bypassed automatically.
# ---------------------------------------------------------------------------

@dataclass
class KgEntityAliasesDTO(BaseDTO[KgEntityAliases]):
    id: str

    async def _initialize_dto(self, model: KgEntityAliases) -> None:
        '''Override to populate DTO fields from the model.'''
        self.id = model.get_cache_key()
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True

    async def _process_core_data(self, model: KgEntityAliases) -> None:
        '''Process core data from the model item.'''
        pass

    async def _process_metadata(self, model: KgEntityAliases) -> None:
        '''Process metadata from the model item.'''
        pass

    async def _initial_validation(self, model: KgEntityAliases) -> None:
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
#   1. Quick: set view_class = KgEntityAliasesView  (replaces DTO automatically)
#   2. Explicit: super().__init__(KgEntityAliases, view_class=KgEntityAliasesView)
# ---------------------------------------------------------------------------

class KgEntityAliasesBase(BaseManager[KgEntityAliases]):
    view_class = None  # DTO is used by default; set to KgEntityAliasesView to opt in

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
            KgEntityAliases,
            dto_class=dto_class or KgEntityAliasesDTO,
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self) -> None:
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgEntityAliases) -> None:
        pass

    async def create_kg_entity_aliases(self, **data: Any) -> KgEntityAliases:
        return await self.create_item(**data)

    async def delete_kg_entity_aliases(self, id: Any) -> bool:
        return await self.delete_item(id)

    async def get_kg_entity_aliases_with_all_related(self, id: Any) -> tuple[KgEntityAliases, Any]:
        return await self.get_item_with_all_related(id)

    async def load_kg_entity_aliases_by_id(self, id: Any) -> KgEntityAliases:
        return await self.load_by_id(id)

    async def load_kg_entity_aliases(self, use_cache: bool = True, **kwargs: Any) -> KgEntityAliases:
        return await self.load_item(use_cache, **kwargs)

    async def update_kg_entity_aliases(self, id: Any, **updates: Any) -> KgEntityAliases:
        return await self.update_item(id, **updates)

    async def load_all_kg_entity_aliases(self, **kwargs: Any) -> list[KgEntityAliases]:
        return await self.load_items(**kwargs)

    async def filter_all_kg_entity_aliases(self, **kwargs: Any) -> list[KgEntityAliases]:
        return await self.filter_items(**kwargs)

    async def get_or_create_kg_entity_aliases(self, defaults: dict[str, Any] | None = None, **kwargs: Any) -> KgEntityAliases | None:
        return await self.get_or_create(defaults, **kwargs)

    async def get_kg_entity_aliases_with_kg_entities(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_entities')

    async def get_all_kg_entity_aliases_with_kg_entities(self) -> list[Any]:
        return await self.get_items_with_related('kg_entities')

    async def get_kg_entity_aliases_with_iam_organizations(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.organizations')

    async def get_all_kg_entity_aliases_with_iam_organizations(self) -> list[Any]:
        return await self.get_items_with_related('iam.organizations')

    async def get_kg_entity_aliases_with_kg_chunk_entities(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_chunk_entities')

    async def get_all_kg_entity_aliases_with_kg_chunk_entities(self) -> list[Any]:
        return await self.get_items_with_related('kg_chunk_entities')

    async def load_all_kg_entity_aliases_by_entity_id(self, entity_id: Any) -> list[Any]:
        return await self.load_items(entity_id=entity_id)

    async def filter_all_kg_entity_aliases_by_entity_id(self, entity_id: Any) -> list[Any]:
        return await self.filter_items(entity_id=entity_id)

    async def load_all_kg_entity_aliases_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.load_items(organization_id=organization_id)

    async def filter_all_kg_entity_aliases_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.filter_items(organization_id=organization_id)

    async def load_all_kg_entity_aliases_by_ids(self, ids: list[Any]) -> list[Any]:
        return await self.load_items_by_ids(ids)

    def add_computed_field(self, field: str) -> None:
        super().add_computed_field(field)

    def add_relation_field(self, field: str) -> None:
        super().add_relation_field(field)

    @property
    def active_kg_entity_aliases_ids(self) -> set[Any]:
        return self.active_item_ids



class KgEntityAliasesManager(KgEntityAliasesBase):
    _instance: KgEntityAliasesManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> KgEntityAliasesManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: KgEntityAliases) -> None:
        pass

kg_entity_aliases_manager_instance = KgEntityAliasesManager()