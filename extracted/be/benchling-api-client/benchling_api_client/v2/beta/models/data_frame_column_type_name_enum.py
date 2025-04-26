from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.data_frame_column_type_name_enum_name import DataFrameColumnTypeNameEnumName
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataFrameColumnTypeNameEnum")


@attr.s(auto_attribs=True, repr=False)
class DataFrameColumnTypeNameEnum:
    """  """

    _name: Union[Unset, DataFrameColumnTypeNameEnumName] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("name={}".format(repr(self._name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DataFrameColumnTypeNameEnum({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        name: Union[Unset, int] = UNSET
        if not isinstance(self._name, Unset):
            name = self._name.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_name() -> Union[Unset, DataFrameColumnTypeNameEnumName]:
            name = UNSET
            _name = d.pop("name")
            if _name is not None and _name is not UNSET:
                try:
                    name = DataFrameColumnTypeNameEnumName(_name)
                except ValueError:
                    name = DataFrameColumnTypeNameEnumName.of_unknown(_name)

            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, DataFrameColumnTypeNameEnumName], UNSET)

        data_frame_column_type_name_enum = cls(
            name=name,
        )

        data_frame_column_type_name_enum.additional_properties = d
        return data_frame_column_type_name_enum

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
    def name(self) -> DataFrameColumnTypeNameEnumName:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: DataFrameColumnTypeNameEnumName) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
