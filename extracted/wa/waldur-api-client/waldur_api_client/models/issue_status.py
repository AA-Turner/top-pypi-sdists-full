from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.issue_status_type import IssueStatusType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueStatus")


@_attrs_define
class IssueStatus:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str): Status name in Jira.
        type_display (str):
        type_ (Union[Unset, IssueStatusType]):
    """

    url: str
    uuid: UUID
    name: str
    type_display: str
    type_: Union[Unset, IssueStatusType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        type_display = self.type_display

        type_: Union[Unset, int] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "type_display": type_display,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        type_display = d.pop("type_display")

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, IssueStatusType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = IssueStatusType(_type_)

        issue_status = cls(
            url=url,
            uuid=uuid,
            name=name,
            type_display=type_display,
            type_=type_,
        )

        issue_status.additional_properties = d
        return issue_status

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
