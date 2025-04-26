from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataFrameColumnTypeMetadataTarget")


@attr.s(auto_attribs=True, repr=False)
class DataFrameColumnTypeMetadataTarget:
    """ Only present if the column type is ObjectLink """

    _base_type_name: Union[Unset, str] = UNSET
    _schema_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("base_type_name={}".format(repr(self._base_type_name)))
        fields.append("schema_id={}".format(repr(self._schema_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DataFrameColumnTypeMetadataTarget({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        base_type_name = self._base_type_name
        schema_id = self._schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if base_type_name is not UNSET:
            field_dict["baseTypeName"] = base_type_name
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_base_type_name() -> Union[Unset, str]:
            base_type_name = d.pop("baseTypeName")
            return base_type_name

        try:
            base_type_name = get_base_type_name()
        except KeyError:
            if strict:
                raise
            base_type_name = cast(Union[Unset, str], UNSET)

        def get_schema_id() -> Union[Unset, None, str]:
            schema_id = d.pop("schemaId")
            return schema_id

        try:
            schema_id = get_schema_id()
        except KeyError:
            if strict:
                raise
            schema_id = cast(Union[Unset, None, str], UNSET)

        data_frame_column_type_metadata_target = cls(
            base_type_name=base_type_name,
            schema_id=schema_id,
        )

        data_frame_column_type_metadata_target.additional_properties = d
        return data_frame_column_type_metadata_target

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
    def base_type_name(self) -> str:
        if isinstance(self._base_type_name, Unset):
            raise NotPresentError(self, "base_type_name")
        return self._base_type_name

    @base_type_name.setter
    def base_type_name(self, value: str) -> None:
        self._base_type_name = value

    @base_type_name.deleter
    def base_type_name(self) -> None:
        self._base_type_name = UNSET

    @property
    def schema_id(self) -> Optional[str]:
        if isinstance(self._schema_id, Unset):
            raise NotPresentError(self, "schema_id")
        return self._schema_id

    @schema_id.setter
    def schema_id(self, value: Optional[str]) -> None:
        self._schema_id = value

    @schema_id.deleter
    def schema_id(self) -> None:
        self._schema_id = UNSET
