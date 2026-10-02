from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.topology_edge_kind_enum import TopologyEdgeKindEnum

T = TypeVar("T", bound="TopologyEdge")


@_attrs_define
class TopologyEdge:
    """
    Attributes:
        source (str):
        target (str):
        kind (TopologyEdgeKindEnum):
    """

    source: str
    target: str
    kind: TopologyEdgeKindEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        target = self.target

        kind = self.kind.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "target": target,
                "kind": kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source")

        target = d.pop("target")

        kind = TopologyEdgeKindEnum(d.pop("kind"))

        topology_edge = cls(
            source=source,
            target=target,
            kind=kind,
        )

        topology_edge.additional_properties = d
        return topology_edge

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
