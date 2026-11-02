from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.data_table_table_schema_columns import DataTableTableSchemaColumns


T = TypeVar("T", bound="DataTableTableSchema")


@_attrs_define
class DataTableTableSchema:
    """
    Attributes:
        datatable_name (str):
        schema_name (str):
        table_name (str):
        columns (DataTableTableSchemaColumns): Columns in this table: column_name -> compact_type
    """

    datatable_name: str
    schema_name: str
    table_name: str
    columns: "DataTableTableSchemaColumns"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datatable_name = self.datatable_name
        schema_name = self.schema_name
        table_name = self.table_name
        columns = self.columns.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datatable_name": datatable_name,
                "schema_name": schema_name,
                "table_name": table_name,
                "columns": columns,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_table_table_schema_columns import DataTableTableSchemaColumns

        d = src_dict.copy()
        datatable_name = d.pop("datatable_name")

        schema_name = d.pop("schema_name")

        table_name = d.pop("table_name")

        columns = DataTableTableSchemaColumns.from_dict(d.pop("columns"))

        data_table_table_schema = cls(
            datatable_name=datatable_name,
            schema_name=schema_name,
            table_name=table_name,
            columns=columns,
        )

        data_table_table_schema.additional_properties = d
        return data_table_table_schema

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
