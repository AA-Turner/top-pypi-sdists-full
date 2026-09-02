from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.import_pg_database_json_body_fork_behavior import ImportPgDatabaseJsonBodyForkBehavior
from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportPgDatabaseJsonBody")


@_attrs_define
class ImportPgDatabaseJsonBody:
    """
    Attributes:
        source (str): Source database: 'datatable://name' or '$res:path'
        target (str): Target database: 'datatable://name' or '$res:path'
        fork_behavior (ImportPgDatabaseJsonBodyForkBehavior):
        target_dbname_override (Union[Unset, str]): Override the target database name
    """

    source: str
    target: str
    fork_behavior: ImportPgDatabaseJsonBodyForkBehavior
    target_dbname_override: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source = self.source
        target = self.target
        fork_behavior = self.fork_behavior.value

        target_dbname_override = self.target_dbname_override

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "target": target,
                "fork_behavior": fork_behavior,
            }
        )
        if target_dbname_override is not UNSET:
            field_dict["target_dbname_override"] = target_dbname_override

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source = d.pop("source")

        target = d.pop("target")

        fork_behavior = ImportPgDatabaseJsonBodyForkBehavior(d.pop("fork_behavior"))

        target_dbname_override = d.pop("target_dbname_override", UNSET)

        import_pg_database_json_body = cls(
            source=source,
            target=target,
            fork_behavior=fork_behavior,
            target_dbname_override=target_dbname_override,
        )

        import_pg_database_json_body.additional_properties = d
        return import_pg_database_json_body

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
