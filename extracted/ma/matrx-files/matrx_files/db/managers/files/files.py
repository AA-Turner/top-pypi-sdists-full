# File: matrx_files/db/managers/files/files.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_orm import BaseManager, BaseDTO, ModelView, build_output_schema
from matrx_files.db.models_files import Files


# ---------------------------------------------------------------------------
# ModelView (new) — opt-in projection layer.
# Stores results flat on the model instance; no duplication, no nesting.
# To activate: set view_class = FilesView on your manager subclass,
# or pass view_class=FilesView to super().__init__().
# When active, the DTO path below is skipped automatically.
# ---------------------------------------------------------------------------

class FilesView(ModelView[Files]):
    """
    Declarative view for Files.

    Configure what gets fetched and shaped automatically on every load:

      prefetch    — relation names to fetch concurrently (FK / IFK / M2M)
      exclude     — model field names to omit from to_dict() output
      inline_fk   — replace FK id columns with the full related object
                    e.g. {"customer_id": "customer"}

    Add async methods (no leading underscore) for computed fields:

        async def display_name(self, model: Files) -> str:
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
#   - JSON Schema generation: FilesSchema.model_json_schema()
#   - Typed API responses: FilesSchema.model_validate(item.to_dict())
#
# Usage example:
#   @app.get("/{id}", response_model=FilesSchema)
#   async def get_files(id: str):
#       item = await files_manager_instance.load_by_id(id)
#       return item.to_dict()
# ---------------------------------------------------------------------------

try:
    FilesSchema = build_output_schema(Files)
except ImportError:
    FilesSchema = None  # type: ignore[assignment]  # pydantic not installed


# ---------------------------------------------------------------------------
# BaseDTO (default) — active by default, fully backward compatible.
# Extend _process_core_data / _process_metadata with your business logic.
# When you are ready to migrate to the View above, set view_class on your
# manager subclass and this DTO will be bypassed automatically.
# ---------------------------------------------------------------------------

@dataclass
class FilesDTO(BaseDTO[Files]):
    id: str

    async def _initialize_dto(self, model: Files) -> None:
        '''Override to populate DTO fields from the model.'''
        self.id = model.get_cache_key()
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True

    async def _process_core_data(self, model: Files) -> None:
        '''Process core data from the model item.'''
        pass

    async def _process_metadata(self, model: Files) -> None:
        '''Process metadata from the model item.'''
        pass

    async def _initial_validation(self, model: Files) -> None:
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
#   1. Quick: set view_class = FilesView  (replaces DTO automatically)
#   2. Explicit: super().__init__(Files, view_class=FilesView)
# ---------------------------------------------------------------------------

class FilesBase(BaseManager[Files]):
    view_class = None  # DTO is used by default; set to FilesView to opt in

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
            Files,
            dto_class=dto_class or FilesDTO,
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self) -> None:
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Files) -> None:
        pass

    async def create_files(self, **data: Any) -> Files:
        return await self.create_item(**data)

    async def delete_files(self, id: Any) -> bool:
        return await self.delete_item(id)

    async def get_files_with_all_related(self, id: Any) -> tuple[Files, Any]:
        return await self.get_item_with_all_related(id)

    async def load_files_by_id(self, id: Any) -> Files:
        return await self.load_by_id(id)

    async def load_files(self, use_cache: bool = True, **kwargs: Any) -> Files:
        return await self.load_item(use_cache, **kwargs)

    async def update_files(self, id: Any, **updates: Any) -> Files:
        return await self.update_item(id, **updates)

    async def load_all_files(self, **kwargs: Any) -> list[Files]:
        return await self.load_items(**kwargs)

    async def filter_all_files(self, **kwargs: Any) -> list[Files]:
        return await self.filter_items(**kwargs)

    async def get_or_create_files(self, defaults: dict[str, Any] | None = None, **kwargs: Any) -> Files | None:
        return await self.get_or_create(defaults, **kwargs)

    async def get_files_with_docproc_processed_documents(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'docproc.processed_documents')

    async def get_all_files_with_docproc_processed_documents(self) -> list[Any]:
        return await self.get_items_with_related('docproc.processed_documents')

    async def get_files_with_self_reference(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'self_reference')

    async def get_all_files_with_self_reference(self) -> list[Any]:
        return await self.get_items_with_related('self_reference')

    async def get_files_with_folders(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'folders')

    async def get_all_files_with_folders(self) -> list[Any]:
        return await self.get_items_with_related('folders')

    async def get_files_with_iam_users(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.users')

    async def get_all_files_with_iam_users(self) -> list[Any]:
        return await self.get_items_with_related('iam.users')

    async def get_files_with_iam_organizations(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.organizations')

    async def get_all_files_with_iam_organizations(self) -> list[Any]:
        return await self.get_items_with_related('iam.organizations')

    async def get_files_with_public_app_instances(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'public.app_instances')

    async def get_all_files_with_public_app_instances(self) -> list[Any]:
        return await self.get_items_with_related('public.app_instances')

    async def get_files_with_file_rag_jobs(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'file_rag_jobs')

    async def get_all_files_with_file_rag_jobs(self) -> list[Any]:
        return await self.get_items_with_related('file_rag_jobs')

    async def get_files_with_file_versions(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'file_versions')

    async def get_all_files_with_file_versions(self) -> list[Any]:
        return await self.get_items_with_related('file_versions')

    async def get_files_with_analysis(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'analysis')

    async def get_all_files_with_analysis(self) -> list[Any]:
        return await self.get_items_with_related('analysis')

    async def get_files_with_analysis_result(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'analysis_result')

    async def get_all_files_with_analysis_result(self) -> list[Any]:
        return await self.get_items_with_related('analysis_result')

    async def get_files_with_entities(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'entities')

    async def get_all_files_with_entities(self) -> list[Any]:
        return await self.get_items_with_related('entities')

    async def get_files_with_overrides(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'overrides')

    async def get_all_files_with_overrides(self) -> list[Any]:
        return await self.get_items_with_related('overrides')

    async def get_files_with_page_annotations(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'page_annotations')

    async def get_all_files_with_page_annotations(self) -> list[Any]:
        return await self.get_items_with_related('page_annotations')

    async def get_files_with_pages(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'pages')

    async def get_all_files_with_pages(self) -> list[Any]:
        return await self.get_items_with_related('pages')

    async def get_files_with_structure(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'structure')

    async def get_all_files_with_structure(self) -> list[Any]:
        return await self.get_items_with_related('structure')

    async def load_all_files_by_created_by(self, created_by: Any) -> list[Any]:
        return await self.load_items(created_by=created_by)

    async def filter_all_files_by_created_by(self, created_by: Any) -> list[Any]:
        return await self.filter_items(created_by=created_by)

    async def load_all_files_by_parent_folder_id(self, parent_folder_id: Any) -> list[Any]:
        return await self.load_items(parent_folder_id=parent_folder_id)

    async def filter_all_files_by_parent_folder_id(self, parent_folder_id: Any) -> list[Any]:
        return await self.filter_items(parent_folder_id=parent_folder_id)

    async def load_all_files_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.load_items(organization_id=organization_id)

    async def filter_all_files_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.filter_items(organization_id=organization_id)

    async def load_all_files_by_parent_file_id(self, parent_file_id: Any) -> list[Any]:
        return await self.load_items(parent_file_id=parent_file_id)

    async def filter_all_files_by_parent_file_id(self, parent_file_id: Any) -> list[Any]:
        return await self.filter_items(parent_file_id=parent_file_id)

    async def load_all_files_by_duplicate_of_file_id(self, duplicate_of_file_id: Any) -> list[Any]:
        return await self.load_items(duplicate_of_file_id=duplicate_of_file_id)

    async def filter_all_files_by_duplicate_of_file_id(self, duplicate_of_file_id: Any) -> list[Any]:
        return await self.filter_items(duplicate_of_file_id=duplicate_of_file_id)

    async def load_all_files_by_canonical_processed_document_id(self, canonical_processed_document_id: Any) -> list[Any]:
        return await self.load_items(canonical_processed_document_id=canonical_processed_document_id)

    async def filter_all_files_by_canonical_processed_document_id(self, canonical_processed_document_id: Any) -> list[Any]:
        return await self.filter_items(canonical_processed_document_id=canonical_processed_document_id)

    async def load_all_files_by_updated_by(self, updated_by: Any) -> list[Any]:
        return await self.load_items(updated_by=updated_by)

    async def filter_all_files_by_updated_by(self, updated_by: Any) -> list[Any]:
        return await self.filter_items(updated_by=updated_by)

    async def load_all_files_by_origin_device_id(self, origin_device_id: Any) -> list[Any]:
        return await self.load_items(origin_device_id=origin_device_id)

    async def filter_all_files_by_origin_device_id(self, origin_device_id: Any) -> list[Any]:
        return await self.filter_items(origin_device_id=origin_device_id)

    async def load_all_files_by_shown_to(self, shown_to: Any) -> list[Any]:
        return await self.load_items(shown_to=shown_to)

    async def filter_all_files_by_shown_to(self, shown_to: Any) -> list[Any]:
        return await self.filter_items(shown_to=shown_to)

    async def load_all_files_by_ids(self, ids: list[Any]) -> list[Any]:
        return await self.load_items_by_ids(ids)

    def add_computed_field(self, field: str) -> None:
        super().add_computed_field(field)

    def add_relation_field(self, field: str) -> None:
        super().add_relation_field(field)

    @property
    def active_files_ids(self) -> set[Any]:
        return self.active_item_ids



class FilesManager(FilesBase):
    _instance: FilesManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> FilesManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: Files) -> None:
        pass

files_manager_instance = FilesManager()