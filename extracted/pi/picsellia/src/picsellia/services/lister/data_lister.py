import logging
from typing import Any
from uuid import UUID

import orjson
from pydantic import Field, model_validator

from picsellia.sdk.connection import Connection
from picsellia.sdk.data import Data
from picsellia.services.lister.default import (
    AbstractItemLister,
    BaseFilter,
)

logger = logging.getLogger(__name__)


class DataFilter(BaseFilter):
    filenames: list[str] | None = Field(default=None, min_length=1)
    object_names: list[str] | None = Field(default=None, min_length=1)
    ids: list[str | UUID] | None = Field(default=None, min_length=1)
    custom_metadata: dict | None = None

    @model_validator(mode="after")
    def check_query(self):
        with_filenames = self.filenames is not None
        with_object_names = self.object_names is not None
        with_ids = self.ids is not None

        if not with_ids and not with_filenames and not with_object_names:
            return self

        if self.limit:
            logger.warning(
                "limit cannot be used with parameters object_names, filenames, ids"
            )

        if self.offset:
            logger.warning(
                "offset cannot be used with parameters object_names, filenames, ids"
            )

        if bool(self.ids) + bool(self.object_names) + bool(self.filenames) > 1:
            raise ValueError("You can only give one of filenames, object_names or ids")

        return self

    def has_list_of_items(self) -> bool:
        return (
            self.object_names is not None
            or self.filenames is not None
            or self.ids is not None
        )


class DataLister(AbstractItemLister[Data, DataFilter]):
    def __init__(self, connection: Connection, datalake_id: UUID):
        super().__init__(connection)
        self.datalake_id = datalake_id

    def _get_query_param_and_items_from_filters(
        self, filters: DataFilter
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
        else:  # pragma: no cover
            raise ValueError("filenames, object_names or ids must be given")
        return query_param, items

    def _get_other_params(self, filters: DataFilter) -> dict[str, Any]:
        params = {}
        if filters.custom_metadata:
            params["custom_metadata"] = orjson.dumps(filters.custom_metadata)
        return params

    def _get_path(self) -> str:
        return f"/api/datalake/{self.datalake_id}/datas"

    def _build_item(self, item: dict) -> Data:
        return Data(self.connection, self.datalake_id, item)
