import logging
from typing import Any
from uuid import UUID

import orjson
from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.dataset_version import DatasetVersion
from picsellia.sdk.experiment import Experiment
from picsellia.sdk.model_version import ModelVersion
from picsellia.types.schemas import ProjectSchema
from picsellia.utils import filter_payload

logger = logging.getLogger("picsellia")


class Project(Dao):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)

    @property
    def name(self) -> str:
        """Name of this (Project)"""
        return self._name

    def __str__(self):
        return f"{Colors.BOLD}Project '{self.name}' {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/project/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> ProjectSchema:
        schema = ProjectSchema(**data)
        self._name = schema.name
        return schema

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
            print(project.get_resource_url_on_platform())
            >>> "https://app.picsellia.com/project/62cffb84-b92c-450c-bc37-8c4dd4d0f590"
            ```

        Returns:
            Url on Platform for this resource
        """

        return f"{self.connection.host}/project/{self.id}"

    @exception_handler
    @beartype
    def list_experiments(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Experiment]:
        """Retrieve all experiments of this project

        Examples:
            ```python
            experiments = my_project.list_experiments()
            ```

        Arguments:
            limit (int, optional): Limit of experiments to retrieve. Defaults to None.
            offset (int, optional): Offset to start retrieving experiments. Defaults to None.
            order_by (list[str], optional): Order by fields. Defaults to None.

        Returns:
            A list of (Experiment) objects, that you can manipulate
        """
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        params = filter_payload(params)
        response = self.connection.get(
            f"/api/project/{self.id}/experiments", params=params
        ).json()
        return [Experiment(self.connection, item) for item in response["items"]]

    @exception_handler
    @beartype
    def delete_all_experiments(self) -> None:
        """Delete all experiments of this project

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
            my_project.delete_all_experiments()
            ```
        """
        experiment_ids = self.connection.get(
            f"/api/project/{self.id}/experiments/ids"
        ).json()
        payload = {"ids": experiment_ids}
        self.connection.delete(
            f"/api/project/{self.id}/experiments", data=orjson.dumps(payload)
        )
        logger.info(f"All experiments of {self} deleted.")

    @exception_handler
    @beartype
    def create_experiment(
        self,
        name: str,
        description: str | None = None,
        base_experiment: Experiment | None = None,
        base_model_version: ModelVersion | None = None,
        parameters: dict | None = None,
    ) -> Experiment:
        """Create an (Experiment) in this (Project).

        By giving parameters, it will create a (Log) parameters on this Experiment with the content of the dict.
        If base_experiment is provided, it will set the base_experiment on this Experiment.
        It will copy the labelmap and Artifacts.
        It might copy parameters of the base_experiment if no other parameters are given.
        If base_model_version is provided it will set the base_model_version on this Experiment.
        It will copy the labelmap and the model files, only if no base_experiment already fill them.
        It might copy the parameters of the base_model_version if no other parameters are given, only if no base_experiment already fill them.

        Examples:
            ```python
            base_model_version = client.get_model_version_by_id("fbddcb6e-16de-4226-9624-0737879af774")
            my_experiment = my_project.create_experiment(
                "test_experiment",
                description="This is a cool experiment",
                base_model_version=base_model_version,
            )
            ```
        Arguments:
            name (str, optional): Name of experiment. Defaults to None.
            description (str, optional): Description of experiment.
            base_experiment ((Experiment), optional): Base (Experiment) of this new experiment. Defaults to None.
            base_model_version ((ModelVersion), optional): Base (ModelVersion) of this new experiment. Defaults to None.
            parameters (dict, optional): Parameters
        Returns:
             A new (Experiment) of this project
        """
        payload: dict[str, Any] = {"name": name, "description": description or ""}
        if parameters is not None:
            payload["parameters"] = parameters

        if base_experiment is not None:
            payload["base_experiment_id"] = base_experiment.id

        if base_model_version is not None:
            payload["base_model_version_id"] = base_model_version.id

        r = self.connection.post(
            f"/api/project/{self.id}/experiments", data=orjson.dumps(payload)
        ).json()
        experiment = Experiment(self.connection, r)
        logger.info(f"{experiment} created")
        return experiment

    @exception_handler
    @beartype
    def update(
        self,
        name: str | None = None,
        description: str | None = None,
        private: bool | None = None,
    ) -> None:
        """Update a project with a new name or description

        Examples:
            ```python
            my_project.update(description="This is a cool project")
            ```

        Arguments:
            name (str, optional): New name of project. Defaults to None.
            description (str, optional): New description of project. Defaults to None.
            private (bool, optional): deprecated field.
        """
        payload = {"name": name, "description": description}

        if private is not None:
            logger.warning(
                "You cannot update privacy of a project anymore. This parameter will not be used"
            )

        # Filter None values
        filtered_payload = filter_payload(payload)
        r = self.connection.patch(
            f"/api/project/{self.id}", data=orjson.dumps(filtered_payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated.")

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete a project.

        :warning: **DANGER ZONE**: Be very careful here!

        It will delete the project and all experiments linked.

        Examples:
            ```python
            my_project.delete()
            ```
        """
        self.connection.delete(f"/api/project/{self.id}")
        logger.info(f"{self} deleted.")

    @exception_handler
    @beartype
    def get_experiment(self, name: str) -> Experiment:
        """Retrieve an existing experiment by name.

        Examples:
            ```python
            my_experiment = my_project.get_experiment("test_experiment")
            ```
        Arguments:
            name (str, optional): Experiment's name.

        Raises:
            Exception: Experiment not found

        Returns:
            An (Experiment) object that you can manipulate
        """
        params = {"name": name}
        r = self.connection.get(
            f"/api/project/{self.id}/experiments/find", params=params
        ).json()
        return Experiment(self.connection, r)

    @exception_handler
    @beartype
    def get_experiment_by_id(self, id: UUID | str) -> Experiment:
        """Retrieve an existing experiment by id.

        Examples:
            ```python
            my_experiment = my_project.get_experiment_by_id("62cffb84-b92c-450c-bc37-8c4dd4d0f590")
            ```
        Arguments:
            id: Experiment's id.

        Raises:
            Exception: Experiment not found

        Returns:
            An (Experiment) object that you can manipulate
        """
        if isinstance(id, str):
            id = UUID(id)
        params = {"id": id}
        r = self.connection.get(
            f"/api/project/{self.id}/experiments/find", params=params
        ).json()
        return Experiment(self.connection, r)

    @exception_handler
    @beartype
    def attach_dataset(self, dataset_version: DatasetVersion) -> None:
        """Attach a dataset version to this project.

        Retrieve or create a dataset version and attach it to this project.

        Examples:
            ```python
            foo_dataset_version = client.get_dataset("foo").get_version("first")
            my_project.attach_dataset(foo_dataset_version)
            ```
        Arguments:
            dataset_version (DatasetVersion): A dataset version to attach to the project.
        """
        payload = {"dataset_version_id": dataset_version.id}
        self.connection.post(
            f"/api/project/{self.id}/datasets", data=orjson.dumps(payload)
        )
        logger.info(f"{dataset_version} successfully attached to {self}")

    @exception_handler
    @beartype
    def detach_dataset(self, dataset_version: DatasetVersion) -> None:
        """Detach a dataset version from this project.

        Examples:
            ```python
            foo_dataset_version = client.get_dataset("foo").get_version("first")
            my_project.attach_dataset(foo_dataset_version)
            my_project.detach_dataset(foo_dataset_version)
            ```
        Arguments:
            dataset_version (DatasetVersion): A dataset version to attach to the project.
        """
        payload = {"ids": [dataset_version.id]}
        self.connection.delete(
            f"/api/project/{self.id}/datasets", data=orjson.dumps(payload)
        )
        logger.info(
            f"{dataset_version} was successfully detached from this project {self}"
        )

    @exception_handler
    @beartype
    def list_dataset_versions(self) -> list[DatasetVersion]:
        """Retrieve all dataset versions attached to this project

        Examples:
            ```python
            datasets = my_project.list_dataset_versions()
            ```

        Returns:
            A list of (DatasetVersion) object attached to this project
        """
        r = self.connection.get(f"/api/project/{self.id}/datasets").json()
        return [DatasetVersion(self.connection, item) for item in r["items"]]
