import logging
from typing import Any
from uuid import UUID

from pydantic import model_validator

from picsellia.sdk.connection import Connection
from picsellia.sdk.evaluation import Evaluation
from picsellia.services.lister.default import AbstractItemLister, BaseFilter

logger = logging.getLogger(__name__)


class EvaluationFilter(BaseFilter):
    @model_validator(mode="after")
    def check_query(self):
        return self

    def has_list_of_items(self) -> bool:
        return False


class EvaluationLister(AbstractItemLister[Evaluation, EvaluationFilter]):
    def __init__(self, connection: Connection, experiment_id: UUID):
        super().__init__(connection)
        self.experiment_id = experiment_id

    def _get_query_param_and_items_from_filters(
        self, filters: EvaluationFilter
    ) -> tuple[str, list]:
        # You cannot filter on list of ids or data ids at the moment, so this method is not used
        raise NotImplementedError()

    def _get_other_params(self, filters: EvaluationFilter) -> dict[str, Any]:
        return {}

    def _get_path(self) -> str:
        return f"/api/experiment/{self.experiment_id}/evaluations"

    def _build_item(self, item: dict) -> Evaluation:
        return Evaluation(self.connection, self.experiment_id, item)
