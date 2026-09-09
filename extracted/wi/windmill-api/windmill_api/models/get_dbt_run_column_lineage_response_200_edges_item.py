from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetDbtRunColumnLineageResponse200EdgesItem")


@_attrs_define
class GetDbtRunColumnLineageResponse200EdgesItem:
    """
    Attributes:
        from_asset_path (str):
        from_column (str):
        to_asset_path (str):
        to_column (str):
        kind (str): dbt's own word for how the value travelled — `copy` (passthrough) or `mod` (transformed). Not an
            enum: the engine treats the set as open.
    """

    from_asset_path: str
    from_column: str
    to_asset_path: str
    to_column: str
    kind: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from_asset_path = self.from_asset_path
        from_column = self.from_column
        to_asset_path = self.to_asset_path
        to_column = self.to_column
        kind = self.kind

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from_asset_path": from_asset_path,
                "from_column": from_column,
                "to_asset_path": to_asset_path,
                "to_column": to_column,
                "kind": kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        from_asset_path = d.pop("from_asset_path")

        from_column = d.pop("from_column")

        to_asset_path = d.pop("to_asset_path")

        to_column = d.pop("to_column")

        kind = d.pop("kind")

        get_dbt_run_column_lineage_response_200_edges_item = cls(
            from_asset_path=from_asset_path,
            from_column=from_column,
            to_asset_path=to_asset_path,
            to_column=to_column,
            kind=kind,
        )

        get_dbt_run_column_lineage_response_200_edges_item.additional_properties = d
        return get_dbt_run_column_lineage_response_200_edges_item

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
