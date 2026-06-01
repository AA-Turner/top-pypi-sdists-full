import logging
from uuid import UUID

import orjson
from beartype import beartype
from deprecation import deprecated

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.exceptions import ResourceNotFoundError
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.dataset_version import DatasetVersion
from picsellia.sdk.resource import Resource
from picsellia.sdk.tag import Tag, TagTarget
from picsellia.sdk.taggable import Taggable
from picsellia.sdk.worker import Worker
from picsellia.types.enums import InferenceType, WorkerType
from picsellia.types.schemas import DatasetSchema
from picsellia.utils import filter_payload

logger = logging.getLogger("picsellia")


class Dataset(Dao, Taggable, Resource):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)
        Taggable.__init__(self, TagTarget.DATASET)
        Resource.__init__(self, "dataset")

    @property
    def name(self) -> str:
        """Name of this (Dataset)"""
        return self._name

    def __str__(self):
        return f"{Colors.YELLOW}Dataset {self.name} {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        schema = DatasetSchema(**data)
        self._name = schema.name
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/dataset/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def get_tags(self) -> list[Tag]:
        """Retrieve the tags of your dataset.

        Examples:
            ```python
            tags = foo_dataset.get_tags()
            assert tags[0].name == "my-dataset-1"
            ```

        Returns:
            List of (Tag) objects
        """
        r = self.sync()
        return [Tag(self.connection, item) for item in r["tags"]]

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
            print(foo_dataset.get_resource_url_on_platform())
            >>> "https://app.picsellia.com/dataset/62cffb84-b92c-450c-bc37-8c4dd4d0f590"
            ```

        Returns:
            Url on Platform for this resource
        """

        return f"{self.connection.host}/dataset/{self.id}"

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete a dataset.

        :warning: **DANGER ZONE**: Be very careful here!

        It will remove this dataset from our database, its versions with their assets and annotations will be removed.
        It will also remove potential annotation campaigns of this dataset versions.

        Examples:
            ```python
            foo_dataset.delete()
            ```
        """
        self.connection.delete(f"/api/dataset/{self.id}")
        logger.info(f"{self} deleted")

    @exception_handler
    @beartype
    def update(
        self,
        name: str | None = None,
        private: bool | None = None,
        description: str | None = None,
    ) -> None:
        """Update name, private or description of this Dataset.

        Examples:
            ```python
            dataset.update(description='My favourite dataset')
            ```

        Arguments:
            name (str, optional): New name of the dataset. Defaults to None.
            private (bool, optional): New private of the dataset. Defaults to None.
            description (str, optional): New description of the dataset. Defaults to None.
        """
        if private is not None:
            logging.warning(
                "'private' parameter is deprecated and will be removed in future versions. "
                "You cannot update to a public dataset from the SDK anymore."
            )

        payload = {"name": name, "description": description}
        filtered_payload = filter_payload(payload)
        r = self.connection.patch(
            f"/api/dataset/{self.id}", data=orjson.dumps(filtered_payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated")

    @exception_handler
    @beartype
    def list_versions(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[DatasetVersion]:
        """List all versions of this dataset

        Examples:
            ```python
            dataset.list_versions()
            ```

        Arguments:
            limit (int, optional): limit of versions to retrieve. Defaults to None.
            offset (int, optional): offset to start retrieving versions. Defaults to None.
            order_by (list[str], optional): fields to order by. Defaults to None.

        Returns:
            List of (DatasetVersion) objects
        """
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        params = filter_payload(params)
        r = self.connection.get(
            f"/api/dataset/{self.id}/versions", params=params
        ).json()
        return [DatasetVersion(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def get_version(self, version: str) -> DatasetVersion:
        """Retrieve one version of a dataset

        Examples:
            ```python
            my_dataset_version = my_dataset.get_version("first")
            ```

        Arguments:
            version (str): version name to retrieve

        Returns:
            a (DatasetVersion) object
        """
        params = {"version": version}
        r = self.connection.get(
            f"/api/dataset/{self.id}/versions/find", params=params
        ).json()
        return DatasetVersion(self.connection, r)

    @exception_handler
    @beartype
    def get_version_by_id(self, id: UUID | str) -> DatasetVersion:
        """Retrieve one version of a dataset

        Examples:
            ```python
            my_dataset_version = my_dataset.get_version_by_id("918351d2-3e96-4970-bb3b-420f33ded895")
            ```

        Arguments:
            id (UUID): id of the version to retrieve

        Returns:
            a (DatasetVersion) object
        """
        if isinstance(id, str):
            id = UUID(id)
        params = {"id": id}
        r = self.connection.get(
            f"/api/dataset/{self.id}/versions/find", params=params
        ).json()
        return DatasetVersion(self.connection, r)

    @exception_handler
    @beartype
    def create_version(
        self,
        version: str,
        description: str = "",
        type: InferenceType | str = InferenceType.NOT_CONFIGURED,
    ) -> DatasetVersion:
        """Create a version of this dataset.

        A versioned dataset (DatasetVersion) takes (Data) from (Datalake) and transform it as annotable (Asset).

        Examples:
            ```python
            foo_dataset = client.create_dataset('foo_dataset')
            foo_dataset_version_1 = foo_dataset.create_version('first')
            some_data = client.get_datalake().list_data(limit=10)
            foo_dataset_version_1.add_data(some_data)
            ```

        Arguments:
            version (str): version name
            description (str): description of this version
            type (InferenceType): type of this version

        Returns:
            A (DatasetVersion) manipulable that can receive data
        """
        payload = {
            "version": version,
            "description": description,
            "type": InferenceType.validate(type),
        }

        r = self.connection.post(
            f"/api/dataset/{self.id}/versions", data=orjson.dumps(payload)
        ).json()
        return DatasetVersion(self.connection, r)

    @exception_handler
    @beartype
    @deprecated(
        deprecated_in="6.24.0",
        removed_in="6.27.0",
        details="This method should not be called anymore. Instead use list_users()",
    )
    def list_workers(self) -> list[Worker]:
        """List all workers of this dataset

        Examples:
            ```python
            dataset.list_workers()
            ```

        Returns:
            List of (Worker) objects
        """
        return [
            Worker(
                self.connection,
                {"id": item.id, "username": item.username, "user_id": item.id},
                WorkerType.DATASET,
            )
            for item in self.list_users()
        ]

    @exception_handler
    @beartype
    @deprecated(
        deprecated_in="6.24.0",
        removed_in="6.27.0",
        details="This method should not be called anymore. Instead use list_users()",
    )
    def find_worker(self, username: str) -> Worker:
        """Find worker of this dataset from its username

        Examples:
            ```python
            dataset.find_worker("John")
            ```

        Arguments:
            username (str): username of the worker on the platform

        Returns:
            A (Worker) object
        """

        for user in self.list_users():
            if user.username == username:
                return Worker(
                    self.connection,
                    {"id": user.id, "username": user.username, "user_id": user.id},
                    WorkerType.DATASET,
                )

        raise ResourceNotFoundError(
            f"There is no worker with username '{username}' in this dataset."
        )
