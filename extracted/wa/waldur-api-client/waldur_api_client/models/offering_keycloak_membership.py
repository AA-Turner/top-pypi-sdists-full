import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.keycloak_user_group_membership_state import KeycloakUserGroupMembershipState
from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingKeycloakMembership")


@_attrs_define
class OfferingKeycloakMembership:
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
        group_role_name (str):
        group_offering_uuid (UUID):
        group_offering_name (str):
        group_resource_name (str):
        group_resource_uuid (UUID):
        group_scope_id (str): Sub-entity identifier within a resource, e.g. Rancher project ID within a cluster.
        group_role_scope_type (str): Level this role applies at, e.g. 'cluster', 'project'. Empty means offering-wide.
        group_role_scope_type_label (str): Human-readable label for scope_type shown to end users, e.g. 'Rancher
            Project', 'Cluster Namespace'. Falls back to capitalized scope_type if empty. Default: ''.
        state (KeycloakUserGroupMembershipState):
        created (datetime.datetime):
        modified (datetime.datetime):
        last_checked (datetime.datetime):
        error_message (str):
        error_traceback (str):
        user (Union[None, Unset, str]):
    """

    uuid: UUID
    url: str
    username: str
    email: str
    first_name: str
    last_name: str
    group: str
    group_name: str
    group_role_name: str
    group_offering_uuid: UUID
    group_offering_name: str
    group_resource_name: str
    group_resource_uuid: UUID
    group_scope_id: str
    group_role_scope_type: str
    state: KeycloakUserGroupMembershipState
    created: datetime.datetime
    modified: datetime.datetime
    last_checked: datetime.datetime
    error_message: str
    error_traceback: str
    group_role_scope_type_label: str = ""
    user: Union[None, Unset, str] = UNSET
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

        group_role_name = self.group_role_name

        group_offering_uuid = str(self.group_offering_uuid)

        group_offering_name = self.group_offering_name

        group_resource_name = self.group_resource_name

        group_resource_uuid = str(self.group_resource_uuid)

        group_scope_id = self.group_scope_id

        group_role_scope_type = self.group_role_scope_type

        group_role_scope_type_label = self.group_role_scope_type_label

        state = self.state.value

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        last_checked = self.last_checked.isoformat()

        error_message = self.error_message

        error_traceback = self.error_traceback

        user: Union[None, Unset, str]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

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
                "group_role_name": group_role_name,
                "group_offering_uuid": group_offering_uuid,
                "group_offering_name": group_offering_name,
                "group_resource_name": group_resource_name,
                "group_resource_uuid": group_resource_uuid,
                "group_scope_id": group_scope_id,
                "group_role_scope_type": group_role_scope_type,
                "group_role_scope_type_label": group_role_scope_type_label,
                "state": state,
                "created": created,
                "modified": modified,
                "last_checked": last_checked,
                "error_message": error_message,
                "error_traceback": error_traceback,
            }
        )
        if user is not UNSET:
            field_dict["user"] = user

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

        group_role_name = d.pop("group_role_name")

        group_offering_uuid = UUID(d.pop("group_offering_uuid"))

        group_offering_name = d.pop("group_offering_name")

        group_resource_name = d.pop("group_resource_name")

        group_resource_uuid = UUID(d.pop("group_resource_uuid"))

        group_scope_id = d.pop("group_scope_id")

        group_role_scope_type = d.pop("group_role_scope_type")

        group_role_scope_type_label = d.pop("group_role_scope_type_label")

        state = KeycloakUserGroupMembershipState(d.pop("state"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        last_checked = isoparse(d.pop("last_checked"))

        error_message = d.pop("error_message")

        error_traceback = d.pop("error_traceback")

        def _parse_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user = _parse_user(d.pop("user", UNSET))

        offering_keycloak_membership = cls(
            uuid=uuid,
            url=url,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            group=group,
            group_name=group_name,
            group_role_name=group_role_name,
            group_offering_uuid=group_offering_uuid,
            group_offering_name=group_offering_name,
            group_resource_name=group_resource_name,
            group_resource_uuid=group_resource_uuid,
            group_scope_id=group_scope_id,
            group_role_scope_type=group_role_scope_type,
            group_role_scope_type_label=group_role_scope_type_label,
            state=state,
            created=created,
            modified=modified,
            last_checked=last_checked,
            error_message=error_message,
            error_traceback=error_traceback,
            user=user,
        )

        offering_keycloak_membership.additional_properties = d
        return offering_keycloak_membership

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
