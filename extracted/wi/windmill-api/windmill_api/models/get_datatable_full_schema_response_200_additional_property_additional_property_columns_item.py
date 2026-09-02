from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyColumnsItem")


@_attrs_define
class GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyColumnsItem:
    """
    Attributes:
        name (str):
        datatype (str):
        primary_key (Union[Unset, bool]):
        default_value (Union[Unset, str]):
        nullable (Union[Unset, bool]):
    """

    name: str
    datatype: str
    primary_key: Union[Unset, bool] = UNSET
    default_value: Union[Unset, str] = UNSET
    nullable: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        datatype = self.datatype
        primary_key = self.primary_key
        default_value = self.default_value
        nullable = self.nullable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "datatype": datatype,
            }
        )
        if primary_key is not UNSET:
            field_dict["primary_key"] = primary_key
        if default_value is not UNSET:
            field_dict["default_value"] = default_value
        if nullable is not UNSET:
            field_dict["nullable"] = nullable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        datatype = d.pop("datatype")

        primary_key = d.pop("primary_key", UNSET)

        default_value = d.pop("default_value", UNSET)

        nullable = d.pop("nullable", UNSET)

        get_datatable_full_schema_response_200_additional_property_additional_property_columns_item = cls(
            name=name,
            datatype=datatype,
            primary_key=primary_key,
            default_value=default_value,
            nullable=nullable,
        )

        get_datatable_full_schema_response_200_additional_property_additional_property_columns_item.additional_properties = (
            d
        )
        return get_datatable_full_schema_response_200_additional_property_additional_property_columns_item

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
