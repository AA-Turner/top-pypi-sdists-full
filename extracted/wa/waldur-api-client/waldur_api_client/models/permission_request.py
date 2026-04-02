import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionRequest")


@_attrs_define
class PermissionRequest:
    """
    Attributes:
        url (str):
        uuid (UUID):
        invitation (str):
        state (str):
        created (datetime.datetime):
        created_by_full_name (str):
        created_by_username (str):
        created_by_email (str):
        reviewed_by_full_name (str):
        reviewed_by_username (str):
        reviewed_at (Union[None, datetime.datetime]): Timestamp when the review was completed
        scope_uuid (UUID):
        scope_name (str):
        customer_uuid (UUID):
        customer_name (str):
        role_name (str):
        role_description (str):
        project_name_template (str):
        review_comment (Union[None, Unset, str]): Optional comment provided during review
    """

    url: str
    uuid: UUID
    invitation: str
    state: str
    created: datetime.datetime
    created_by_full_name: str
    created_by_username: str
    created_by_email: str
    reviewed_by_full_name: str
    reviewed_by_username: str
    reviewed_at: Union[None, datetime.datetime]
    scope_uuid: UUID
    scope_name: str
    customer_uuid: UUID
    customer_name: str
    role_name: str
    role_description: str
    project_name_template: str
    review_comment: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        invitation = self.invitation

        state = self.state

        created = self.created.isoformat()

        created_by_full_name = self.created_by_full_name

        created_by_username = self.created_by_username

        created_by_email = self.created_by_email

        reviewed_by_full_name = self.reviewed_by_full_name

        reviewed_by_username = self.reviewed_by_username

        reviewed_at: Union[None, str]
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        scope_uuid = str(self.scope_uuid)

        scope_name = self.scope_name

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        role_name = self.role_name

        role_description = self.role_description

        project_name_template = self.project_name_template

        review_comment: Union[None, Unset, str]
        if isinstance(self.review_comment, Unset):
            review_comment = UNSET
        else:
            review_comment = self.review_comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "invitation": invitation,
                "state": state,
                "created": created,
                "created_by_full_name": created_by_full_name,
                "created_by_username": created_by_username,
                "created_by_email": created_by_email,
                "reviewed_by_full_name": reviewed_by_full_name,
                "reviewed_by_username": reviewed_by_username,
                "reviewed_at": reviewed_at,
                "scope_uuid": scope_uuid,
                "scope_name": scope_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "role_name": role_name,
                "role_description": role_description,
                "project_name_template": project_name_template,
            }
        )
        if review_comment is not UNSET:
            field_dict["review_comment"] = review_comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        invitation = d.pop("invitation")

        state = d.pop("state")

        created = isoparse(d.pop("created"))

        created_by_full_name = d.pop("created_by_full_name")

        created_by_username = d.pop("created_by_username")

        created_by_email = d.pop("created_by_email")

        reviewed_by_full_name = d.pop("reviewed_by_full_name")

        reviewed_by_username = d.pop("reviewed_by_username")

        def _parse_reviewed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = isoparse(data)

                return reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewed_at"))

        scope_uuid = UUID(d.pop("scope_uuid"))

        scope_name = d.pop("scope_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        role_name = d.pop("role_name")

        role_description = d.pop("role_description")

        project_name_template = d.pop("project_name_template")

        def _parse_review_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        review_comment = _parse_review_comment(d.pop("review_comment", UNSET))

        permission_request = cls(
            url=url,
            uuid=uuid,
            invitation=invitation,
            state=state,
            created=created,
            created_by_full_name=created_by_full_name,
            created_by_username=created_by_username,
            created_by_email=created_by_email,
            reviewed_by_full_name=reviewed_by_full_name,
            reviewed_by_username=reviewed_by_username,
            reviewed_at=reviewed_at,
            scope_uuid=scope_uuid,
            scope_name=scope_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            role_name=role_name,
            role_description=role_description,
            project_name_template=project_name_template,
            review_comment=review_comment,
        )

        permission_request.additional_properties = d
        return permission_request

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
