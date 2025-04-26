from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.data_frame_column_type_metadata import DataFrameColumnTypeMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataFrameColumnMetadata")


@attr.s(auto_attribs=True, repr=False)
class DataFrameColumnMetadata:
    """  """

    _display_name: Union[Unset, str] = UNSET
    _type: Union[Unset, DataFrameColumnTypeMetadata] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("display_name={}".format(repr(self._display_name)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DataFrameColumnMetadata({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        display_name = self._display_name
        type: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_display_name() -> Union[Unset, str]:
            display_name = d.pop("displayName")
            return display_name

        try:
            display_name = get_display_name()
        except KeyError:
            if strict:
                raise
            display_name = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, DataFrameColumnTypeMetadata]:
            type: Union[Unset, Union[Unset, DataFrameColumnTypeMetadata]] = UNSET
            _type = d.pop("type")

            if not isinstance(_type, Unset):
                type = DataFrameColumnTypeMetadata.from_dict(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, DataFrameColumnTypeMetadata], UNSET)

        data_frame_column_metadata = cls(
            display_name=display_name,
            type=type,
        )

        data_frame_column_metadata.additional_properties = d
        return data_frame_column_metadata

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def display_name(self) -> str:
        if isinstance(self._display_name, Unset):
            raise NotPresentError(self, "display_name")
        return self._display_name

    @display_name.setter
    def display_name(self, value: str) -> None:
        self._display_name = value

    @display_name.deleter
    def display_name(self) -> None:
        self._display_name = UNSET

    @property
    def type(self) -> DataFrameColumnTypeMetadata:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: DataFrameColumnTypeMetadata) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
