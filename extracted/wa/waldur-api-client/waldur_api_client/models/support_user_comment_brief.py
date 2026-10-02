import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SupportUserCommentBrief")


@_attrs_define
class SupportUserCommentBrief:
    """
    Attributes:
        uuid (UUID):
        description (str):
        created (datetime.datetime):
        issue_key (str):
        issue_uuid (UUID):
        is_public (Union[Unset, bool]):
    """

    uuid: UUID
    description: str
    created: datetime.datetime
    issue_key: str
    issue_uuid: UUID
    is_public: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        description = self.description

        created = self.created.isoformat()

        issue_key = self.issue_key

        issue_uuid = str(self.issue_uuid)

        is_public = self.is_public

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "description": description,
                "created": created,
                "issue_key": issue_key,
                "issue_uuid": issue_uuid,
            }
        )
        if is_public is not UNSET:
            field_dict["is_public"] = is_public

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        description = d.pop("description")

        created = isoparse(d.pop("created"))

        issue_key = d.pop("issue_key")

        issue_uuid = UUID(d.pop("issue_uuid"))

        is_public = d.pop("is_public", UNSET)

        support_user_comment_brief = cls(
            uuid=uuid,
            description=description,
            created=created,
            issue_key=issue_key,
            issue_uuid=issue_uuid,
            is_public=is_public,
        )

        support_user_comment_brief.additional_properties = d
        return support_user_comment_brief

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
