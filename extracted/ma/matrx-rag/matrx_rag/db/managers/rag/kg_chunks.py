# File: matrx_rag/db/managers/rag/kg_chunks.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_orm import BaseManager, BaseDTO, ModelView, build_output_schema
from matrx_rag.db.models_rag import KgChunks


# ---------------------------------------------------------------------------
# ModelView (new) — opt-in projection layer.
# Stores results flat on the model instance; no duplication, no nesting.
# To activate: set view_class = KgChunksView on your manager subclass,
# or pass view_class=KgChunksView to super().__init__().
# When active, the DTO path below is skipped automatically.
# ---------------------------------------------------------------------------

class KgChunksView(ModelView[KgChunks]):
    """
    Declarative view for KgChunks.

    Configure what gets fetched and shaped automatically on every load:

      prefetch    — relation names to fetch concurrently (FK / IFK / M2M)
      exclude     — model field names to omit from to_dict() output
      inline_fk   — replace FK id columns with the full related object
                    e.g. {"customer_id": "customer"}

    Add async methods (no leading underscore) for computed fields:

        async def display_name(self, model: KgChunks) -> str:
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
#   - JSON Schema generation: KgChunksSchema.model_json_schema()
#   - Typed API responses: KgChunksSchema.model_validate(item.to_dict())
#
# Usage example:
#   @app.get("/{id}", response_model=KgChunksSchema)
#   async def get_kg_chunks(id: str):
#       item = await kg_chunks_manager_instance.load_by_id(id)
#       return item.to_dict()
# ---------------------------------------------------------------------------

try:
    KgChunksSchema = build_output_schema(KgChunks)
except ImportError:
    KgChunksSchema = None  # type: ignore[assignment]  # pydantic not installed


# ---------------------------------------------------------------------------
# BaseDTO (default) — active by default, fully backward compatible.
# Extend _process_core_data / _process_metadata with your business logic.
# When you are ready to migrate to the View above, set view_class on your
# manager subclass and this DTO will be bypassed automatically.
# ---------------------------------------------------------------------------

@dataclass
class KgChunksDTO(BaseDTO[KgChunks]):
    id: str

    async def _initialize_dto(self, model: KgChunks) -> None:
        '''Override to populate DTO fields from the model.'''
        self.id = model.get_cache_key()
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True

    async def _process_core_data(self, model: KgChunks) -> None:
        '''Process core data from the model item.'''
        pass

    async def _process_metadata(self, model: KgChunks) -> None:
        '''Process metadata from the model item.'''
        pass

    async def _initial_validation(self, model: KgChunks) -> None:
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
#   1. Quick: set view_class = KgChunksView  (replaces DTO automatically)
#   2. Explicit: super().__init__(KgChunks, view_class=KgChunksView)
# ---------------------------------------------------------------------------

class KgChunksBase(BaseManager[KgChunks]):
    view_class = None  # DTO is used by default; set to KgChunksView to opt in

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
            KgChunks,
            dto_class=dto_class or KgChunksDTO,
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self) -> None:
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgChunks) -> None:
        pass

    async def create_kg_chunks(self, **data: Any) -> KgChunks:
        return await self.create_item(**data)

    async def delete_kg_chunks(self, id: Any) -> bool:
        return await self.delete_item(id)

    async def get_kg_chunks_with_all_related(self, id: Any) -> tuple[KgChunks, Any]:
        return await self.get_item_with_all_related(id)

    async def load_kg_chunks_by_id(self, id: Any) -> KgChunks:
        return await self.load_by_id(id)

    async def load_kg_chunks(self, use_cache: bool = True, **kwargs: Any) -> KgChunks:
        return await self.load_item(use_cache, **kwargs)

    async def update_kg_chunks(self, id: Any, **updates: Any) -> KgChunks:
        return await self.update_item(id, **updates)

    async def load_all_kg_chunks(self, **kwargs: Any) -> list[KgChunks]:
        return await self.load_items(**kwargs)

    async def filter_all_kg_chunks(self, **kwargs: Any) -> list[KgChunks]:
        return await self.filter_items(**kwargs)

    async def get_or_create_kg_chunks(self, defaults: dict[str, Any] | None = None, **kwargs: Any) -> KgChunks | None:
        return await self.get_or_create(defaults, **kwargs)

    async def get_kg_chunks_with_agent_definition(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'agent.definition')

    async def get_all_kg_chunks_with_agent_definition(self) -> list[Any]:
        return await self.get_items_with_related('agent.definition')

    async def get_kg_chunks_with_self_reference(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'self_reference')

    async def get_all_kg_chunks_with_self_reference(self) -> list[Any]:
        return await self.get_items_with_related('self_reference')

    async def get_kg_chunks_with_docproc_page_extraction_results(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'docproc.page_extraction_results')

    async def get_all_kg_chunks_with_docproc_page_extraction_results(self) -> list[Any]:
        return await self.get_items_with_related('docproc.page_extraction_results')

    async def get_kg_chunks_with_docproc_page_extraction_runs(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'docproc.page_extraction_runs')

    async def get_all_kg_chunks_with_docproc_page_extraction_runs(self) -> list[Any]:
        return await self.get_items_with_related('docproc.page_extraction_runs')

    async def get_kg_chunks_with_iam_organizations(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.organizations')

    async def get_all_kg_chunks_with_iam_organizations(self) -> list[Any]:
        return await self.get_items_with_related('iam.organizations')

    async def get_kg_chunks_with_docproc_processed_document_pages(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'docproc.processed_document_pages')

    async def get_all_kg_chunks_with_docproc_processed_document_pages(self) -> list[Any]:
        return await self.get_items_with_related('docproc.processed_document_pages')

    async def get_kg_chunks_with_docproc_processed_documents(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'docproc.processed_documents')

    async def get_all_kg_chunks_with_docproc_processed_documents(self) -> list[Any]:
        return await self.get_items_with_related('docproc.processed_documents')

    async def get_kg_chunks_with_iam_users(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.users')

    async def get_all_kg_chunks_with_iam_users(self) -> list[Any]:
        return await self.get_items_with_related('iam.users')

    async def get_kg_chunks_with_embeddings_google_gemini_2_1536(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'embeddings_google_gemini_2_1536')

    async def get_all_kg_chunks_with_embeddings_google_gemini_2_1536(self) -> list[Any]:
        return await self.get_items_with_related('embeddings_google_gemini_2_1536')

    async def get_kg_chunks_with_embeddings_oai_3_small_1536(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'embeddings_oai_3_small_1536')

    async def get_all_kg_chunks_with_embeddings_oai_3_small_1536(self) -> list[Any]:
        return await self.get_items_with_related('embeddings_oai_3_small_1536')

    async def get_kg_chunks_with_embeddings_voyage_4_large_1024(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'embeddings_voyage_4_large_1024')

    async def get_all_kg_chunks_with_embeddings_voyage_4_large_1024(self) -> list[Any]:
        return await self.get_items_with_related('embeddings_voyage_4_large_1024')

    async def get_kg_chunks_with_embeddings_voyage_code_3_1024(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'embeddings_voyage_code_3_1024')

    async def get_all_kg_chunks_with_embeddings_voyage_code_3_1024(self) -> list[Any]:
        return await self.get_items_with_related('embeddings_voyage_code_3_1024')

    async def get_kg_chunks_with_kg_chunk_entities(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_chunk_entities')

    async def get_all_kg_chunks_with_kg_chunk_entities(self) -> list[Any]:
        return await self.get_items_with_related('kg_chunk_entities')

    async def get_kg_chunks_with_kg_edges(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_edges')

    async def get_all_kg_chunks_with_kg_edges(self) -> list[Any]:
        return await self.get_items_with_related('kg_edges')

    async def get_kg_chunks_with_kg_value_matches(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'kg_value_matches')

    async def get_all_kg_chunks_with_kg_value_matches(self) -> list[Any]:
        return await self.get_items_with_related('kg_value_matches')

    async def get_kg_chunks_with_scope_item_value_suggestions(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'scope_item_value_suggestions')

    async def get_all_kg_chunks_with_scope_item_value_suggestions(self) -> list[Any]:
        return await self.get_items_with_related('scope_item_value_suggestions')

    async def load_all_kg_chunks_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.load_items(organization_id=organization_id)

    async def filter_all_kg_chunks_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.filter_items(organization_id=organization_id)

    async def load_all_kg_chunks_by_parent_chunk_id(self, parent_chunk_id: Any) -> list[Any]:
        return await self.load_items(parent_chunk_id=parent_chunk_id)

    async def filter_all_kg_chunks_by_parent_chunk_id(self, parent_chunk_id: Any) -> list[Any]:
        return await self.filter_items(parent_chunk_id=parent_chunk_id)

    async def load_all_kg_chunks_by_processed_document_id(self, processed_document_id: Any) -> list[Any]:
        return await self.load_items(processed_document_id=processed_document_id)

    async def filter_all_kg_chunks_by_processed_document_id(self, processed_document_id: Any) -> list[Any]:
        return await self.filter_items(processed_document_id=processed_document_id)

    async def load_all_kg_chunks_by_primary_page_id(self, primary_page_id: Any) -> list[Any]:
        return await self.load_items(primary_page_id=primary_page_id)

    async def filter_all_kg_chunks_by_primary_page_id(self, primary_page_id: Any) -> list[Any]:
        return await self.filter_items(primary_page_id=primary_page_id)

    async def load_all_kg_chunks_by_page_numbers(self, page_numbers: Any) -> list[Any]:
        return await self.load_items(page_numbers=page_numbers)

    async def filter_all_kg_chunks_by_page_numbers(self, page_numbers: Any) -> list[Any]:
        return await self.filter_items(page_numbers=page_numbers)

    async def load_all_kg_chunks_by_derived_from_chunk_id(self, derived_from_chunk_id: Any) -> list[Any]:
        return await self.load_items(derived_from_chunk_id=derived_from_chunk_id)

    async def filter_all_kg_chunks_by_derived_from_chunk_id(self, derived_from_chunk_id: Any) -> list[Any]:
        return await self.filter_items(derived_from_chunk_id=derived_from_chunk_id)

    async def load_all_kg_chunks_by_agent_id(self, agent_id: Any) -> list[Any]:
        return await self.load_items(agent_id=agent_id)

    async def filter_all_kg_chunks_by_agent_id(self, agent_id: Any) -> list[Any]:
        return await self.filter_items(agent_id=agent_id)

    async def load_all_kg_chunks_by_extraction_run_id(self, extraction_run_id: Any) -> list[Any]:
        return await self.load_items(extraction_run_id=extraction_run_id)

    async def filter_all_kg_chunks_by_extraction_run_id(self, extraction_run_id: Any) -> list[Any]:
        return await self.filter_items(extraction_run_id=extraction_run_id)

    async def load_all_kg_chunks_by_extraction_result_id(self, extraction_result_id: Any) -> list[Any]:
        return await self.load_items(extraction_result_id=extraction_result_id)

    async def filter_all_kg_chunks_by_extraction_result_id(self, extraction_result_id: Any) -> list[Any]:
        return await self.filter_items(extraction_result_id=extraction_result_id)

    async def load_all_kg_chunks_by_created_by(self, created_by: Any) -> list[Any]:
        return await self.load_items(created_by=created_by)

    async def filter_all_kg_chunks_by_created_by(self, created_by: Any) -> list[Any]:
        return await self.filter_items(created_by=created_by)

    async def load_all_kg_chunks_by_updated_by(self, updated_by: Any) -> list[Any]:
        return await self.load_items(updated_by=updated_by)

    async def filter_all_kg_chunks_by_updated_by(self, updated_by: Any) -> list[Any]:
        return await self.filter_items(updated_by=updated_by)

    async def load_all_kg_chunks_by_ids(self, ids: list[Any]) -> list[Any]:
        return await self.load_items_by_ids(ids)

    def add_computed_field(self, field: str) -> None:
        super().add_computed_field(field)

    def add_relation_field(self, field: str) -> None:
        super().add_relation_field(field)

    @property
    def active_kg_chunks_ids(self) -> set[Any]:
        return self.active_item_ids



class KgChunksManager(KgChunksBase):
    _instance: KgChunksManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> KgChunksManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: KgChunks) -> None:
        pass

kg_chunks_manager_instance = KgChunksManager()