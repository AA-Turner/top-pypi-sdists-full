from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingKeycloakMembershipRequest")


@_attrs_define
class OfferingKeycloakMembershipRequest:
    """
    Attributes:
        username (str): Keycloak user username
        email (str): User's email for notifications
        offering (str):
        role (str):
        resource (Union[None, Unset, str]):
        scope_id (Union[Unset, str]):  Default: ''.
        user (Union[None, Unset, str]):
    """

    username: str
    email: str
    offering: str
    role: str
    resource: Union[None, Unset, str] = UNSET
    scope_id: Union[Unset, str] = ""
    user: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        email = self.email

        offering = self.offering

        role = self.role

        resource: Union[None, Unset, str]
        if isinstance(self.resource, Unset):
            resource = UNSET
        else:
            resource = self.resource

        scope_id = self.scope_id

        user: Union[None, Unset, str]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "email": email,
                "offering": offering,
                "role": role,
            }
        )
        if resource is not UNSET:
            field_dict["resource"] = resource
        if scope_id is not UNSET:
            field_dict["scope_id"] = scope_id
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        email = d.pop("email")

        offering = d.pop("offering")

        role = d.pop("role")

        def _parse_resource(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource = _parse_resource(d.pop("resource", UNSET))

        scope_id = d.pop("scope_id", UNSET)

        def _parse_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user = _parse_user(d.pop("user", UNSET))

        offering_keycloak_membership_request = cls(
            username=username,
            email=email,
            offering=offering,
            role=role,
            resource=resource,
            scope_id=scope_id,
            user=user,
        )

        offering_keycloak_membership_request.additional_properties = d
        return offering_keycloak_membership_request

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
