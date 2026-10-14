from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rejected_point import RejectedPoint


T = TypeVar("T", bound="MetricReportResult")


@_attrs_define
class MetricReportResult:
    """
    Attributes:
        accepted (int):
        rejected (list['RejectedPoint']):
    """

    accepted: int
    rejected: list["RejectedPoint"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accepted = self.accepted

        rejected = []
        for rejected_item_data in self.rejected:
            rejected_item = rejected_item_data.to_dict()
            rejected.append(rejected_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accepted": accepted,
                "rejected": rejected,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rejected_point import RejectedPoint

        d = dict(src_dict)
        accepted = d.pop("accepted")

        rejected = []
        _rejected = d.pop("rejected")
        for rejected_item_data in _rejected:
            rejected_item = RejectedPoint.from_dict(rejected_item_data)

            rejected.append(rejected_item)

        metric_report_result = cls(
            accepted=accepted,
            rejected=rejected,
        )

        metric_report_result.additional_properties = d
        return metric_report_result

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
