from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListDataMetricsResponse200NextCursor")


@_attrs_define
class ListDataMetricsResponse200NextCursor:
    """Present when more rows may follow: pass its fields back as the `cursor_*` params. Absent means the catalog is
    exhausted.

        Attributes:
            table_path (str):
            kind (str):
            name (str):
            script_path (str):
    """

    table_path: str
    kind: str
    name: str
    script_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        table_path = self.table_path
        kind = self.kind
        name = self.name
        script_path = self.script_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "table_path": table_path,
                "kind": kind,
                "name": name,
                "script_path": script_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        table_path = d.pop("table_path")

        kind = d.pop("kind")

        name = d.pop("name")

        script_path = d.pop("script_path")

        list_data_metrics_response_200_next_cursor = cls(
            table_path=table_path,
            kind=kind,
            name=name,
            script_path=script_path,
        )

        list_data_metrics_response_200_next_cursor.additional_properties = d
        return list_data_metrics_response_200_next_cursor

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
