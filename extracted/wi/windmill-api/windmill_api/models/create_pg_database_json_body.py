from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreatePgDatabaseJsonBody")


@_attrs_define
class CreatePgDatabaseJsonBody:
    """
    Attributes:
        source (str): Datatable source to determine connection info: 'datatable://name' or '$res:path'
        target_dbname (str): Name for the new database
    """

    source: str
    target_dbname: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source = self.source
        target_dbname = self.target_dbname

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "target_dbname": target_dbname,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source = d.pop("source")

        target_dbname = d.pop("target_dbname")

        create_pg_database_json_body = cls(
            source=source,
            target_dbname=target_dbname,
        )

        create_pg_database_json_body.additional_properties = d
        return create_pg_database_json_body

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
