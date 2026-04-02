import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Comment")


@_attrs_define
class Comment:
    """
    Attributes:
        url (str):
        uuid (UUID):
        issue (str):
        issue_key (str):
        description (str):
        author_name (str):
        author_uuid (UUID):
        author_user (str):
        author_email (str):
        backend_id (Union[None, str]):
        created (datetime.datetime):
        update_is_available (bool):
        destroy_is_available (bool):
        is_public (Union[Unset, bool]):
        remote_id (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    issue: str
    issue_key: str
    description: str
    author_name: str
    author_uuid: UUID
    author_user: str
    author_email: str
    backend_id: Union[None, str]
    created: datetime.datetime
    update_is_available: bool
    destroy_is_available: bool
    is_public: Union[Unset, bool] = UNSET
    remote_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        issue = self.issue

        issue_key = self.issue_key

        description = self.description

        author_name = self.author_name

        author_uuid = str(self.author_uuid)

        author_user = self.author_user

        author_email = self.author_email

        backend_id: Union[None, str]
        backend_id = self.backend_id

        created = self.created.isoformat()

        update_is_available = self.update_is_available

        destroy_is_available = self.destroy_is_available

        is_public = self.is_public

        remote_id: Union[None, Unset, str]
        if isinstance(self.remote_id, Unset):
            remote_id = UNSET
        else:
            remote_id = self.remote_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "issue": issue,
                "issue_key": issue_key,
                "description": description,
                "author_name": author_name,
                "author_uuid": author_uuid,
                "author_user": author_user,
                "author_email": author_email,
                "backend_id": backend_id,
                "created": created,
                "update_is_available": update_is_available,
                "destroy_is_available": destroy_is_available,
            }
        )
        if is_public is not UNSET:
            field_dict["is_public"] = is_public
        if remote_id is not UNSET:
            field_dict["remote_id"] = remote_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        issue = d.pop("issue")

        issue_key = d.pop("issue_key")

        description = d.pop("description")

        author_name = d.pop("author_name")

        author_uuid = UUID(d.pop("author_uuid"))

        author_user = d.pop("author_user")

        author_email = d.pop("author_email")

        def _parse_backend_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id"))

        created = isoparse(d.pop("created"))

        update_is_available = d.pop("update_is_available")

        destroy_is_available = d.pop("destroy_is_available")

        is_public = d.pop("is_public", UNSET)

        def _parse_remote_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        remote_id = _parse_remote_id(d.pop("remote_id", UNSET))

        comment = cls(
            url=url,
            uuid=uuid,
            issue=issue,
            issue_key=issue_key,
            description=description,
            author_name=author_name,
            author_uuid=author_uuid,
            author_user=author_user,
            author_email=author_email,
            backend_id=backend_id,
            created=created,
            update_is_available=update_is_available,
            destroy_is_available=destroy_is_available,
            is_public=is_public,
            remote_id=remote_id,
        )

        comment.additional_properties = d
        return comment

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
