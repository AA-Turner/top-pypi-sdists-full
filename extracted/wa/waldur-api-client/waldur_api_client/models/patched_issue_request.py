from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedIssueRequest")


@_attrs_define
class PatchedIssueRequest:
    """
    Attributes:
        summary (Union[Unset, str]):
        description (Union[Unset, str]):
        assignee (Union[None, Unset, str]):
        offering (Union[None, UUID, Unset]):
        is_reported_manually (Union[Unset, bool]): Set true if issue is created by regular user via portal. Default:
            False.
    """

    summary: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    assignee: Union[None, Unset, str] = UNSET
    offering: Union[None, UUID, Unset] = UNSET
    is_reported_manually: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summary = self.summary

        description = self.description

        assignee: Union[None, Unset, str]
        if isinstance(self.assignee, Unset):
            assignee = UNSET
        else:
            assignee = self.assignee

        offering: Union[None, Unset, str]
        if isinstance(self.offering, Unset):
            offering = UNSET
        elif isinstance(self.offering, UUID):
            offering = str(self.offering)
        else:
            offering = self.offering

        is_reported_manually = self.is_reported_manually

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if summary is not UNSET:
            field_dict["summary"] = summary
        if description is not UNSET:
            field_dict["description"] = description
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if offering is not UNSET:
            field_dict["offering"] = offering
        if is_reported_manually is not UNSET:
            field_dict["is_reported_manually"] = is_reported_manually

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        def _parse_assignee(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        assignee = _parse_assignee(d.pop("assignee", UNSET))

        def _parse_offering(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                offering_type_0 = UUID(data)

                return offering_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        offering = _parse_offering(d.pop("offering", UNSET))

        is_reported_manually = d.pop("is_reported_manually", UNSET)

        patched_issue_request = cls(
            summary=summary,
            description=description,
            assignee=assignee,
            offering=offering,
            is_reported_manually=is_reported_manually,
        )

        patched_issue_request.additional_properties = d
        return patched_issue_request

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
