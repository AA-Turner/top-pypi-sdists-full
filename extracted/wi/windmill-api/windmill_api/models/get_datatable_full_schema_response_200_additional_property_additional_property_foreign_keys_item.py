from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item_columns_item import (
        GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItemColumnsItem,
    )


T = TypeVar("T", bound="GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItem")


@_attrs_define
class GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItem:
    """
    Attributes:
        columns
            (List['GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItemColumnsItem']):
        on_delete (str):
        on_update (str):
        target_table (Union[Unset, str]):
        fk_constraint_name (Union[Unset, str]):
    """

    columns: List["GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItemColumnsItem"]
    on_delete: str
    on_update: str
    target_table: Union[Unset, str] = UNSET
    fk_constraint_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        columns = []
        for columns_item_data in self.columns:
            columns_item = columns_item_data.to_dict()

            columns.append(columns_item)

        on_delete = self.on_delete
        on_update = self.on_update
        target_table = self.target_table
        fk_constraint_name = self.fk_constraint_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "columns": columns,
                "on_delete": on_delete,
                "on_update": on_update,
            }
        )
        if target_table is not UNSET:
            field_dict["target_table"] = target_table
        if fk_constraint_name is not UNSET:
            field_dict["fk_constraint_name"] = fk_constraint_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item_columns_item import (
            GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItemColumnsItem,
        )

        d = src_dict.copy()
        columns = []
        _columns = d.pop("columns")
        for columns_item_data in _columns:
            columns_item = GetDatatableFullSchemaResponse200AdditionalPropertyAdditionalPropertyForeignKeysItemColumnsItem.from_dict(
                columns_item_data
            )

            columns.append(columns_item)

        on_delete = d.pop("on_delete")

        on_update = d.pop("on_update")

        target_table = d.pop("target_table", UNSET)

        fk_constraint_name = d.pop("fk_constraint_name", UNSET)

        get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item = cls(
            columns=columns,
            on_delete=on_delete,
            on_update=on_update,
            target_table=target_table,
            fk_constraint_name=fk_constraint_name,
        )

        get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item.additional_properties = (
            d
        )
        return get_datatable_full_schema_response_200_additional_property_additional_property_foreign_keys_item

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
