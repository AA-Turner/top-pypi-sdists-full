from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PublishMigrationBody")


@_attrs_define
class PublishMigrationBody:
    """one best-effort data table migration attached to a project (per data table)

    Attributes:
        datatable_name (str):
        sql (str):
        enabled (bool):
        sql_down (Union[Unset, str]): defaults to an empty string when omitted
    """

    datatable_name: str
    sql: str
    enabled: bool
    sql_down: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datatable_name = self.datatable_name
        sql = self.sql
        enabled = self.enabled
        sql_down = self.sql_down

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datatable_name": datatable_name,
                "sql": sql,
                "enabled": enabled,
            }
        )
        if sql_down is not UNSET:
            field_dict["sql_down"] = sql_down

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        datatable_name = d.pop("datatable_name")

        sql = d.pop("sql")

        enabled = d.pop("enabled")

        sql_down = d.pop("sql_down", UNSET)

        publish_migration_body = cls(
            datatable_name=datatable_name,
            sql=sql,
            enabled=enabled,
            sql_down=sql_down,
        )

        publish_migration_body.additional_properties = d
        return publish_migration_body

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
