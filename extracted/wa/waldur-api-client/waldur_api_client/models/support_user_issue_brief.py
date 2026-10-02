import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SupportUserIssueBrief")


@_attrs_define
class SupportUserIssueBrief:
    """
    Attributes:
        uuid (UUID):
        type_ (str):
        summary (str):
        status (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        key (Union[Unset, str]):
    """

    uuid: UUID
    type_: str
    summary: str
    status: str
    created: datetime.datetime
    modified: datetime.datetime
    key: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        type_ = self.type_

        summary = self.summary

        status = self.status

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        key = self.key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "type": type_,
                "summary": summary,
                "status": status,
                "created": created,
                "modified": modified,
            }
        )
        if key is not UNSET:
            field_dict["key"] = key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        type_ = d.pop("type")

        summary = d.pop("summary")

        status = d.pop("status")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        key = d.pop("key", UNSET)

        support_user_issue_brief = cls(
            uuid=uuid,
            type_=type_,
            summary=summary,
            status=status,
            created=created,
            modified=modified,
            key=key,
        )

        support_user_issue_brief.additional_properties = d
        return support_user_issue_brief

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
