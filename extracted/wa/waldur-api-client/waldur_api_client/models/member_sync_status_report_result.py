from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MemberSyncStatusReportResult")


@_attrs_define
class MemberSyncStatusReportResult:
    """
    Attributes:
        stored (int):
        skipped (list[str]):
    """

    stored: int
    skipped: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stored = self.stored

        skipped = self.skipped

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stored": stored,
                "skipped": skipped,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stored = d.pop("stored")

        skipped = cast(list[str], d.pop("skipped"))

        member_sync_status_report_result = cls(
            stored=stored,
            skipped=skipped,
        )

        member_sync_status_report_result.additional_properties = d
        return member_sync_status_report_result

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
