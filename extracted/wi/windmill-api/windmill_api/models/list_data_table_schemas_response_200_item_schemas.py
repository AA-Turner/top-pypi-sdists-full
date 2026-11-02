from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_data_table_schemas_response_200_item_schemas_additional_property import (
        ListDataTableSchemasResponse200ItemSchemasAdditionalProperty,
    )


T = TypeVar("T", bound="ListDataTableSchemasResponse200ItemSchemas")


@_attrs_define
class ListDataTableSchemasResponse200ItemSchemas:
    """Hierarchical schema: schema_name -> table_name -> column_name -> compact_type (e.g. 'int4', 'text?', 'int4?=0')"""

    additional_properties: Dict[str, "ListDataTableSchemasResponse200ItemSchemasAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_data_table_schemas_response_200_item_schemas_additional_property import (
            ListDataTableSchemasResponse200ItemSchemasAdditionalProperty,
        )

        d = src_dict.copy()
        list_data_table_schemas_response_200_item_schemas = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ListDataTableSchemasResponse200ItemSchemasAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        list_data_table_schemas_response_200_item_schemas.additional_properties = additional_properties
        return list_data_table_schemas_response_200_item_schemas

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "ListDataTableSchemasResponse200ItemSchemasAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "ListDataTableSchemasResponse200ItemSchemasAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
