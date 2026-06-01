import logging
from typing import Any
from uuid import UUID

import orjson

from picsellia.sdk.connection import Connection
from picsellia.sdk.predicted_asset import PredictedAsset
from picsellia.services.lister.default import AbstractItemLister, BaseFilter

logger = logging.getLogger(__name__)


class PredictedAssetFilter(BaseFilter):
    assignment_status: str | None = None
    assignment_step_id: UUID | None = None
    assignment_user_id: UUID | None = None
    custom_metadata: dict | None = None

    def has_list_of_items(self) -> bool:
        return False


class PredictedAssetLister(AbstractItemLister[PredictedAsset, PredictedAssetFilter]):
    def __init__(self, connection: Connection, deployment_id: UUID):
        super().__init__(connection)
        self.deployment_id = deployment_id

    def _get_query_param_and_items_from_filters(
        self, filters: PredictedAssetFilter
    ) -> tuple[str, list]:
        raise NotImplementedError()

    def _get_other_params(self, filters: PredictedAssetFilter) -> dict[str, Any]:
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
        return f"/api/deployment/{self.deployment_id}/predictedassets"

    def _build_item(self, item: dict) -> PredictedAsset:
        return PredictedAsset(self.connection, self.deployment_id, item)
