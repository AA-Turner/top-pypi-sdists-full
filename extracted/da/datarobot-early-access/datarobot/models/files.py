#  Copyright 2025 DataRobot, Inc. and its affiliates.
#
#  All rights reserved.
#
#  DataRobot, Inc. Confidential.
#
#  This is unpublished proprietary source code of DataRobot, Inc.
#  and its affiliates.
#
#  The copyright notice above does not evidence any actual or intended
#  publication of such source code.
from __future__ import annotations

from datetime import datetime
from io import IOBase
import os
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type, Union, cast

import dateutil
from requests import Response
import trafaret as t

from datarobot._compat import Int, String, TypedDict
from datarobot.enums import (
    DEFAULT_MAX_WAIT,
    DEFAULT_TIMEOUT,
    SHARING_RECIPIENT_TYPE,
    FileLocationType,
    FilesOverwriteStrategy,
    LocalSourceType,
    StrEnum,
)
from datarobot.errors import InvalidUsageError
from datarobot.models.api_object import APIObject
from datarobot.models.credential import CredentialDataSchema
from datarobot.models.dataset import _remove_empty_params
from datarobot.models.sharing import CatalogSharedRole, CatalogSharedRoleRequest, ModifyCatalogSharedRolePayload
from datarobot.models.user_blueprints.models import HumanReadable
from datarobot.utils import assert_single_parameter
from datarobot.utils.pagination import unpaginate
from datarobot.utils.source import parse_source_type
from datarobot.utils.waiters import wait_for_async_resolution


class CatalogAccessType(StrEnum):
    """Enum of catalog access types for filtering search results."""

    OWNED = "owned"
    SHARED = "shared"
    CREATED = "created"
    ANY = "any"


_file_schema = t.Dict({
    t.Key("file_name") >> "name": String,
    t.Key("file_type") >> "type": String,
    t.Key("file_size") >> "size": Int(),
    t.Key("ingest_errors", optional=True): t.Or(String(allow_blank=True), t.Null),
    t.Key("file_created_at", optional=True) >> "created_at": t.Or(t.Call(dateutil.parser.parse), t.Null),
    t.Key("file_checksum", optional=True) >> "checksum": t.Or(String, t.Null),
})

_files_schema = t.Dict({
    t.Key("id"): String,
    t.Key("name"): String,
    t.Key("description", optional=True): t.Or(String, t.Null),
    t.Key("type"): String,
    t.Key("tags"): t.List(String),
    t.Key("num_files", optional=True): t.Int,
    t.Key("from_archive", optional=True): t.Bool(),
    t.Key("created_at"): t.Call(dateutil.parser.parse),
    t.Key("created_by", optional=True): t.Or(String, t.Null),
})

_file_catalog_search_schema = t.Dict({
    t.Key("id"): String,
    t.Key("catalog_name") >> "name": String,
    t.Key("description", optional=True): t.Or(String, t.Null),
    t.Key("info_creator_full_name") >> "created_by": String,
    t.Key("info_creation_date") >> "created_at": t.Call(dateutil.parser.parse),
    t.Key("last_modification_date") >> "last_modified_at": t.Call(dateutil.parser.parse),
    t.Key("last_modifier_full_name") >> "last_modified_by": String,
    t.Key("tags"): t.List(String),
    t.Key("num_files", optional=True): t.Or(Int, t.Null),
    t.Key("from_archive", optional=True): t.Or(bool, t.Null),
}).ignore_extra("*")


_files_stage_schema = t.Dict({"catalog_id": String, "stage_id": String}).ignore_extra("*")

_files_details_schema = t.Dict({
    t.Key("id"): t.String(),
    t.Key("catalog_version_id"): t.String(),
}).allow_extra("*")


class DeletionResult(TypedDict):
    path: str
    numFilesDeleted: int


class FileLink(TypedDict):
    fileName: str
    url: str


class File(APIObject, HumanReadable):
    """
    Represents an individual file within a Files container.

    This class represents a single file contained within a Files container in the DataRobot catalog.
    It provides information about individual files such as name, size, and path within the archive.

    Attributes
    ----------
    name: str
        The name of the individual file.
    type: str
        The type of the file.
    size: int
        The size of the file in bytes.
    ingest_errors: str
        The errors encountered during ingestion of the file.
    created_at: datetime or None
        The datetime when the file was created.
    checksum: str or None
        The checksum of the file, if available.
    """

    _converter = _file_schema.allow_extra("*")

    def __init__(
        self,
        name: str,
        type: str,
        size: int,
        ingest_errors: str | None = None,
        created_at: datetime | None = None,
        checksum: str | None = None,
    ):
        self.name = name
        self.type = type
        self.size = size
        self.ingest_errors = ingest_errors
        self.created_at = created_at
        self.checksum = checksum


class FilesStage(APIObject, HumanReadable):
    """A place to accumulate multiple uploaded files
    before they're added into corresponding files container.

    .. versionadded:: v3.10

    Attributes
    ----------
    catalog_id: str
        The unique identifier for the files container.
        The `FilesStage` can be applied only to that files container.
    stage_id: str
        The unique identifier for the `FilesStage` object.
    """

    _converter = _files_stage_schema

    def __init__(self, catalog_id: str, stage_id: str):
        self.catalog_id = catalog_id
        self.stage_id = stage_id

    def apply(self, overwrite: Optional[FilesOverwriteStrategy] = FilesOverwriteStrategy.RENAME) -> "Files":
        """
        Add the files uploaded into this `FilesStage` into the corresponding files container.
        You can call this method only once for a particular `FilesStage`.

        .. versionadded:: v3.10

        Parameters
        ----------
        overwrite: Optional[FilesOverwriteStrategy]
            How to deal with a name conflict between an existing file and an uploaded one.
            RENAME (default): Rename an uploaded file using the "<filename> (n).ext" pattern.
            REPLACE: Prefer an uploaded file.
            SKIP: Prefer an existing file.
            ERROR: Return an "HTTP 409 Conflict" response in case of a naming conflict.

        Returns
        -------
        response: Files
            A fully armed and operational Files container.
        """
        url = f"files/{self.catalog_id}/fromStage/"
        response = self._client.post(url, json={"stageId": self.stage_id, "overwrite": overwrite})
        return Files.get(response.json()["catalogId"])

    def upload(self, source: str | IOBase, file_name: str | None = None) -> None:
        """Upload a file into the `FilesStage`.

        .. versionadded:: v3.10

        Parameters
        ----------
        source: str | IOBase
            Local file path or a file-like object to upload.
        file_name: str
            The file name to apply on the server side.
        """
        url = f"files/{self.catalog_id}/stages/{self.stage_id}/upload/"

        if isinstance(source, str):
            fname = file_name or os.path.basename(source)
            self._client.build_request_with_file(
                method="post",
                url=url,
                fname=fname,
                file_path=source,
                read_timeout=DEFAULT_TIMEOUT.UPLOAD,
            )
        else:
            fname = cast(str, getattr(source, "name", file_name))
            self._client.build_request_with_file(
                method="post",
                url=url,
                fname=fname,
                filelike=source,
                read_timeout=DEFAULT_TIMEOUT.UPLOAD,
            )


class FilesDetails(APIObject):
    _converter = _files_details_schema

    def __init__(self, id: str, catalog_version_id: str) -> None:
        self.id = id
        self.version_id = catalog_version_id

    @classmethod
    def get(cls, files_id: str) -> "FilesDetails":
        """
        Gets the details about a files container.

        Parameters
        ----------
        files_id:
            The ID of the files container.

        Returns
        -------
        FilesDetails
            An instance of FilesDetails containing the details of the files container.
        """
        path = f"catalogItems/{files_id}/extendedDetails/"
        return cls.from_location(path)


class Files(APIObject):
    """
    Represents one or more files associated with a single entity in the DataRobot catalog.

    This class provides functionality to interact with files stored in the DataRobot catalog,
    including retrieving and updating file information and downloading file contents.

    .. versionadded:: v3.8

    Attributes
    ----------
    id: str
        The unique identifier for the files container.
    name: str
        The name of the files container.
    type: str
        The type of files container.
    tags: List[str]
        A list of tags associated with the files container.
    num_files: int
        The number of files in the container.
    from_archive: bool
        Whether the files container was extracted from an archive.
    created_at: datetime
        A timestamp from when the files container was created.
    created_by: str
        The username of the user who created the files container.
    description: Optional[str]
        An optional description of the files container.
    """

    _converter = _files_schema.allow_extra("*")
    _path = "files/"
    _async_status_location: str | None = None

    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        tags: List[str],
        created_at: datetime,
        created_by: str,
        from_archive: bool = False,
        num_files: int | None = None,
        description: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.tags = tags
        self.num_files = num_files
        self.from_archive = from_archive
        self.created_at = created_at
        self.created_by = created_by
        self.description = description

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, id={self.id!r})"

    @classmethod
    def get(cls: Type["Files"], files_id: str) -> "Files":
        """
        Gets the information about a files container.

        .. versionadded:: v3.8

        Parameters
        ----------
        files_id: str
            The ID of the files container.

        Returns
        -------
        files: Files
            The queried files container.
        """

        path = f"catalogItems/{files_id}/"
        return cls.from_location(path)

    def download(
        self,
        file_name: Optional[str] = None,
        file_path: Optional[str] = None,
        filelike: Optional[IOBase] = None,
        version_id: Optional[str] = None,
    ) -> None:
        """
        Retrieves uploaded file contents.
        Writes it to either the file or a file-like object that can write bytes.

        Only one of ``file_path`` or ``filelike`` can be provided. If a file-like object is
        provided, the user is responsible for closing it when they are done.

        The user must also have permission to download data.

        .. versionadded:: v3.8

        Parameters
        ----------
        file_name: Optional[str]
            The name of the file to download from the files container.
            If not provided, if the file container was created from an archive,
            it will download the original archive file.
            Otherwise, if there is only a single file contained in the container, it will download that.
        file_path: Optional[str]
            The destination to write the file to.
        filelike: Optional[IOBase]
            A file-like object to write to.  The object must be able to write bytes. The user is
            responsible for closing the object.
        version_id: Optional[str]
            If provided, download from the specified version instead of the latest version.
        Returns
        -------
        None
        """
        assert_single_parameter(("filelike", "file_path"), filelike, file_path)
        data = {}
        if file_name:
            data["fileName"] = file_name

        if version_id:
            path = f"{self._path}{self.id}/versions/{version_id}/downloads/"
        else:
            path = f"{self._path}{self.id}/downloads/"
        response = self._client.post(path, json=data, stream=True)
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1000):
                    f.write(chunk)
        if filelike:
            for chunk in response.iter_content(chunk_size=1000):
                filelike.write(chunk)

    @classmethod
    def upload(
        cls,
        source: Union[str, IOBase],
        tags: Optional[List[str]] = None,
        use_archive_contents: bool = True,
        *,
        wait_for_completion: bool = True,
    ) -> "Files":
        """
        This method covers Files container creation from local materials (file) and a URL.

        .. versionadded:: v3.8

        Parameters
        ----------
        source: str or file object
            Pass a URL, filepath, or file to create and return a Files container.
        tags: Optional[List[str]]
            A list of tags associated with the files container.
        use_archive_contents: bool (default: True)
            If True, extract archive contents and associate with the Files container.
            If False, the archive file will be uploaded as-is.

        Returns
        -------
        response: Files
            The Files container created from the uploaded data source.

        Raises
        ------
        InvalidUsageError
            If the source parameter cannot be determined to be a URL, filepath, or file object.

        Examples
        --------
        .. code-block:: python

            # Upload a local file
            files_a = Files.upload("./data/document.pdf")

            # Create a files container via URL with tags
            files_b = Files.upload(
                "https://example.com/document.pdf",
                tags=["web", "document"]
            )

            # Create files container using a local file object without extracting archive contents
            with open("./data/archive.zip", "rb") as file_pointer:
                files_c = Files.upload(file_pointer, use_archive_contents=False)
        """
        error_msg = f"Source parameter ({source}) cannot be determined to be a URL, filepath, or file object."
        try:
            source_type = parse_source_type(source)
        except InvalidUsageError:
            raise InvalidUsageError(error_msg)

        if source_type == FileLocationType.URL:
            return cls.create_from_url(
                url=cast(str, source),
                tags=tags,
                use_archive_contents=use_archive_contents,
                wait_for_completion=wait_for_completion,
            )
        elif source_type == FileLocationType.PATH:
            return cls.create_from_file(
                file_path=cast(str, source),
                tags=tags,
                use_archive_contents=use_archive_contents,
                wait_for_completion=wait_for_completion,
            )
        elif source_type == LocalSourceType.FILELIKE:
            return cls.create_from_file(
                filelike=cast(IOBase, source),
                tags=tags,
                use_archive_contents=use_archive_contents,
                wait_for_completion=wait_for_completion,
            )
        else:
            raise InvalidUsageError(error_msg)

    @classmethod
    def create_from_url(
        cls,
        url: str,
        tags: Optional[List[str]] = None,
        use_archive_contents: bool = True,
        max_wait: int = DEFAULT_MAX_WAIT,
        *,
        wait_for_completion: bool = True,
    ) -> "Files":
        """
        Create a new files container in the DataRobot catalog from a URL.

        This method uploads a file from a given URL to the DataRobot catalog. The method will wait
        for the upload to complete before returning.

        .. versionadded:: v3.8

        Parameters
        ----------
        url: str
            The URL of the file to upload. Must be accessible by the DataRobot server.
        tags: Optional[List[str]]
            A list of tags associated with the files container.
        use_archive_contents: bool
            If True, extract archive contents and associate with the Files container.
            If False, the archive file will be uploaded as-is. Defaults to True.
        max_wait: Optional[int]
            Maximum time in seconds to wait for the upload to complete. Defaults to DEFAULT_MAX_WAIT.

        Returns
        -------
        Files
            The newly created files container.

        Raises
        ------
        AsyncTimeoutError
            If the upload takes longer than ``max_wait`` seconds.
        """
        endpoint = f"{cls._path}fromURL/"
        payload: Dict[str, str] = {"url": url, "use_archive_contents": str(use_archive_contents)}

        response = cls._client.post(endpoint, data=payload)

        file = cls._get_files_from_async(response, wait_for_completion=wait_for_completion, max_wait=max_wait)

        if tags:
            file.modify(tags=tags)
        return file

    @classmethod
    def create_from_file(
        cls,
        file_path: Optional[str] = None,
        filelike: Optional[IOBase] = None,
        tags: Optional[List[str]] = None,
        use_archive_contents: bool = True,
        read_timeout: int = DEFAULT_TIMEOUT.UPLOAD,
        max_wait: int = DEFAULT_MAX_WAIT,
        *,
        wait_for_completion: bool = True,
    ) -> "Files":
        """
        A blocking call that creates a new files container from a file. Returns the files
        container once the file has been successfully uploaded and processed.

        Warning: This function does not clean up its open files. If you pass a filelike, you are
        responsible for closing it. If you pass a ``file_path``, this will create a file object from
        the ``file_path`` but will not close it.

        .. versionadded:: v3.8

        Parameters
        ----------
        file_path: Optional[str]
            The path to the file. This will create a files container object pointing to that file but
            will not close the local file.
        filelike: Optional[str]
            An open and readable file object.
        tags: Optional[List[str]]
            A list of tags associated with the files container.
        use_archive_contents: bool
            If True, extract archive contents and associate with the Files container.
            If False, the archive file will be uploaded as-is. Defaults to True.
        read_timeout: Optional[int]
            The maximum number of seconds to wait for the server to respond indicating that the
            initial upload is complete.
        max_wait: Optional[int]
            Time in seconds after which files container creation is considered unsuccessful.

        Returns
        -------
        response: Files
            A fully armed and operational Files container.
        """
        assert_single_parameter(("filelike", "file_path"), file_path, filelike)

        upload_url = f"{cls._path}fromFile/"
        default_fname = "file"

        # Prepare additional form data
        form_data = {"use_archive_contents": str(use_archive_contents)}

        if file_path:
            fname = os.path.basename(file_path)
            response = cls._client.build_request_with_file(
                method="post",
                url=upload_url,
                fname=fname,
                file_path=file_path,
                read_timeout=read_timeout,
                form_data=form_data,
            )
        else:
            fname = getattr(filelike, "name", default_fname)
            response = cls._client.build_request_with_file(
                method="post",
                url=upload_url,
                fname=fname,
                filelike=filelike,
                read_timeout=read_timeout,
                form_data=form_data,
            )

        file = cls._get_files_from_async(response, wait_for_completion=wait_for_completion, max_wait=max_wait)

        if tags:
            file.modify(tags=tags)
        return file

    @classmethod
    def create_from_data_source(
        cls,
        data_source_id: str,
        tags: Optional[List[str]] = None,
        credential_id: Optional[str] = None,
        credential_data: Optional[Dict[str, str]] = None,
        use_archive_contents: bool = True,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> "Files":
        """
        A blocking call that creates a new Files container from data stored at a DataSource.
        Returns the files container once it has been successfully uploaded and processed.

        .. versionadded:: v3.8

        Parameters
        ----------
        data_source_id: str
            The ID of the DataSource to use as the source of data.
        tags: Optional[List[str]]
            A list of tags associated with the files container.
        credential_id: Optional[str]
            The ID of the set of credentials to use for authentication.
        credential_data: Optional[Dict[str, str]]
            The credentials to authenticate with the database, to use instead of credential ID.
        use_archive_contents: bool
            If True, extract archive contents and associate with the files container.
            If False, the archive file will be uploaded as-is. Defaults to True.
        max_wait: Optional[int]
            Time in seconds after which files container creation is considered unsuccessful.

        Returns
        -------
        response: Files
            The Files container created from the uploaded data.
        """
        base_data = {
            "data_source_id": data_source_id,
            "credential_id": credential_id,
            "credential_data": credential_data,
            "use_archive_contents": str(use_archive_contents),
        }
        data = _remove_empty_params(base_data)

        if "credential_data" in data:
            data["credential_data"] = CredentialDataSchema(data["credential_data"])

        upload_url = f"{cls._path}fromDataSource/"
        response = cls._client.post(upload_url, data=data)

        new_file_location = wait_for_async_resolution(cls._client, response.headers["Location"], max_wait)
        file = cls.from_location(new_file_location)
        if tags:
            file.modify(tags=tags)
        return file

    def update(self) -> None:
        """
        Updates the Files container attributes in place with the latest information from the server.

        .. versionadded:: v3.8

        Returns
        -------
        None
        """
        new_file = self.get(self.id)
        update_attrs = (
            "name",
            "description",
            "type",
            "tags",
            "num_files",
            "from_archive",
            "created_at",
            "created_by",
        )
        for attr in update_attrs:
            setattr(self, attr, getattr(new_file, attr))

    def modify(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        """
        Modifies the Files container name, description and/or tags.
        Updates the object in place.

        .. versionadded:: v3.8

        Parameters
        ----------
        name: Optional[str]
            The new name of the files container.

        description: Optional[str]
            The new description of the files container.
        tags: Optional[List[str]]
            A list of tags attached to the files container.
            If any tags were previously specified for the files container, they will be overwritten.
            If omitted or None, keep previous tags.
            To clear them, specify [].

        Returns
        -------
        None
        """
        if name is None and description is None and tags is None:
            return
        # if we omit tags, it will clear them,
        # so in case where it is None, we want to preserve
        # categories and only clear them when it is []
        if tags is None:
            tags = self.tags

        url = f"catalogItems/{self.id}/"
        params = {"name": name, "description": description, "tags": tags}
        params = _remove_empty_params(params)

        response = self._client.patch(url, data=params)
        data = response.json()
        self.name = data.get("name", data.get("catalogName", ""))
        self.description = data["description"]
        self.tags = data["tags"]

    @classmethod
    def delete(cls, files_id: str) -> None:
        """
        Soft-deletes a files container. You cannot get, list, or do any actions with it, except to restore it.

        .. versionadded:: v3.8

        Parameters
        ----------
        files_id: str
            The ID of the files container to mark for deletion.

        Returns
        -------
        None
        """
        cls._client.delete(f"{cls._path}{files_id}/")

    @classmethod
    def un_delete(cls, files_id: str) -> None:
        """
        Restores a previously soft-deleted files container. If the files container was not deleted, nothing happens.

        .. versionadded:: v3.8

        Parameters
        ----------
        files_id: str
            The ID of the files container to un-delete.

        Returns
        -------
        None
        """
        cls._client.patch(f"{cls._path}{files_id}/deleted/")

    @classmethod
    def search_catalog(
        cls,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
        owner_user_id: Optional[str] = None,
        owner_username: Optional[str] = None,
        order_by: str = "-created",
        access_type: CatalogAccessType = CatalogAccessType.ANY,
    ) -> List["FilesCatalogSearch"]:
        """
        Fetch a list of the files container catalog entries the current user has access to
        based on an optional search term, tags, owner user info, or sort order.

        .. versionadded:: v3.8

        Parameters
        ----------
        search: Optional[str]
            A value to search for in the file's name, description, tags, etc. The search is case-insensitive.
            If no value is provided for this parameter, or if the empty string is used,
            or if the string contains only whitespace, no filtering will be done. Partial matching
            is performed on files container name and description fields while all other fields will only match
            if the search matches the whole value exactly.

        tags: Optional[List[str]]
            If provided, the results will be filtered to include only items with the specified tag.

        limit: Optional[int] (default: 100)
            At most this many results are returned. To specify no limit, use 0.
            The default may change and a maximum limit may be imposed without notice.

        offset: Optional[int] (default: 0)
            This many results will be skipped.

        owner_user_id: Optional[str]
            Filter results to those owned by one or more owner identified by UID.

        owner_username: Optional[str]
            Filter results to those owned by one or more owner identified by username.

        order_by: Optional[str] (default: '-created')
            Sort order which will be applied to a catalog list. Valid options are ``catalogName``,
            ``originalName``, ``description``, ``created``, and ``relevance``. For all options other
            than relevance, you may prefix the attribute name with a dash to sort
            in descending order. For example, ``orderBy='-catalogName'``.

        access_type: Optional[CatalogAccessType] (default: CatalogAccessType.ANY)
            Access type used to filter returned results:
            'owned' items are owned by the requester, 'shared' items have been shared with the requester,
            'created' items have been created by the requester, and 'any' items matches all.

        Returns
        -------
        List[FilesCatalogSearch]
            A list of FileCatalogSearch objects matching the search criteria.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.
        """
        return FilesCatalogSearch.search_catalog(
            search=search,
            tags=tags,
            limit=limit,
            offset=offset,
            owner_user_id=owner_user_id,
            owner_username=owner_username,
            order_by=order_by,
            access_type=access_type,
        )

    def clone(
        self,
        *,
        omit: str | List[str] | None = None,
        wait_for_completion: bool = True,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> Files:
        """Duplicate the files container.

        .. versionadded:: v3.10

        Parameters
        ----------
        omit:
            Don't duplicate some files.
        wait_for_completion:
            Set to *False* if you don't want to wait for the operation completion.
        max_wait:
            Raise AsyncTimeoutError if wait_for_completion=True
            and the operation took more than this number of seconds.
        """
        url = f"files/{self.id}/clone/"

        if isinstance(omit, str):
            omit = [omit]

        response = self._client.post(url, data={"omit": omit})
        return self._get_files_from_async(response, wait_for_completion=wait_for_completion, max_wait=max_wait)

    def create_stage(self) -> "FilesStage":
        """
        Create a new `FilesStage` for this files container.

        .. versionadded:: v3.10

        """
        response = self._client.post(f"files/{self.id}/stages/")
        return FilesStage.from_server_data(response.json())

    def apply_stage(self, stage: "FilesStage") -> None:
        """
        Apply the `FilesStage` for this files container.

        .. versionadded:: v3.10

        """
        file = stage.apply()
        self.num_files = file.num_files

    def wait_for_completion(self) -> None:
        """Wait for initial upload completion."""
        if self._async_status_location is None:
            return

        location = wait_for_async_resolution(self._client, self._async_status_location)

        new_file = Files.from_location(location)
        self.num_files = new_file.num_files
        self.from_archive = new_file.from_archive
        self._async_status_location = None

    @classmethod
    def _get_files_from_async(cls, response: Response, *, wait_for_completion: bool = True, max_wait: int) -> "Files":
        """Get `Files` entity from the response.
        Conditionally wait for an async operation resolution.

        Parameters
        ----------
        response
            HTTP response for an action which has just created a new files container.
        wait_for_completion
            Set the parameter to False to get the entity before the operation completed.
        max_wait:
            Raise AsyncTimeoutError if wait_for_completion=True
            and the operation took more than this number of seconds.
        """
        if wait_for_completion:
            new_file_location = wait_for_async_resolution(cls._client, response.headers["Location"], max_wait)
            return cls.from_location(new_file_location)

        else:
            entity = cls.from_location(f"catalogItems/{response.json()['catalogId']}/")
            if "Location" in response.headers:
                entity.set_async_status_location(response.headers["Location"])

            return entity

    def set_async_status_location(self, async_status_location: str) -> None:
        """Assign a URL to keep track of an async operation completion."""
        self._async_status_location = async_status_location

    def list_contained_files(
        self,
        file_type: str = "",
        limit: int = 100,
        offset: int = 0,
        recursive: bool = True,
        prefix: Optional[str] = None,
        version_id: Optional[str] = None,
    ) -> List[File]:
        """
        Returns a list of all individual files within a Files container.

        This method retrieves information about all individual files contained within
        a Files object. This is useful for Files objects that contain multiple files
        or are archives.

        Parameters
        ----------
        file_type:
            Filter results by file type (e.g., 'txt', 'pdf').
        limit:
            Maximum number of files to return. Set to 0 for no limit.
        offset:
            Number of files to skip before returning results.
        recursive:
            If True, list files recursively within all subdirectories.
        prefix:
            If provided, only list files whose paths start with this prefix.
        version_id:
            If provided, retrieve from the specified version instead of the latest version.

        Returns
        -------
        List[File]
            A list of File objects representing individual files within the Files container.
        """
        endpoint = (
            f"{self._path}{self.id}/versions/{version_id}/allFiles/"
            if version_id
            else f"{self._path}{self.id}/allFiles/"
        )
        params: Dict[str, Union[int, str]] = {"offset": offset, "recursive": str(recursive).lower()}

        if file_type:
            params["file_type"] = file_type
        if limit > 0:
            params["limit"] = limit
        if prefix:
            params["prefix"] = prefix

        fetch_all_data = limit == 0
        files_data = (
            list(unpaginate(endpoint, params, self._client))
            if fetch_all_data
            else self._client.get(endpoint, params=params).json()["data"]
        )
        return [File.from_server_data(file_data) for file_data in files_data]

    def get_shared_roles(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        share_recipient_type: Optional[SHARING_RECIPIENT_TYPE] = None,
    ) -> List[CatalogSharedRole]:
        """
        Lists the roles for users, groups, and organizations who have access to this files container.

        Parameters
        ----------
        id:
            Only return the access control information for a organization, group or user with this
            ID.
        name:
            Only return the access control information for a organization, group or user with this
            name.
        share_recipient_type:
            Only returns results with the given recipient type.

        Returns
        -------
        List[CatalogSharedRole]
            A list of CatalogSharedRole objects representing the shared roles for this files container.
        """
        params = {
            "id": id,
            "name": name,
            "share_recipient_type": share_recipient_type.value if share_recipient_type else None,
        }
        params = _remove_empty_params(params)
        path = f"{self._path}{self.id}/sharedRoles/"
        return [CatalogSharedRole.from_server_data(role) for role in unpaginate(path, params, self._client)]

    def copy(
        self,
        source_path: str | Iterable[str],
        *,
        target: str | None = None,
        target_files: Optional["Files"] = None,
        overwrite: FilesOverwriteStrategy = FilesOverwriteStrategy.RENAME,
        max_wait: int = DEFAULT_MAX_WAIT,
        wait_for_completion: bool = True,
    ) -> "Files":
        """
        Copy file(s) and/or folder(s) within
        the same or into another files container.

        Parameters
        ----------
        source_path:
            file(s) and/or folder(s) to copy.
        target:
            Either a folder to copy file(s) into
            or a new file name if only one file is being copied.
        target_files:
            Files collection to copy files into.
        overwrite:
            Strategy to handle naming conflicts at the target location.
        max_wait:
             Raise TimeoutError if the operation took more than this number of seconds to complete.
        wait_for_completion:
            Whether to wait for the copy operation to complete before returning.
        """
        if isinstance(source_path, str):
            sources = [source_path]
        elif isinstance(source_path, Iterable):
            sources = list(source_path)
        else:
            raise ValueError(source_path)

        url = f"files/{self.id}/copyBatch/"
        response = self._client.post(
            url,
            json={
                "sources": sources,
                "target": target,
                "targetCatalogId": target_files and target_files.id,
                "overwrite": overwrite.value,
            },
        )
        return self._get_files_from_async(response, max_wait=max_wait, wait_for_completion=wait_for_completion)

    def copy_within_container(
        self,
        source_path: str,
        target_path: str,
        overwrite: FilesOverwriteStrategy = FilesOverwriteStrategy.RENAME,
    ) -> Files:
        """
        Copy a file or folder to another path within the same container.

        Parameters
        ----------
        source_path:
            The path of the source file or folder to copy.
        target_path:
            The destination path where the file or folder should be copied.
        overwrite:
            Strategy to handle naming conflicts at the target location.
        """
        url = f"files/{self.id}/copy/"
        response = self._client.post(
            url,
            json={
                "source": source_path,
                "target": target_path,
                "overwrite": overwrite.value,
            },
        )
        return self.from_location(f"catalogItems/{response.json()['catalogId']}/")

    def rename_files(
        self,
        from_path: str,
        to_path: str,
        *,
        overwrite: Optional[FilesOverwriteStrategy] = None,
    ) -> "Files":
        """
        Rename/move a file or folder within this catalog, and optionally overwrite.

        Parameters
        ----------
        from_path:
            Source path under this catalog.
        to_path:
            Target path under this catalog.
        overwrite:
            Strategy for overwriting existing paths. If not provided, not sent in the request.

        Returns
        -------
        Files
            The updated Files object after the rename.
        """
        url = f"{self._path}{self.id}/allFiles/"
        payload: Dict[str, Any] = {"fromPath": from_path, "toPath": to_path}
        if overwrite is not None:
            payload["overwrite"] = overwrite.value
        response = self._client.patch(url, json=payload)
        resp_body = response.json() if response.text else {}
        catalog_id = resp_body.get("catalogId", self.id)
        return self.from_location(f"catalogItems/{catalog_id}/")

    def delete_files(self, paths: List[str]) -> Tuple[Files, List[DeletionResult]]:
        """
        Recursively delete files or folders at the given paths. Silently ignore paths that do not exist.

        Parameters
        ----------
        paths:
            List of file or folder paths to delete. Folders are deleted recursively.

        Returns
        -------
        Tuple[Files, List[DeletionResult]]
            The updated Files object and a list of results for each path indicating the number of
            files deleted that path was responsible for.
        """
        url = f"files/{self.id}/allFiles/"
        response = self._client.delete(url, json={"paths": paths})
        resp_body = response.json()
        return self.from_location(f"catalogItems/{resp_body['catalogId']}/"), resp_body["results"]

    @classmethod
    def create_empty_catalog_item_dir(cls) -> "Files":
        """Create an empty catalog item directory and return its Files object."""
        response = cls._client.post(cls._path, json={})
        resp_body = response.json()
        return cls.from_location(f"catalogItems/{resp_body['catalogId']}/")

    def upload_from_url(
        self,
        url: str,
        use_archive_contents: bool = True,
        overwrite: FilesOverwriteStrategy = FilesOverwriteStrategy.RENAME,
        max_wait: int = DEFAULT_MAX_WAIT,
        *,
        wait_for_completion: bool = True,
        prefix: Optional[str] = None,
    ) -> "Files":
        """
        Loads the file(s) from a URL into this catalog item.

        Parameters
        ----------
        url:
            The URL of the file or archive to load. Must be accessible by the DataRobot server.
        use_archive_contents:
            If True, extract archive contents into the catalog item. If False, upload the
            file as-is. Defaults to True.
        overwrite:
            How to handle name conflicts with existing files. Defaults to RENAME.
        max_wait:
            Maximum time in seconds to wait for the upload to complete. Defaults to DEFAULT_MAX_WAIT.
        wait_for_completion:
            If True, block until the upload completes. If False, return after starting the upload.
            Defaults to True.
        prefix:
            Folder path inside the catalog item to upload into. If None, upload to the catalog root.

        Returns
        -------
        Files
            This catalog item. When ``wait_for_completion`` is False, the returned object has async
            status set so callers can use ``wait_for_completion()`` to track the operation.

        Raises
        ------
        AsyncTimeoutError
            If ``wait_for_completion`` is True and the upload takes longer than ``max_wait`` seconds.
        """
        endpoint = f"{self._path}{self.id}/fromURL/"
        payload = {
            "url": url,
            "useArchiveContents": str(use_archive_contents),
            "overwrite": overwrite.value,
            "prefix": prefix,
        }
        response = self._client.post(endpoint, json=payload)
        return self._get_files_from_async(
            response,
            max_wait=max_wait,
            wait_for_completion=wait_for_completion,
        )

    def upload_from_data_source(
        self,
        data_source_id: str,
        credential_id: Optional[str] = None,
        credential_data: Optional[Dict[str, str]] = None,
        prefix: Optional[str] = None,
        use_archive_contents: bool = True,
        overwrite: FilesOverwriteStrategy = FilesOverwriteStrategy.RENAME,
        *,
        max_wait: int = DEFAULT_MAX_WAIT,
        wait_for_completion: bool = True,
    ) -> "Files":
        """
        A blocking call that uploads files from a data source into the Files container.
        Returns the updated files container once files have been successfully uploaded.

        Parameters
        ----------
        data_source_id: str
            The ID of the DataSource to use as the source of data.
        tags: Optional[List[str]]
            A list of tags associated with the files container.
        credential_id: Optional[str]
            The ID of the set of credentials to use for authentication.
        credential_data: Optional[Dict[str, str]]
            The credentials to authenticate with the database, to use instead of credential ID.
        use_archive_contents: bool
            If True, extract archive contents and associate with the files container.
            If False, the archive file will be uploaded as-is. Defaults to True.
        prefix: Optional[str]
            Folder path inside the catalog item to upload into. If None, upload to the catalog root.
        overwrite: FilesOverwriteStrategy
            Strategy to use to handle name conflicts with existing files on upload.
        max_wait: Optional[int]
            Time in seconds after which files container creation is considered unsuccessful.
        wait_for_completion: bool
            If True, block until the upload completes. If False, return after starting the upload.

        Returns
        -------
        response: Files
            The Files container with the new uploaded files.
        """
        base_data = {
            "data_source_id": data_source_id,
            "credential_id": credential_id,
            "credential_data": CredentialDataSchema(credential_data) if credential_data else None,
            "use_archive_contents": str(use_archive_contents),
            "prefix": prefix,
            "overwrite": overwrite.value,
        }
        payload = _remove_empty_params(base_data)

        url = f"{self._path}{self.id}/fromDataSource/"
        response = self._client.post(url, json=payload)
        return self._get_files_from_async(response, max_wait=max_wait, wait_for_completion=wait_for_completion)

    def generate_signed_urls(
        self, file_names: List[str], duration: int = 600, version_id: Optional[str] = None
    ) -> List[FileLink]:
        """
        Generate signed URLs for one or more files.

        Parameters
        ----------
        file_names:
            List of file paths in the catalog for which to generate signed URLs.
        duration:
            Duration in seconds for which the signed URLs should remain valid. Maximum is 3000 seconds.
        version_id:
            Version ID of the catalog item to target. If not provided, the latest version is used. Allows caller to
            retrieve signed URLs for earlier versions of files.

        Returns
        -------
        List[FileLink]
            A list of dictionaries for each file name with its corresponding signed url.
        """
        url = f"files/{self.id}/links/" if version_id is None else f"files/{self.id}/versions/{version_id}/links/"
        response = self._client.post(
            url,
            json={
                "fileNames": file_names,
                "duration": duration,
            },
        )
        return cast(List[FileLink], response.json()["links"])

    def upload_file(
        self,
        file: Union[str, IOBase],
        prefix: Optional[str] = None,
        use_archive_contents: bool = True,
        overwrite: FilesOverwriteStrategy = FilesOverwriteStrategy.RENAME,
        read_timeout: int = DEFAULT_TIMEOUT.UPLOAD,
        max_wait: int = DEFAULT_MAX_WAIT,
        *,
        wait_for_completion: bool = True,
        file_name: Optional[str] = None,
    ) -> "Files":
        """
        A blocking call to upload a file into an existing file container. Returns the updated
        files container once the file has been successfully uploaded and processed.

        Warning: This function does not clean up its open files. If you pass a file-like object, you are
        responsible for closing it. If you pass a file path, this will create a file object from
        the file path but will not close it.

        Parameters
        ----------
        file:
            The path to the file or a file-like object to upload.
        prefix:
            An optional prefix (folder path) to place the uploaded file into.
        use_archive_contents:
            If True, extract archive contents and associate with the Files container.
            If False, the archive file will be uploaded as-is. Defaults to True.
        overwrite:
            How to deal with a name conflict between an existing file and an uploaded one.
            RENAME (default): Rename an uploaded file using the "<filename> (n).ext" pattern.
            REPLACE: Prefer an uploaded file.
            SKIP: Prefer an existing file.
            ERROR: Return an "HTTP 409 Conflict" response in case of a naming conflict.
        read_timeout:
            The maximum number of seconds to wait for the server to respond indicating that the
            initial upload is complete.
        max_wait:
            Time in seconds after which files container creation is considered unsuccessful.
        wait_for_completion:
            Set to *False* if you don't want to wait for the operation completion.
        file_name:
            The file name to apply on the server side. Defaults to the base name for a file path
            or "file" for a file-like object.

        Returns
        -------
        response: Files
            The updated Files container including the newly uploaded file(s).
        """
        request_kwargs: Dict[str, Union[str, IOBase]]
        if isinstance(file, str):
            fname = file_name or os.path.basename(file)
            request_kwargs = {"file_path": file}
        elif isinstance(file, IOBase):
            fname = file_name or "file"
            request_kwargs = {"filelike": file}
        else:
            raise InvalidUsageError(f"File parameter ({file}) must be a file path or a file-like object.")

        form_data = {
            "use_archive_contents": str(use_archive_contents),
            "overwrite": overwrite.value,
            "prefix": prefix,
        }
        response = self._client.build_request_with_file(
            method="post",
            url=f"{self._path}{self.id}/fromFile/",
            fname=fname,
            read_timeout=read_timeout,
            form_data=form_data,
            **request_kwargs,
        )
        return self._get_files_from_async(response, wait_for_completion=wait_for_completion, max_wait=max_wait)

    def modify_shared_roles(
        self,
        roles: List[CatalogSharedRoleRequest],
        apply_grant_to_linked_objects: bool = False,
        operation: str = "updateRoles",
    ) -> None:
        """
        Grant access, remove access or update roles for users, groups, and organizations who have access to this file
        container. Up to 100 roles may be set in a single request.

        Parameters
        ----------
        roles: List[CatalogSharedRoleRequest]
            A list of role requests to modify the roles for.
        apply_grant_to_linked_objects: bool
            If ``true`` for any users being granted access to the entity,
            grant the user read access to any linked objects. Ignored if no such
            objects are relevant for the entity. This will not result in access
            being lowered for a user if the user already has higher access to
            linked objects than read access. However, if the target user does
            not have sharing permissions to the linked object, they will be given
            sharing access without lowering existing permissions. May result in an
            error if the user making the call does not have sufficient permissions
            to complete the grant.
        operation: str
            The name of the action being taken. The only supported operation is ``updateRoles``.

        Examples
        --------
        Grant access to a user by name:

        .. code-block:: python

            >>> from datarobot.enums import TARGET_SHARING_ROLE, SHARING_RECIPIENT_TYPE
            >>> from datarobot.models.sharing import CatalogSharedRoleRequest
            >>> from datarobot.models.files import Files

            >>> files = Files.get("my-files-id")
            >>> files.modify_shared_roles(
            ...     roles=[
            ...         CatalogSharedRoleRequest(
            ...             role=TARGET_SHARING_ROLE.EDITOR,
            ...             share_recipient_type=SHARING_RECIPIENT_TYPE.USER,
            ...             name="target_user_name",
            ...         )
            ...     ],
            ... )

        Remove access to a group by ID:

        .. code-block:: python

            >>> from datarobot.enums import TARGET_SHARING_ROLE, SHARING_RECIPIENT_TYPE
            >>> from datarobot.models.sharing import CatalogSharedRoleRequest
            >>> from datarobot.models.files import Files

            >>> files = Files.get("my-files-id")
            >>> files.modify_shared_roles(
            ...     roles=[
            ...         CatalogSharedRoleRequest(
            ...             role=TARGET_SHARING_ROLE.NO_ROLE,
            ...             share_recipient_type=SHARING_RECIPIENT_TYPE.GROUP,
            ...             id="group-id",
            ...         )
            ...     ],
            ... )
        """
        payload = ModifyCatalogSharedRolePayload(
            roles=roles, apply_grant_to_linked_objects=apply_grant_to_linked_objects, operation=operation
        )
        self._client.patch(f"{self._path}{self.id}/sharedRoles/", data=payload)


class FilesCatalogSearch(APIObject, HumanReadable):
    """
    An ``APIObject`` representing a file catalog entry the current user has access to
    based on an optional search term and/or tags.

    .. versionadded:: v3.8

    Attributes
    ----------
    id: str
        The ID of the catalog entry linked to the file.

    name: str
        The name of the files container in the catalog.

    description: Optional[str] (default: None)
        The description of the file.

    tags: List[str]
        A list of tags associated with the files container.

    num_files: Optional[int] (default: None)
        The number of files in the container.

    from_archive: Optional[bool] (default: None)
        Whether the files container was extracted from an archive.

    created_by: str
        The name of the user that created the file.

    created_at: datetime
        The timestamp when the catalog item was created.

    last_modified_by: str
        The name of the user that last modified the catalog item.

    last_modified_at: datetime
        The timestamp when the catalog item was last modified.
    """

    _path = "catalogItems/"
    _converter = _file_catalog_search_schema

    def __init__(
        self,
        id: str,
        name: str,
        created_by: str,
        created_at: datetime,
        last_modified_at: datetime,
        last_modified_by: str,
        tags: List[str],
        from_archive: Optional[bool] = None,
        num_files: Optional[int] = None,
        description: Optional[str] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.created_by = created_by
        self.created_at = created_at
        self.last_modified_at = last_modified_at
        self.last_modified_by = last_modified_by
        self.description = description
        self.tags = tags
        self.num_files = num_files
        self.from_archive = from_archive

    @classmethod
    def search_catalog(
        cls,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
        owner_user_id: Optional[str] = None,
        owner_username: Optional[str] = None,
        order_by: str = "-created",
        access_type: CatalogAccessType = CatalogAccessType.ANY,
    ) -> List["FilesCatalogSearch"]:
        """
        Fetch a list of the files container entries the current user has access to
        based on an optional search term, tags, owner user info, or sort order.

        .. versionadded:: v3.8

        Parameters
        ----------
        search: Optional[str]
            A value to search for in the file's name, description, tags, etc. The search is case-insensitive.
            If no value is provided for this parameter, or if the empty string is used,
            or if the string contains only whitespace, no filtering will be done. Partial matching
            is performed on files container name and description fields while all other fields will only match
            if the search matches the whole value exactly.

        tags: Optional[List[str]]
            If provided, the results will be filtered to include only items with the specified tag.

        limit: Optional[int] (default: 100)
            At most this many results are returned. To specify no limit, use 0.
            The default may change and a maximum limit may be imposed without notice.

        offset: Optional[int] (default: 0)
            This many results will be skipped.

        owner_user_id: Optional[str]
            Filter results to those owned by one or more owner identified by UID.

        owner_username: Optional[str]
            Filter results to those owned by one or more owner identified by username.

        order_by: Optional[str] (default: '-created')
            Sort order which will be applied to a catalog list. Valid options are ``catalogName``,
            ``originalName``, ``description``, ``created``, and ``relevance``. For all options other
            than relevance, you may prefix the attribute name with a dash to sort
            in descending order. For example, ``orderBy='-catalogName'``.

        access_type: Optional[CatalogAccessType] (default: CatalogAccessType.ANY)
            Access type used to filter returned results:
            'owned' items are owned by the requester, 'shared' items have been shared with the requester,
            'created' items have been created by the requester, and 'any' items matches all.

        Returns
        -------
        List[FilesCatalogSearch]
            A list of FileCatalogSearch objects matching the search criteria.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.
        """
        params = {
            "search_for": search,
            "tag": [tag.strip() for tag in tags if tag] if tags else None,
            "type": "files",
            "limit": limit,
            "offset": offset,
            "owner_user_id": owner_user_id,
            "owner_username": owner_username,
            "order_by": order_by,
            "access_type": access_type,
        }
        params = _remove_empty_params(params)
        if limit == 0:
            data = list(unpaginate(cls._path, params, cls._client))
        else:
            data = cls._client.get(cls._path, params=params).json()["data"]

        return [cls.from_server_data(a) for a in data]
