import logging
from operator import countOf
from pathlib import Path
from time import sleep
from uuid import UUID

import deprecation
import orjson
from beartype import beartype

from picsellia import exceptions as exceptions
from picsellia import pxl_multithreading as mlt
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.exceptions import UnprocessableData, WaitingAttemptsTimeout
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.data_projection import DataProjection
from picsellia.sdk.datasource import DataSource
from picsellia.sdk.downloadable import Downloadable
from picsellia.sdk.multi_object import MultiObject
from picsellia.sdk.tag import Tag, TagTarget
from picsellia.sdk.taggable import Taggable
from picsellia.types.enums import DataType, DataUploadStatus
from picsellia.types.schemas import DataSchema, ImageSchema, VideoSchema

logger = logging.getLogger("picsellia")


class Data(Dao, Downloadable, Taggable):
    def __init__(self, connexion: Connection, datalake_id: UUID, data: dict):
        Dao.__init__(self, connexion, data)
        Downloadable.__init__(self)
        Taggable.__init__(self, TagTarget.DATA)
        self._datalake_id = datalake_id
        self._embeddings = None

    def __str__(self):
        return f"{Colors.GREEN}Data{Colors.ENDC} object (id: {self.id})"

    @property
    def datalake_id(self) -> UUID:
        """UUID of (Datalake) where this (Data) is"""
        return self._datalake_id

    @property
    def object_name(self) -> str:
        """Object name of this (Data)"""
        return self._object_name

    @property
    def content_type(self) -> str:
        """Content type of this (Data)"""
        return self._content_type

    @property
    def filename(self) -> str:
        """Filename of this (Data)"""
        return self._filename

    @property
    def large(self) -> bool:
        """If true, this (Data) file is considered large"""
        return True

    @property
    def type(self) -> DataType:
        """Type of this (Data)"""
        return self._type

    @property
    def width(self) -> int:
        """Width of this (Data)"""
        if self._upload_status != DataUploadStatus.DONE:
            return 0

        return self._width

    @property
    def height(self) -> int:
        """Height of this (Data)"""
        if self._upload_status != DataUploadStatus.DONE:
            return 0

        return self._height

    @property
    @deprecation.deprecated(deprecated_in="6.13.0", removed_in="7.0.0")
    def duration(self) -> int:
        """This property is no longer supported"""
        return 0

    @property
    def metadata(self) -> dict | None:
        """Metadata of this Data. Can be None"""
        return self._metadata

    @property
    def custom_metadata(self) -> dict | None:
        """Custom metadata of this Data. Can be None"""
        return self._custom_metadata

    @property
    def upload_status(self) -> DataUploadStatus:
        """Status of upload of this Data. You can only use your data if this value is DONE."""
        return self._upload_status

    @property
    def embeddings(self) -> dict | None:
        """Embeddings of this Data. Can be None if data was not indexed"""
        if not self._embeddings:
            self._load_embeddings()
        return self._embeddings

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        data_type = DataType.validate(data["type"])
        data_upload_status = DataUploadStatus.validate(data["upload_status"])

        if data_upload_status != DataUploadStatus.DONE:
            schema = DataSchema(**data)
        elif data_type == DataType.IMAGE:
            schema = ImageSchema(**data)
        elif data_type == DataType.VIDEO:
            schema = VideoSchema(**data)
        else:
            raise NotImplementedError("This data cannot be used at the moment.")

        # Downloadable properties
        self._object_name = schema.object_name
        self._filename = schema.filename
        self._url = schema.url
        self._metadata = schema.metadata
        self._custom_metadata = schema.custom_metadata
        self._upload_status = data_upload_status
        self._content_type = schema.content_type

        self._type = schema.type
        if data_upload_status == DataUploadStatus.DONE:
            self._height = schema.meta.height
            self._width = schema.meta.width

        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/data/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def reset_url(self) -> str:
        """Reset url property of this Data by calling platform.

        Returns:
            A url as a string of this Data.
        """
        r = self.connection.get(f"/api/data/{self.id}/presigned-url")
        self._url = r.json()["presigned_url"]
        return self._url

    def is_ready(self) -> bool:
        return self.upload_status not in [
            DataUploadStatus.PENDING,
            DataUploadStatus.COMPUTING,
        ]

    @exception_handler
    @beartype
    def wait_for_upload_done(
        self, blocking_time_increment: float = 1.0, attempts: int = 20
    ):
        attempt = 0
        while attempt < attempts:
            self.sync()
            if self.is_ready():
                break

            sleep(blocking_time_increment)
            attempt += 1
            logger.info(
                f"Waited for {blocking_time_increment * attempt}s, trying {attempts - attempt} times again in {blocking_time_increment}s"
            )

        if attempt >= attempts:
            raise WaitingAttemptsTimeout(
                f"Data is still being processed, but we waited for {blocking_time_increment * attempts}s."
                "Please wait a few more moment"
            )

        if self.upload_status == DataUploadStatus.ERROR:
            logger.error("This data could not be processed by our services")
            raise UnprocessableData(self)

    @exception_handler
    @beartype
    def get_tags(self) -> list[Tag]:
        """Retrieve the tags of your data.

        Examples:
            ```python
            tags = data.get_tags()
            assert tags[0].name == "bicycle"
            ```

        Returns:
            List of (Tag) objects.
        """
        r = self.sync()
        return [Tag(self.connection, item) for item in r["tags"]]

    @exception_handler
    @beartype
    def get_datasource(self) -> DataSource | None:
        """Retrieve (DataSource) of this Data if it exists. Else, will return None.

        Examples:
            ```python
            data_source = data.get_datasource()
            assert data_source is None
            ```

        Returns:
            A (DataSource) object or None.
        """
        r = self.sync()
        if "data_source" not in r or r["data_source"] is None:
            return None

        return DataSource(self.connection, r["data_source"])

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete data and remove it from datalake.

        :warning: **DANGER ZONE**: Be very careful here!

        Remove this data from datalake, and all assets linked to this data.

        Examples:
            ```python
            data.delete()
            ```
        """
        response = self.connection.delete(f"/api/data/{self.id}")
        assert response.status_code == 204
        logger.info(f"1 data (id: {self.id}) deleted from datalake {self.datalake_id}.")

    @exception_handler
    @beartype
    def update_metadata(self, metadata: dict | None) -> None:
        """This method will update metadata of your (Data).
        If you want to update location of your Data, you must update both longitude and latitude at the same time.
        """
        payload = {"metadata": metadata}
        r = self.connection.patch(
            f"/api/data/{self.id}", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(f"Metadata of {self.id} updated.")

    @exception_handler
    @beartype
    def update_custom_metadata(self, custom_metadata: dict | None):
        """This method will update custom_metadata of your (Data)."""
        payload = {"custom_metadata": custom_metadata}
        r = self.connection.patch(
            f"/api/data/{self.id}/custom-metadata", data=orjson.dumps(payload)
        ).json()
        self._custom_metadata = r["custom_metadata"]
        logger.info(f"Metadata of {self.id} updated.")

    def _load_embeddings(self) -> dict | None:
        r = self.connection.get(
            f"/api/visual-search/datalake/{self.datalake_id}/points/scroll",
            params={
                "with_vector": True,
                "with_payload": False,
                "has_error": False,
                "limit": 1,
            },
        ).json()
        if "points" not in r or len(r["points"]) == 0 or "vector" not in r["points"][0]:
            return None

        self._embeddings = r["points"][0]["vector"]
        return self._embeddings

    @exception_handler
    @beartype
    def list_projections(self, type: str | None = None) -> list[DataProjection]:
        """List (DataProjection) of this (Data).

        Examples:
            ```python
            projections = data.list_projections()
            projections[0].download()
            ```
        Returns:
            a list of (DataProjection)
        """
        if type is not None:
            logging.warning(
                "'type' parameter is deprecated and will be removed in future versions. "
            )

        r = self.connection.get(f"/api/data/{self.id}/projections").json()
        return [DataProjection(self.connection, self.id, item) for item in r["items"]]


class MultiData(MultiObject[Data], Taggable):
    @beartype
    def __init__(self, connexion: Connection, datalake_id: UUID, items: list[Data]):
        MultiObject.__init__(self, connexion, items)
        Taggable.__init__(self, TagTarget.DATA)
        self.datalake_id = datalake_id

    def __str__(self) -> str:
        return f"{Colors.GREEN}MultiData for datalake {self.datalake_id} {Colors.ENDC}, size: {len(self)}"

    def __getitem__(self, key) -> "Data | MultiData":
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.items)))
            data = [self.items[i] for i in indices]
            return MultiData(self.connection, self.datalake_id, data)
        return self.items[key]

    @beartype
    def __add__(self, other) -> "MultiData":
        self.assert_same_connection(other)
        items = self.items.copy()
        if isinstance(other, MultiData):
            items.extend(other.items.copy())
        elif isinstance(other, Data):
            items.append(other)
        else:
            raise exceptions.BadRequestError("You can't add these two objects")

        return MultiData(self.connection, self.datalake_id, items)

    @beartype
    def __iadd__(self, other) -> "MultiData":
        self.assert_same_connection(other)

        if isinstance(other, MultiData):
            self.extend(other.items.copy())
        elif isinstance(other, Data):
            self.append(other)
        else:
            raise exceptions.BadRequestError("You can't add these two objects")

        return self

    def copy(self) -> "MultiData":
        return MultiData(self.connection, self.datalake_id, self.items.copy())

    @exception_handler
    @beartype
    def split(self, ratio: float) -> tuple["MultiData", "MultiData"]:
        s = round(ratio * len(self.items))
        return MultiData(self.connection, self.datalake_id, self.items[:s]), MultiData(
            self.connection, self.datalake_id, self.items[s:]
        )

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete a bunch of data and remove them from datalake.

        :warning: **DANGER ZONE**: Be very careful here!

        Remove a bunch of data from datalake, and all assets linked to each data.

        Examples:
            ```python
            whole_data = datalake.list_data(limit=3)
            whole_data.delete()
            ```
        """
        payload = {"ids": self.ids}
        self.connection.delete(
            f"/api/datalake/{self.datalake_id}/datas",
            data=orjson.dumps(payload),
        )
        logger.info(f"{len(self.items)} data deleted from datalake {self.datalake_id}.")

    @exception_handler
    @beartype
    def download(
        self,
        target_path: str | Path = "./",
        force_replace: bool = False,
        max_workers: int | None = None,
        use_id: bool = False,
    ) -> None:
        """Download this multi data in given target path


        Examples:
            ```python
            bunch_of_data = client.get_datalake().list_data(limit=25)
            bunch_of_data.download('./downloads/')
            ```
        Arguments:
            target_path (str or Path, optional): Target path where to download. Defaults to './'.
            force_replace: (bool, optional): Replace an existing file if exists. Defaults to False.
            max_workers (int, optional): Number of max workers used to download. Defaults to os.cpu_count() + 4.
            use_id (bool, optional): If true, will download file with id and extension as file name. Defaults to False.
        """

        def download_one_data(item: Data):
            return item._do_download(target_path, force_replace, use_id=use_id)

        results = mlt.do_mlt_function(
            self.items, download_one_data, lambda item: item.id, max_workers=max_workers
        )
        downloaded = countOf(results.values(), True)

        logger.info(
            f"{downloaded} data downloaded (over {len(results)}) in directory {target_path}"
        )

    @exception_handler
    @beartype
    def wait_for_upload_done(
        self, blocking_time_increment: float = 1.0, attempts: int = 20
    ):
        errors = {}
        attempt = 0
        while attempt < attempts:
            still_pending = 0
            for data in self:
                if not data.is_ready():
                    data.sync()
                    if not data.is_ready():
                        still_pending += 1

                if (
                    data.upload_status == DataUploadStatus.ERROR
                    and data.filename not in errors
                ):
                    errors[data.filename] = data

            if still_pending == 0:
                break

            logger.info(
                f"{still_pending} are still being processed by our services, waiting for {blocking_time_increment}s "
                f"and retrying {attempts - attempt} times."
            )
            sleep(blocking_time_increment)
            attempt += 1

        if attempt >= attempts:
            raise WaitingAttemptsTimeout(
                f"Data is still being processed, but we waited for {blocking_time_increment * attempts}s. "
                "Please wait a few more moment"
            )

        if len(errors) > 0:
            filenames = ", ".join(list(errors.keys()))
            logger.error(
                f"Some data could not be processed by our services: {filenames}"
            )
