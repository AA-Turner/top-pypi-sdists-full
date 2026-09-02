from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_table_tables_schemas import DataTableTablesSchemas


T = TypeVar("T", bound="DataTableTables")


@_attrs_define
class DataTableTables:
    """
    Attributes:
        datatable_name (str):
        schemas (DataTableTablesSchemas): Hierarchical metadata: schema_name -> table_names
        error (Union[Unset, str]):
    """

    datatable_name: str
    schemas: "DataTableTablesSchemas"
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datatable_name = self.datatable_name
        schemas = self.schemas.to_dict()

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datatable_name": datatable_name,
                "schemas": schemas,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_table_tables_schemas import DataTableTablesSchemas

        d = src_dict.copy()
        datatable_name = d.pop("datatable_name")

        schemas = DataTableTablesSchemas.from_dict(d.pop("schemas"))

        error = d.pop("error", UNSET)

        data_table_tables = cls(
            datatable_name=datatable_name,
            schemas=schemas,
            error=error,
        )

        data_table_tables.additional_properties = d
        return data_table_tables

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
