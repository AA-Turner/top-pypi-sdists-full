from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.site_maintenance_reservation_request import SiteMaintenanceReservationRequest


T = TypeVar("T", bound="MaintenanceReservationImportRequest")


@_attrs_define
class MaintenanceReservationImportRequest:
    """
    Attributes:
        reservations (list['SiteMaintenanceReservationRequest']):
    """

    reservations: list["SiteMaintenanceReservationRequest"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reservations = []
        for reservations_item_data in self.reservations:
            reservations_item = reservations_item_data.to_dict()
            reservations.append(reservations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reservations": reservations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.site_maintenance_reservation_request import SiteMaintenanceReservationRequest

        d = dict(src_dict)
        reservations = []
        _reservations = d.pop("reservations")
        for reservations_item_data in _reservations:
            reservations_item = SiteMaintenanceReservationRequest.from_dict(reservations_item_data)

            reservations.append(reservations_item)

        maintenance_reservation_import_request = cls(
            reservations=reservations,
        )

        maintenance_reservation_import_request.additional_properties = d
        return maintenance_reservation_import_request

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
