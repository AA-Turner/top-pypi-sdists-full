from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_stats_offering_count import AgentStatsOfferingCount


T = TypeVar("T", bound="AgentStatsIdentities")


@_attrs_define
class AgentStatsIdentities:
    """
    Attributes:
        total (int):
        by_offering (list['AgentStatsOfferingCount']):
    """

    total: int
    by_offering: list["AgentStatsOfferingCount"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        by_offering = []
        for by_offering_item_data in self.by_offering:
            by_offering_item = by_offering_item_data.to_dict()
            by_offering.append(by_offering_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "by_offering": by_offering,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_stats_offering_count import AgentStatsOfferingCount

        d = dict(src_dict)
        total = d.pop("total")

        by_offering = []
        _by_offering = d.pop("by_offering")
        for by_offering_item_data in _by_offering:
            by_offering_item = AgentStatsOfferingCount.from_dict(by_offering_item_data)

            by_offering.append(by_offering_item)

        agent_stats_identities = cls(
            total=total,
            by_offering=by_offering,
        )

        agent_stats_identities.additional_properties = d
        return agent_stats_identities

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
