from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_push_device_push_environment import ManagedAgentsPushDevicePushEnvironment
from ..models.managed_agents_push_device_token_kind import ManagedAgentsPushDeviceTokenKind
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsPushDevice")



@_attrs_define
class ManagedAgentsPushDevice:
    """ One registered push address, without the token itself. The token is an address the caller already holds; it is never
    returned, so it cannot reach a log or an error body twice.

        Example:
            {'app_version': 'example', 'bundle_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at':
                '2026-02-18T09:30:00Z', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'push_environment':
                'sandbox', 'token_kind': 'app', 'updated_at': '2026-02-18T09:30:00Z', 'user_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            bundle_id (str): Application bundle identifier the registering app reported. Kept to tell builds apart; the
                notifier addresses every push to the application it is configured for, never to this value.
            created_at (datetime.datetime): RFC 3339 timestamp the device first registered.
            organization_id (str): Organization the device is registered under. Server-assigned from the authenticated
                principal and never accepted from the request body.
            push_environment (ManagedAgentsPushDevicePushEnvironment): Which APNs host minted the token. A token minted by
                one host is rejected by the other.
            token_kind (ManagedAgentsPushDeviceTokenKind): Which push address this is: app for the token UIApplication
                vends, widget for the one a WidgetKit extension vends, live_activity for one running Live Activity card, and
                push_to_start for the token that may raise one.
            updated_at (datetime.datetime): RFC 3339 timestamp of the most recent registration. A device renews its
                registration while its sign-in lasts, so this is also when it last said it was alive; a registration not renewed
                for three days is dropped.
            user_id (str): User who registered the device. Server-assigned from the authenticated principal; only this user
                may withdraw the registration.
            app_version (str | Unset): Application version that registered, for diagnosing a build that stopped receiving
                pushes.
     """

    bundle_id: str
    created_at: datetime.datetime
    organization_id: str
    push_environment: ManagedAgentsPushDevicePushEnvironment
    token_kind: ManagedAgentsPushDeviceTokenKind
    updated_at: datetime.datetime
    user_id: str
    app_version: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        bundle_id = self.bundle_id

        created_at = self.created_at.isoformat()

        organization_id = self.organization_id

        push_environment = self.push_environment.value

        token_kind = self.token_kind.value

        updated_at = self.updated_at.isoformat()

        user_id = self.user_id

        app_version = self.app_version


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bundle_id": bundle_id,
            "created_at": created_at,
            "organization_id": organization_id,
            "push_environment": push_environment,
            "token_kind": token_kind,
            "updated_at": updated_at,
            "user_id": user_id,
        })
        if app_version is not UNSET:
            field_dict["app_version"] = app_version

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bundle_id = d.pop("bundle_id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        organization_id = d.pop("organization_id")

        push_environment = ManagedAgentsPushDevicePushEnvironment(d.pop("push_environment"))




        token_kind = ManagedAgentsPushDeviceTokenKind(d.pop("token_kind"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        user_id = d.pop("user_id")

        app_version = d.pop("app_version", UNSET)

        managed_agents_push_device = cls(
            bundle_id=bundle_id,
            created_at=created_at,
            organization_id=organization_id,
            push_environment=push_environment,
            token_kind=token_kind,
            updated_at=updated_at,
            user_id=user_id,
            app_version=app_version,
        )


        managed_agents_push_device.additional_properties = d
        return managed_agents_push_device

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
