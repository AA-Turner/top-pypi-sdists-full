from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.changelog_release_summary_status_enum import ChangelogReleaseSummaryStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangelogReleaseSummary")


@_attrs_define
class ChangelogReleaseSummary:
    """
    Attributes:
        version (str):
        type_ (str):
        status (ChangelogReleaseSummaryStatusEnum):
        date (Union[Unset, str]):
        has_breaking (Union[Unset, bool]):
        has_security (Union[Unset, bool]):
        max_security_urgency (Union[None, Unset, str]):
    """

    version: str
    type_: str
    status: ChangelogReleaseSummaryStatusEnum
    date: Union[Unset, str] = UNSET
    has_breaking: Union[Unset, bool] = UNSET
    has_security: Union[Unset, bool] = UNSET
    max_security_urgency: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        type_ = self.type_

        status = self.status.value

        date = self.date

        has_breaking = self.has_breaking

        has_security = self.has_security

        max_security_urgency: Union[None, Unset, str]
        if isinstance(self.max_security_urgency, Unset):
            max_security_urgency = UNSET
        else:
            max_security_urgency = self.max_security_urgency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "type": type_,
                "status": status,
            }
        )
        if date is not UNSET:
            field_dict["date"] = date
        if has_breaking is not UNSET:
            field_dict["has_breaking"] = has_breaking
        if has_security is not UNSET:
            field_dict["has_security"] = has_security
        if max_security_urgency is not UNSET:
            field_dict["max_security_urgency"] = max_security_urgency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        version = d.pop("version")

        type_ = d.pop("type")

        status = ChangelogReleaseSummaryStatusEnum(d.pop("status"))

        date = d.pop("date", UNSET)

        has_breaking = d.pop("has_breaking", UNSET)

        has_security = d.pop("has_security", UNSET)

        def _parse_max_security_urgency(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_security_urgency = _parse_max_security_urgency(d.pop("max_security_urgency", UNSET))

        changelog_release_summary = cls(
            version=version,
            type_=type_,
            status=status,
            date=date,
            has_breaking=has_breaking,
            has_security=has_security,
            max_security_urgency=max_security_urgency,
        )

        changelog_release_summary.additional_properties = d
        return changelog_release_summary

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
