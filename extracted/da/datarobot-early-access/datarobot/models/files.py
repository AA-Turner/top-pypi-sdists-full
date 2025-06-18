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
from datetime import datetime
from io import IOBase
import os
from typing import cast, Dict, List, Optional, Type, Union

import dateutil
import trafaret as t

from datarobot._compat import Int, String
from datarobot.enums import (
    DEFAULT_MAX_WAIT,
    DEFAULT_TIMEOUT,
    FileLocationType,
    LocalSourceType,
    StrEnum,
)
from datarobot.errors import InvalidUsageError
from datarobot.models.api_object import APIObject
from datarobot.models.credential import CredentialDataSchema
from datarobot.models.dataset import _remove_empty_params
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


_file_schema = t.Dict(
    {
        t.Key("file_name") >> "name": String,
        t.Key("file_type") >> "type": String,
        t.Key("file_size") >> "size": Int(),
        t.Key(
            "ingest_errors",
        ): String(allow_blank=True),
    }
)

_files_schema = t.Dict(
    {
        t.Key("id"): String,
        t.Key("name"): String,
        t.Key("description", optional=True): t.Or(String, t.Null),
        t.Key("type"): String,
        t.Key("tags"): t.List(String),
        t.Key("num_files"): Int(),
        t.Key("from_archive"): t.Bool(),
        t.Key("created_at"): t.Call(dateutil.parser.parse),
        t.Key("created_by", optional=True): t.Or(String, t.Null),
    }
)

_file_catalog_search_schema = t.Dict(
    {
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
    }
).ignore_extra("*")


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
    """

    _converter = _file_schema.allow_extra("*")

    def __init__(
        self,
        name: str,
        type: str,
        size: int,
        ingest_errors: str,
    ):
        self.name = name
        self.type = type
        self.size = size
        self.ingest_errors = ingest_errors


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

    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        tags: List[str],
        num_files: int,
        from_archive: bool,
        created_at: datetime,
        created_by: str,
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
        Get information about a files container.

        .. versionadded:: v3.8

        Parameters
        ----------
        files_id: str
            The id of the files container.

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
    ) -> None:
        """
        Retrieves uploaded file contents.
        Writes it to either the file or a file-like object that can write bytes.

        Only one of file_path or filelike can be provided. If a file-like object is
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

        Returns
        -------
        None
        """
        assert_single_parameter(("filelike", "file_path"), filelike, file_path)
        params = {}
        if file_name:
            params["file_name"] = file_name

        response = self._client.post(
            f"{self._path}{self.id}/downloads/", params=params, stream=True
        )
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
                url=cast(str, source), tags=tags, use_archive_contents=use_archive_contents
            )
        elif source_type == FileLocationType.PATH:
            return cls.create_from_file(
                file_path=cast(str, source), tags=tags, use_archive_contents=use_archive_contents
            )
        elif source_type == LocalSourceType.FILELIKE:
            return cls.create_from_file(
                filelike=cast(IOBase, source), tags=tags, use_archive_contents=use_archive_contents
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
            If the upload takes longer than max_wait seconds.
        """
        endpoint = f"{cls._path}fromURL/"
        payload: Dict[str, str] = {"url": url, "use_archive_contents": str(use_archive_contents)}

        response = cls._client.post(endpoint, data=payload)

        new_file_location = wait_for_async_resolution(
            cls._client, response.headers["Location"], max_wait
        )
        if tags:
            cls._client.patch(new_file_location, data={"tags": tags})
        new_file = cls.from_location(new_file_location)
        return new_file

    @classmethod
    def create_from_file(
        cls,
        file_path: Optional[str] = None,
        filelike: Optional[IOBase] = None,
        tags: Optional[List[str]] = None,
        use_archive_contents: bool = True,
        read_timeout: int = DEFAULT_TIMEOUT.UPLOAD,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> "Files":
        """
        A blocking call that creates a new files container from a file. Returns when the file has
        been successfully uploaded and processed.

        Warning: This function does not clean up its open files. If you pass a filelike, you are
        responsible for closing it. If you pass a file_path, this will create a file object from
        the file_path but will not close it.

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
            A fully armed and operational Files container
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

        new_file_location = wait_for_async_resolution(
            cls._client, response.headers["Location"], max_wait
        )
        file = cls.from_location(new_file_location)
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
        Returns when the files container has been successfully uploaded and processed.

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
            The Files container created from the uploaded data
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

        new_file_location = wait_for_async_resolution(
            cls._client, response.headers["Location"], max_wait
        )
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
        Soft-deletes a files container. You cannot get, list, or do any actions with it, except for undeleting it.

        .. versionadded:: v3.8

        Parameters
        ----------
        files_id: str
            The id of the files container to mark for deletion.

        Returns
        -------
        None
        """
        cls._client.delete(f"{cls._path}{files_id}/")

    @classmethod
    def un_delete(cls, files_id: str) -> None:
        """
        Undeletes a previously deleted files container. If the files container was not deleted, nothing happens.

        .. versionadded:: v3.8

        Parameters
        ----------
        files_id: str
            The id of the files container to un-delete.

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

        limit: Optional[int] (default: 100), at most this many results are returned. To specify no
            limit, use 0. The default may change and a maximum limit may be imposed without notice.

        offset: Optional[int] (default: 0), this many results will be skipped.

        owner_user_id: Optional[str]
            Filter results to those owned by one or more owner identified by UID.

        owner_username: Optional[str]
            Filter results to those owned by one or more owner identified by username.

        order_by: Optional[str] (default: '-created')
            Sort order which will be applied to a catalog list, valid options are "catalogName",
            "originalName", "description", "created", and "relevance". For all options other
            than relevance, you may prefix the attribute name with a dash to sort
            in descending order. E.g., orderBy='-catalogName'.

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
            If the server responded with 4xx status
        datarobot.errors.ServerError
            If the server responded with 5xx status
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

    def list_contained_files(
        self, file_type: str = "", limit: int = 100, offset: int = 0
    ) -> List["File"]:
        """
        List all individual files within a Files container.

        .. versionadded:: v3.8

        This method retrieves information about all individual files contained within
        a Files object. This is useful for Files objects that contain multiple files
        or are archives.

        Parameters
        ----------
        file_type: str
            Filter results by file type (e.g., 'txt', 'pdf').
        limit: Optional[int] (default: 100)
            Maximum number of files to return. Set to 0 for no limit.
        offset: Optional[int] (default: 0)
            Number of files to skip before returning results.

        Returns
        -------
        List[File]
            A list of File objects representing individual files within the Files container.

        Raises
        ------
        ClientError
            If the Files object is not found or access is denied.
        ServerError
            If there's a server-side error while retrieving the file list.
        """
        endpoint = f"{self._path}{self.id}/allFiles/"
        params: Dict[str, Union[int, str]] = {"offset": offset}
        if file_type:
            params["file_type"] = file_type
        if limit == 0:
            files_data = list(unpaginate(endpoint, params, self._client))
        else:
            params["limit"] = limit
            files_data = self._client.get(endpoint, params=params).json()["data"]

        return [File.from_server_data(file_data) for file_data in files_data]


class FilesCatalogSearch(APIObject, HumanReadable):
    """
    An APIObject representing a file catalog entry the current user has access to
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

        limit: Optional[int] (default: 100), at most this many results are returned. To specify no
            limit, use 0. The default may change and a maximum limit may be imposed without notice.

        offset: Optional[int] (default: 0), this many results will be skipped.

        owner_user_id: Optional[str]
            Filter results to those owned by one or more owner identified by UID.

        owner_username: Optional[str]
            Filter results to those owned by one or more owner identified by username.

        order_by: Optional[str] (default: '-created')
            Sort order which will be applied to a catalog list, valid options are "catalogName",
            "originalName", "description", "created", and "relevance". For all options other
            than relevance, you may prefix the attribute name with a dash to sort
            in descending order. e.g., orderBy='-catalogName'.

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
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
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
