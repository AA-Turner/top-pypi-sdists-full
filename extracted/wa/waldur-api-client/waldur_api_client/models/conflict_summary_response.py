from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.conflict_summary_response_by_severity import ConflictSummaryResponseBySeverity
    from ..models.conflict_summary_response_by_status import ConflictSummaryResponseByStatus
    from ..models.conflict_summary_response_by_type import ConflictSummaryResponseByType


T = TypeVar("T", bound="ConflictSummaryResponse")


@_attrs_define
class ConflictSummaryResponse:
    """
    Attributes:
        total (int):
        by_status (ConflictSummaryResponseByStatus):
        by_severity (ConflictSummaryResponseBySeverity):
        by_type (ConflictSummaryResponseByType):
    """

    total: int
    by_status: "ConflictSummaryResponseByStatus"
    by_severity: "ConflictSummaryResponseBySeverity"
    by_type: "ConflictSummaryResponseByType"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        by_status = self.by_status.to_dict()

        by_severity = self.by_severity.to_dict()

        by_type = self.by_type.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "by_status": by_status,
                "by_severity": by_severity,
                "by_type": by_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conflict_summary_response_by_severity import ConflictSummaryResponseBySeverity
        from ..models.conflict_summary_response_by_status import ConflictSummaryResponseByStatus
        from ..models.conflict_summary_response_by_type import ConflictSummaryResponseByType

        d = dict(src_dict)
        total = d.pop("total")

        by_status = ConflictSummaryResponseByStatus.from_dict(d.pop("by_status"))

        by_severity = ConflictSummaryResponseBySeverity.from_dict(d.pop("by_severity"))

        by_type = ConflictSummaryResponseByType.from_dict(d.pop("by_type"))

        conflict_summary_response = cls(
            total=total,
            by_status=by_status,
            by_severity=by_severity,
            by_type=by_type,
        )

        conflict_summary_response.additional_properties = d
        return conflict_summary_response

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
