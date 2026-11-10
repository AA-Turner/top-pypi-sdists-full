import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="MaintenanceReservation")


@_attrs_define
class MaintenanceReservation:
    """
    Attributes:
        name (str): Slurm reservation name to use.
        maintenance_uuid (UUID):
        maintenance_name (str):
        state (str):
        impact_level (str):
        start (datetime.datetime):
        end (datetime.datetime):
        partitions (list[str]): Partitions to reserve; empty means all nodes.
        flags (list[str]):
    """

    name: str
    maintenance_uuid: UUID
    maintenance_name: str
    state: str
    impact_level: str
    start: datetime.datetime
    end: datetime.datetime
    partitions: list[str]
    flags: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        maintenance_uuid = str(self.maintenance_uuid)

        maintenance_name = self.maintenance_name

        state = self.state

        impact_level = self.impact_level

        start = self.start.isoformat()

        end = self.end.isoformat()

        partitions = self.partitions

        flags = self.flags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "maintenance_uuid": maintenance_uuid,
                "maintenance_name": maintenance_name,
                "state": state,
                "impact_level": impact_level,
                "start": start,
                "end": end,
                "partitions": partitions,
                "flags": flags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        maintenance_uuid = UUID(d.pop("maintenance_uuid"))

        maintenance_name = d.pop("maintenance_name")

        state = d.pop("state")

        impact_level = d.pop("impact_level")

        start = isoparse(d.pop("start"))

        end = isoparse(d.pop("end"))

        partitions = cast(list[str], d.pop("partitions"))

        flags = cast(list[str], d.pop("flags"))

        maintenance_reservation = cls(
            name=name,
            maintenance_uuid=maintenance_uuid,
            maintenance_name=maintenance_name,
            state=state,
            impact_level=impact_level,
            start=start,
            end=end,
            partitions=partitions,
            flags=flags,
        )

        maintenance_reservation.additional_properties = d
        return maintenance_reservation

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
