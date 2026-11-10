from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MaintenanceReservationImportResult")


@_attrs_define
class MaintenanceReservationImportResult:
    """
    Attributes:
        created (list[str]):
        updated (list[str]):
        unchanged (list[str]):
        skipped (list[str]):
    """

    created: list[str]
    updated: list[str]
    unchanged: list[str]
    skipped: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created

        updated = self.updated

        unchanged = self.unchanged

        skipped = self.skipped

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "updated": updated,
                "unchanged": unchanged,
                "skipped": skipped,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created = cast(list[str], d.pop("created"))

        updated = cast(list[str], d.pop("updated"))

        unchanged = cast(list[str], d.pop("unchanged"))

        skipped = cast(list[str], d.pop("skipped"))

        maintenance_reservation_import_result = cls(
            created=created,
            updated=updated,
            unchanged=unchanged,
            skipped=skipped,
        )

        maintenance_reservation_import_result.additional_properties = d
        return maintenance_reservation_import_result

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
