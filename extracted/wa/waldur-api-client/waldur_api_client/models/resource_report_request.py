from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.report_section_request import ReportSectionRequest


T = TypeVar("T", bound="ResourceReportRequest")


@_attrs_define
class ResourceReportRequest:
    """
    Attributes:
        report (list['ReportSectionRequest']):
    """

    report: list["ReportSectionRequest"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        report = []
        for report_item_data in self.report:
            report_item = report_item_data.to_dict()
            report.append(report_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "report": report,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.report_section_request import ReportSectionRequest

        d = dict(src_dict)
        report = []
        _report = d.pop("report")
        for report_item_data in _report:
            report_item = ReportSectionRequest.from_dict(report_item_data)

            report.append(report_item)

        resource_report_request = cls(
            report=report,
        )

        resource_report_request.additional_properties = d
        return resource_report_request

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
