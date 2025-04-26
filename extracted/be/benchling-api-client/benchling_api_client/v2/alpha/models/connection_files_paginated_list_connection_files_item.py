import datetime
from typing import Any, cast, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.connection_files_paginated_list_connection_files_item_data_type import (
    ConnectionFilesPaginatedListConnectionFilesItemDataType,
)
from ..models.connection_files_paginated_list_connection_files_item_status import (
    ConnectionFilesPaginatedListConnectionFilesItemStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectionFilesPaginatedListConnectionFilesItem")


@attr.s(auto_attribs=True, repr=False)
class ConnectionFilesPaginatedListConnectionFilesItem:
    """  """

    _connection_id: Union[Unset, str] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _data_type: Union[Unset, ConnectionFilesPaginatedListConnectionFilesItemDataType] = UNSET
    _download_url: Union[Unset, str] = UNSET
    _filename: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _instrument_query_id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _status: Union[Unset, ConnectionFilesPaginatedListConnectionFilesItemStatus] = UNSET

    def __repr__(self):
        fields = []
        fields.append("connection_id={}".format(repr(self._connection_id)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("data_type={}".format(repr(self._data_type)))
        fields.append("download_url={}".format(repr(self._download_url)))
        fields.append("filename={}".format(repr(self._filename)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("instrument_query_id={}".format(repr(self._instrument_query_id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("status={}".format(repr(self._status)))
        return "ConnectionFilesPaginatedListConnectionFilesItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        connection_id = self._connection_id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        data_type: Union[Unset, int] = UNSET
        if not isinstance(self._data_type, Unset):
            data_type = self._data_type.value

        download_url = self._download_url
        filename = self._filename
        id = self._id
        instrument_query_id = self._instrument_query_id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if connection_id is not UNSET:
            field_dict["connectionId"] = connection_id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if data_type is not UNSET:
            field_dict["dataType"] = data_type
        if download_url is not UNSET:
            field_dict["downloadUrl"] = download_url
        if filename is not UNSET:
            field_dict["filename"] = filename
        if id is not UNSET:
            field_dict["id"] = id
        if instrument_query_id is not UNSET:
            field_dict["instrumentQueryId"] = instrument_query_id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_connection_id() -> Union[Unset, str]:
            connection_id = d.pop("connectionId")
            return connection_id

        try:
            connection_id = get_connection_id()
        except KeyError:
            if strict:
                raise
            connection_id = cast(Union[Unset, str], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_data_type() -> Union[Unset, ConnectionFilesPaginatedListConnectionFilesItemDataType]:
            data_type = UNSET
            _data_type = d.pop("dataType")
            if _data_type is not None and _data_type is not UNSET:
                try:
                    data_type = ConnectionFilesPaginatedListConnectionFilesItemDataType(_data_type)
                except ValueError:
                    data_type = ConnectionFilesPaginatedListConnectionFilesItemDataType.of_unknown(_data_type)

            return data_type

        try:
            data_type = get_data_type()
        except KeyError:
            if strict:
                raise
            data_type = cast(Union[Unset, ConnectionFilesPaginatedListConnectionFilesItemDataType], UNSET)

        def get_download_url() -> Union[Unset, str]:
            download_url = d.pop("downloadUrl")
            return download_url

        try:
            download_url = get_download_url()
        except KeyError:
            if strict:
                raise
            download_url = cast(Union[Unset, str], UNSET)

        def get_filename() -> Union[Unset, str]:
            filename = d.pop("filename")
            return filename

        try:
            filename = get_filename()
        except KeyError:
            if strict:
                raise
            filename = cast(Union[Unset, str], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_instrument_query_id() -> Union[Unset, str]:
            instrument_query_id = d.pop("instrumentQueryId")
            return instrument_query_id

        try:
            instrument_query_id = get_instrument_query_id()
        except KeyError:
            if strict:
                raise
            instrument_query_id = cast(Union[Unset, str], UNSET)

        def get_modified_at() -> Union[Unset, datetime.datetime]:
            modified_at: Union[Unset, datetime.datetime] = UNSET
            _modified_at = d.pop("modifiedAt")
            if _modified_at is not None and not isinstance(_modified_at, Unset):
                modified_at = isoparse(cast(str, _modified_at))

            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_status() -> Union[Unset, ConnectionFilesPaginatedListConnectionFilesItemStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = ConnectionFilesPaginatedListConnectionFilesItemStatus(_status)
                except ValueError:
                    status = ConnectionFilesPaginatedListConnectionFilesItemStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, ConnectionFilesPaginatedListConnectionFilesItemStatus], UNSET)

        connection_files_paginated_list_connection_files_item = cls(
            connection_id=connection_id,
            created_at=created_at,
            data_type=data_type,
            download_url=download_url,
            filename=filename,
            id=id,
            instrument_query_id=instrument_query_id,
            modified_at=modified_at,
            status=status,
        )

        return connection_files_paginated_list_connection_files_item

    @property
    def connection_id(self) -> str:
        if isinstance(self._connection_id, Unset):
            raise NotPresentError(self, "connection_id")
        return self._connection_id

    @connection_id.setter
    def connection_id(self, value: str) -> None:
        self._connection_id = value

    @connection_id.deleter
    def connection_id(self) -> None:
        self._connection_id = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def data_type(self) -> ConnectionFilesPaginatedListConnectionFilesItemDataType:
        if isinstance(self._data_type, Unset):
            raise NotPresentError(self, "data_type")
        return self._data_type

    @data_type.setter
    def data_type(self, value: ConnectionFilesPaginatedListConnectionFilesItemDataType) -> None:
        self._data_type = value

    @data_type.deleter
    def data_type(self) -> None:
        self._data_type = UNSET

    @property
    def download_url(self) -> str:
        """URL to download the file. This URL is only valid for 24 hours."""
        if isinstance(self._download_url, Unset):
            raise NotPresentError(self, "download_url")
        return self._download_url

    @download_url.setter
    def download_url(self, value: str) -> None:
        self._download_url = value

    @download_url.deleter
    def download_url(self) -> None:
        self._download_url = UNSET

    @property
    def filename(self) -> str:
        if isinstance(self._filename, Unset):
            raise NotPresentError(self, "filename")
        return self._filename

    @filename.setter
    def filename(self, value: str) -> None:
        self._filename = value

    @filename.deleter
    def filename(self) -> None:
        self._filename = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def instrument_query_id(self) -> str:
        if isinstance(self._instrument_query_id, Unset):
            raise NotPresentError(self, "instrument_query_id")
        return self._instrument_query_id

    @instrument_query_id.setter
    def instrument_query_id(self, value: str) -> None:
        self._instrument_query_id = value

    @instrument_query_id.deleter
    def instrument_query_id(self) -> None:
        self._instrument_query_id = UNSET

    @property
    def modified_at(self) -> datetime.datetime:
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime.datetime) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def status(self) -> ConnectionFilesPaginatedListConnectionFilesItemStatus:
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: ConnectionFilesPaginatedListConnectionFilesItemStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
