# File: matrx_rag/db/managers/rag/library_audit_log.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_orm import BaseManager, BaseDTO, ModelView, build_output_schema
from matrx_rag.db.models_rag import LibraryAuditLog


# ---------------------------------------------------------------------------
# ModelView (new) — opt-in projection layer.
# Stores results flat on the model instance; no duplication, no nesting.
# To activate: set view_class = LibraryAuditLogView on your manager subclass,
# or pass view_class=LibraryAuditLogView to super().__init__().
# When active, the DTO path below is skipped automatically.
# ---------------------------------------------------------------------------

class LibraryAuditLogView(ModelView[LibraryAuditLog]):
    """
    Declarative view for LibraryAuditLog.

    Configure what gets fetched and shaped automatically on every load:

      prefetch    — relation names to fetch concurrently (FK / IFK / M2M)
      exclude     — model field names to omit from to_dict() output
      inline_fk   — replace FK id columns with the full related object
                    e.g. {"customer_id": "customer"}

    Add async methods (no leading underscore) for computed fields:

        async def display_name(self, model: LibraryAuditLog) -> str:
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
#   - JSON Schema generation: LibraryAuditLogSchema.model_json_schema()
#   - Typed API responses: LibraryAuditLogSchema.model_validate(item.to_dict())
#
# Usage example:
#   @app.get("/{id}", response_model=LibraryAuditLogSchema)
#   async def get_library_audit_log(id: str):
#       item = await library_audit_log_manager_instance.load_by_id(id)
#       return item.to_dict()
# ---------------------------------------------------------------------------

try:
    LibraryAuditLogSchema = build_output_schema(LibraryAuditLog)
except ImportError:
    LibraryAuditLogSchema = None  # type: ignore[assignment]  # pydantic not installed


# ---------------------------------------------------------------------------
# BaseDTO (default) — active by default, fully backward compatible.
# Extend _process_core_data / _process_metadata with your business logic.
# When you are ready to migrate to the View above, set view_class on your
# manager subclass and this DTO will be bypassed automatically.
# ---------------------------------------------------------------------------

@dataclass
class LibraryAuditLogDTO(BaseDTO[LibraryAuditLog]):
    id: str

    async def _initialize_dto(self, model: LibraryAuditLog) -> None:
        '''Override to populate DTO fields from the model.'''
        self.id = model.get_cache_key()
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True

    async def _process_core_data(self, model: LibraryAuditLog) -> None:
        '''Process core data from the model item.'''
        pass

    async def _process_metadata(self, model: LibraryAuditLog) -> None:
        '''Process metadata from the model item.'''
        pass

    async def _initial_validation(self, model: LibraryAuditLog) -> None:
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
#   1. Quick: set view_class = LibraryAuditLogView  (replaces DTO automatically)
#   2. Explicit: super().__init__(LibraryAuditLog, view_class=LibraryAuditLogView)
# ---------------------------------------------------------------------------

class LibraryAuditLogBase(BaseManager[LibraryAuditLog]):
    view_class = None  # DTO is used by default; set to LibraryAuditLogView to opt in

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
            LibraryAuditLog,
            dto_class=dto_class or LibraryAuditLogDTO,
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self) -> None:
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: LibraryAuditLog) -> None:
        pass

    async def create_library_audit_log(self, **data: Any) -> LibraryAuditLog:
        return await self.create_item(**data)

    async def delete_library_audit_log(self, id: Any) -> bool:
        return await self.delete_item(id)

    async def get_library_audit_log_with_all_related(self, id: Any) -> tuple[LibraryAuditLog, Any]:
        return await self.get_item_with_all_related(id)

    async def load_library_audit_log_by_id(self, id: Any) -> LibraryAuditLog:
        return await self.load_by_id(id)

    async def load_library_audit_log(self, use_cache: bool = True, **kwargs: Any) -> LibraryAuditLog:
        return await self.load_item(use_cache, **kwargs)

    async def update_library_audit_log(self, id: Any, **updates: Any) -> LibraryAuditLog:
        return await self.update_item(id, **updates)

    async def load_library_audit_logs(self, **kwargs: Any) -> list[LibraryAuditLog]:
        return await self.load_items(**kwargs)

    async def filter_library_audit_logs(self, **kwargs: Any) -> list[LibraryAuditLog]:
        return await self.filter_items(**kwargs)

    async def get_or_create_library_audit_log(self, defaults: dict[str, Any] | None = None, **kwargs: Any) -> LibraryAuditLog | None:
        return await self.get_or_create(defaults, **kwargs)

    async def get_library_audit_log_with_iam_organizations(self, id: Any) -> tuple[Any, Any]:
        return await self.get_item_with_related(id, 'iam.organizations')

    async def get_library_audit_logs_with_iam_organizations(self) -> list[Any]:
        return await self.get_items_with_related('iam.organizations')

    async def load_library_audit_logs_by_target_organization_id(self, target_organization_id: Any) -> list[Any]:
        return await self.load_items(target_organization_id=target_organization_id)

    async def filter_library_audit_logs_by_target_organization_id(self, target_organization_id: Any) -> list[Any]:
        return await self.filter_items(target_organization_id=target_organization_id)

    async def load_library_audit_logs_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.load_items(organization_id=organization_id)

    async def filter_library_audit_logs_by_organization_id(self, organization_id: Any) -> list[Any]:
        return await self.filter_items(organization_id=organization_id)

    async def load_library_audit_logs_by_ids(self, ids: list[Any]) -> list[Any]:
        return await self.load_items_by_ids(ids)

    def add_computed_field(self, field: str) -> None:
        super().add_computed_field(field)

    def add_relation_field(self, field: str) -> None:
        super().add_relation_field(field)

    @property
    def active_library_audit_log_ids(self) -> set[Any]:
        return self.active_item_ids



class LibraryAuditLogManager(LibraryAuditLogBase):
    _instance: LibraryAuditLogManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> LibraryAuditLogManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: LibraryAuditLog) -> None:
        pass

library_audit_log_manager_instance = LibraryAuditLogManager()