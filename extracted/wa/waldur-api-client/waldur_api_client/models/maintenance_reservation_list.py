from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.maintenance_reservation import MaintenanceReservation


T = TypeVar("T", bound="MaintenanceReservationList")


@_attrs_define
class MaintenanceReservationList:
    """
    Attributes:
        enabled (bool): Maintenance sync is enabled for the offering.
        prefix (str): Reservations with this name prefix are Waldur's to manage.
        reservations (list['MaintenanceReservation']):
    """

    enabled: bool
    prefix: str
    reservations: list["MaintenanceReservation"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        prefix = self.prefix

        reservations = []
        for reservations_item_data in self.reservations:
            reservations_item = reservations_item_data.to_dict()
            reservations.append(reservations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "prefix": prefix,
                "reservations": reservations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.maintenance_reservation import MaintenanceReservation

        d = dict(src_dict)
        enabled = d.pop("enabled")

        prefix = d.pop("prefix")

        reservations = []
        _reservations = d.pop("reservations")
        for reservations_item_data in _reservations:
            reservations_item = MaintenanceReservation.from_dict(reservations_item_data)

            reservations.append(reservations_item)

        maintenance_reservation_list = cls(
            enabled=enabled,
            prefix=prefix,
            reservations=reservations,
        )

        maintenance_reservation_list.additional_properties = d
        return maintenance_reservation_list

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
