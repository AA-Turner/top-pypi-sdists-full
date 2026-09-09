from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dbt_column_lineage_edges_item import DbtColumnLineageEdgesItem


T = TypeVar("T", bound="DbtColumnLineage")


@_attrs_define
class DbtColumnLineage:
    """The direct column-to-column lineage the asked-for relations' columns sit in — the connected component around them —
    in the terms the canvas draws: relations and columns, never dbt's node ids.

        Attributes:
            edges (List['DbtColumnLineageEdgesItem']):
            truncated (bool): The component reaches further than `edges`, which holds the part nearest the asked-for
                relations. A trace that stops short is otherwise indistinguishable from one that ends.
    """

    edges: List["DbtColumnLineageEdgesItem"]
    truncated: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        edges = []
        for edges_item_data in self.edges:
            edges_item = edges_item_data.to_dict()

            edges.append(edges_item)

        truncated = self.truncated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "edges": edges,
                "truncated": truncated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dbt_column_lineage_edges_item import DbtColumnLineageEdgesItem

        d = src_dict.copy()
        edges = []
        _edges = d.pop("edges")
        for edges_item_data in _edges:
            edges_item = DbtColumnLineageEdgesItem.from_dict(edges_item_data)

            edges.append(edges_item)

        truncated = d.pop("truncated")

        dbt_column_lineage = cls(
            edges=edges,
            truncated=truncated,
        )

        dbt_column_lineage.additional_properties = d
        return dbt_column_lineage

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
