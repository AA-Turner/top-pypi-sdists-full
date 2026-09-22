from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

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
        instance (bool): on the instance database, the only kind that can be under roles or have its access edited
        permissioned (bool):
        usable_roles (List[str]): the roles the caller may connect as, by name; empty when not under roles
        default_role (str):
        can_create_schema (bool): whether the role the listing connected as may create schemas
        creatable_schemas (List[str]): the schemas the role the listing connected as may create in
        error (Union[Unset, str]):
    """

    datatable_name: str
    schemas: "DataTableTablesSchemas"
    instance: bool
    permissioned: bool
    usable_roles: List[str]
    default_role: str
    can_create_schema: bool
    creatable_schemas: List[str]
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datatable_name = self.datatable_name
        schemas = self.schemas.to_dict()

        instance = self.instance
        permissioned = self.permissioned
        usable_roles = self.usable_roles

        default_role = self.default_role
        can_create_schema = self.can_create_schema
        creatable_schemas = self.creatable_schemas

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datatable_name": datatable_name,
                "schemas": schemas,
                "instance": instance,
                "permissioned": permissioned,
                "usable_roles": usable_roles,
                "default_role": default_role,
                "can_create_schema": can_create_schema,
                "creatable_schemas": creatable_schemas,
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

        instance = d.pop("instance")

        permissioned = d.pop("permissioned")

        usable_roles = cast(List[str], d.pop("usable_roles"))

        default_role = d.pop("default_role")

        can_create_schema = d.pop("can_create_schema")

        creatable_schemas = cast(List[str], d.pop("creatable_schemas"))

        error = d.pop("error", UNSET)

        data_table_tables = cls(
            datatable_name=datatable_name,
            schemas=schemas,
            instance=instance,
            permissioned=permissioned,
            usable_roles=usable_roles,
            default_role=default_role,
            can_create_schema=can_create_schema,
            creatable_schemas=creatable_schemas,
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
