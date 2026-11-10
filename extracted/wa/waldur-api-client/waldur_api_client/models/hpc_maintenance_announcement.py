from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcMaintenanceAnnouncement")


@_attrs_define
class HpcMaintenanceAnnouncement:
    """
    Attributes:
        uuid (UUID):
        name (str):
        message (str):
        state (str):
        impact (str):
        outage (bool):
        impact_description (str):
        start (int):
        end (int):
        partitions (list[str]):
        expected_reservation (str): Reservation the site agent creates for it, when sync is enabled.
        reservation_in_place (Union[None, bool]): Whether the cluster holds it; null when no reservation is due.
    """

    uuid: UUID
    name: str
    message: str
    state: str
    impact: str
    outage: bool
    impact_description: str
    start: int
    end: int
    partitions: list[str]
    expected_reservation: str
    reservation_in_place: Union[None, bool]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        message = self.message

        state = self.state

        impact = self.impact

        outage = self.outage

        impact_description = self.impact_description

        start = self.start

        end = self.end

        partitions = self.partitions

        expected_reservation = self.expected_reservation

        reservation_in_place: Union[None, bool]
        reservation_in_place = self.reservation_in_place

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "message": message,
                "state": state,
                "impact": impact,
                "outage": outage,
                "impact_description": impact_description,
                "start": start,
                "end": end,
                "partitions": partitions,
                "expected_reservation": expected_reservation,
                "reservation_in_place": reservation_in_place,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        message = d.pop("message")

        state = d.pop("state")

        impact = d.pop("impact")

        outage = d.pop("outage")

        impact_description = d.pop("impact_description")

        start = d.pop("start")

        end = d.pop("end")

        partitions = cast(list[str], d.pop("partitions"))

        expected_reservation = d.pop("expected_reservation")

        def _parse_reservation_in_place(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        reservation_in_place = _parse_reservation_in_place(d.pop("reservation_in_place"))

        hpc_maintenance_announcement = cls(
            uuid=uuid,
            name=name,
            message=message,
            state=state,
            impact=impact,
            outage=outage,
            impact_description=impact_description,
            start=start,
            end=end,
            partitions=partitions,
            expected_reservation=expected_reservation,
            reservation_in_place=reservation_in_place,
        )

        hpc_maintenance_announcement.additional_properties = d
        return hpc_maintenance_announcement

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
