from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SendAllAssignmentBatchesResponse")


@_attrs_define
class SendAllAssignmentBatchesResponse:
    """
    Attributes:
        batches_sent (int):
        skipped (int):
    """

    batches_sent: int
    skipped: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        batches_sent = self.batches_sent

        skipped = self.skipped

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batches_sent": batches_sent,
                "skipped": skipped,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        batches_sent = d.pop("batches_sent")

        skipped = d.pop("skipped")

        send_all_assignment_batches_response = cls(
            batches_sent=batches_sent,
            skipped=skipped,
        )

        send_all_assignment_batches_response.additional_properties = d
        return send_all_assignment_batches_response

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
