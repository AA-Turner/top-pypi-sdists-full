import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.keycloak_user_group_membership_state import KeycloakUserGroupMembershipState

T = TypeVar("T", bound="KeycloakUserGroupMembership")


@_attrs_define
class KeycloakUserGroupMembership:
    """
    Attributes:
        uuid (UUID):
        url (str):
        username (str): Keycloak user username
        email (str): User's email for notifications
        first_name (str):
        last_name (str):
        group (str):
        group_name (str):
        group_role (str):
        group_scope_type (str):
        group_scope_name (Union[None, str]): Get the name of the cluster or project
        state (KeycloakUserGroupMembershipState):
        created (datetime.datetime):
        modified (datetime.datetime):
        last_checked (datetime.datetime):
        error_message (str):
        error_traceback (str):
    """

    uuid: UUID
    url: str
    username: str
    email: str
    first_name: str
    last_name: str
    group: str
    group_name: str
    group_role: str
    group_scope_type: str
    group_scope_name: Union[None, str]
    state: KeycloakUserGroupMembershipState
    created: datetime.datetime
    modified: datetime.datetime
    last_checked: datetime.datetime
    error_message: str
    error_traceback: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        username = self.username

        email = self.email

        first_name = self.first_name

        last_name = self.last_name

        group = self.group

        group_name = self.group_name

        group_role = self.group_role

        group_scope_type = self.group_scope_type

        group_scope_name: Union[None, str]
        group_scope_name = self.group_scope_name

        state = self.state.value

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        last_checked = self.last_checked.isoformat()

        error_message = self.error_message

        error_traceback = self.error_traceback

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "group": group,
                "group_name": group_name,
                "group_role": group_role,
                "group_scope_type": group_scope_type,
                "group_scope_name": group_scope_name,
                "state": state,
                "created": created,
                "modified": modified,
                "last_checked": last_checked,
                "error_message": error_message,
                "error_traceback": error_traceback,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        username = d.pop("username")

        email = d.pop("email")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        group = d.pop("group")

        group_name = d.pop("group_name")

        group_role = d.pop("group_role")

        group_scope_type = d.pop("group_scope_type")

        def _parse_group_scope_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        group_scope_name = _parse_group_scope_name(d.pop("group_scope_name"))

        state = KeycloakUserGroupMembershipState(d.pop("state"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        last_checked = isoparse(d.pop("last_checked"))

        error_message = d.pop("error_message")

        error_traceback = d.pop("error_traceback")

        keycloak_user_group_membership = cls(
            uuid=uuid,
            url=url,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            group=group,
            group_name=group_name,
            group_role=group_role,
            group_scope_type=group_scope_type,
            group_scope_name=group_scope_name,
            state=state,
            created=created,
            modified=modified,
            last_checked=last_checked,
            error_message=error_message,
            error_traceback=error_traceback,
        )

        keycloak_user_group_membership.additional_properties = d
        return keycloak_user_group_membership

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
