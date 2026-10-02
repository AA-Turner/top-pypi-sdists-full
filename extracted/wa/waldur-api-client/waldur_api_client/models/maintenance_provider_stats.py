from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MaintenanceProviderStats")


@_attrs_define
class MaintenanceProviderStats:
    """
    Attributes:
        uuid (str): Service provider UUID
        name (str): Service provider name
        total (int): Total maintenances
        active (int): Active maintenances
        scheduled (int): Scheduled maintenances
        completed (int): Completed maintenances
    """

    uuid: str
    name: str
    total: int
    active: int
    scheduled: int
    completed: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        total = self.total

        active = self.active

        scheduled = self.scheduled

        completed = self.completed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "total": total,
                "active": active,
                "scheduled": scheduled,
                "completed": completed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        total = d.pop("total")

        active = d.pop("active")

        scheduled = d.pop("scheduled")

        completed = d.pop("completed")

        maintenance_provider_stats = cls(
            uuid=uuid,
            name=name,
            total=total,
            active=active,
            scheduled=scheduled,
            completed=completed,
        )

        maintenance_provider_stats.additional_properties = d
        return maintenance_provider_stats

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
