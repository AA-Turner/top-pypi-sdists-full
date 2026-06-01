from uuid import UUID

from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.exceptions import ResourceNotFoundError
from picsellia.sdk.artifact import Artifact
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.evaluation import MultiEvaluation
from picsellia.sdk.log import Log
from picsellia.services.training import TrainingService
from picsellia.types.schemas import FastTrainingSchema


class FastTraining(Dao):
    def __init__(
        self, connexion: Connection, dataset_version_id: UUID, data: dict
    ) -> None:
        data["id"] = data["experiment_id"]
        Dao.__init__(self, connexion, data)
        self.dataset_version_id = dataset_version_id

    @property
    def experiment_id(self):
        """Id of (Experiment) for this Fast Training"""
        return self._experiment_id

    @property
    def experiment_name(self) -> str:
        """Name of (Experiment) for this Fast Training"""
        return self._experiment_name

    def __str__(self):
        return f"{Colors.BLUE}Fast Training for Experiment '{self.experiment_name}' {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        schema = FastTrainingSchema(**data)
        self._status = schema.status
        self._experiment_id = schema.experiment_id
        self._experiment_name = schema.experiment_name
        self._job_id = schema.job_id
        self._job_run_id = schema.job_run_id
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        items = self.connection.get(
            f"/api/dataset/version/{self.dataset_version_id}/fast-training",
            params={"experiment_id": self.experiment_id},
        ).json()["trainings"]
        if len(items) != 1:
            raise ResourceNotFoundError("This training was not found")
        self.refresh(items[0])
        return items[0]

    @exception_handler
    @beartype
    def list_evaluations(
        self,
        limit: int | None = None,
        offset: int | None = None,
        q: str | None = None,
    ) -> MultiEvaluation:
        """List evaluations done in this (FastTraining).

         Arguments:
            limit (int, optional): if given, will limit the number of evaluations returned
            offset (int, optional): if given, will return evaluations that would have been returned
                                    after this offset in given order
            q (str, optional): if given, will try to apply query to filter evaluations

        Returns:
            A (MultiEvaluation)
        """
        return TrainingService(self.connection, self.experiment_id).list_evaluations(
            limit, offset, q
        )

    @exception_handler
    @beartype
    def list_logs(self, limit: int | None = None, offset: int | None = None) -> list:
        """List everything that has been logged.

        List everything that has been logged to an experiment.

        Examples:
            ```python
            logs = experiment.list_logs()
            assert logs[0].type == LogType.Table
            assert logs[0].data == {"batch_size":4, "epochs":1000}
            ```

        Arguments:
            limit (int, optional): limit of logs to retrieve. Defaults to None.
            offset (int, optional): offset to start retrieving logs. Defaults to None.

        Returns:
            A list of (Log) objects
        """
        return TrainingService(self.connection, self.experiment_id).list_logs(
            limit, offset
        )

    @exception_handler
    @beartype
    def get_log(self, name: str) -> Log:
        """Retrieve a (Log) from its name in this (FastTraining).

        Arguments:
            name (str): name of the log to retrieve
        Returns:
            A (Log) object
        """
        return TrainingService(self.connection, self.experiment_id).get_log(name)

    @exception_handler
    @beartype
    def get_parameters(self) -> dict:
        """Retrieve parameters of this (FastTraining)

        Return:
            a dict
        """
        return TrainingService(self.connection, self.experiment_id).get_parameters()

    @exception_handler
    @beartype
    def list_artifacts(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Artifact]:
        """List artifacts stored for this (FastTraining).

        Arguments:
            limit (int, optional): limit of artifacts to retrieve. Defaults to None.
            offset (int, optional): offset to start retrieving artifacts. Defaults to None.
            order_by (list[str], optional): fields to order by. Defaults to None.

        Returns:
            A list of (Artifact) objects that you can manipulate
        """
        return TrainingService(self.connection, self.experiment_id).list_artifacts(
            limit, offset, order_by
        )
