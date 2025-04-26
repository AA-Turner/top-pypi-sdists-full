from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConvertToCSV")


@attr.s(auto_attribs=True, repr=False)
class ConvertToCSV:
    """  """

    _blob_or_file_id: str
    _automation_output_file_id: Union[Unset, str] = UNSET
    _connection_id: Union[Unset, str] = UNSET
    _mapper_config: Union[Unset, str] = UNSET
    _transform_type: Union[Unset, str] = UNSET
    _vendor: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("blob_or_file_id={}".format(repr(self._blob_or_file_id)))
        fields.append("automation_output_file_id={}".format(repr(self._automation_output_file_id)))
        fields.append("connection_id={}".format(repr(self._connection_id)))
        fields.append("mapper_config={}".format(repr(self._mapper_config)))
        fields.append("transform_type={}".format(repr(self._transform_type)))
        fields.append("vendor={}".format(repr(self._vendor)))
        return "ConvertToCSV({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        blob_or_file_id = self._blob_or_file_id
        automation_output_file_id = self._automation_output_file_id
        connection_id = self._connection_id
        mapper_config = self._mapper_config
        transform_type = self._transform_type
        vendor = self._vendor

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if blob_or_file_id is not UNSET:
            field_dict["blobOrFileId"] = blob_or_file_id
        if automation_output_file_id is not UNSET:
            field_dict["automationOutputFileId"] = automation_output_file_id
        if connection_id is not UNSET:
            field_dict["connectionId"] = connection_id
        if mapper_config is not UNSET:
            field_dict["mapperConfig"] = mapper_config
        if transform_type is not UNSET:
            field_dict["transformType"] = transform_type
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

        def get_automation_output_file_id() -> Union[Unset, str]:
            automation_output_file_id = d.pop("automationOutputFileId")
            return automation_output_file_id

        try:
            automation_output_file_id = get_automation_output_file_id()
        except KeyError:
            if strict:
                raise
            automation_output_file_id = cast(Union[Unset, str], UNSET)

        def get_connection_id() -> Union[Unset, str]:
            connection_id = d.pop("connectionId")
            return connection_id

        try:
            connection_id = get_connection_id()
        except KeyError:
            if strict:
                raise
            connection_id = cast(Union[Unset, str], UNSET)

        def get_mapper_config() -> Union[Unset, str]:
            mapper_config = d.pop("mapperConfig")
            return mapper_config

        try:
            mapper_config = get_mapper_config()
        except KeyError:
            if strict:
                raise
            mapper_config = cast(Union[Unset, str], UNSET)

        def get_transform_type() -> Union[Unset, str]:
            transform_type = d.pop("transformType")
            return transform_type

        try:
            transform_type = get_transform_type()
        except KeyError:
            if strict:
                raise
            transform_type = cast(Union[Unset, str], UNSET)

        def get_vendor() -> Union[Unset, str]:
            vendor = d.pop("vendor")
            return vendor

        try:
            vendor = get_vendor()
        except KeyError:
            if strict:
                raise
            vendor = cast(Union[Unset, str], UNSET)

        convert_to_csv = cls(
            blob_or_file_id=blob_or_file_id,
            automation_output_file_id=automation_output_file_id,
            connection_id=connection_id,
            mapper_config=mapper_config,
            transform_type=transform_type,
            vendor=vendor,
        )

        return convert_to_csv

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
    def automation_output_file_id(self) -> str:
        """ The ID of an AutomationOutputFile configured to with CSV transform argument. Transform parameters will be read from file settings. """
        if isinstance(self._automation_output_file_id, Unset):
            raise NotPresentError(self, "automation_output_file_id")
        return self._automation_output_file_id

    @automation_output_file_id.setter
    def automation_output_file_id(self, value: str) -> None:
        self._automation_output_file_id = value

    @automation_output_file_id.deleter
    def automation_output_file_id(self) -> None:
        self._automation_output_file_id = UNSET

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
    def mapper_config(self) -> str:
        """ A JSON configuration specifying how to convert a JSON file to CSV. Reach out to Benchling Support for more information about how to create a mapperConfig. """
        if isinstance(self._mapper_config, Unset):
            raise NotPresentError(self, "mapper_config")
        return self._mapper_config

    @mapper_config.setter
    def mapper_config(self, value: str) -> None:
        self._mapper_config = value

    @mapper_config.deleter
    def mapper_config(self) -> None:
        self._mapper_config = UNSET

    @property
    def transform_type(self) -> str:
        """ The transform type to use to convert an ASM file to CSV. """
        if isinstance(self._transform_type, Unset):
            raise NotPresentError(self, "transform_type")
        return self._transform_type

    @transform_type.setter
    def transform_type(self, value: str) -> None:
        self._transform_type = value

    @transform_type.deleter
    def transform_type(self) -> None:
        self._transform_type = UNSET

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
