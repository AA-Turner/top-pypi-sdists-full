import logging
from uuid import UUID

from beartype import beartype

import picsellia.exceptions as exceptions
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.dataset_version import DatasetVersion
from picsellia.types.schemas import ModelContextSchema, ModelDataSchema

logger = logging.getLogger("picsellia")


class ModelContext(Dao):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)

    @property
    def experiment_id(self) -> UUID:
        """UUID of the original (Experiment) that generated this (Model)"""
        return self._experiment_id

    @property
    def datasets(self) -> list[ModelDataSchema] | None:
        """List of (ModelDataSchema) with ids, names, and repartition of (DatasetVersion) used by original (Experiment)"""
        return self._datasets

    @property
    def parameters(self) -> dict:
        """Parameters used by original (Experiment) to generated (Model)"""
        return self._parameters

    def __str__(self):
        return f"A {Colors.BLUE}model context{Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/model/context/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> ModelContextSchema:
        schema = ModelContextSchema(**data)
        self._experiment_id = schema.experiment_id
        self._datasets = schema.datas
        self._parameters = schema.parameters
        return schema

    @exception_handler
    @beartype
    def get_infos(self) -> dict:
        """Retrieve some infos about this context

        Examples:
            ```python
            infos = model_context.get_infos()
            ```

        Returns:
            A dict with experiment, datasets and parameters
        """
        return {
            "experiment": self.experiment_id,
            "datasets": self.datasets,
            "parameters": self.parameters,
        }

    @exception_handler
    @beartype
    def get_experiment(self):
        """Retrieve source experiment of this context

        It will raise an exception if this context has no experiment source

        Examples:
            ```python
            exp = model_context.get_experiment()
            ```

        Returns:
            An (Experiment) object
        """
        if self.experiment_id is None:
            raise exceptions.ContextSourceNotDefined(
                "This context has no experiment source"
            )

        from .experiment import Experiment

        r = self.connection.get(f"/api/experiment/{self.experiment_id}").json()
        return Experiment(self.connection, r)

    @exception_handler
    @beartype
    def get_dataset_version(self, name: str) -> DatasetVersion:
        """Retrieve dataset version used to train or evaluate the model, by the name given when attached experiment and dataset.

        It will raise an exception if this context has no dataset attached with given name.

        Examples:
            ```python
            dataset_version = model_context.get_dataset_version("train")
            ```

        Arguments:
            name (str): Name of the dataset version attached to the experiment

        Returns:
            A (DatasetVersion) object
        """
        if self._datasets is None or self._datasets == []:
            raise exceptions.ContextDataNotDefined("This context has no data")

        for data in self._datasets:
            if data.name == name:
                r = self.connection.get(
                    f"/api/dataset/version/{data.version_id}"
                ).json()
                return DatasetVersion(self.connection, r)

        raise exceptions.ContextDataNotDefined(
            f"This context has no dataset attached with {name}"
        )

    @exception_handler
    @beartype
    def retrieve_datasets(
        self,
    ) -> dict[str, DatasetVersion]:
        """Retrieve datasets used to train and evaluate (or else) the model

        It will raise an exception if this context has no data

        Examples:
            ```python
            dataset_versions = model_context.retrieve_datasets()
            ```

        Returns:
            A dict with dataset name as key and (DatasetVersion) as value
        """
        if self._datasets is None or self._datasets == []:
            raise exceptions.ContextSourceNotDefined("This context has no data")

        datasets = {}
        for dataset_version in self._datasets:
            r = self.connection.get(
                f"/api/dataset/version/{dataset_version.version_id}"
            ).json()
            datasets[dataset_version.name] = DatasetVersion(self.connection, r)
        return datasets
