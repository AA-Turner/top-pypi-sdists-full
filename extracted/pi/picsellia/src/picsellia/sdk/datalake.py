import logging
import os
from pathlib import Path
from uuid import UUID

import orjson
from beartype import beartype
from deprecation import deprecated

import picsellia.pxl_multithreading as mlt
from picsellia import exceptions
from picsellia.colors import Colors
from picsellia.compatibility import add_data_mandatory_query_parameters
from picsellia.decorators import exception_handler
from picsellia.exceptions import (
    BadRequestError,
    NoConnectorFound,
    NoDataError,
    NothingDoneError,
    UnprocessableData,
)
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.data import Data, MultiData
from picsellia.sdk.data_projection import DataProjection
from picsellia.sdk.datasource import DataSource
from picsellia.sdk.job import Job
from picsellia.sdk.processing import Processing
from picsellia.sdk.tag import Tag
from picsellia.services.data_uploader import DataUploader
from picsellia.services.datasource import DataSourceService
from picsellia.services.error_manager import ErrorManager
from picsellia.services.lister.data_lister import DataFilter, DataLister
from picsellia.services.visual_search import DatalakeVisualSearchService
from picsellia.types.enums import DataUploadStatus, ObjectDataType, TagTarget
from picsellia.types.schemas import CloudObject, CloudProjectionObject, DatalakeSchema
from picsellia.utils import (
    combine_two_ql,
    convert_tag_list_to_query_language,
    filter_payload,
)

logger = logging.getLogger("picsellia")


class Datalake(Dao):
    def __init__(self, connexion: Connection, organization_id: UUID, data: dict):
        Dao.__init__(self, connexion, data)
        self._organization_id = organization_id

    def __str__(self):
        return f"{Colors.GREEN}Datalake '{self.name}'{Colors.ENDC} (id: {self.id})"

    @property
    def name(self) -> str:
        """Name of this (Datalake)"""
        return self._name

    @property
    def connector_id(self) -> UUID:
        """Connector id used by this (Datalake)"""
        if self._connector_id is None:
            raise NoConnectorFound(
                "This datalake has no connector. You cannot retrieve and upload data into this datalake."
            )
        return self._connector_id

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        schema = DatalakeSchema(**data)
        self._name = schema.name
        if schema.connector_id is not None:
            self._connector_id = schema.connector_id
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/datalake/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
            print(foo_dataset.get_resource_url_on_platform())
            >>> "https://app.picsellia.com/datalake/62cffb84-b92c-450c-bc37-8c4dd4d0f590"
            ```

        Returns:
            Url on Platform for this resource
        """

        return f"{self.connection.host}/datalake/{self.id}"

    @exception_handler
    @beartype
    def upload_data(  # noqa: C901
        self,
        filepaths: str | Path | list[str | Path],
        tags: list[str | Tag] | None = None,
        source: str | DataSource | None = None,
        max_workers: int | None = None,
        error_manager: ErrorManager | None = None,
        metadata: None | dict | list[dict] = None,
        fill_metadata: bool | None = False,
        wait_for_unprocessable_data: bool | None = True,
        upload_dir: str | None = None,
        custom_metadata: None | dict | list[dict] = None,
    ) -> Data | MultiData:
        """Upload data into this datalake.

        Upload files representing data, into a datalake.
        You can give some tags as a list.
        You can give a source for your data.

        If some data fails to upload, check the example to see how
        to retrieve the list of file paths that failed.

        For more information about metadata, check https://documentation.picsellia.com/docs/metadata

        Examples:
            ```python
            from picsellia.services.error_manager import ErrorManager

            source_camera_one = client.get_datasource("camera-one")
            source_camera_two = client.get_datasource("camera-two")

            lake = client.get_datalake()

            tag_car = lake.get_data_tag("car")
            tag_huge_car = lake.get_data_tag("huge-car")

            lake.upload_data(filepaths=["porsche.png", "ferrari.png"], tags=[tag_car], source=source_camera_one)
            lake.upload_data(filepaths="truck.png", tags=[tag_huge_car], source=source_camera_two, metadata={"longitude": 43.6027273, "latitude": 1.4541129}, fill_metadata=True)

            error_manager = ErrorManager()
            lake.upload_data(filepaths=["twingo.png", "path/unknown.png", error_manager=error_manager)

            # This call will return a list of UploadError to see what was wrong
            error_paths = [error.path for error in error_manager.errors]
            ```
        Arguments:
            filepaths (str or Path or list[str or Path]): Filepaths of your data
            tags (list[Tag], optional): Data Tags that will be given to data. Defaults to [].
            source (DataSource, optional): Source of your data.
            max_workers (int, optional): Number of max workers used to upload. Defaults to os.cpu_count() + 4.
            error_manager (ErrorManager, optional): Giving an ErrorManager will allow you to retrieve errors
            metadata (Dict or list[Dict], optional): Add some metadata to given data, filepaths length must match
                 this parameter. Defaults to no metadata.
            fill_metadata (bool, optional): Whether read exif tags of image and add it into metadata field.
                 If some fields are already given in metadata fields, they will be overridden.
            wait_for_unprocessable_data (bool, optional): If true, this method will wait for all data to be fully
                uploaded and processed by our services. Defaults to true.
            upload_dir (str, optional): This parameter can only be used with private object-storages. Specify this parameter to prefix the object name of the data. Filename will still contain a generated uuid4
            custom_metadata (Dict or list[Dict], optional): Add custom metadata to given data, filepaths length must match this parameter. Defaults to no custom metadata.
        Returns:
            A (Data) object or a (MultiData) object that wraps a list of Data.
        """
        computed_tag_ids = self._get_or_create_data_tag_ids(tags)
        source = self._get_or_create_data_source(source)

        if metadata and isinstance(metadata, dict):
            metadata = [metadata]

        if custom_metadata and isinstance(custom_metadata, dict):
            custom_metadata = [custom_metadata]

        if isinstance(filepaths, str) or isinstance(filepaths, Path):
            filepaths = [filepaths]

        if metadata and len(metadata) != len(filepaths):
            raise BadRequestError(
                f"Given list of metadata has {len(metadata)} objects but list of paths has {len(filepaths)} objects."
                f"Please give the same number of objects if you want to have metadata added to your data"
            )

        if custom_metadata and len(custom_metadata) != len(filepaths):
            raise BadRequestError(
                f"Given list of custom metadata has {len(custom_metadata)} objects but list of paths has {len(filepaths)} objects."
                f"Please give the same number of objects if you want to have custom metadata added to your data"
            )

        uploader = DataUploader(
            self.connection,
            self.id,
            self.connector_id,
            computed_tag_ids=computed_tag_ids,
            source=source,
            fill_metadata=fill_metadata,
            upload_dir=upload_dir,
            error_manager=error_manager,
        )

        def _upload(items: tuple[str | Path, dict | None, dict | None]):
            response = uploader.upload(items)
            if not response:
                return None

            return Data(self.connection, self.id, response.json())

        logger.info("🌎 Starting upload..")

        # Create batches from filepaths and metadata
        batches = [
            (
                filepaths[k],
                metadata[k] if metadata else None,
                custom_metadata[k] if custom_metadata else None,
            )
            for k in range(len(filepaths))
        ]

        results = mlt.do_mlt_function(
            batches, _upload, h=lambda batch: batch[0], max_workers=max_workers
        )

        error_data = []
        pending_data = []
        uploaded_data = []
        for _, data in results.items():
            if data is None:
                continue

            if data.upload_status == DataUploadStatus.ERROR:
                if error_manager:
                    error_manager.append(UnprocessableData(data))
                error_data.append(data)
            else:
                uploaded_data.append(data)
                if not data.is_ready():
                    pending_data.append(data)

        if len(uploaded_data) != len(filepaths) or len(error_data) > 0:
            logger.error(
                f"❌ {len(filepaths) - len(uploaded_data) + len(error_data)} data not uploaded."
            )
            if error_manager:
                logger.error(
                    "Calling error_manager.errors will return a list of UploadError objects to see what happened"
                )

        if len(uploaded_data) == 0:
            raise NothingDoneError("Nothing has been uploaded.")
        elif len(uploaded_data) == 1:
            first = uploaded_data[0]
            if (
                first.upload_status != DataUploadStatus.DONE
                and wait_for_unprocessable_data
            ):
                logger.info(
                    f"{first.filename} data is being processed on Picsellia, please wait a few moment.."
                )
                first.wait_for_upload_done(blocking_time_increment=5.0, attempts=30)
            logger.info(f"✅ {first.filename} data uploaded in {self}")
            return first
        else:
            if wait_for_unprocessable_data and len(pending_data) > 0:
                pending_multi_data = MultiData(self.connection, self.id, pending_data)
                pending_multi_data.wait_for_upload_done(
                    blocking_time_increment=5.0, attempts=30
                )
            logger.info(f"✅ {len(uploaded_data)} data uploaded in {self}")
            return MultiData(self.connection, self.id, uploaded_data)

    @exception_handler
    @beartype
    def find_data(
        self,
        filename: str | None = None,
        object_name: str | None = None,
        id: str | UUID | None = None,
    ) -> Data:
        """Find a data into this datalake

        You can find it by giving its filename or its object name or its id

        Examples:
            ```python
            my_data = my_datalake.find_data(filename="test.png")
            ```
        Arguments:
            filename (str, optional): filename of the data. Defaults to None.
            object_name (str, optional): object name in the storage S3. Defaults to None.
            id (str or UUID, optional): id of the data. Defaults to None

        Raises:
            If no data match the query, it will raise a NotFoundError.
            In some case, it can raise an InvalidQueryError,
                it might be because platform stores 2 data matching this query (for example if filename is duplicated)

        Returns:
            The (Data) found
        """
        assert not (filename is None and object_name is None and id is None), (
            "Select at least one criteria to find a data"
        )

        params = {}
        if id is not None:
            params["id"] = id

        if filename is not None:
            params["filename"] = filename

        if object_name is not None:
            params["object_name"] = object_name

        params = add_data_mandatory_query_parameters(params)

        r = self.connection.get(
            f"/api/datalake/{self.id}/datas/find", params=params
        ).json()
        return Data(self.connection, self.id, r)

    @exception_handler
    @beartype
    def list_data(
        self,
        limit: int | None = None,
        offset: int | None = None,
        page_size: int | None = None,
        order_by: list[str] | None = None,
        tags: str | Tag | list[str | Tag] | None = None,
        filenames: list[str] | None = None,
        intersect_tags: bool | None = False,
        object_names: list[str] | None = None,
        q: str | None = None,
        ids: list[str | UUID] | None = None,
        custom_metadata: dict | None = None,
    ) -> MultiData:
        """List data of this datalake.

        If there is no data, raise a NoDataError exception.

        Returned object is a MultiData. An object that allows manipulation of a bunch of data.
        You can add tags on them or feed a dataset with them.

        Examples:
            ```python
            lake = client.get_datalake()
            data = lake.list_data()
            ```

        Arguments:
            limit (int, optional): if given, will limit the number of data returned
            offset (int, optional): if given, will return data that would have been returned
                                    after this offset in given order
            page_size (int, optional): deprecated.
            order_by (list[str], optional): if not empty, will order data by fields given in this parameter
            filenames (list[str], optional): if given, will return data that have filename equals to one of given filenames
            object_names (list[str], optional): if  given, will return data that have object name equals to one of given object names
            tags (str, (Tag), list[(Tag) or str], optional): if given, will return data that have one of given tags
                                                            by default. if `intersect_tags` is True, it will return data
                                                            that have all the given tags
            intersect_tags (bool, optional): if True, and a list of tags is given, will return data that have
                                             all the given tags. Defaults to False.
            q (str, optional): if given, will filter data with given query. Defaults to None.
            ids: (list[UUID]): ids of the data you're looking for. Defaults to None.
            custom_metadata: (dict, optional): filter based on the custom_metadata linked to the Data. Defaults to None

        Raises:
            NoDataError: When datalake has no data, raise this exception.

        Returns:
            A (MultiData) object that wraps a list of (Data).
        """
        if page_size:
            logger.warning("page_size is deprecated and not used anymore.")

        tags_q = convert_tag_list_to_query_language(tags, intersect_tags)
        query = combine_two_ql(q, tags_q)

        filters = DataFilter.model_validate(
            {
                "limit": limit,
                "offset": offset,
                "order_by": order_by,
                "filenames": filenames,
                "object_names": object_names,
                "ids": ids,
                "query": query,
                "custom_metadata": custom_metadata,
            }
        )
        data = DataLister(self.connection, self.id).list_items(filters)

        if len(data) == 0:
            raise NoDataError("No data found in this datalake with this query")

        return MultiData(self.connection, self.id, data)

    @exception_handler
    @beartype
    def create_data_tag(self, name: str) -> Tag:
        """Create a data tag used in this datalake

        Examples:
            ```python
            tag_car = lake.create_data_tag("car")
            ```
        Arguments:
            name (str): Name of the tag to create

        Returns:
            A (Tag) object
        """
        payload = {"name": name}
        r = self.connection.post(
            f"/api/datalake/{self.id}/tags", data=orjson.dumps(payload)
        ).json()
        return Tag(self.connection, r)

    @exception_handler
    @beartype
    def get_data_tag(self, name: str) -> Tag:
        """Retrieve a data tag used in this datalake.

        Examples:
            ```python
            tag_car = lake.get_data_tag("car")
            ```

        Arguments:
            name (str): Name of the tag to retrieve

        Returns:
            A (Tag) object
        """
        params = {"name": name}
        r = self.connection.get(
            f"/api/datalake/{self.id}/tags/find", params=params
        ).json()
        return Tag(self.connection, r)

    @exception_handler
    @beartype
    def get_or_create_data_tag(self, name: str) -> Tag:
        """Retrieve a data tag used in this datalake by its name.
        If tag does not exist, create it and return it.

        Examples:
            ```python
            tag = lake.get_or_create_data_tag("new_tag")
            ```

        Arguments:
            name (str): Name of the tag to retrieve or create

        Returns:
            A (Tag) object
        """
        try:
            return self.get_data_tag(name)
        except exceptions.ResourceNotFoundError:
            return self.create_data_tag(name)

    @exception_handler
    @beartype
    def list_data_tags(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Tag]:
        """List all tags of this datalake

        Examples:
            ```python
            tags = lake.list_data_tags()
            assert tag_car in tags
            ```

        Arguments:
            limit (int, optional): Limit the number of tags returned. Defaults to None.
            offset (int, optional): Offset to start listing tags. Defaults to None.
            order_by (list[str], optional): Order the tags returned by given fields. Defaults to None.

        Returns:
            A List of (Tag)
        """
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        params = filter_payload(params)
        r = self.connection.get(f"/api/datalake/{self.id}/tags", params=params).json()
        return [Tag(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def create_projection(
        self,
        data: Data,
        name: str,
        path: str,
        additional_info: dict = None,
        fill_metadata: bool = False,
    ) -> DataProjection:
        """Attach a Projection to an already existing Data.
        A Projection is another file that will be viewable along the original Data in the UI and in the annotation (if the type is compatible with the web browser).
        You can add as many Projections to a Data as you want.
        The type of this projection will be set to 'CUSTOM'

        Arguments:
            data (Data): target (Data).
            name (str): projection name.
            path (str): path of the file to upload
            additional_info (dict, optional): some data to attach to your projection. Defaults to None
            fill_metadata (bool, optional): if true, we will read image and add exif metadata to your projection. Defaults to False.

        Returns:
            A (DataProjection) object
        """

        info = additional_info or {}
        image_metadata = DataUploader.prepare_metadata_from_image(
            path, info, fill_metadata
        )

        filename = os.path.basename(path)
        file_size = Path(path).stat().st_size
        object_name = self.connection.generate_data_object_name(
            filename, ObjectDataType.DATA_PROJECTION, self.connector_id
        )
        _, _, content_type = self.connection.upload_file(
            object_name, path, connector_id=self.connector_id
        )
        return self._create_projection_from_cloud_image(
            data,
            name,
            object_name,
            filename,
            content_type,
            file_size,
            image_metadata.width,
            image_metadata.height,
            image_metadata.metadata,
        )

    @exception_handler
    @beartype
    def _create_projection_from_cloud_image(
        self,
        data: Data,
        name: str,
        object_name: str,
        filename: str,
        content_type: str,
        file_size: int,
        width: int,
        height: int,
        metadata: dict | None,
    ) -> DataProjection:
        payload = {
            "name": name,
            "file_size": file_size,
            "object_name": object_name,
            "filename": filename,
            "content_type": content_type,
            "width": width,
            "height": height,
            "additional_info": metadata,
        }
        item = self.connection.post(
            f"/api/data/{data.id}/projections",
            data=orjson.dumps(payload),
        ).json()
        logger.info(f"Projection {name} created for data {data.id}")
        return DataProjection(self.connection, data.id, item)

    @exception_handler
    @beartype
    def import_bucket_objects(
        self,
        prefixes: list[str],
        tags: list[str | Tag] | None = None,
        source: str | DataSource | None = None,
    ) -> Job:
        """Asynchronously import files from your remote storage (bucket) into this (Datalake)
        Only files with known content-types will be added.

        This method takes a list of prefixes. Prefixes can either be full object names or the prefix to a bunch of object names
        Given tags and source will be added to all imported data.
        We will read exif of your image to create metadata.

        You can only call this method if you use a private object storage with this datalake, owned by your organization.
        You should use this method carefully as it can import your whole S3 in the platform if you import for example "/"

        If you want to import projections from your object storage, or if you want to add custom_metadata,
        you could instead call import_cloud_objects()

        This method will return a Job object, you can call job.wait_for_done() to wait for import.
        As it might be a long task, we don't wait_for_done() in the method.

        Args:
            prefixes: list of prefixes to import
            tags: list of tags that will be added to data
            source: data source that will be specified on data

        Returns:
            A (Job) that you can wait for done.
        """

        tag_ids = self._get_or_create_data_tag_ids(tags)
        source = self._get_or_create_data_source(source)

        payload = {
            "datalake_id": self.id,
            "prefixes": prefixes,
            "tag_ids": tag_ids,
        }
        if source:
            payload["data_source_id"] = source.id

        return self._request_import_bucket_objects(payload)

    @exception_handler
    @beartype
    def import_cloud_objects(self, cloud_objects: dict[str, dict | CloudObject]) -> Job:
        """Asynchronously import files from your bucket into this Datalake.
        Only files with known content-types will be added.

        This method is limited to 500 elements.
        If you have more elements to import, consider batching and calling this method multiple times.

        The keys are the object_names of the data you want to import, the values are CloudObjects that represents all the additional information that needs to be stored against your Data.
        CloudObject is defined in picsellia.types.schemas, it's a pydantic model, but you can also give a dict, SDK will try to parse it.

        CloudObject allows: \n
        - metadata (dict, optional): metadata to attach to the data that will be created on the platform. It must match requirements from https://documentation.picsellia.com/update/docs/datalake-metadata#/
        - custom_metadata (dict): a dict of metadata to attach to the created Data
        - tags (list[str]): a list of tag names, the SDK will get or create each name
        - data_source (str): a str, the SDK will get or create source

        You can only call this method if you use a private object storage with this datalake, owned by your organization.

        This will launch one asynchronous job, it is returned by this method and can be waited

        Examples:
            ```python
                from picsellia.types.schemas import CloudObject, CloudProjectionObject
                datalake = client.get_datalake()
                job = datalake.import_cloud_objects(
                    cloud_objects={
                        "/bucket/path/object-1.jpg": {
                            "metadata": {
                                "reference": "XYZ1"
                            },
                            "tags": ["tag-1", "tag-2"],
                            "data_source": "cloud",
                            "custom_metadata": {"value": 10},
                        },
                        "/bucket/path/object-2.jpg": CloudObject(
                            "metadata"={
                                "reference": "XYZ1"
                            },
                            tags=["tag-1"],
                            data_source="cloud",
                            custom_metadata={"value": 25},
                        ),
                    }
                )
                job.wait_for_done()
                datalake.import_cloud_projections(
                    cloud_projections={
                        "/bucket/path/object-1.jpg": [
                            {
                                "name": "view",
                                "object_name": "/bucket/path/object-1-projection.jpg",
                            }
                        ],
                        "/bucket/path/object-2.jpg": [
                                CloudProjectionObject(
                                    name="pr1",
                                    object_name="/bucket/path/object-2-projection.jpg",
                                )
                        ],
                    }
                )
            ```
        Args:
            cloud_objects (dict): dict with object names as keys and CloudObject as values
        Returns:
            A (Job) that you can wait for done.
        """
        if len(cloud_objects) < 1 or len(cloud_objects) > 500:
            raise ValueError(
                "Parameter 'cloud_objects' must have at least 1 and less than 500 elements."
            )

        payload = {"datalake_id": self.id, "objects": {}}
        for name, obj in cloud_objects.items():
            payload["objects"][name] = (
                CloudObject(**obj).model_dump()
                if isinstance(obj, dict)
                else obj.model_dump()
            )

        return self._request_import_bucket_objects(payload)

    def _request_import_bucket_objects(self, payload: dict) -> Job:
        r = self.connection.post(
            path=f"/api/datalake/{self.id}/objects",
            data=orjson.dumps(payload),
        ).json()
        self.refresh(r["datalake"])
        return Job(self.connection, r["job"], version=2)

    @exception_handler
    @beartype
    def import_cloud_projections(
        self, cloud_projections: dict[str, list[dict | CloudProjectionObject]]
    ) -> Job:
        """Asynchronously import files from your bucket as (DataProjection) into this Datalake.
        Only files with known content-types will be added.

        This method is limited to 500 elements.
        If you have more elements to import, consider batching and calling this method multiple times.

        The keys must be object names of Data that are ALREADY exist in your Datalake. The values are a list of CloudProjectionObjects (or the corresponding dict), that represents a (DataProjection).
        CloudProjectionObject is defined in picsellia.types.schemas, it's a pydantic model, but you can also give a dict, SDK will try to parse it.

        CloudProjectionObject must have: \n
        - name (str): name of your projection
        - object_name (str): path in your bucket of your projection file.

        You can only call this method if you use a private object storage with this datalake, owned by your organization.

        This will launch one asynchronous job, it is returned by this method and can be waited

        Examples:
            ```python
                from picsellia.types.schemas import CloudObject, CloudProjectionObject
                datalake = client.get_datalake()
                datalake.import_cloud_projections(
                    cloud_projections={
                        "/bucket/path/object-1.jpg": [
                            {
                                "name": "view",
                                "object_name": "/bucket/path/object-1-projection.jpg",
                            }
                        ],
                        "/bucket/path/object-2.jpg": [
                            CloudProjectionObject(
                                name="pr1",
                                object_name="/bucket/path/object-2-projection.jpg",
                            )
                        ],
                    }
                )
            ```
        Args:
            cloud_projections (dict): dict with object names as keys and CloudProjectionObject as values
        Returns:
            A (Job) that you can wait for done.
        """
        if len(cloud_projections) < 1 or len(cloud_projections) > 500:
            raise ValueError(
                "Parameter 'cloud_projections' must have at least 1 and less than 500 elements."
            )

        payload = {"datalake_id": self.id, "projections": {}}
        for name, projections in cloud_projections.items():
            payload["projections"][name] = [
                (
                    CloudProjectionObject(**obj).model_dump()
                    if isinstance(obj, dict)
                    else obj.model_dump()
                )
                for obj in projections
            ]

        r = self.connection.post(
            path=f"/api/datalake/{self.id}/objects/projections",
            data=orjson.dumps(payload),
        ).json()
        self.refresh(r["datalake"])
        return Job(self.connection, r["job"], version=2)

    def _get_or_create_data_tag_ids(self, tags: list[str | Tag] | None):
        tag_ids = []
        if tags:
            for tag in tags:
                if isinstance(tag, str):
                    computed_tag = self.get_or_create_data_tag(tag)
                else:
                    if tag.target_type == TagTarget.DATA:
                        computed_tag = tag
                    else:
                        computed_tag = self.create_data_tag(tag.name)

                tag_ids.append(computed_tag.id)
        return tag_ids

    def _get_or_create_data_source(self, source: str | DataSource | None):
        if isinstance(source, str):
            return DataSourceService.get_or_create_datasource(
                self.connection, self._organization_id, source
            )
        else:
            return source

    @exception_handler
    @beartype
    def update_multiple_data(self, objects: dict[UUID, dict | CloudObject]) -> None:
        """Update metadata, custom_metadata, tags and source of multiple data.

        This method is limited to 100 elements.
        If you have more elements to import, consider batching and calling this method multiple times.

        The keys are the ids of the data you want to import, the values are CloudObjects that represents all the additional information that needs to be stored against your Data.
        CloudObject is defined in picsellia.types.schemas, it's a pydantic model, but you can also give a dict, SDK will try to parse it.

        CloudObject allows: \n
        - metadata (dict, optional): metadata to attach to the data that will be created on the platform. It must match requirements from https://documentation.picsellia.com/update/docs/datalake-metadata#/
        - custom_metadata (dict): a dict of metadata to attach to the created Data
        - tags (list[str]): a list of tag names, the SDK will get or create each name
        - data_source (str): a str, the SDK will get or create source

        Examples:
            ```python
                from picsellia.types.schemas import CloudObject, CloudProjectionObject
                datalake = client.get_datalake()
                data = datalake.list_data(limit=2)
                datalake.update_multiple_data(
                    objects={
                        data[0].id: {
                            "metadata": {
                                "reference": "XYZ1"
                            },
                            "tags": ["tag-1", "tag-2"],
                            "data_source": "cloud",
                            "custom_metadata": {"value": 10},
                        },
                        data[1].id: CloudObject(
                            "metadata"={
                                "reference": "XYZ1"
                            },
                            tags=["tag-1"],
                            data_source="cloud",
                            custom_metadata={"value": 25},
                        ),
                    }
                )
            ```
        Args:
            objects (dict): dict with data ids as keys and CloudObject as values
        Returns:
            A (Job) that you can wait for done.
        """
        if len(objects) < 1 or len(objects) > 100:
            raise ValueError(
                "Parameter 'objects' must have at least 1 and less than 100 elements."
            )

        payload = {"datalake_id": self.id, "objects": {}}
        for id, obj in objects.items():
            payload["objects"][str(id)] = (
                CloudObject(**obj).model_dump()
                if isinstance(obj, dict)
                else obj.model_dump()
            )

        self.connection.patch(
            path=f"/api/datalake/{self.id}/data/bulk", data=orjson.dumps(payload)
        )

    @exception_handler
    @beartype
    def launch_processing(
        self,
        processing: Processing,
        data: list[Data] | MultiData,
        parameters: dict = None,
        cpu: int = None,
        gpu: int = None,
        model_version_id: UUID = None,
        target_datalake_name: str = None,
        inputs: dict | None = None,
    ) -> Job:
        """Launch given processing onto this datalake version. You can give specific cpu, gpu or parameters.

        You must set the "inputs" dict so it matches the inputs configuration defined in the platform.
        It will fail if inputs are not matching expected inputs.

        If not given, it will use default values specified in Processing.
        If processing cannot be launched on this Datalake it will raise before launching.

        Examples:
            ```python
            processing = client.get_processing("data auto tagging")
            data = datalake.list_data(limit=10)
            model_version = client.get_model("my-model").get_version("v0")
            datalake.launch_processing(processing, data, inputs={"model_version_id": model_version.id, "target_datalake_name": "new-datalake"})
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

        if target_datalake_name:
            logging.warning(
                "'target_datalake_name' parameter is deprecated and will be removed in future versions. "
                "If you want to give a target_datalake_name, you should add it inside inputs directly"
            )
            if "target_datalake_name" not in inputs:
                inputs["target_datalake_name"] = target_datalake_name

        data_ids = list({datum.id for datum in data})
        payload = {
            "processing_id": processing.id,
            "parameters": parameters,
            "data_ids": data_ids,
            "cpu": cpu,
            "gpu": gpu,
            "model_version_id": model_version_id,
            "target_datalake_name": target_datalake_name,
            "inputs": inputs,
        }
        r = self.connection.post(
            f"/api/datalake/{self.id}/processing/launch",
            data=orjson.dumps(payload),
        ).json()
        return Job(self.connection, r, version=2)

    @exception_handler
    @beartype
    def embeddings_computation_status(self):
        """Return the status of the Visual Search for this (Datalake)

        Returns:
            a dict with status
        """
        return self.connection.get(
            f"/api/visual-search/datalake/{self.id}/status"
        ).json()

    @exception_handler
    @beartype
    def similar_search(self, data: Data, limit: int) -> MultiData:
        """
        Will return a (MultiData) object with data that are similar to given (Data), ordered by score.
        This is computed with Visual Search feature.
        Each data will have a temporary attribute _score, if you want to access the similarity score.

        Returns:
            a MultiData object
        """
        return DatalakeVisualSearchService(
            self.connection, self.id
        ).query_visual_search(str(data.id), limit)

    @exception_handler
    @beartype
    @deprecated(
        deprecated_in="6.32.0",
        details="This method has been renamed into similar_search",
    )
    def visual_search(self, data: Data, limit: int) -> MultiData:
        return self.similar_search(data, limit)

    @exception_handler
    @beartype
    def text_search(self, query: str, limit: int) -> MultiData:
        """
        Will return a MultiData object with data that match your query, ordered by score.
        This is computed with Visual Search feature.
        Each data will have a temporary attribute _score, if you want to access the similarity score.

        Returns:
            a MultiData object
        """
        return DatalakeVisualSearchService(
            self.connection, self.id
        ).query_visual_search(query, limit)

    @exception_handler
    @beartype
    def count_embeddings(self) -> int:
        """Return the number of data indexed by the Visual Search in this (Datalake)

        Returns:
            number of data indexed
        """
        r = self.connection.get(
            f"/api/visual-search/datalake/{self.id}/points/count"
        ).json()
        return r["count"]

    @exception_handler
    @beartype
    def list_embeddings(self, limit: int) -> list[dict]:
        """Return the list of embeddings computed for this (Datalake)

        Returns:
            a list of dict with data of indexation
            each dictionary contains:
                - id (str): UUID of the (Data)
                - vector (dict): Model-specific vector embeddings where:
                    - key (str): Embedder identifier
                    - value (list): Vector embedding as list of floats
        """
        return DatalakeVisualSearchService(self.connection, self.id).list_embeddings(
            limit, with_vector=True, with_payload=False, has_error=False
        )
