from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.connection_files_paginated_list_connection_files_item import (
    ConnectionFilesPaginatedListConnectionFilesItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectionFilesPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class ConnectionFilesPaginatedList:
    """  """

    _connection_files: Union[Unset, List[ConnectionFilesPaginatedListConnectionFilesItem]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("connection_files={}".format(repr(self._connection_files)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "ConnectionFilesPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        connection_files: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._connection_files, Unset):
            connection_files = []
            for connection_files_item_data in self._connection_files:
                connection_files_item = connection_files_item_data.to_dict()

                connection_files.append(connection_files_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if connection_files is not UNSET:
            field_dict["connectionFiles"] = connection_files
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_connection_files() -> Union[Unset, List[ConnectionFilesPaginatedListConnectionFilesItem]]:
            connection_files = []
            _connection_files = d.pop("connectionFiles")
            for connection_files_item_data in _connection_files or []:
                connection_files_item = ConnectionFilesPaginatedListConnectionFilesItem.from_dict(
                    connection_files_item_data, strict=False
                )

                connection_files.append(connection_files_item)

            return connection_files

        try:
            connection_files = get_connection_files()
        except KeyError:
            if strict:
                raise
            connection_files = cast(
                Union[Unset, List[ConnectionFilesPaginatedListConnectionFilesItem]], UNSET
            )

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        connection_files_paginated_list = cls(
            connection_files=connection_files,
            next_token=next_token,
        )

        return connection_files_paginated_list

    @property
    def connection_files(self) -> List[ConnectionFilesPaginatedListConnectionFilesItem]:
        if isinstance(self._connection_files, Unset):
            raise NotPresentError(self, "connection_files")
        return self._connection_files

    @connection_files.setter
    def connection_files(self, value: List[ConnectionFilesPaginatedListConnectionFilesItem]) -> None:
        self._connection_files = value

    @connection_files.deleter
    def connection_files(self) -> None:
        self._connection_files = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
