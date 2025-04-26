from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConvertToASM")


@attr.s(auto_attribs=True, repr=False)
class ConvertToASM:
    """  """

    _blob_or_file_id: str
    _connection_id: Union[Unset, str] = UNSET
    _vendor: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("blob_or_file_id={}".format(repr(self._blob_or_file_id)))
        fields.append("connection_id={}".format(repr(self._connection_id)))
        fields.append("vendor={}".format(repr(self._vendor)))
        return "ConvertToASM({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        blob_or_file_id = self._blob_or_file_id
        connection_id = self._connection_id
        vendor = self._vendor

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if blob_or_file_id is not UNSET:
            field_dict["blobOrFileId"] = blob_or_file_id
        if connection_id is not UNSET:
            field_dict["connectionId"] = connection_id
        if vendor is not UNSET:
            field_dict["vendor"] = vendor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_blob_or_file_id() -> str:
            blob_or_file_id = d.pop("blobOrFileId")
            return blob_or_file_id

        try:
            blob_or_file_id = get_blob_or_file_id()
        except KeyError:
            if strict:
                raise
            blob_or_file_id = cast(str, UNSET)

        def get_connection_id() -> Union[Unset, str]:
            connection_id = d.pop("connectionId")
            return connection_id

        try:
            connection_id = get_connection_id()
        except KeyError:
            if strict:
                raise
            connection_id = cast(Union[Unset, str], UNSET)

        def get_vendor() -> Union[Unset, str]:
            vendor = d.pop("vendor")
            return vendor

        try:
            vendor = get_vendor()
        except KeyError:
            if strict:
                raise
            vendor = cast(Union[Unset, str], UNSET)

        convert_to_asm = cls(
            blob_or_file_id=blob_or_file_id,
            connection_id=connection_id,
            vendor=vendor,
        )

        return convert_to_asm

    @property
    def blob_or_file_id(self) -> str:
        """ The ID of a blob link or the API ID of a file to process. """
        if isinstance(self._blob_or_file_id, Unset):
            raise NotPresentError(self, "blob_or_file_id")
        return self._blob_or_file_id

    @blob_or_file_id.setter
    def blob_or_file_id(self, value: str) -> None:
        self._blob_or_file_id = value

    @property
    def connection_id(self) -> str:
        """ The ID of a connection to read the instrument vendor from. """
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
    def vendor(self) -> str:
        """ The instrument vendor to use for conversion. See /connect/list-allotropy-vendors. """
        if isinstance(self._vendor, Unset):
            raise NotPresentError(self, "vendor")
        return self._vendor

    @vendor.setter
    def vendor(self, value: str) -> None:
        self._vendor = value

    @vendor.deleter
    def vendor(self) -> None:
        self._vendor = UNSET
