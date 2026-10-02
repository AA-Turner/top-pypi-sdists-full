from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentStatsOfferingCount")


@_attrs_define
class AgentStatsOfferingCount:
    """
    Attributes:
        offering_name (str):
        offering_uuid (UUID):
        count (int):
    """

    offering_name: str
    offering_uuid: UUID
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_name = self.offering_name

        offering_uuid = str(self.offering_uuid)

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering__name": offering_name,
                "offering__uuid": offering_uuid,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_name = d.pop("offering__name")

        offering_uuid = UUID(d.pop("offering__uuid"))

        count = d.pop("count")

        agent_stats_offering_count = cls(
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            count=count,
        )

        agent_stats_offering_count.additional_properties = d
        return agent_stats_offering_count

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
