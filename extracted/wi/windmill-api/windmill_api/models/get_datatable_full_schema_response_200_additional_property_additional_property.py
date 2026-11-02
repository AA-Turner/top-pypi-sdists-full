from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_datatable_full_schema_response_200_additional_property_additional_property_columns_item import (
        GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyColumnsItem,
    )
    from ..models.get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item import (
        GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItem,
    )


T = TypeVar("T", bound="GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalProperty")


@_attrs_define
class GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalProperty:
    """
    Attributes:
        name (str):
        columns (List['GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyColumnsItem']):
        foreign_keys (List['GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItem']):
        pk_constraint_name (Union[Unset, str]):
    """

    name: str
    columns: List["GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyColumnsItem"]
    foreign_keys: List["GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItem"]
    pk_constraint_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        columns = []
        for columns_item_data in self.columns:
            columns_item = columns_item_data.to_dict()

            columns.append(columns_item)

        foreign_keys = []
        for foreign_keys_item_data in self.foreign_keys:
            foreign_keys_item = foreign_keys_item_data.to_dict()

            foreign_keys.append(foreign_keys_item)

        pk_constraint_name = self.pk_constraint_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "columns": columns,
                "foreign_keys": foreign_keys,
            }
        )
        if pk_constraint_name is not UNSET:
            field_dict["pk_constraint_name"] = pk_constraint_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_datatable_full_schema_response_200_additional_property_additional_property_columns_item import (
            GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyColumnsItem,
        )
        from ..models.get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item import (
            GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItem,
        )

        d = src_dict.copy()
        name = d.pop("name")

        columns = []
        _columns = d.pop("columns")
        for columns_item_data in _columns:
            columns_item = GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyColumnsItem.from_dict(
                columns_item_data
            )

            columns.append(columns_item)

        foreign_keys = []
        _foreign_keys = d.pop("foreign_keys")
        for foreign_keys_item_data in _foreign_keys:
            foreign_keys_item = (
                GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItem.from_dict(
                    foreign_keys_item_data
                )
            )

            foreign_keys.append(foreign_keys_item)

        pk_constraint_name = d.pop("pk_constraint_name", UNSET)

        get_datatable_full_schema_response_200_additional_property_additional_property = cls(
            name=name,
            columns=columns,
            foreign_keys=foreign_keys,
            pk_constraint_name=pk_constraint_name,
        )

        get_datatable_full_schema_response_200_additional_property_additional_property.additional_properties = d
        return get_datatable_full_schema_response_200_additional_property_additional_property

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
