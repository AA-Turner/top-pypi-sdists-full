import logging
from functools import partial
from operator import countOf
from pathlib import Path
from uuid import UUID

import orjson
from beartype import beartype

import picsellia.exceptions as exceptions
from picsellia import pxl_multithreading as mlt
from picsellia.colors import Colors
from picsellia.compatibility import add_data_mandatory_query_parameters
from picsellia.decorators import exception_handler
from picsellia.sdk.annotation import Annotation
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.data import Data, MultiData
from picsellia.sdk.downloadable import Downloadable
from picsellia.sdk.multi_object import MultiObject
from picsellia.sdk.tag import Tag
from picsellia.sdk.taggable import Taggable
from picsellia.sdk.worker import Worker
from picsellia.types.enums import DataType, DataUploadStatus, TagTarget
from picsellia.types.schemas import (
    AssetSchema,
    ImageMetaSchema,
    ImageSchema,
    VideoMetaSchema,
    VideoSchema,
)

logger = logging.getLogger("picsellia")


class Asset(Dao, Downloadable, Taggable):
    def __init__(self, connexion: Connection, dataset_version_id: UUID, data: dict):
        Dao.__init__(self, connexion, data)
        Downloadable.__init__(self)
        Taggable.__init__(self, TagTarget.ASSET)
        self._dataset_version_id = dataset_version_id
        self._embeddings = None

    @property
    def dataset_version_id(self) -> UUID:
        """UUID of (DatasetVersion) where this (Asset) is"""
        return self._dataset_version_id

    @property
    def data_id(self) -> UUID:
        """UUID of (Data) of this (Asset)"""
        return self._data_id

    @property
    def object_name(self) -> str:
        """Object name of this (Asset)"""
        return self._object_name

    @property
    def filename(self) -> str:
        """Filename of this (Asset)"""
        return self._filename

    @property
    def large(self) -> bool:
        """If true, this (Asset) file is considered large"""
        return True

    @property
    def type(self) -> DataType:
        """Type of this (Asset)"""
        return self._type

    @property
    def width(self) -> int:
        """Width of this (Asset)."""
        return self._width

    @property
    def height(self) -> int:
        """Height of this (Asset)."""
        return self._height

    @property
    def content_type(self) -> str | None:
        """Content type of this (Asset)."""
        return self._content_type

    @property
    def duration(self) -> int:
        """This field is no longer supported"""
        return 0

    @property
    def metadata(self) -> dict | None:
        """Metadata of this (Asset). Can be None"""
        return self._metadata

    @property
    def custom_metadata(self) -> dict | None:
        """Custom metadata of this (Asset). Can be None"""
        return self._custom_metadata

    @property
    def embeddings(self) -> dict | None:
        """Embeddings of this (Asset). Can be None if asset was not indexed"""
        if not self._embeddings:
            self._load_embeddings()
        return self._embeddings

    def __str__(self):
        return f"{Colors.YELLOW}Asset '{self.filename}' ({self.type}) {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> AssetSchema:
        schema = AssetSchema(**data)
        self._data_id = schema.data.id

        # Downloadable properties
        self._object_name = schema.data.object_name
        self._filename = schema.data.filename
        self._url = schema.data.url
        self._metadata = schema.data.metadata
        self._custom_metadata = schema.data.custom_metadata

        self._type = schema.data.type
        self._content_type = schema.data.content_type
        self._height = schema.data.meta.height
        self._width = schema.data.meta.width
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/asset/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def reset_url(self) -> str:
        """Reset url property of this Asset by calling platform.

        Returns:
            A url as str of this Asset.
        """
        r = self.connection.get(f"/api/data/{self.data_id}/presigned-url")
        self._url = r.json()["presigned_url"]
        return self._url

    @exception_handler
    @beartype
    def to_data_schema(self) -> ImageSchema | VideoSchema:
        if self.type == DataType.IMAGE:
            meta = ImageMetaSchema(height=self.height, width=self.width)
            schema_class = ImageSchema
        elif self.type == DataType.VIDEO:
            meta = VideoMetaSchema(height=self.height, width=self.width)
            schema_class = VideoSchema
        else:  # pragma: no cover
            raise NotImplementedError()

        return schema_class(
            id=self.data_id,
            object_name=self.object_name,
            filename=self.filename,
            type=self.type,
            url=self._url,
            meta=meta,
            upload_status=DataUploadStatus.DONE,
            content_type=self._content_type,
        )

    @exception_handler
    @beartype
    def get_tags(self) -> list[Tag]:
        """Retrieve the tags of your asset.

        Examples:
            ```python
            tags = asset.get_tags()
            assert tags[0].name == "bicycle"
            ```

        Returns:
            List of (Tag) objects
        """
        r = self.sync()
        return [Tag(self.connection, item) for item in r["tags"]]

    @exception_handler
    @beartype
    def get_data(self):
        """Retrieve data of this asset

            ```python
            data = asset.get_data()
            assert data.id == asset.data_id
            assert data.filename == asset.filename
            ```

        Returns:
            A (Data) object
        """
        r = self.connection.get(f"/api/data/{self.data_id}").json()
        return Data(self.connection, UUID(r["datalake_id"]), r)

    @exception_handler
    @beartype
    def get_data_tags(self) -> list[Tag]:
        """Retrieve data tags of this asset

            ```python
            tags = asset.get_data_tags()
            assert tags[0].name == "bicycle"
            ```

        Returns:
            List of (Tag) objects
        """
        r = self.connection.get(f"/api/data/{self.data_id}").json()
        return [Tag(self.connection, item) for item in r["tags"]]

    @exception_handler
    @beartype
    def get_annotation(self, worker: Worker | None = None) -> Annotation:
        """Retrieve the last annotation created on this asset.

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            some_annotation = one_asset.get_annotation()
            ```

        Returns:
            An object (Annotation)
        """
        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        r = self.connection.get(f"/api/asset/{self.id}/annotations/find").json()
        return Annotation(self.connection, self.dataset_version_id, self.id, r)

    @exception_handler
    @beartype
    def create_annotation(
        self, duration: float | int = 0.0, worker: Worker | None = None
    ) -> Annotation:
        """Create an annotation on this asset.

        This method can be called on asset that are not synced in a campaign.

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            some_annotation = one_asset.create_annotation(0.120)
            ```

        Arguments:
            duration (float, optional): Duration of the annotation. Defaults to 0.0.

        Returns:
            An object (Annotation)
        """
        payload = {"duration": float(duration)}
        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        r = self.connection.post(
            f"/api/asset/{self.id}/annotations", data=orjson.dumps(payload)
        ).json()
        return Annotation(self.connection, self.dataset_version_id, self.id, r)

    @exception_handler
    @beartype
    def list_annotations(self) -> list[Annotation]:
        """List all annotation of an asset

        Examples:
            ```python
            annotations = one_asset.list_annotations()
            ```

        Returns:
            A list of (Annotation)
        """
        r = self.connection.get(f"/api/asset/{self.id}/annotations").json()
        return [
            Annotation(self.connection, self.dataset_version_id, self.id, item)
            for item in r["items"]
        ]

    @exception_handler
    @beartype
    def delete_annotations(self, workers: list[Worker] | None = None) -> None:
        """Delete all annotations of an asset: it will erase every shape of every annotation.

        This method cannot be called on dataset with a campaign.

        Workers parameter is deprecated and cannot be used anymore. It will be removed in 6.27
        If given, this method will raise, to prevent unexpected behaviour

        :warning: **DANGER ZONE**: Be careful here !

        Examples:
            ```python
            one_asset.delete_annotations()
            ```
        """
        payload = {"asset_ids": [self.id]}
        if workers is not None:
            logger.warning("workers is deprecated and should not be used anymore.")
            raise NotImplementedError()

        self.connection.delete(
            f"/api/dataset/version/{self.dataset_version_id}/annotations",
            data=orjson.dumps(payload),
        )
        logger.info(f"All annotations of {self} were removed.")

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this asset from its dataset

        :warning: **DANGER ZONE**: Be very careful here!

        Remove this asset and its annotation from the dataset it belongs

        Examples:
            ```python
            one_asset.delete()
            ```
        """
        self.connection.delete(f"/api/asset/{self.id}")
        logger.info(f"{self} removed from dataset")

    def _load_embeddings(self) -> dict | None:
        r = self.connection.get(
            f"/api/visual-search/dataset-version/{self.dataset_version_id}/points/scroll",
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


class MultiAsset(MultiObject[Asset], Taggable):
    @beartype
    def __init__(
        self, connexion: Connection, dataset_version_id: UUID, items: list[Asset]
    ):
        MultiObject.__init__(self, connexion, items)
        Taggable.__init__(self, TagTarget.ASSET)
        self.dataset_version_id = dataset_version_id

    def __str__(self) -> str:
        return f"{Colors.GREEN}MultiAsset for dataset version {self.dataset_version_id} {Colors.ENDC}, size: {len(self)}"

    def __getitem__(self, key) -> "Asset | MultiAsset":
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.items)))
            assets = [self.items[i] for i in indices]
            return MultiAsset(self.connection, self.dataset_version_id, assets)
        return self.items[key]

    @beartype
    def __add__(self, other) -> "MultiAsset":
        self.assert_same_connection(other)
        items = self.items.copy()
        if isinstance(other, MultiAsset):
            items.extend(other.items.copy())
        elif isinstance(other, Asset):
            items.append(other)
        else:
            raise exceptions.BadRequestError("You can't add these two objects")

        return MultiAsset(self.connection, self.dataset_version_id, items)

    @beartype
    def __iadd__(self, other) -> "MultiAsset":
        self.assert_same_connection(other)

        if isinstance(other, MultiAsset):
            self.extend(other.items.copy())
        elif isinstance(other, Asset):
            self.append(other)
        else:
            raise exceptions.BadRequestError("You can't add these two objects")

        return self

    def copy(self) -> "MultiAsset":
        return MultiAsset(self.connection, self.dataset_version_id, self.items.copy())

    @exception_handler
    @beartype
    def split(self, ratio: float) -> tuple["MultiAsset", "MultiAsset"]:
        s = round(ratio * len(self.items))
        return MultiAsset(
            self.connection, self.dataset_version_id, self.items[:s]
        ), MultiAsset(self.connection, self.dataset_version_id, self.items[s:])

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete assets from their dataset

        :warning: **DANGER ZONE**: Be very careful here!

        Remove these assets and its annotation from the dataset it belongs

        Examples:
            ```python
            some_assets = dataset.list_assets()[:10]
            some_assets.delete()
            ```
        """
        payload = {"ids": self.ids}
        self.connection.delete(
            f"/api/dataset/version/{self.dataset_version_id}/assets",
            data=orjson.dumps(payload),
        )
        logger.info(f"{len(self.items)} assets removed from {self}")

    @exception_handler
    @beartype
    def download(
        self,
        target_path: str | Path = "./",
        force_replace: bool = False,
        max_workers: int | None = None,
        use_id: bool = False,
    ) -> None:
        """Download this multi asset in given target path


        Examples:
            ```python
            bunch_of_assets = client.get_dataset("foo_dataset").get_version("first").list_assets()
            bunch_of_assets.download('./downloads/')
            ```
        Arguments:
            target_path (str or Path, optional): Target path where to download. Defaults to './'.
            max_workers (int, optional): Number of max workers used to download. Defaults to os.cpu_count() + 4.
            force_replace: (bool, optional): Replace an existing file if exists. Defaults to False.
            use_id (bool, optional): If true, will download file with id and extension as file name. Defaults to False.
        """

        def download_one_data(item: Asset):
            return item._do_download(target_path, force_replace, use_id=use_id)

        results = mlt.do_mlt_function(
            self.items, download_one_data, lambda item: item.id, max_workers=max_workers
        )
        downloaded = countOf(results.values(), True)

        logger.info(
            f"{downloaded} assets downloaded (over {len(results)}) in directory {target_path}"
        )

    @exception_handler
    @beartype
    def delete_annotations(self, workers: list[Worker] | None = None) -> None:
        """Delete all annotations of all these assets: it will erase every shape of every annotation of every asset.

        Workers parameter is deprecated and cannot be used anymore. It will be removed in 6.27
        If given, this method will raise, to prevent unexpected behaviour

        :warning: **DANGER ZONE**: Be careful here !

        Examples:
            ```python
            multiple_assets.delete_annotations()
            ```
        """
        payload = {"asset_ids": self.ids}
        if workers:
            logger.warning("workers is deprecated and should not be used anymore.")
            raise NotImplementedError()

        self.connection.delete(
            f"/api/dataset/version/{self.dataset_version_id}/annotations",
            data=orjson.dumps(payload),
        )
        logger.info(f"All annotations of {len(self)} assets were removed.")

    @exception_handler
    @beartype
    def as_list_of_data(self) -> list[Data]:
        """
            Convert a MultiAsset into a List of Data. Assets can come from different Datalake.
            This is slower than calling .as_multidata(), so if you know that all your data are coming
            from the same datalake, you should call .as_multidata instead

        Returns:
            A list of (Data) object
        """
        if not self.items:  # pragma: no cover
            raise exceptions.NoDataError("There is no data into this MultiAsset")

        return [asset.get_data() for asset in self.items]

    @exception_handler
    @beartype
    def as_multidata(self, force_refresh: bool = True) -> MultiData:
        """
            Convert a MultiAsset into a MultiData.
            Assets must all be in the same datalake to be retrieved.
            In case of a dataset with multiple datalake source, you can use .as_list_of_data() that will return a list of data but slower

        Arguments:
            force_refresh (bool, optional): when False, will not refresh data by calling platform.

        Returns:
            a (MultiData) object
        """
        if not self.items:  # pragma: no cover
            raise exceptions.NoDataError("There is no data into this MultiAsset")

        if force_refresh:
            data_list = self._retrieve_all_data_with_refresh()
        else:
            data_list = self._retrieve_all_data_without_refresh()
        return MultiData(self.connection, data_list[0].datalake_id, data_list)

    def _retrieve_all_data_with_refresh(self):
        def _do_list_data_of_datalake(
            datalake_id: UUID,
            ids: list[UUID],
            limit: int,
            offset: int,
        ) -> tuple[list[Data], int]:
            params = {"limit": limit, "offset": offset}
            data = {"ids": ids}
            add_data_mandatory_query_parameters(data)
            r = self.connection.xget(
                f"/api/datalake/{datalake_id}/datas",
                params=params,
                data=orjson.dumps(data),
            ).json()
            return (
                [Data(self.connection, datalake_id, item) for item in r["items"]],
                r["count"],
            )

        first_data = self.items[0].get_data()
        if len(self.items) == 1:
            return [first_data]

        return mlt.do_paginate(
            limit=None,
            offset=None,
            page_size=None,
            f=partial(
                _do_list_data_of_datalake,
                first_data.datalake_id,
                [asset.data_id for asset in self.items],
            ),
        )

    def _retrieve_all_data_without_refresh(self):
        first_data = self.items[0].get_data()
        return [
            Data(
                self.connection,
                first_data.datalake_id,
                data=asset.to_data_schema().model_dump(),
            )
            for asset in self.items
        ]
