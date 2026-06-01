from uuid import UUID

from picsellia.exceptions import NoDataError
from picsellia.sdk.artifact import Artifact
from picsellia.sdk.connection import Connection
from picsellia.sdk.evaluation import MultiEvaluation
from picsellia.sdk.log import Log
from picsellia.services.lister.evaluation_lister import (
    EvaluationFilter,
    EvaluationLister,
)


class TrainingService:
    """This service is used by Experiment and FastTraining dao to fetch evaluations, artifacts and logs."""

    def __init__(self, connection: Connection, experiment_id: UUID):
        self.connection = connection
        self.experiment_id = experiment_id

    def list_evaluations(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
        q: str | None = None,
    ) -> MultiEvaluation:
        filters = EvaluationFilter.model_validate(
            {"limit": limit, "offset": offset, "order_by": order_by, "query": q}
        )
        evaluations = EvaluationLister(self.connection, self.experiment_id).list_items(
            filters
        )

        if len(evaluations) == 0:
            raise NoDataError(
                "No evaluation done by this training found with this query"
            )

        return MultiEvaluation(self.connection, self.experiment_id, evaluations)

    def list_logs(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Log]:
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        r = self.connection.get(
            f"/api/experiment/{self.experiment_id}/logs/extended", params=params
        ).json()
        return [Log(self.connection, item) for item in r["items"]]

    def get_log(self, name: str) -> Log:
        params = {"name": name}
        r = self.connection.get(
            f"/api/experiment/{self.experiment_id}/logs/find", params=params
        ).json()
        return Log(self.connection, r)

    def list_artifacts(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Artifact]:
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        r = self.connection.get(
            f"/api/experiment/{self.experiment_id}/artifacts", params=params
        ).json()
        return [Artifact(self.connection, item) for item in r["items"]]

    def get_parameters(self) -> dict:
        return self.get_log("parameters").data
