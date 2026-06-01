import logging
import os
from collections import Counter
from datetime import date
from functools import partial
from pathlib import Path
from typing import Any
from uuid import UUID

import orjson
from beartype import beartype
from picsellia_annotations.coco import Category, COCOFile
from picsellia_annotations.coco import Image as COCOImage
from picsellia_annotations.video_coco import Video as COCOVideo
from picsellia_annotations.video_coco import VideoCOCOFile
from picsellia_annotations.voc import Object
from tqdm import tqdm

import picsellia.pxl_multithreading as mlt
from picsellia import exceptions
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.exceptions import (
    BadRequestError,
    ForbiddenError,
    NoDataError,
    RequestTooLargeError,
    ResourceNotFoundError,
)
from picsellia.sdk.annotation import Annotation, MultiAnnotation
from picsellia.sdk.annotation_campaign import AnnotationCampaign
from picsellia.sdk.asset import Asset, MultiAsset
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.data import Data, MultiData
from picsellia.sdk.fast_training import FastTraining
from picsellia.sdk.job import Job
from picsellia.sdk.label import Label
from picsellia.sdk.label_group import LabelGroup
from picsellia.sdk.processing import Processing
from picsellia.sdk.tag import Tag, TagTarget
from picsellia.sdk.taggable import Taggable
from picsellia.sdk.worker import Worker
from picsellia.services import coco_importer, voc_importer, yolo_importer
from picsellia.services.asset_splitter import AssetSplitter
from picsellia.services.coco_file_builder import COCOFileBuilder
from picsellia.services.lister.asset_lister import AssetFilter, AssetLister
from picsellia.services.visual_search import (
    DatasetVersionVisualSearchService,
    PolygonVisualSearchService,
    RectangleVisualSearchService,
)
from picsellia.types.enums import (
    AnnotationFileType,
    AnnotationStatus,
    ImportAnnotationMode,
    InferenceType,
    ObjectDataType,
)
from picsellia.types.schemas import DatasetVersionSchema, DatasetVersionStats
from picsellia.utils import (
    chunk_list,
    combine_two_ql,
    convert_tag_list_to_query_language,
    filter_payload,
    flatten_dict,
)

logger = logging.getLogger("picsellia")

BATCH_IDS_SIZE = 10000


class DatasetVersion(Dao, Taggable):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)
        Taggable.__init__(self, TagTarget.DATASET_VERSION)

    @property
    def origin_id(self) -> UUID:
        """UUID of the (Dataset) origin"""
        return self._origin_id

    @property
    def name(self) -> str:
        """Name of the (Dataset) origin"""
        return self._name

    @property
    def version(self) -> str:
        """Version of this (DatasetVersion)"""
        return self._version

    @property
    def type(self) -> InferenceType:
        """Type of this (DatasetVersion)"""
        return self._type

    def __str__(self):
        return f"{Colors.YELLOW}Version '{self.version}' of dataset {self.name} {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
            print(foo_dataset_version.get_resource_url_on_platform())
            >>> "https://app.picsellia.com/dataset/62cffb84-b92c-450c-bc37-8c4dd4d0f590"
            ```

        Returns:
            Url on Platform for this resource
        """

        return f"{self.connection.host}/dataset/version/{self.id}"

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        schema = DatasetVersionSchema(**data)
        self._name = schema.name
        self._version = schema.version
        self._type = schema.type
        self._origin_id = schema.origin_id
        self._annotation_campaign_id = schema.annotation_campaign_id
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/dataset/version/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def get_tags(self) -> list[Tag]:
        """Retrieve tags of your dataset version.

        Examples:
            ```python
            tags = foo_dataset_version.get_tags()
            assert tags[0].name == "training-dataset"
            ```

        Returns:
            List of (Tag) objects
        """
        r = self.sync()
        return [Tag(self.connection, item) for item in r["tags"]]

    @exception_handler
    @beartype
    def add_data(
        self,
        data: Data | list[Data] | MultiData,
        tags: list[str | Tag] | None = None,
        wait: bool | None = True,
    ) -> Job:
        """Feed this version with data coming from a datalake.

        A versioned dataset (DatasetVersion) takes (Data) from (Datalake) and transform it as annotable (Asset).
        You can give tags that will be added as asset tags to every created asset.

        Examples:
            ```python
            foo_dataset = client.create_dataset('foo_dataset')
            foo_dataset_version_1 = foo_dataset.create_version('first')
            some_data = client.get_datalake().list_data(limit=1000)
            foo_dataset_version_1.add_data(some_data)
            ```

        Arguments:
            data (Data, list[Data] or MultiData): data to add to dataset
            tags (list[str | Tag]) : tags to add to every asset created
            wait: (bool, Optional): if True, it will wait for the background task to end. Defaults to True.

        Returns:
            A (Job) object that you can use to monitor the progress of this operation.
        """
        if isinstance(data, Data):
            data_ids = [data.id]
        else:
            data_ids = list({data.id for data in data})

        if not data_ids:
            raise ValueError("data parameter cannot be empty")

        asset_tag_ids = set()
        asset_tag_names = set()
        if tags:
            for tag in tags:
                tag_name = tag.name if isinstance(tag, Tag) else tag
                tag_created = self.get_or_create_asset_tag(tag_name)
                asset_tag_ids.add(tag_created.id)
                asset_tag_names.add(tag_created.name)

        jobs = []
        for batch_data_ids, _ in chunk_list(data_ids, BATCH_IDS_SIZE):
            payload = {"asset_tag_ids": list(asset_tag_ids), "data_ids": batch_data_ids}
            r = self.connection.post(
                f"/api/dataset/version/{self.id}/assets", data=orjson.dumps(payload)
            ).json()
            jobs.append(
                (Job(self.connection, r["job"], version=1), len(batch_data_ids))
            )

        logger.info(
            f"Data are being added as assets to {self}.\n"
            "This operation can take some time (depending on how much asset you're adding)."
        )

        if wait:
            logger.info("Waiting for data to be added..")
            with tqdm(total=len(data_ids), initial=0, ncols=100, colour="red") as pbar:
                for job, count in jobs:
                    job.wait_for_done()
                    pbar.update(count)

        if asset_tag_names:
            tag_names = ", ".join(asset_tag_names)
            logger.info(f"Each asset created will have tags: {tag_names}")

        return jobs[-1][0]

    @exception_handler
    @beartype
    def fork(
        self,
        version: str,
        description: str | None = None,
        assets: list[Asset] | MultiAsset | Asset | None = None,
        type: InferenceType | str = InferenceType.NOT_CONFIGURED,
        with_tags: bool = False,
        with_labels: bool = False,
        with_annotations: bool = False,
        wait: bool | None = True,
    ) -> tuple["DatasetVersion", Job]:
        """Fork this dataset version into another dataset version, with the same origin.

        Will create a new dataset version, with the same origin and the given version.
        You can give a description and a default type.
        You can give a list of asset coming from this dataset version to add into the new dataset version.
        Only these assets will be added to the new dataset.
        If with_tags is True, tags of each asset will be transferred to the new dataset version.
        If with_labels is True, labels of source dataset version will be transferred into new dataset version.
        If with_annotations is True, labels and annotations will be transferred to new dataset version.
            This might take more time.

        Examples:
            ```python
            foo_dataset_version = client.get_dataset('my_datatest').get_version('first')
            assets = foo_dataset_version.list_assets(limit=100)
            bar_dataset_version = foo_dataset_version.fork(version='second', assets=assets)
            ```

        Arguments:
            version (str): new version name
            description (str, optional): description, defaults to "Forked from version '<version_name>'"
            assets ((MultiAsset) or (Asset), optional): assets to add to the new dataset version, defaults will be all assets
            type (InferenceType, optional): inference type of the new dataset version, defaults to NOT_CONFIGURED
            with_tags (bool, optional): if true tags of assets will be added to the new dataset version, defaults to false
            with_labels (bool, optional): if true, labelmap will be transferred to new dataset version, defaults to false
            with_annotations (bool, optional): if true annotations of each asset will be added to the new dataset version, defaults to false
            wait: (bool, Optional): if True, it will wait for the background task to end. Defaults to True.

        Returns:
            A tuple with (DatasetVersion) and (Job)
        """
        type = InferenceType.validate(type)

        if version == "":
            raise ValueError("Version name can't be empty")

        if description is None:
            description = f"Fork from {self.version}"

        payload = {
            "parent_id": self.id,
            "version": version,
            "description": description,
            "type": type,
            "with_tags": with_tags,
            "with_labels": with_labels,
            "with_annotations": with_annotations,
        }

        if assets is not None:
            if isinstance(assets, Asset):
                payload["asset_ids"] = [assets.id]
            elif len(assets) <= BATCH_IDS_SIZE:
                payload["asset_ids"] = [asset.id for asset in assets]
            else:
                payload["asset_ids"] = []

        r = self.connection.post(
            f"/api/dataset/{self.origin_id}/fork", data=orjson.dumps(payload)
        ).json()
        dataset_version = DatasetVersion(self.connection, r["dataset_version"])
        job = Job(self.connection, r["job"], version=1)
        if wait:
            job.wait_for_done()

        if assets is None:
            logger.info(f"{self} forked with all assets")
            return dataset_version, job

        if isinstance(assets, Asset):
            logger.info(f"{self} forked with one asset")
            return dataset_version, job

        if len(assets) <= BATCH_IDS_SIZE:
            logger.info(f"{self} forked with {len(assets)} assets")
            return dataset_version, job

        logger.info(f"{self} forked.")
        return dataset_version, self.copy_assets_to(
            dataset_version, assets, with_tags, with_annotations, wait
        )

    @exception_handler
    @beartype
    def copy_assets_to(
        self,
        destination: "DatasetVersion",
        assets: list[Asset] | MultiAsset | Asset,
        with_tags: bool = False,
        with_annotations: bool = False,
        wait: bool | None = True,
    ):
        """Copy assets from this dataset version into a destination dataset version

        assets must come from this dataset version.

        You need to give a list of asset coming from this dataset version to add into the destination dataset version.

        If with_tags is True, tags of each asset will be transferred to the destination dataset version.
        If with_annotations is True, labels and annotations will be transferred to destination dataset version.
            This might take more time.

        Examples:
            ```python
            foo_dataset_version = client.get_dataset('my_dataset').get_version('first')
            assets = foo_dataset_version.list_assets(limit=100)

            bar_dataset_version = client.get_dataset('my_dataset').get_version('second')
            foo_dataset_version.copy_assets_to(bar_dataset_version, assets, with_annotations=True)
            ```

        Arguments:
            destination (DatasetVersion): must have the same origin.
            assets ((MultiAsset), list of (Asset) or (Asset)): assets to add to the destination.
            with_tags (bool, optional): if true tags of assets will be added to copied assets. Defaults to False
            with_annotations (bool, optional): if true annotations of each asset will be added to copied assets. Defaults to False.
            wait: (bool, Optional): if True, it will wait for the background task to end. Defaults to True.

        Returns:
            A (Job) that you can wait for
        """
        if destination.origin_id != self.origin_id:
            raise BadRequestError("You cannot add assets from different origin dataset")

        if destination.id == self.id:
            raise BadRequestError(
                "You cannot copy assets inside the same dataset version"
            )

        if isinstance(assets, Asset):
            asset_ids = [assets.id]
        else:
            asset_ids = list({asset.id for asset in assets})

        jobs = []
        for batch_data_ids, _ in chunk_list(asset_ids, BATCH_IDS_SIZE):
            payload = {
                "destination_id": destination.id,
                "asset_ids": batch_data_ids,
                "with_annotations": with_annotations,
                "with_tags": with_tags,
            }
            r = self.connection.post(
                f"/api/dataset/version/{self.id}/assets/copy",
                data=orjson.dumps(payload),
            ).json()
            jobs.append(
                (Job(self.connection, r["job"], version=1), len(batch_data_ids))
            )

        logger.info(
            f"Assets from {self} are being copied to {destination}.\n"
            "This operation can take some time (depending on how much asset you're copying)."
        )
        if wait:
            logger.info("Waiting for assets to be copied..")
            with tqdm(total=len(asset_ids), initial=0, ncols=100, colour="red") as pbar:
                for job, count in jobs:
                    job.wait_for_done()
                    pbar.update(count)

        return jobs[-1][0]

    @exception_handler
    @beartype
    def find_asset(
        self,
        data: Data | None = None,
        filename: str | None = None,
        object_name: str | None = None,
        id: str | UUID | None = None,
    ) -> Asset:
        """Find an asset into this dataset version

        You can find it by giving its supposed Data object, its filename or its object name

        Examples:
            ```python
            my_asset = my_dataset_version.find_asset(filename="test.png")
            ```
        Arguments:
            data (Data, optional): data linked to asset. Defaults to None.
            filename (str, optional): filename of the asset. Defaults to None.
            object_name (str, optional): object name in the storage S3. Defaults to None.
            id (str, optional): id of the asset. Defaults to None.

        Raises:
            If no asset match the query, it will raise a NotFoundError.
            In some case, it can raise an InvalidQueryError,
                it might be because platform stores 2 assets matching this query (for example if filename is duplicated)

        Returns:
            The (Asset) found
        """
        assert not (
            data is None and filename is None and object_name is None and id is None
        ), "Select at least one criteria to find an asset"

        params = {}
        if data is not None:
            params["data_id"] = data.id

        if filename is not None:
            params["filename"] = filename

        if object_name is not None:
            params["object_name"] = object_name

        if id is not None:
            params["id"] = id

        r = self.connection.get(
            f"/api/dataset/version/{self.id}/assets/find", params=params
        ).json()
        return Asset(self.connection, self.id, r)

    @exception_handler
    @beartype
    def list_assets(
        self,
        limit: int | None = None,
        offset: int | None = None,
        page_size: int | None = None,
        order_by: list[str] | None = None,
        tags: Tag | list[Tag] | str | list[str] | None = None,
        data_tags: Tag | list[Tag] | str | list[str] | None = None,
        intersect_tags: bool = False,
        intersect_data_tags: bool = False,
        filenames: list[str] | None = None,
        object_names: list[str] | None = None,
        ids: list[str | UUID] | None = None,
        filenames_startswith: list[str] | None = None,
        q: str | None = None,
        data_ids: list[str | UUID] | None = None,
        assignment_status: str | None = None,
        assignment_step_id: UUID | None = None,
        assignment_user_id: str | UUID | None = None,
        custom_metadata: dict | None = None,
    ) -> MultiAsset:
        """List (Asset) of this (DatasetVersion)

        Examples:
            ```python
            assets = foo_dataset_version.list_assets()
            ```

        Arguments:
            limit (int, optional): the number of assets that will be retrieved
            offset (int, optional): from where to start accessing the assets. you will retrieve offset:offset+limit assets from the whole list.
            page_size (int, optional): deprecated.
            order_by (str, optional): what property to sort on. Defaults to descending created_at.
            tags (str, (Tag), list[(Tag) or str], optional): if given, will return assets that have one of given tags
                                                            by default. if `intersect_tags` is True,
                                                            it will return assets that have all the given tags
            intersect_tags (bool, optional): if True, and a list of tags is given, will return assets that have
                                             all the given tags. Defaults to False.
            data_tags (str, (Tag), list[(Tag) or str], optional): if given, will return assets that have one of given
                                                            data tags by default. if `intersect_data_tags` is True,
                                                            it will return assets that have all the given data tags
            intersect_data_tags (bool, optional): if True, and a list of data tags is given, will return assets that have
                                             all the given data tags. Defaults to False.
            filenames (list[str], optional): if given, will return assets that have filename equals to one of given filenames
            filenames_startswith (list[str], optional): if given, will return assets that have filename starting with to one of given filenames
            object_names (list[str], optional): if  given, will return assets that have object name equals to one of given object names
            ids: (list[UUID]): ids of the assets you're looking for. Defaults to None.
            q (str, optional): a query using the Picsellia Query Language. Defaults to None
            data_ids (list[UUID], optional): ids of the data linked to the assets you are looking for. Defaults to None.
            assignment_status (str, optional): only with campaigns. It's the desired status for the last assignments linked to your assets.
            assignment_step_id (UUID, optional): only with campaigns. It's the desired step of the assignment you want to retrieve.
            assignment_user_id (UUID, optional): only with campaigns. It's the desired user assigned to the assignments you want to retrieve.
            custom_metadata: (dict, optional): filter based on the custom_metadata linked to the asset's Data. Defaults to None
        Returns:
            A (MultiAsset) object that wraps some (Asset) that you can manipulate.
        """
        if page_size:
            logger.warning("page_size is deprecated and not used anymore.")

        qt = convert_tag_list_to_query_language(tags, intersect_tags)
        qd = convert_tag_list_to_query_language(
            data_tags, intersect_data_tags, prefix="data."
        )
        query = combine_two_ql(qt, combine_two_ql(q, qd))

        filters = AssetFilter.model_validate(
            {
                "limit": limit,
                "offset": offset,
                "order_by": order_by,
                "filenames": filenames,
                "object_names": object_names,
                "filename_startswith": filenames_startswith,
                "data_ids": data_ids,
                "ids": ids,
                "query": query,
                "assignment_status": assignment_status,
                "assignment_step_id": assignment_step_id,
                "assignment_user_id": assignment_user_id,
                "custom_metadata": custom_metadata,
            }
        )
        assets = AssetLister(self.connection, self.id).list_items(filters)

        if len(assets) == 0:
            raise NoDataError("No asset retrieved")

        return MultiAsset(self.connection, self.id, assets)

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete a dataset version.

        :warning: **DANGER ZONE**: Be very careful here!

        It will remove this dataset version from our database, all of its assets and annotations will be removed.
        It will also remove potential annotation campaign of this dataset version.

        Examples:
            ```python
            foo_dataset_version.delete()
            ```
        """
        self.connection.delete(f"/api/dataset/version/{self.id}")
        logger.info(f"{self} deleted")

    @exception_handler
    @beartype
    def set_type(self, type: str | InferenceType) -> None:
        """Set inference type of this DatasetVersion.
            You can pass a string with the exact key corresponding to inference type or an enum value InferenceType.

        Examples:
            ```python
            dataset_version.set_type('object_detection')
            dataset_version.set_type(InferenceType.SEGMENTATION)
            ```

        Arguments:
            type (str or InferenceType): type to give to this dataset version
        """
        inference_type = InferenceType.validate(type)
        payload = {"type": inference_type}
        r = self.connection.patch(
            f"/api/dataset/version/{self.id}", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} is now of type {inference_type.name}")

    @exception_handler
    @beartype
    def update(
        self,
        version: str | None = None,
        description: str | None = None,
        type: str | InferenceType | None = None,
    ) -> None:
        """Update version, description and type of Dataset.

        Examples:
            ```python
            dataset_version.update(description='My favourite dataset')
            ```

        Arguments:
            version (str, optional): New version name of the dataset. Defaults to None.
            description (str, optional): New description of the dataset. Defaults to None.
            type (str or InferenceType, optional): New type of the dataset. Defaults to None.
        """
        payload = {"version": version, "description": description}
        if type:
            payload["type"] = InferenceType.validate(type)
        filtered_payload = filter_payload(payload)
        r = self.connection.patch(
            f"/api/dataset/version/{self.id}",
            data=orjson.dumps(filtered_payload),
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated")

    @exception_handler
    @beartype
    def download(
        self,
        target_path: str | Path | None = None,
        force_replace: bool = False,
        max_workers: int | None = None,
        use_id: bool = False,
    ) -> None:
        """Downloads assets of a dataset version.

        It will download all assets from a dataset version into specified folder.
        If target_path is None, it will download into ./<dataset_name>/<dataset_version>
        You can precise a number of threads to use while downloading.

        Examples:
            ```python
            foo_dataset_version.download('~/Downloads/dataset_pics')
            ```
        Arguments:
            target_path (str or Path, optional): Target folder. Defaults to None.
            force_replace: (bool, optional): Replace an existing file if exists. Defaults to False.
            max_workers (int, optional): Number of max workers used to download. Defaults to os.cpu_count() + 4.
            use_id (bool, optional): If true, will download file with id and extension as file name. Defaults to False.
        """
        if target_path is not None:
            path = target_path
        else:
            path = os.path.join("./", self.name, self.version)

        Path(path).mkdir(parents=True, exist_ok=True)

        logger.debug(f"Retrieving assets of {self}...")
        multi_assets = self.list_assets()

        logger.debug("Downloading assets...")
        multi_assets.download(path, force_replace, max_workers, use_id=use_id)

        logger.info(f"Assets of {self} downloaded into {path}")

    @exception_handler
    @beartype
    def list_labels(self) -> list[Label]:
        """Get all labels of a dataset version.

        It will retrieve a list of label objects.

        Examples:
            ```python
            foo_dataset_version.create_label("today")
            labels = foo_dataset_version.list_labels()
            assert labels[0].name == "today"
            ```

        Returns:
            List of (Label)
        """
        r = self.connection.get(f"/api/dataset/version/{self.id}/labels").json()
        return [
            Label(self.connection, item, dataset_version_id=self._id)
            for item in r["items"]
        ]

    @exception_handler
    @beartype
    def create_label(self, name: str) -> Label:
        """Add label to a dataset version.

        You have to give a name to the label.

        Examples:
            ```python
            foo_dataset_version.create_label("today")
            ```
        Arguments:
            name (str): label name to create

        Returns:
            A (Label) object
        """

        payload = {"name": name}
        r = self.connection.post(
            f"/api/dataset/version/{self.id}/labels", data=orjson.dumps(payload)
        ).json()
        label = Label(self.connection, r, dataset_version_id=self._id)
        logger.info(f"{label} has been added to {self}")
        return label

    @exception_handler
    @beartype
    def get_label(self, name: str) -> Label:
        """Find label in a dataset version.

        Examples:
            ```python
            label = foo_dataset_version.get_label("today")
            ```
        Arguments:
            name (str): label name to find

        Returns:
            A (Label) object
        """

        params = {"name": name}
        r = self.connection.get(
            f"/api/dataset/version/{self.id}/labels/find", params=params
        ).json()
        return Label(self.connection, r, dataset_version_id=self._id)

    @exception_handler
    @beartype
    def get_or_create_label(self, name: str) -> Label:
        """Retrieve a label used in this dataset version by its name.
        If label does not exist, create it and return it.

        Examples:
            ```python
            label = dataset_version.get_or_create_label("new_label")
            ```
        Arguments:
            name (str): label name to retrieve or create

        Returns:
            A (label) object
        """
        try:
            return self.get_label(name)
        except ResourceNotFoundError:
            return self.create_label(name)

    @exception_handler
    @beartype
    def list_label_groups(self) -> list[LabelGroup]:
        """List all (LabelGroup) of this (DatasetVersion)

        Examples:
            ```python
            foo_dataset_version.create_label_group("group")
            labels = foo_dataset_version.list_label_groups()
            ```

        Returns:
            a list of (LabelGroup)
        """
        r = self.connection.get(f"/api/dataset/version/{self.id}/labelgroups").json()
        return [
            LabelGroup(self.connection, item, dataset_version_id=self.id)
            for item in r["items"]
        ]

    @exception_handler
    @beartype
    def create_label_group(
        self, name: str, parent: LabelGroup | None = None
    ) -> LabelGroup:
        """Add label to a dataset version.

        You have to give a name to the label.

        Examples:
            ```python
            foo_dataset_version.create_label("today")
            ```
        Arguments:
            name (str): name of this group
            parent (LabelGroup, optional): parent of this group

        Returns:
            A (LabelGroup) object
        """

        payload: dict[str, Any] = {"name": name}
        if parent:
            if parent.dataset_version_id != self.id:
                raise ValueError("Given parent must be in this DatasetVersion")
            payload["parent_id"] = parent.id

        r = self.connection.post(
            f"/api/dataset/version/{self.id}/labelgroups", data=orjson.dumps(payload)
        ).json()
        group = LabelGroup(self.connection, r, dataset_version_id=self.id)
        logger.info(f"{group} has been added to {self}")
        return group

    @exception_handler
    @beartype
    def list_annotations(
        self,
        worker: Worker | None = None,
        status: AnnotationStatus | str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
        page_size: int | None = None,
    ) -> MultiAnnotation:
        """Retrieve annotations of a dataset version.

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            annotations = foo_dataset_version.list_annotations()
            ```
        Arguments:
            limit (int, optional): Limit number of annotations to retrieve.
                Defaults to None, all annotations will be retrieved.
            offset (int, optional): Offset to begin with when listing annotations.
                Defaults to None, starting at 0.
            page_size (int, optional): Size of each page when retrieving .
                Defaults to None, page will be equals to default pagination.
            order_by (list[str], optional): Order annotation by some criteria.
                Defaults to None.
            status (AnnotationStatus, optional): Status of annotations to retrieve.
                Defaults to None.

        Raises:
            NoDataError: When no annotations retrieved

        Returns:
            A (MultiAnnotation) object
        """
        if status:
            status = AnnotationStatus.validate(status)

        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        annotations = mlt.do_paginate(
            limit,
            offset,
            page_size,
            partial(self._do_list_annotations, status, order_by),
        )

        if len(annotations) == 0:
            raise NoDataError("No annotation retrieved")

        return MultiAnnotation(self.connection, self.id, annotations)

    def _do_list_annotations(
        self,
        status: AnnotationStatus | None,
        order_by: list[str] | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Annotation], int]:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by is not None:
            params["order_by"] = order_by
        if status is not None:
            params["status"] = status.value

        r = self.connection.get(
            f"/api/dataset/version/{self.id}/annotations", params=params
        ).json()
        annotations = [
            Annotation(self.connection, self.id, UUID(item["asset_id"]), item)
            for item in r["items"]
        ]
        count = r["count"]
        return annotations, count

    def _list_annotation_ids(
        self,
        status: AnnotationStatus | None = None,
        asset_ids: list[UUID] | None = None,
    ):
        params = {}
        if status is not None:
            params["status"] = status.value
        if asset_ids is not None:
            params["asset_ids"] = asset_ids
        return self.connection.get(
            f"/api/dataset/version/{self.id}/annotations/ids", params=params
        ).json()

    @exception_handler
    @beartype
    def load_annotations(
        self,
        worker: Worker | None = None,
        status: AnnotationStatus | None = None,
        assets: list[Asset] | MultiAsset | None = None,
        chunk_size: int | None = None,
        max_workers: int | None = None,
        skip_error: bool = False,
    ) -> dict:
        """Load these annotation by retrieving shapes with labels, asset_id and worker_id

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            dict_annotations = foo_dataset_version.load_annotations()
            ```
        Arguments:
            status (AnnotationStatus, optional): Status of annotations to retrieve. Defaults to None.
            assets (list[Asset] or MultiAsset, None], optional): List of the asset to retrieve. Defaults to None.
            chunk_size (int, optional): Size of chunk of annotations to load by request. Defaults to 10 for segmentation and multi dataset, 100 for other types.
            max_workers (int, optional): Number of max workers used to load annotations. Defaults to os.cpu_count() + 4.
            skip_error (bool, optional): skip error of a chunk and return partial annotations. Default to False

        Returns:
            A dict of annotations
        """
        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        if assets is not None:
            ids = []
            asset_ids = [asset.id for asset in assets]
            for ids_chunk in mlt.do_chunk_called_function(
                asset_ids,
                f=partial(self._list_annotation_ids, status),
                chunk_size=50,
            ):
                ids.extend(ids_chunk)
        else:
            ids = self._list_annotation_ids(status)

        if not chunk_size:
            if self.type in [
                InferenceType.SEGMENTATION,
                InferenceType.LINE,
                InferenceType.MULTI,
            ]:
                chunk_size = 10
            else:
                chunk_size = 100

        return MultiAnnotation.load_annotations_from_ids(
            self.connection, self.id, ids, chunk_size, max_workers, skip_error
        )

    @exception_handler
    @beartype
    def export_annotation_file(
        self,
        annotation_file_type: AnnotationFileType | str,
        target_path: str | Path = "./",
        assets: MultiAsset | list[Asset] | None = None,
        worker: Worker | None = None,
        status: AnnotationStatus | str | None = None,
        force_replace: bool = True,
        export_video: bool = False,
        use_id: bool = False,
    ) -> str:
        """Export annotations of this dataset version into a file, and download it.
        It will only export the last created annotation and its shapes.

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            dataset_v0.export_annotation_file(AnnotationFileType.COCO, "./")
            ```
        Arguments:
            annotation_file_type (AnnotationFileType): choose to export in Pascal VOC format, YOLO format or COCO format.
            target_path (str or Path, optional): directory path where file is downloaded. Defaults to current directory.
            assets (MultiAsset or list[Asset], optional): a list of assets of this dataset version.
                Only these assets will be concerned by this export. Defaults to None.
            status (AnnotationStatus, optional): status of annotations. Defaults to None.
            force_replace (bool, optional): if true, will replace an existing file annotation. Defaults to True.
            export_video (bool, optional): if true, will export video of your dataset, instead of assets. Defaults to False.
            use_id (bool, optional): if true, id will be used when generating annotation files.
                For example, in coco file, assuming you have "image_1.png", it will generate tag like
                <filename>018c59e3-b21b-7006-a82b-047d3931db81.png</filename>.
                You should combine this method with dataset_version.download(use_id=True)
                Defaults to False.
        Returns:
            Path of downloaded file.
        """
        payload = {
            "type": AnnotationFileType.validate(annotation_file_type),
            "export_video": export_video,
            "use_id": use_id,
        }
        if assets is not None:
            payload["asset_ids"] = [asset.id for asset in assets]

        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        if status is not None:
            payload["status"] = AnnotationStatus.validate(status)

        r = self.connection.post(
            f"/api/dataset/version/{self.id}/annotations/export",
            data=orjson.dumps(payload),
        ).json()

        path = os.path.join(target_path, r["object_name"])
        self.connection.do_download_file(
            path=path,
            url=r["presigned_url"],
            is_large=True,
            force_replace=force_replace,
        )
        return path

    @exception_handler
    @beartype
    def build_coco_file_locally(
        self,
        worker: Worker | None = None,
        status: AnnotationStatus | str | None = None,
        enforced_ordered_categories: list[str] | None = None,
        assets: MultiAsset | list[Asset] | None = None,
        use_id: bool = False,
    ) -> COCOFile:
        """Build a coco file locally instead of exporting it from the platform.
        This method will load annotations of a dataset with given filters, then build all coco annotations,
        then load all assets and labels from platform needed in this coco file and return a coco file.
        It will only build a file with the last created Annotation that match given filters.

        Returned coco file can be then written into a file

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            coco_file = dataset_v0.build_coco_file_locally()
            ```

        Arguments:
            status (AnnotationStatus, optional): status of annotations. Defaults to None.
            assets (MultiAsset or list[Asset], optional): assets of annotations. Defaults to None.
            enforced_ordered_categories (list[str], optional): use this parameter to enforce an order of categories
                                                                 for the coco file. Defaults to None.
            use_id (bool, optional): set True if you downloaded assets with id as filenames, COCO File will then use ids
                                     as filenames. Defaults to False.
        Returns:
            A COCO File object
        """
        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        label_names = {str(label.id): label.name for label in self.list_labels()}
        if enforced_ordered_categories:
            for enforced_category in enforced_ordered_categories:
                if enforced_category not in label_names.values():
                    raise ResourceNotFoundError(
                        f"Category {enforced_category} is not a label of this dataset version"
                    )

        skeletons = {}
        if self.type in [InferenceType.KEYPOINT, InferenceType.MULTI]:
            skeletons = {
                label_names[label_id]: skeleton
                for label_id, skeleton in self.get_skeletons().items()
            }

        categories = COCOFileBuilder.prepare_categories(
            list(label_names.values()), enforced_ordered_categories
        )
        builder = COCOFileBuilder(categories)
        annotations = self.load_annotations(status=status, assets=assets)
        asset_ids = builder.load_coco_annotations(annotations)
        loaded_assets = self.list_assets(ids=asset_ids)
        builder.load_coco_images(loaded_assets, use_id=use_id)
        builder.load_coco_categories(skeletons)
        return builder.build()

    @exception_handler
    @beartype
    def _assert_import_annotation_possible(self):
        self.sync()
        if self.type not in [
            InferenceType.OBJECT_DETECTION,
            InferenceType.SEGMENTATION,
            InferenceType.CLASSIFICATION,
            InferenceType.KEYPOINT,
            InferenceType.MASK,
        ]:
            raise TypeError(
                f"You need to set up type of this dataset before importing annotation files."
                f"This dataset is {self.type} at the moment. Call .set_type() to change type."
            )

    @exception_handler
    @beartype
    def _assert_labels_created(
        self, labels_retrieved: list[str], labels_file: list[str]
    ):
        if len(labels_retrieved) != len(labels_file):
            labels_not_found = set(labels_retrieved).difference(set(labels_file))
            raise ResourceNotFoundError(
                f"Labels {labels_not_found} were not found during upload."
                f"Call import with force_create_label=True or create missing labels manually"
            )

    @exception_handler
    @beartype
    def import_annotations_yolo_files(
        self,
        configuration_yaml_path: str | Path,
        file_paths: list[str | Path],
        worker: Worker | None = None,
        mode: ImportAnnotationMode | str = ImportAnnotationMode.REPLACE,
        force_create_label: bool = True,
        fail_on_asset_not_found: bool = True,
        status: AnnotationStatus | None = None,
    ) -> dict[str, int]:
        """Read a yolo annotation configuration file, then read all given file paths with annotations parse it and create annotations and shape for all assets

        Annotations of assets that are already in a campaign won't be imported.

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            dataset_v0.import_annotations_yolo_files(configuration_yaml_path="data.yaml", file_paths=["asset1.txt"])
            ```

        Arguments:
            configuration_yaml_path (str, Path): Path to file of configuration
            file_paths (list[str] or Path): Paths of annotation files to import
            mode (ImportAnnotationMode, optional): Mode used to import.
                    REPLACE will delete worker annotation if exists and replace it.
                    CONCATENATE will create shapes on existing annotation.
                    SKIP will do nothing on existing annotation.
                    Defaults to ImportAnnotationMode.REPLACE.
            force_create_label (bool): Ensures labels are created if they don't exist. Defaults to True.
            fail_on_asset_not_found (bool): If one filename is not found in dataset, fail before importing annotations. Defaults to True.
            status (AnnotationStatus): Annotation status to set to created annotations.

        Raises:
            FileNotFoundException: if file is not found

        Returns:
            A dict with annotation id as string keys and number of shapes created as integer.
        """
        mode = ImportAnnotationMode.validate(mode)

        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        if not file_paths:
            logger.info("No file given ")
            return {}

        self._assert_import_annotation_possible()

        logger.info("Reading filenames")
        # filename -> file_path
        files: dict[str, Path] = yolo_importer.read_filenames_from_file_paths(
            file_paths
        )

        logger.info("Reading labels from configuration file")
        label_names: list[str] = yolo_importer.parse_configuration_file(
            configuration_yaml_path
        )
        labels: list[Label] = self._create_labels_from_names(
            label_names, force_create_label
        )

        logger.info("Retrieving assets")
        multi_assets = self.list_assets(filenames_startswith=list(files.keys()))
        assets: dict[str, Asset] = yolo_importer.match_assets_with_filenames(
            files, multi_assets
        )
        yolo_importer.assert_coherence_files_assets(
            files, assets, fail_on_asset_not_found
        )

        logger.info("Parsing yolo files")
        annotations = yolo_importer.parse_files_to_annotations(
            self.type, files, assets, labels
        )

        logger.info("Creating annotations..")
        results = mlt.do_chunk_called_function(
            annotations, partial(self._bulk_create_annotations, mode, status)
        )
        return flatten_dict(results, lambda value: value >= 0)

    @exception_handler
    @beartype
    def _create_labels_from_names(
        self, label_names: list[str], force_create_label: bool
    ):
        if force_create_label:
            self._bulk_get_or_create_labels(label_names)

        return [self.get_label(label_name) for label_name in label_names]

    @exception_handler
    @beartype
    def import_annotation_voc_file(
        self,
        file_path: str | Path,
        worker: Worker | None = None,
        mode: ImportAnnotationMode | str = ImportAnnotationMode.REPLACE,
        force_create_label: bool = True,
        status: AnnotationStatus | None = None,
    ) -> dict[str, int]:
        """Read a Pascal VOC file, parse it and create some annotations and shape for one given asset

        Annotations of assets that are already in a campaign won't be imported.

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            dataset_v0.import_annotation_voc_file(file_path="voc.xml")
            ```

        Arguments:
            file_path (str or Path): Path of file to import
            mode (ImportAnnotationMode, optional): Mode used to import.
                    REPLACE will delete worker annotation if exists and replace it.
                    CONCATENATE will create shapes on existing annotation.
                    KEEP will do nothing on existing annotation.
                    Defaults to ImportAnnotationMode.REPLACE.
            force_create_label (bool): Ensures labels are created if they don't exist. Defaults to True.
            status (AnnotationStatus, optional): status given to created annotations. Defaults to None.

        Raises:
            FileNotFoundException: if file is not found

        Returns:
            A dict with annotation id as string keys and number of shapes created as integer.
        """
        self._assert_import_annotation_possible()

        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        mode = ImportAnnotationMode.validate(mode)

        logger.info("Parsing VOC file")
        vocfile = voc_importer.parse_file(file_path)
        objects = voc_importer.parse_objects(vocfile)

        logger.info("Reading labels")
        labels: dict[str, str] = self._read_labels_from_voc_objects(
            objects, force_create_label
        )

        logger.info("Retrieving asset")
        asset = self.find_asset(filename=vocfile.annotation.filename)

        logger.info("Reading shapes..")
        annotations = voc_importer.read_annotations_from_voc_objects(
            self.type, objects, labels, asset
        )

        logger.info("Creating annotations..")
        return self._bulk_create_annotations(mode, status, annotations)

    @exception_handler
    @beartype
    def _read_labels_from_voc_objects(
        self, objects: list[Object], force_create_label: bool
    ) -> dict[str, str]:
        label_names = list({obj.name for obj in objects})
        if force_create_label:
            self._bulk_get_or_create_labels(label_names)

        labels: dict[str, str] = {}
        for label in self.list_labels():
            if label.name in label_names:
                labels[label.name] = str(label.id)

        self._assert_labels_created(list(labels.keys()), label_names)
        return labels

    @exception_handler
    @beartype
    def import_annotations_coco_file(
        self,
        file_path: Path | str,
        worker: Worker | None = None,
        mode: ImportAnnotationMode | str = ImportAnnotationMode.REPLACE,
        force_create_label: bool = True,
        fail_on_asset_not_found: bool = True,
        status: AnnotationStatus | None = None,
        use_id: bool = False,
    ) -> dict[str, int]:
        """Read a COCO file, parse it and create some annotations and shape for given assets

        Annotations of assets that are already in a campaign won't be imported.

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            dataset_v0.import_annotations_coco_file(file_path="coco.json")
            ```

        Arguments:
            file_path (str): Path of file to import
            mode (ImportAnnotationMode, optional): Mode used to import.
                    REPLACE will delete worker annotation if exists and replace it.
                    CONCATENATE will create shapes on existing annotation.
                    KEEP will do nothing on existing annotation.
                    Defaults to ImportAnnotationMode.REPLACE.
            force_create_label (bool): Ensure labels are created if they don't exist. Defaults to True
            fail_on_asset_not_found (bool): Raise an error if asset is not found. Defaults to True
            status (AnnotationStatus, optional): Annotation Status of imported annotations, default will be PENDING.
                                                 Defaults to None.
            use_id (bool, optional): If your coco file have asset id as filename, set this to true.
                                                Defaults to False.

        Raises:
            FileNotFoundException: if file is not found

        Returns:
            A dict with annotation id as string keys and number of shapes created as integer.

        """
        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        self._assert_import_annotation_possible()
        mode = ImportAnnotationMode.validate(mode)

        logger.info(f"Parsing file {file_path}..")
        cocofile = coco_importer.parse_coco_file(file_path)
        return self._import_coco_file(
            cocofile,
            mode,
            force_create_label,
            fail_on_asset_not_found,
            status,
            use_id,
        )

    @exception_handler
    @beartype
    def import_annotations_coco_video_file(
        self,
        file_path: Path | str,
        worker: Worker | None = None,
        mode: ImportAnnotationMode | str = ImportAnnotationMode.REPLACE,
        force_create_label: bool = True,
        fail_on_asset_not_found: bool = True,
        status: AnnotationStatus | None = None,
        use_id: bool = False,
    ) -> dict[str, int]:
        """Read a Video COCO file, parse it and create some annotations and shape for given assets.
        Experimental feature: the availability and support of this feature can change until it’s stable

        Annotations of assets that are already in a campaign won't be imported.

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            dataset_v0.import_annotations_coco_video_file(file_path="coco_vid.json")
            ```

        Arguments:
            file_path (str): Path of file to import
            mode (ImportAnnotationMode, optional): Mode used to import.
                    REPLACE will delete worker annotation if exists and replace it.
                    CONCATENATE will create shapes on existing annotation.
                    KEEP will do nothing on existing annotation.
                    Defaults to ImportAnnotationMode.REPLACE.
            force_create_label (bool): Ensure labels are created if they don't exist. Defaults to True
            fail_on_asset_not_found (bool): Raise an error if asset is not found. Defaults to True
            status (AnnotationStatus, optional): Annotation Status of imported annotations, default will be PENDING.
                                                 Defaults to None.
            use_id (bool, optional): If your coco file have asset id as filename, set this to true.
                                                Defaults to False.

        Raises:
            FileNotFoundException: if file is not found

        Returns:
            A dict with annotation id as string keys and number of shapes created as integer.

        """
        logger.warning(
            "Experimental feature: the availability and support of this feature can change until it’s stable"
        )
        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        self._assert_import_annotation_possible()
        mode = ImportAnnotationMode.validate(mode)

        logger.info(f"Parsing file {file_path}..")
        coco_file = coco_importer.parse_coco_video_file(file_path)
        return self._import_coco_file(
            coco_file,
            mode,
            force_create_label,
            fail_on_asset_not_found,
            status,
            use_id,
        )

    def _import_coco_file(
        self,
        cocofile: COCOFile | VideoCOCOFile,
        mode: ImportAnnotationMode | str = ImportAnnotationMode.REPLACE,
        force_create_label: bool = True,
        fail_on_asset_not_found: bool = True,
        status: AnnotationStatus | None = None,
        use_id: bool = False,
    ) -> dict[str, int]:
        import_video = isinstance(cocofile, VideoCOCOFile)

        logger.info("Reading categories as labels..")
        labels: dict[int, Label] = self._find_labels_from_coco_categories(
            cocofile.categories, force_create_label
        )
        if self.type == InferenceType.KEYPOINT:
            self._ensures_skeleton_set(labels, cocofile.categories)

        if import_video:
            coco_assets = cocofile.videos
        else:
            coco_assets = cocofile.images

        logger.info("Reading images as assets...")
        assets: dict[int, tuple[str, dict | None]] = (
            self._read_images_and_retrieve_assets_and_attributes(
                coco_assets, fail_on_asset_not_found, use_id
            )
        )

        logger.info("Reading shapes..")
        if import_video:
            annotations: list[dict] = coco_importer.read_video_annotations(
                self.type, cocofile.annotations, cocofile.images, labels, assets
            )
        else:
            annotations: list[dict] = coco_importer.read_annotations(
                self.type, cocofile.annotations, labels, assets
            )

        logger.info("Creating annotations..")
        results = mlt.do_chunk_called_function(
            annotations, partial(self._bulk_create_annotations, mode, status)
        )
        return flatten_dict(results, lambda value: value >= 0)

    def _find_labels_from_coco_categories(
        self, categories: list[Category], force_create_label: bool
    ) -> dict[int, Label]:
        """This will convert a list of coco Category into a label mapping of id to Label
        If force_create_label is true, this will create automatically (Label) and (LabelGroup) objects.
        (LabelGroup) objects will be created
        """
        category_ids: dict[str, int] = {}
        supercategories: dict[str, str] = {}
        for category in categories:
            category_ids[category.name] = category.id
            if category.supercategory:
                supercategories[category.name] = category.supercategory

        category_names = list(category_ids.keys())
        if force_create_label:
            labels = self._create_labels_from_categories(
                category_names, supercategories
            )
        else:
            labels = self.list_labels()

        label_map: dict[int, Label] = {}
        for label in labels:
            if label.name in category_ids:
                label_map[category_ids[label.name]] = label

        self._assert_labels_created(
            category_names, [label.name for label in label_map.values()]
        )
        return label_map

    def _create_labels_from_categories(
        self, category_names: list[str], supercategories: dict[str, str]
    ) -> list[Label]:
        labels = {
            label.name: label
            for label in self._bulk_get_or_create_labels(category_names)
        }
        groups = {
            group.name: group
            for group in self._bulk_get_or_create_dotted_label_groups(
                list(supercategories.values())
            )
        }
        for category_name, parent_name in supercategories.items():
            # parent_name looks like a.b.c and we only want c here, labelmap have already been created
            parent = parent_name.rstrip(".").split(".")[-1]
            if category_name not in labels or parent not in groups:
                continue
            labels[category_name].set_group(groups[parent])

        return list(labels.values())

    @exception_handler
    @beartype
    def _bulk_get_or_create_labels(self, label_names: list[str]) -> list[Label]:
        payload = {"names": label_names}
        r = self.connection.xget(
            f"/api/dataset/version/{self.id}/bulk-labels",
            data=orjson.dumps(payload),
        ).json()
        return [Label(self.connection, item, dataset_version_id=self._id) for item in r]

    @exception_handler
    @beartype
    def _bulk_get_or_create_dotted_label_groups(
        self, group_names: list[str]
    ) -> list[LabelGroup]:
        """
        Convert a list of group names like ["a.b.c", "d"] into (LabelGroup) with hierarchical links.
        Some weird cases are skipped : "a.b.a", ".b", "a..b"
        """
        groups = set()
        parents = {}
        for group in group_names:
            split = [c for c in group.split(".") if c]
            if len(set(split)) != len(split):
                logger.error(
                    f"{group} cannot exist, some leaf are looping. We will skip this one"
                )
                continue
            if len(split) == 0:
                continue
            if len(split) == 1:
                groups.add(split[0])
                continue

            groups.add(split[0])
            for k in range(1, len(split)):
                groups.add(split[k])
                parent = split[k - 1]
                if split[k] in parents and parents[split[k]] != parent:
                    logger.error(
                        f"Supercategories are misconfigured, {group} cannot exist because "
                        f"another group defines {parents[split[k]]} as parent of {split[k]}. "
                        f"We will keep this one."
                    )
                    continue
                parents[split[k]] = parent

        existing_groups = {group.name: group for group in self.list_label_groups()}
        new_groups = set(groups) - (existing_groups.keys())
        for group in new_groups:
            existing_groups[group] = self.create_label_group(group)

        for group, parent in parents.items():
            if group not in existing_groups or parent not in existing_groups:
                continue
            existing_groups[group].set_parent(existing_groups[parent])

        return list(existing_groups.values())

    def _ensures_skeleton_set(
        self, labels: dict[int, Label], categories: list[Category]
    ) -> None:
        skeletons = self.get_skeletons()
        for category in categories:
            if isinstance(category.keypoints, str):
                vertices = [category.keypoints]
                edges = []
            elif isinstance(category.keypoints, list):
                vertices = category.keypoints
                edges = category.skeleton
                if category.skeleton is None:
                    raise ValueError(
                        "Dataset KEYPOINT needs coco file with keypoints categories filled with `skeletons` key"
                    )
            else:
                raise ValueError(
                    "Dataset KEYPOINT needs coco file with keypoints categories filled with `keypoints` key"
                )

            label = labels[category.id]
            try:
                skeleton = skeletons[str(label.id)]
            except KeyError:
                skeleton = None

            if (
                skeleton is None
                or skeleton["edges"] != edges
                or skeleton["vertices"] != vertices
            ):
                label.set_skeleton(vertices=vertices, edges=edges)

    @exception_handler
    @beartype
    def _read_images_and_retrieve_assets_and_attributes(
        self,
        coco_assets: list[COCOImage] | list[COCOVideo],
        fail_on_asset_not_found: bool,
        use_id: bool,
    ) -> dict[int, tuple[str, dict | None]]:
        filenames = {}
        attributes = {}
        for coco_asset in coco_assets:
            filenames[coco_asset.file_name] = coco_asset.id
            attributes[coco_asset.file_name] = (
                coco_asset.attributes if isinstance(coco_asset, COCOImage) else None
            )
        if use_id:
            # asset ids are in filename keys of coco file, as <id>.<extension>
            asset_ids = [filename.split(".")[0] for filename in filenames.keys()]
            multi_assets = self.list_assets(ids=asset_ids)
        else:
            multi_assets = self.list_assets(filenames=list(filenames.keys()))

        if fail_on_asset_not_found and len(multi_assets) != len(filenames):
            raise ResourceNotFoundError(
                "Some filenames were not found in this dataset version."
            )

        assets = {}
        for asset in multi_assets:
            if use_id:
                key = asset.id_with_extension
            else:
                key = asset.filename
            image_id = filenames[key]
            asset_attributes = attributes.get(key, None)
            assets[image_id] = (str(asset.id), asset_attributes)
        return assets

    @exception_handler
    @beartype
    def _bulk_create_annotations(
        self,
        import_type: ImportAnnotationMode,
        status: AnnotationStatus | None,
        annotations: list[dict],
    ):
        def send_bulk_annotation(payload: dict) -> dict:
            return self.connection.post(
                f"/api/dataset/version/{self.id}/bulk-annotations",
                data=orjson.dumps(payload),
            ).json()

        payload: dict[str, Any] = {
            "import_type": import_type,
            "annotations": annotations,
        }
        if status:
            payload["status"] = status

        try:
            return send_bulk_annotation(payload)
        except RequestTooLargeError:
            logger.info("There is a lot of data, sending one by one..")
            result = Counter({})
            for annotation in annotations:
                payload = {"import_type": import_type, "annotations": [annotation]}
                result += Counter(send_bulk_annotation(payload))
            return result

    @exception_handler
    @beartype
    def delete_all_annotations(self, workers: list[Worker] | None = None) -> None:
        """Delete all annotations of this dataset version.

        This method cannot be called on dataset with a campaign.

        Workers parameter is deprecated and cannot be used anymore. It will be removed in 6.27
        If given, this method will raise, to prevent unexpected behaviour

        :warning: **DANGER ZONE**: Be very careful here!

        It will remove all annotation of every asset of this dataset version.

        Examples:
            ```python
            foo_dataset_version.delete_all_annotations()
            ```
        """
        payload = {"asset_ids": ["__all__"]}

        if workers:
            logger.warning("workers is deprecated and should not be used anymore.")
            raise NotImplementedError()

        self.connection.delete(
            f"/api/dataset/version/{self.id}/annotations",
            data=orjson.dumps(payload),
        )
        logger.info(f"All annotations in {self} were removed.")

    @exception_handler
    @beartype
    def synchronize(
        self, target_dir: str, do_download: bool = False
    ) -> MultiAsset | None:
        """Synchronize this dataset version with target dir by comparing assets in target dir with assets uploaded in dataset version.

        Examples:
            ```python
            foo_dataset.synchronize('./foo_dataset/first')
            ```
        Arguments:
            target_dir (str): directory to synchronize against
            do_download (bool): do download files when they are not in local directory

        Returns:
            A MultiAsset object with assets downloaded if do_download is True
        """
        assert os.path.isdir(target_dir), "Please select a valid directory path"
        logger.info("⌛️ Scanning Dataset Assets..")
        assets: MultiAsset = self.list_assets()
        filenames = {asset.filename for asset in assets.items}
        logger.info("🔍 Scanning Local Dataset Folder ..")
        local_filenames = {
            local_filename
            for local_filename in os.listdir(target_dir)
            if os.path.isfile(os.path.join(target_dir, local_filename))
        }

        not_uploaded = local_filenames - filenames
        if len(not_uploaded) > 0:
            logger.info(
                f"📚 {len(not_uploaded)} assets not uploaded. You need to add data to the datalake first with :"
            )
            filepaths = [
                os.path.join(target_dir, filename) for filename in not_uploaded
            ]
            logger.info(f"filepaths = {filepaths}")
            logger.info("list_data = client.get_datalake().upload_data(filepaths)")
            logger.info(
                f'client.get_dataset_by_id({self.origin_id}).get_version("{self.version}").add_data(list_data)'
            )

        not_downloaded = filenames - local_filenames
        if len(not_downloaded) > 0:
            assets_to_download = list(
                filter(
                    lambda asset: asset.filename in not_downloaded,
                    assets.items,
                )
            )
            multi_assets = MultiAsset(self.connection, self.id, assets_to_download)
            logger.info(f"📚 {len(not_downloaded)} assets not downloaded")
            if do_download:
                logger.info(f"📚 Downloading {len(not_downloaded)} assets")
                multi_assets.download(target_dir)
            else:
                logger.info(
                    "📚 Call this method again with do_download=True if you want to download these assets"
                )
            return multi_assets
        else:
            logger.info("✅ Dataset is up-to-date.")
            return None

    @exception_handler
    @beartype
    def retrieve_stats(self) -> DatasetVersionStats:
        """Retrieve statistics of this dataset version (label repartition, number of objects, number of annotations).

        Examples:
            ```python
            stats = foo_dataset_version.retrieve_stats()
            assert stats.label_repartition == {"cat": 23, "dog": 2}
            assert stats.nb_objects == 25
            assert stats.nb_annotations == 5
            ```

        Returns:
            A DatasetVersionStats schema with keys:
                - label_repartition: dict with label names as keys and number of shape with these labels as value
                - nb_objects: total number of objects (sum of label_repartition values)
                - nb_annotations: total number of (Annotation) objects of this dataset version
        """
        r = self.connection.get(f"/api/dataset/version/{self.id}/stats").json()
        return DatasetVersionStats(**r)

    @exception_handler
    @beartype
    def get_or_create_asset_tag(self, name: str) -> Tag:
        """Retrieve an asset tag used in this dataset version by its name.
        If tag does not exist, create it and return it.

        Examples:
            ```python
            tag = dataset_version.get_or_create_asset_tag("new_tag")
            ```
        Arguments:
            name (str): Name of the tag to retrieve or create

        Returns:
            A (Tag) object
        """
        try:
            return self.get_asset_tag(name)
        except exceptions.ResourceNotFoundError:
            return self.create_asset_tag(name)

    @exception_handler
    @beartype
    def create_asset_tag(self, name: str) -> Tag:
        """Create asset tag only available in this dataset version.

        Examples:
            ```python
            tag_dog = dataset_v0.create_asset_tag("dog")
            ```
        Arguments:
            name (str): name of tag to create

        Returns:
            A (Tag) object
        """
        payload = {"name": name}
        r = self.connection.post(
            f"/api/dataset/version/{self.id}/tags", data=orjson.dumps(payload)
        ).json()
        return Tag(self.connection, r)

    @exception_handler
    @beartype
    def get_asset_tag(self, name: str) -> Tag:
        """Retrieve an asset tag used in this dataset version.

        Examples:
            ```python
            tag_dog = dataset_v0.get_asset_tag("dog")
            ```
        Arguments:
            name (str): Name of the tag you're looking for

        Returns:
            A (Tag) object
        """
        params = {"name": name}
        r = self.connection.get(
            f"/api/dataset/version/{self.id}/tags/find", params=params
        ).json()
        return Tag(self.connection, r)

    @exception_handler
    @beartype
    def convert_tags_to_classification(
        self, tag_type: TagTarget, tags: list[Tag]
    ) -> Job:
        """This method will convert ASSET or DATA given tags to Classification objects.

        This can only works with a Classification dataset.
        It will create labels from tag names.
        It will not create annotations on assets that are synced in a campaign.

        Arguments:
            tag_type (TagTarget): Data or Asset.
            tags (list[Tag]): list of tags to use to create classifications.

        Returns:
            A (Job) object
        """
        assert self.type == InferenceType.CLASSIFICATION, (
            "You cannot convert tags on this dataset."
        )
        assert tag_type == TagTarget.ASSET or tag_type == TagTarget.DATA, (
            "You can only convert asset tags or data tags"
        )

        tag_ids = []
        for tag in tags:
            if tag.target_type != tag_type:
                raise TypeError(f"{tag} is not a {tag_type} type of tag.")

            tag_ids.append(tag.id)

        payload = {"tag_ids": tag_ids, "tag_type": tag_type}

        r = self.connection.post(
            f"/api/dataset/version/{self.id}/tags/convert", data=orjson.dumps(payload)
        ).json()
        logger.info(
            f"Tags (of type {tag_type}) are being converted into classifications."
            "This operation can take some time, please wait for returned job to end."
        )
        return Job(self.connection, r, version=1)

    @exception_handler
    @beartype
    def list_asset_tags(self) -> list[Tag]:
        """List asset tags created in this dataset version

        Examples:
            ```python
            tags = dataset_v0.list_asset_tags()
            assert tag_dog in tags
            ```

        Returns:
            A list of (Tag)
        """
        r = self.connection.get(f"/api/dataset/version/{self.id}/tags").json()
        return [Tag(self.connection, item) for item in r["items"]]

    @beartype
    def train_test_split(
        self,
        prop: float = 0.8,
        random_seed: Any | None = None,
        load_asset_page_size: int = 100,
    ) -> tuple[MultiAsset, MultiAsset, dict[str, list], dict[str, list], list[Label]]:
        """Split a DatasetVersion into 2 MultiAssets and return their label repartition.

        Examples:
            ```python
            train_assets, eval_assets, count_train, count_eval, labels = dataset_version.train_test_split()
            ```
        Arguments:
            prop (float, optional): Percentage of data for training set. Defaults to 0.8.
            random_seed (Any, optional): Use a seed to ensures same result if run multiple times. Defaults to None.
            load_asset_page_size (int, optional): Page size when loading assets. Defaults to 100.

        Returns:
            A tuple with all of this information (
                list of train assets,
                list of test assets,
                dict of repartition of classes for train assets, with {"x": list of labels, "y":  list of label count},
                dict of repartition of classes for test assets, with {"x": list of labels, "y":  list of label count},
                list of labels
            )
        """
        if prop > 1 or prop < 0:
            raise ValueError("Please give a 'prop' parameter between 0 and 1")

        multi_assets, label_distributions, labels = self.split_into_multi_assets(
            [prop, 1.0 - prop], random_seed, load_asset_page_size
        )
        distributions = [
            {
                "x": list(label_repartition.keys()),
                "y": list(label_repartition.values()),
            }
            for label_repartition in label_distributions
        ]

        return (
            multi_assets[0],
            multi_assets[1],
            distributions[0],
            distributions[1],
            labels,
        )

    @beartype
    def train_test_val_split(
        self,
        ratios: list[float] = None,
        random_seed: Any | None = None,
        load_asset_page_size: int = 100,
    ) -> tuple[
        MultiAsset,
        MultiAsset,
        MultiAsset,
        dict[str, list],
        dict[str, list],
        dict[str, list],
        list[Label],
    ]:
        """Split a DatasetVersion into 3 MultiAssets and return their label repartition.
        By default, will split with a ratio of 0.64, 0.16 and 0.20

        Examples:
            ```python
            train_assets, test_assets, val_assets, count_train, count_test, count_val, labels = dataset_version.train_test_val_split()
            ```
        Arguments:
            ratios (list of float, optional): Ratios of split used for training and eval set.
                Defaults to [0.64, 0.16, 0.20]
            random_seed (Any, optional): Use a seed to ensures same result if run multiple times. Defaults to None.
            load_asset_page_size (int, optional): Page size when loading assets. Defaults to 100.

        Returns:
            A tuple with all of this information (
                list of train assets,
                list of test assets
                list of val assets,
                dict of repartition of classes for train assets, with {"x": list of labels, "y":  list of label count},
                dict of repartition of classes for test assets, with {"x": list of labels, "y":  list of label count},
                dict of repartition of classes for val assets, with {"x": list of labels, "y":  list of label count},
                list of labels
            )
        """
        if not ratios:
            ratios = [0.64, 0.16, 0.20]

        if len(ratios) != 3:
            raise ValueError("Ratios list should be a list of 3 elements")

        multi_assets, label_distributions, labels = self.split_into_multi_assets(
            ratios, random_seed, load_asset_page_size
        )
        distributions = [
            {
                "x": list(label_repartition.keys()),
                "y": list(label_repartition.values()),
            }
            for label_repartition in label_distributions
        ]

        return (
            multi_assets[0],
            multi_assets[1],
            multi_assets[2],
            distributions[0],
            distributions[1],
            distributions[2],
            labels,
        )

    @beartype
    def split_into_multi_assets(
        self,
        ratios: list[float | int],
        random_seed: Any | None = None,
        load_asset_page_size: int = 100,
    ) -> tuple[list[MultiAsset], list[dict[str, int]], list[Label]]:
        """Split dataset into multiple MultiAsset, proportionally according to given ratios.

        Examples:
            ```python
            split_assets, counts, labels = dataset.split_into_multi_assets([0.2, 0.5, 0.3])
            train_assets = split_assets[0]
            test_assets = split_assets[1]
            val_assets = split_assets[2]
            ```
        Arguments:
            ratios (list of float): Percentage of data that will go into each category.
                Will be normalized but sum should be equals to one if you don't want to be confused.
            random_seed (Any, optional): Use a seed to ensures same result if run multiple times. Defaults to None.
            load_asset_page_size (int, optional): Page size when loading assets. Defaults to 100.

        Returns:
            A tuple with all of this information (
                list of MultiAsset,
                dict of repartition of classes for each MultiAsset,
                list of labels
            )
        """
        if not ratios or len(ratios) < 2:
            raise NoDataError("Please give at least two proportions")

        # Fetch assets and annotation
        fetched_raw_assets = self._do_list_items_with_annotations(load_asset_page_size)

        # Fetch labels
        labels = self.list_labels()
        label_names = {str(label.id): label.name for label in labels}

        # Split annotations according to ratios
        ratios = AssetSplitter.normalize_ratios(ratios)
        AssetSplitter.shuffle_items(fetched_raw_assets, random_seed)
        split_items = AssetSplitter.split_with_ratios(fetched_raw_assets, ratios)

        multi_assets: list[MultiAsset] = []
        distributions: list[dict[str, int]] = []
        for raw_items in split_items:
            assets, label_distribution = AssetSplitter.convert_items_to_assets(
                self.connection, self.id, raw_items, label_names
            )
            multi_assets.append(MultiAsset(self.connection, self.id, assets))
            distributions.append(label_distribution)

        return (
            multi_assets,
            distributions,
            labels,
        )

    @exception_handler
    @beartype
    def _do_list_items_with_annotations(self, load_asset_page_size: int):
        # Retrieve assets
        extended_assets = mlt.do_paginate(
            None, None, load_asset_page_size, self._do_list_assets_extended
        )
        if not extended_assets:
            raise NoDataError("No asset with annotation found in this dataset")

        # Retrieve annotations
        items = []
        for item in extended_assets:
            if not item["annotations"]:
                logger.debug(f"No annotation for asset {item['data']['filename']}")
                continue

            items.append(item)

        return items

    @exception_handler
    @beartype
    def _do_list_assets_extended(
        self, limit: int, offset: int
    ) -> tuple[list[dict], int]:
        params = {"limit": limit, "offset": offset}
        r = self.connection.get(
            f"/api/dataset/version/{self.id}/assets/extended", params=params
        ).json()
        return r["items"], r["count"]

    @exception_handler
    @beartype
    def create_campaign(
        self,
        name: str | None = None,
        description: str | None = None,
        instructions_file_path: str | None = None,
        instructions_text: str | None = None,
        end_date: date | None = None,
        auto_add_new_assets: bool | None = False,
        auto_close_on_completion: bool | None = False,
    ) -> AnnotationCampaign:
        """Create campaign on a dataset version.

        Examples:
            ```python
            foo_dataset_version.create_campaign()
            ```
        Arguments:
            name (str, optional): deprecated, it should not be used anymore. Defaults to None.
            description (str, optional): Description of the campaign. Defaults to None.
            instructions_file_path (str, optional): Instructions file path. Defaults to None.
            instructions_text (str, optional): Instructions text. Defaults to None.
            end_date (date, optional): End date of the campaign. Defaults to None.
            auto_add_new_assets (bool, optional): If true, new assets of this dataset will be added as a task
                                                    in the campaign. Defaults to False.
            auto_close_on_completion (bool, optional): If true, campaign will be close when all tasks will be done.
                                                        Defaults to False.

        Returns:
            An (AnnotationCampaign) object
        """
        if name is not None:
            logging.warning(
                "'name' parameter is deprecated and will be removed in future versions. "
                "You cannot set a name to a Campaign anymore."
            )

        payload = {
            "description": description,
            "instructions_text": instructions_text,
            "end_date": end_date,
            "auto_add_new_assets": auto_add_new_assets,
            "auto_close_on_completion": auto_close_on_completion,
        }

        if instructions_file_path:
            instructions_file_name = os.path.basename(instructions_file_path)
            object_name = self.connection.generate_dataset_version_object_name(
                instructions_file_name,
                ObjectDataType.CAMPAIGN_FILE,
                dataset_version_id=self.id,
            )
            self.connection.upload_file(object_name, instructions_file_path)
            payload["instructions_object_name"] = object_name

        r = self.connection.post(
            f"/api/dataset/version/{self.id}/campaigns",
            data=orjson.dumps(payload),
        ).json()
        campaign = AnnotationCampaign(self.connection, r)
        self._annotation_campaign_id = campaign.id
        logger.info(f"{campaign} has been created to {self}")
        return campaign

    @exception_handler
    @beartype
    def get_campaign(self) -> AnnotationCampaign:
        """Get campaign of a dataset version.

        Examples:
            ```python
            foo_dataset_version.get_campaign()
            ```
        Returns:
            An (AnnotationCampaign) object
        """
        if not self._annotation_campaign_id:
            self.sync()

        if not self._annotation_campaign_id:
            raise NoDataError(
                "There is no annotation campaign defined in this dataset version"
            )

        try:
            r = self.connection.get(
                f"/api/campaigns/annotation/{self._annotation_campaign_id}"
            ).json()
        except (ForbiddenError, ResourceNotFoundError):
            self._annotation_campaign_id = None
            raise

        return AnnotationCampaign(self.connection, r)

    @exception_handler
    @beartype
    def launch_processing(
        self,
        processing: Processing,
        parameters: dict = None,
        cpu: int = None,
        gpu: int = None,
        model_version_id: UUID = None,
        target_version_name: str = None,
        assets: list[Asset] | MultiAsset | None = None,
        inputs: dict | None = None,
    ) -> Job:
        """Launch given processing onto this dataset version. You can give specific cpu, gpu or parameters.

        You must set the "inputs" dict so it matches the inputs configuration defined in the platform.
        It will fail if inputs are not matching expected inputs.

        If not given, it will use default values specified in Processing.
        If processing cannot be launched on this DatasetVersion it will raise before launching.

        Examples:
            ```python
            processing = client.get_processing("pre-annotation")
            assets = dataset_version.list_assets(limit=10)
            foo_dataset_version.launch_processing(processing, assets=assets , inputs={"model_version_id": "018c59e4-776e-7fd0-a428-d24d4aec631e", "target_version_name": "new-version"})
            ```

        Returns:
            A (Job) object
        """
        inputs = inputs or {}
        if model_version_id:
            logging.warning(
                "'model_version_id' parameter is deprecated and will be removed in future versions. "
                "If you want to give a model_version_id, you should add it inside inputs directly"
            )
            if "model_version_id" not in inputs:
                inputs["model_version_id"] = model_version_id

        if target_version_name:
            logging.warning(
                "'target_version_name' parameter is deprecated and will be removed in future versions. "
                "If you want to give a target_version_name, you should add it inside inputs directly"
            )
            if "target_version_name" not in inputs:
                inputs["target_version_name"] = target_version_name

        asset_ids = list({asset.id for asset in assets}) if assets else None
        payload = {
            "processing_id": processing.id,
            "parameters": parameters,
            "asset_ids": asset_ids,
            "cpu": cpu,
            "gpu": gpu,
            "model_version_id": model_version_id,
            "target_version_name": target_version_name,
            "inputs": inputs,
        }
        r = self.connection.post(
            f"/api/dataset/version/{self.id}/processing/launch",
            data=orjson.dumps(payload),
        ).json()
        return Job(self.connection, r, version=2)

    @exception_handler
    @beartype
    def activate_visual_search(self, wait: bool = True) -> Job:
        """This method will activate the embedding computation and visual search feature on this (DatasetVersion)"""
        r = self.connection.post(f"/api/visual-search/dataset-version/{self.id}").json()
        job = Job(self.connection, {"id": r["job_id"], "status": "RUNNING"}, version=2)
        if wait:
            logger.info("Waiting for visual search activation...")
            job.wait_for_done()
            logger.info(f"Visual search is now possible for {self}")
        else:
            logger.info("Visual search will be available in a few moment")
        return job

    @exception_handler
    @beartype
    def deactivate_visual_search(self) -> None:
        """This method will disable the visual search feature for this (DatasetVersion)"""
        self.connection.delete(f"/api/visual-search/dataset-version/{self.id}")
        logger.info(f"Visual search is now deactivated for {self}")

    @exception_handler
    @beartype
    def embeddings_computation_status(self):
        """Return the status of the Visual Search for this (DatasetVersion)

        Returns:
            a dict with status
        """
        return self.connection.get(
            f"/api/visual-search/dataset-version/{self.id}/status"
        ).json()

    @exception_handler
    @beartype
    def similar_search(self, asset: Asset, limit: int) -> MultiAsset:
        """
        Will return a (MultiAsset) object with asset that are similar to given (Asset), ordered by score.
        This is computed with Visual Search feature.
        Each asset will have a temporary attribute _score, if you want to access the similarity score.

        Returns:
            a MultiData object
        """
        return DatasetVersionVisualSearchService(
            self.connection, self.id
        ).query_visual_search(str(asset.id), limit)

    @exception_handler
    @beartype
    def text_search(self, query: str, limit: int) -> MultiAsset:
        """
        Will return a (MultiAsset) object with data that match your query, ordered by score.
        This is computed with Visual Search feature.
        Each data will have a temporary attribute _score, if you want to access the similarity score.

        Returns:
            a MultiAsset object
        """
        return DatasetVersionVisualSearchService(
            self.connection, self.id
        ).query_visual_search(query, limit)

    @exception_handler
    @beartype
    def count_embeddings(self) -> int:
        """Return the number of asset indexed by the Visual Search in this (DatasetVersion)

        Returns:
            number of asset indexed
        """
        r = self.connection.get(
            f"/api/visual-search/dataset-version/{self.id}/points/count"
        ).json()
        return r["count"]

    @exception_handler
    @beartype
    def list_embeddings(self, limit: int) -> list[dict]:
        """Return the list of embeddings computed for this (DatasetVersion)

        Returns:
            a list of dict with data of indexation
            each dictionary contains:
                - id (str): UUID of the (Data)
                - vector (dict): Model-specific vector embeddings where:
                    - key (str): Embedder identifier
                    - value (list): Vector embedding as list of floats
        """
        return DatasetVersionVisualSearchService(
            self.connection, self.id
        ).list_embeddings(limit, with_vector=True, with_payload=False, has_error=False)

    @exception_handler
    @beartype
    def compute_shapes_embeddings(self, wait: bool = True) -> Job:
        """This method will activate the embedding computation and visual search feature on this (DatasetVersion)"""
        r = self.connection.post(
            f"/api/dataset/version/{self.id}/embeddings/shapes"
        ).json()
        job = Job(self.connection, {"id": r["job_id"], "status": "RUNNING"}, version=2)
        if wait:
            logger.info(f"Shapes are being synced on visual search for {self}")
            job.wait_for_done(blocking_time_increment=5.0, attempts=100)
            logger.info(f"Shape embeddings have been computed {self}")
        else:
            logger.info("Shape embeddings will be available in a few moment")
        return job

    @exception_handler
    @beartype
    def delete_shape_embeddings(self) -> None:
        """This method will activate the embedding computation and visual search feature on this (DatasetVersion)"""
        self.connection.delete(f"/api/dataset/version/{self.id}/embeddings/shapes")
        logger.info(f"Shapes are being synced on visual search for {self}")

    @exception_handler
    @beartype
    def list_rectangles_embeddings(self, limit: int) -> list[dict]:
        """Returns the list of embeddings available for each (Rectangle) in this (DatasetVersion)

        Returns:
            a list of dict with indexed embeddings data
            each dictionary contains:
                - id (str): UUID of the (Rectangle)
                - vector (dict): Model-specific vector embeddings where:
                    - key (str): Embedder identifier
                    - value (list): Vector embedding as list of floats
                - payload (dict) with key label_id

        """
        return RectangleVisualSearchService(self.connection, self.id).list_embeddings(
            limit, with_vector=True, with_payload=True, has_error=False
        )

    @exception_handler
    @beartype
    def list_polygons_embeddings(self, limit: int) -> list[dict]:
        """Returns the list of embeddings available for each (Polygon) in this (DatasetVersion)

        Returns:
            a list of dict with indexed embeddings data
            each dictionary contains:
                - id (str): UUID of the (Polygon)
                - vector (dict): Model-specific vector embeddings where:
                    - key (str): Embedder identifier
                    - value (list): Vector embedding as list of floats
                - payload (dict) with key label_id

        """
        return PolygonVisualSearchService(self.connection, self.id).list_embeddings(
            limit, with_vector=True, with_payload=True, has_error=False
        )

    @exception_handler
    @beartype
    def get_shapes_embeddings_status(self):
        """Return the status of the Visual Search for this (DatasetVersion)

        Returns:
            a dict with status
        """
        return self.connection.get(
            f"/api/dataset/version/{self.id}/embeddings/shapes/status"
        ).json()

    @exception_handler
    @beartype
    def start_fast_training(self, description: str | None = None) -> FastTraining:
        """
        This method will start a fast training with this dataset as input data.

        Returns:
            a (FastTraining) object
        """
        logger.warning(
            "Experimental feature: the availability and support of this feature can change until it’s stable"
        )
        payload = {"description": description}
        r = self.connection.post(
            f"/api/dataset/version/{self.id}/fast-training", data=orjson.dumps(payload)
        ).json()
        return FastTraining(self.connection, self.id, r)

    @exception_handler
    @beartype
    def list_fast_trainings(self) -> list[FastTraining]:
        """
        This method will return all fast trainings running

        Returns:
            a list of (FastTraining) object
        """
        r = self.connection.get(f"/api/dataset/version/{self.id}/fast-training").json()
        return [FastTraining(self.connection, self.id, item) for item in r["trainings"]]

    @exception_handler
    @beartype
    def get_asset_tag_analytics(self) -> dict[str, Any]:
        """This method returns a repartition of tag used in your dataset"""
        return self.connection.get(
            f"/api/dataset/version/{self.id}/analytics/tags",
            params={"tag_type": "ASSET"},
        ).json()

    @exception_handler
    @beartype
    def get_data_tag_analytics(self) -> dict[str, Any]:
        """This method returns a repartition of tag used in your dataset"""
        return self.connection.get(
            f"/api/dataset/version/{self.id}/analytics/tags",
            params={"tag_type": "DATA"},
        ).json()

    @exception_handler
    @beartype
    def lock(self) -> None:
        """
        Lock the resource, you won't be able to do anything that create, update or delete something on this (DatasetVersion)

        :warning: **DANGER ZONE**: Be very careful here!
        """
        self.connection.post(f"/api/dataset/version/{self.id}/lock").json()
        logging.info(f"{self} is now locked")

    @exception_handler
    @beartype
    def unlock(self) -> None:
        """
        Unlock the resource, you will be able to create, update or delete something linked to this (DatasetVersion)

        :warning: **DANGER ZONE**: Be very careful here!
        """
        self.connection.post(f"/api/dataset/version/{self.id}/unlock").json()
        logging.info(f"{self} is now locked")

    @exception_handler
    @beartype
    def get_skeletons(self) -> dict[str, dict]:
        """Get all skeletons of labels of this (DatasetVersion)

        Returns:
            a dict matching label with a dict with key edges and vertices
        """
        return self.connection.get(
            f"/api/dataset/version/{self.id}/labels/skeleton"
        ).json()["items"]

    @exception_handler
    @beartype
    def get_attributes(self) -> dict | None:
        """Get attributes configuration of this (DatasetVersion).
        Returns:
            a dict with attributes
        """
        return self.connection.get(f"/api/dataset/version/{self.id}/attributes").json()[
            "attributes"
        ]

    @exception_handler
    @beartype
    def set_attributes(self, attributes: dict | None):
        """Set attributes configuration of this (DatasetVersion).

        The `attributes` parameter is a dict mapping attribute names (str) to their
        configuration. Each attribute configuration is a dict with the following fields:

        - `display_name` (str | None): Optional display name (1-256 chars).
        - `required` (bool): Whether the attribute is required.
        - `input_type` (str): One of "STRING", "INTEGER", "FLOAT", "BOOLEAN".
        - `archived` (bool): Whether the attribute is archived (default False). An archived attribute cannot be required.
        - `choices` (list | None): Optional list of allowed values (not available for BOOLEAN).
            When defined, must have 1-64 items (2-64 for STRING). Cannot be combined with min/max.
        - `allow_multiple` (bool | None): Whether multiple choices can be selected (requires `choices`).
        - `min` (int | float | None): Optional minimum value (INTEGER, FLOAT only). Must be less than `max`.
        - `max` (int | float | None): Optional maximum value (INTEGER, FLOAT only). Must be greater than `min`.

        Example:
            ```python
            dataset_version.set_attributes({
                "color": {
                    "display_name": "Color",
                    "required": True,
                    "input_type": "STRING",
                    "choices": ["red", "green", "blue"],
                    "allow_multiple": True,
                },
                "score": {
                    "display_name": "Score",
                    "required": False,
                    "input_type": "FLOAT",
                    "min": 0.0,
                    "max": 1.0,
                },
                "count": {
                    "display_name": "Count",
                    "required": False,
                    "input_type": "INTEGER",
                    "choices": [1, 2, 3, 4, 5],
                    "allow_multiple": False,
                },
                "is_valid": {
                    "display_name": "Is Valid",
                    "required": True,
                    "input_type": "BOOLEAN",
                },
            })
            ```

        Args:
            attributes: A dict mapping attribute names to their configuration, or None to clear all attributes.
        """
        payload = {"attributes": attributes}
        self.connection.post(
            f"/api/dataset/version/{self.id}/attributes", data=orjson.dumps(payload)
        )
        logger.info(f"{self}' attributes updated")
