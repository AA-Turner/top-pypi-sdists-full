from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.role_hygiene_finding import RoleHygieneFinding


T = TypeVar("T", bound="RoleHygieneReport")


@_attrs_define
class RoleHygieneReport:
    """
    Attributes:
        roles_checked (int):
        roles_with_findings (int):
        error_count (int):
        warning_count (int):
        info_count (int):
        findings (list['RoleHygieneFinding']):
    """

    roles_checked: int
    roles_with_findings: int
    error_count: int
    warning_count: int
    info_count: int
    findings: list["RoleHygieneFinding"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        roles_checked = self.roles_checked

        roles_with_findings = self.roles_with_findings

        error_count = self.error_count

        warning_count = self.warning_count

        info_count = self.info_count

        findings = []
        for findings_item_data in self.findings:
            findings_item = findings_item_data.to_dict()
            findings.append(findings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "roles_checked": roles_checked,
                "roles_with_findings": roles_with_findings,
                "error_count": error_count,
                "warning_count": warning_count,
                "info_count": info_count,
                "findings": findings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.role_hygiene_finding import RoleHygieneFinding

        d = dict(src_dict)
        roles_checked = d.pop("roles_checked")

        roles_with_findings = d.pop("roles_with_findings")

        error_count = d.pop("error_count")

        warning_count = d.pop("warning_count")

        info_count = d.pop("info_count")

        findings = []
        _findings = d.pop("findings")
        for findings_item_data in _findings:
            findings_item = RoleHygieneFinding.from_dict(findings_item_data)

            findings.append(findings_item)

        role_hygiene_report = cls(
            roles_checked=roles_checked,
            roles_with_findings=roles_with_findings,
            error_count=error_count,
            warning_count=warning_count,
            info_count=info_count,
            findings=findings,
        )

        role_hygiene_report.additional_properties = d
        return role_hygiene_report

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
