import logging
from typing import Any
from uuid import UUID

import orjson
from pydantic import Field, model_validator

from picsellia.sdk.asset import Asset
from picsellia.sdk.connection import Connection
from picsellia.services.lister.default import AbstractItemLister, BaseFilter

logger = logging.getLogger(__name__)


class AssetFilter(BaseFilter):
    filenames: list[str] | None = Field(default=None, min_length=1)
    object_names: list[str] | None = Field(default=None, min_length=1)
    ids: list[str | UUID] | None = Field(default=None, min_length=1)
    filename_startswith: list[str] | None = Field(default=None, min_length=1)
    data_ids: list[str | UUID] | None = None
    assignment_status: str | None = None
    assignment_step_id: UUID | None = None
    assignment_user_id: UUID | None = None
    custom_metadata: dict | None = None

    @model_validator(mode="after")
    def check_query(self):
        with_filenames = self.filenames is not None
        with_object_names = self.object_names is not None
        with_ids = self.ids is not None
        with_data_ids = self.data_ids is not None
        with_filename_startswith = self.filename_startswith is not None

        if (
            not with_ids
            and not with_filenames
            and not with_object_names
            and not with_filename_startswith
            and not with_data_ids
        ):
            return self

        if self.limit:
            logger.warning(
                "limit cannot be used with parameters object_names, filenames, ids, data_ids, filename_startswith"
            )

        if self.offset:
            logger.warning(
                "offset cannot be used with parameters object_names, filenames, ids, data_ids, filename_startswith"
            )

        if (
            bool(self.ids)
            + bool(self.object_names)
            + bool(self.filenames)
            + bool(self.data_ids)
            + bool(self.filename_startswith)
            > 1
        ):
            raise ValueError(
                "You can only give one of filenames, object_names, ids, data_ids or filename_startswith"
            )

        return self

    def has_list_of_items(self) -> bool:
        return (
            self.object_names is not None
            or self.filenames is not None
            or self.ids is not None
            or self.data_ids is not None
            or self.filename_startswith is not None
        )


class AssetLister(AbstractItemLister[Asset, AssetFilter]):
    def __init__(self, connection: Connection, dataset_version_id: UUID):
        super().__init__(connection)
        self.dataset_version_id = dataset_version_id

    def _get_query_param_and_items_from_filters(
        self, filters: AssetFilter
    ) -> tuple[str, list]:
        if filters.ids:
            query_param = "ids"
            items = filters.ids
        elif filters.object_names:
            query_param = "object_names"
            items = filters.object_names
        elif filters.filenames:
            query_param = "filenames"
            items = filters.filenames
        elif filters.filename_startswith:
            query_param = "filename_startswith"
            items = filters.filename_startswith
        elif filters.data_ids:
            query_param = "data_ids"
            items = filters.data_ids
        else:  # pragma: no cover
            raise ValueError(
                "filenames, object_names, ids, filename_startswith or data_ids must be given"
            )
        return query_param, items

    def _get_other_params(self, filters: AssetFilter) -> dict[str, Any]:
        params = {}
        if filters.assignment_status:
            params["assignment_status"] = filters.assignment_status
        if filters.assignment_step_id:
            params["assignment_step_id"] = filters.assignment_step_id
        if filters.assignment_user_id:
            params["assignment_user_id"] = filters.assignment_user_id
        if filters.custom_metadata:
            params["custom_metadata"] = orjson.dumps(filters.custom_metadata)
        return params

    def _get_path(self) -> str:
        return f"/api/dataset/version/{self.dataset_version_id}/assets"

    def _build_item(self, item: dict) -> Asset:
        return Asset(self.connection, self.dataset_version_id, item)
