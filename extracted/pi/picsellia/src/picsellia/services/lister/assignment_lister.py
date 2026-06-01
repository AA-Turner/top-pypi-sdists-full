import abc
import logging
from typing import Any, Generic, Literal, TypeVar
from uuid import UUID

import orjson
from pydantic import model_validator

from picsellia.sdk.annotation_campaign_assignment import AnnotationCampaignAssignment
from picsellia.sdk.campaign.abstract_assignment import AbstractAssignment
from picsellia.sdk.connection import Connection
from picsellia.sdk.review_campaign_assignment import ReviewCampaignAssignment
from picsellia.services.lister.default import (
    AbstractItemLister,
    BaseFilter,
    TFilter,
)
from picsellia.types.enums import AssignmentStatus

logger = logging.getLogger(__name__)


class AssignmentFilter(BaseFilter):
    status: AssignmentStatus | None = None
    step_id: UUID | None = None
    user_id: UUID | Literal["unassigned"] | None = None
    custom_metadata: dict | None = None

    @model_validator(mode="after")
    def check_query(self):
        return self

    def has_list_of_items(self) -> bool:
        return False


TCampaignAssignment = TypeVar("TCampaignAssignment", bound=AbstractAssignment)


class AbstractCampaignAssignmentLister(
    AbstractItemLister[TCampaignAssignment, AssignmentFilter],
    abc.ABC,
    Generic[TCampaignAssignment],
):
    def __init__(self, connection: Connection, campaign_id: UUID):
        super().__init__(connection)
        self.campaign_id = campaign_id

    def _get_query_param_and_items_from_filters(
        self, filters: TFilter
    ) -> tuple[str, list]:
        raise NotImplementedError()

    def _get_other_params(self, filters: AssignmentFilter) -> dict[str, Any]:
        params = {}
        if filters.status:
            params["status"] = filters.status.value
        if filters.step_id:
            params["step_id"] = filters.step_id
        if filters.user_id:
            params["user_id"] = filters.user_id
        if filters.custom_metadata:
            params["custom_metadata"] = orjson.dumps(filters.custom_metadata)
        return params


class AnnotationCampaignAssignmentLister(
    AbstractCampaignAssignmentLister[AnnotationCampaignAssignment]
):
    def _get_path(self) -> str:
        return f"/api/campaigns/annotation/{self.campaign_id}/assignments"

    def _build_item(self, data: dict) -> AnnotationCampaignAssignment:
        return AnnotationCampaignAssignment(self.connection, self.campaign_id, data)


class ReviewCampaignAssignmentLister(
    AbstractCampaignAssignmentLister[ReviewCampaignAssignment]
):
    def _get_path(self) -> str:
        return f"/api/campaigns/review/{self.campaign_id}/assignments"

    def _build_item(self, data: dict) -> ReviewCampaignAssignment:
        return ReviewCampaignAssignment(self.connection, self.campaign_id, data)
