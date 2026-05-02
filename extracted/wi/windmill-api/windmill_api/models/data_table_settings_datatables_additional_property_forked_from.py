from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_table_settings_datatables_additional_property_forked_from_schema import (
        DataTableSettingsDatatablesAdditionalPropertyForkedFromSchema,
    )


T = TypeVar("T", bound="DataTableSettingsDatatablesAdditionalPropertyForkedFrom")


@_attrs_define
class DataTableSettingsDatatablesAdditionalPropertyForkedFrom:
    """Fork origin info with schema snapshot

    Attributes:
        schema (Union[Unset, DataTableSettingsDatatablesAdditionalPropertyForkedFromSchema]): Schema snapshot at fork
            time
    """

    schema: Union[Unset, "DataTableSettingsDatatablesAdditionalPropertyForkedFromSchema"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_table_settings_datatables_additional_property_forked_from_schema import (
            DataTableSettingsDatatablesAdditionalPropertyForkedFromSchema,
        )

        d = src_dict.copy()
        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, DataTableSettingsDatatablesAdditionalPropertyForkedFromSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = DataTableSettingsDatatablesAdditionalPropertyForkedFromSchema.from_dict(_schema)

        data_table_settings_datatables_additional_property_forked_from = cls(
            schema=schema,
        )

        data_table_settings_datatables_additional_property_forked_from.additional_properties = d
        return data_table_settings_datatables_additional_property_forked_from

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
