# File: matrx_files/db/managers/files/rate_limit_buckets.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_orm import BaseManager, BaseDTO, ModelView, build_output_schema
from matrx_files.db.models_files import RateLimitBuckets


# ---------------------------------------------------------------------------
# ModelView (new) — opt-in projection layer.
# Stores results flat on the model instance; no duplication, no nesting.
# To activate: set view_class = RateLimitBucketsView on your manager subclass,
# or pass view_class=RateLimitBucketsView to super().__init__().
# When active, the DTO path below is skipped automatically.
# ---------------------------------------------------------------------------

class RateLimitBucketsView(ModelView[RateLimitBuckets]):
    """
    Declarative view for RateLimitBuckets.

    Configure what gets fetched and shaped automatically on every load:

      prefetch    — relation names to fetch concurrently (FK / IFK / M2M)
      exclude     — model field names to omit from to_dict() output
      inline_fk   — replace FK id columns with the full related object
                    e.g. {"customer_id": "customer"}

    Add async methods (no leading underscore) for computed fields:

        async def display_name(self, model: RateLimitBuckets) -> str:
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
#   - JSON Schema generation: RateLimitBucketsSchema.model_json_schema()
#   - Typed API responses: RateLimitBucketsSchema.model_validate(item.to_dict())
#
# Usage example:
#   @app.get("/{id}", response_model=RateLimitBucketsSchema)
#   async def get_rate_limit_buckets(id: str):
#       item = await rate_limit_buckets_manager_instance.load_by_id(id)
#       return item.to_dict()
# ---------------------------------------------------------------------------

try:
    RateLimitBucketsSchema = build_output_schema(RateLimitBuckets)
except ImportError:
    RateLimitBucketsSchema = None  # type: ignore[assignment]  # pydantic not installed


# ---------------------------------------------------------------------------
# BaseDTO (default) — active by default, fully backward compatible.
# Extend _process_core_data / _process_metadata with your business logic.
# When you are ready to migrate to the View above, set view_class on your
# manager subclass and this DTO will be bypassed automatically.
# ---------------------------------------------------------------------------

@dataclass
class RateLimitBucketsDTO(BaseDTO[RateLimitBuckets]):
    id: str

    async def _initialize_dto(self, model: RateLimitBuckets) -> None:
        '''Override to populate DTO fields from the model.'''
        self.id = model.get_cache_key()
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True

    async def _process_core_data(self, model: RateLimitBuckets) -> None:
        '''Process core data from the model item.'''
        pass

    async def _process_metadata(self, model: RateLimitBuckets) -> None:
        '''Process metadata from the model item.'''
        pass

    async def _initial_validation(self, model: RateLimitBuckets) -> None:
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
#   1. Quick: set view_class = RateLimitBucketsView  (replaces DTO automatically)
#   2. Explicit: super().__init__(RateLimitBuckets, view_class=RateLimitBucketsView)
# ---------------------------------------------------------------------------

class RateLimitBucketsBase(BaseManager[RateLimitBuckets]):
    view_class = None  # DTO is used by default; set to RateLimitBucketsView to opt in

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
            RateLimitBuckets,
            dto_class=dto_class or RateLimitBucketsDTO,
            fetch_on_init_limit=fetch_on_init_limit,
            FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
        )

    def _initialize_manager(self) -> None:
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: RateLimitBuckets) -> None:
        pass

    async def create_rate_limit_buckets(self, **data: Any) -> RateLimitBuckets:
        return await self.create_item(**data)

    async def delete_rate_limit_buckets(self, id: Any) -> bool:
        return await self.delete_item(id)

    async def get_rate_limit_buckets_with_all_related(self, id: Any) -> tuple[RateLimitBuckets, Any]:
        return await self.get_item_with_all_related(id)

    async def load_rate_limit_buckets_by_id(self, id: Any) -> RateLimitBuckets:
        return await self.load_by_id(id)

    async def load_rate_limit_buckets(self, use_cache: bool = True, **kwargs: Any) -> RateLimitBuckets:
        return await self.load_item(use_cache, **kwargs)

    async def update_rate_limit_buckets(self, id: Any, **updates: Any) -> RateLimitBuckets:
        return await self.update_item(id, **updates)

    async def load_all_rate_limit_buckets(self, **kwargs: Any) -> list[RateLimitBuckets]:
        return await self.load_items(**kwargs)

    async def filter_all_rate_limit_buckets(self, **kwargs: Any) -> list[RateLimitBuckets]:
        return await self.filter_items(**kwargs)

    async def get_or_create_rate_limit_buckets(self, defaults: dict[str, Any] | None = None, **kwargs: Any) -> RateLimitBuckets | None:
        return await self.get_or_create(defaults, **kwargs)

    async def load_all_rate_limit_buckets_by_ids(self, ids: list[Any]) -> list[Any]:
        return await self.load_items_by_ids(ids)

    def add_computed_field(self, field: str) -> None:
        super().add_computed_field(field)

    def add_relation_field(self, field: str) -> None:
        super().add_relation_field(field)

    @property
    def active_rate_limit_buckets_ids(self) -> set[Any]:
        return self.active_item_ids



class RateLimitBucketsManager(RateLimitBucketsBase):
    _instance: RateLimitBucketsManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> RateLimitBucketsManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: RateLimitBuckets) -> None:
        pass

rate_limit_buckets_manager_instance = RateLimitBucketsManager()