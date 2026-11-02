from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar(
    "T", bound="GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItemColumnsItem"
)


@_attrs_define
class GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItemColumnsItem:
    """
    Attributes:
        source_column (Union[Unset, str]):
        target_column (Union[Unset, str]):
    """

    source_column: Union[Unset, str] = UNSET
    target_column: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source_column = self.source_column
        target_column = self.target_column

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if source_column is not UNSET:
            field_dict["source_column"] = source_column
        if target_column is not UNSET:
            field_dict["target_column"] = target_column

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source_column = d.pop("source_column", UNSET)

        target_column = d.pop("target_column", UNSET)

        get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item_columns_item = cls(
            source_column=source_column,
            target_column=target_column,
        )

        get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item_columns_item.additional_properties = (
            d
        )
        return get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item_columns_item

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
