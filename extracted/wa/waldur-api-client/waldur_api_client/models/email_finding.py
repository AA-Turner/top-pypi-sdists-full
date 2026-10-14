from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EmailFinding")


@_attrs_define
class EmailFinding:
    """
    Attributes:
        level (str): OK, WARNING or ERROR
        code (str): Stable machine-readable id
        title (str): Short summary
        detail (str): What was observed
        remediation (str): How to fix it
    """

    level: str
    code: str
    title: str
    detail: str
    remediation: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        level = self.level

        code = self.code

        title = self.title

        detail = self.detail

        remediation = self.remediation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "level": level,
                "code": code,
                "title": title,
                "detail": detail,
                "remediation": remediation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        level = d.pop("level")

        code = d.pop("code")

        title = d.pop("title")

        detail = d.pop("detail")

        remediation = d.pop("remediation")

        email_finding = cls(
            level=level,
            code=code,
            title=title,
            detail=detail,
            remediation=remediation,
        )

        email_finding.additional_properties = d
        return email_finding

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
