from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_register_push_device_request_push_environment import ManagedAgentsRegisterPushDeviceRequestPushEnvironment
from ..models.managed_agents_register_push_device_request_token_kind import ManagedAgentsRegisterPushDeviceRequestTokenKind
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsRegisterPushDeviceRequest")



@_attrs_define
class ManagedAgentsRegisterPushDeviceRequest:
    """ Request body for registering one device to be notified about the caller's fleet. The organization and the user
    always come from the authenticated principal.

        Example:
            {'app_version': 'example', 'bundle_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'device_token': 'example',
                'push_environment': 'sandbox', 'token_kind': 'app'}

        Attributes:
            bundle_id (str): Application bundle identifier the registering app reports. Recorded to tell builds apart;
                pushes are always addressed to the application the service is configured for.
            device_token (str): The device token APNs issued, hex-encoded as the device reported it; stored lowercase. An
                address, not a credential: it authorises nothing and is useless without the notifier's signing key.
            push_environment (ManagedAgentsRegisterPushDeviceRequestPushEnvironment): Which APNs host minted the token. A
                development build registers sandbox; a build installed from TestFlight or the App Store registers production.
            token_kind (ManagedAgentsRegisterPushDeviceRequestTokenKind): app for the token the application vends, widget
                for the one a WidgetKit extension vends, live_activity for one running Live Activity card, and push_to_start for
                the push-to-start token that may raise one. A phone can register any of these without the others.
            app_version (str | Unset): Application version registering, kept only so a build that stopped receiving
                notifications can be identified.
     """

    bundle_id: str
    device_token: str
    push_environment: ManagedAgentsRegisterPushDeviceRequestPushEnvironment
    token_kind: ManagedAgentsRegisterPushDeviceRequestTokenKind
    app_version: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        bundle_id = self.bundle_id

        device_token = self.device_token

        push_environment = self.push_environment.value

        token_kind = self.token_kind.value

        app_version = self.app_version


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bundle_id": bundle_id,
            "device_token": device_token,
            "push_environment": push_environment,
            "token_kind": token_kind,
        })
        if app_version is not UNSET:
            field_dict["app_version"] = app_version

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bundle_id = d.pop("bundle_id")

        device_token = d.pop("device_token")

        push_environment = ManagedAgentsRegisterPushDeviceRequestPushEnvironment(d.pop("push_environment"))




        token_kind = ManagedAgentsRegisterPushDeviceRequestTokenKind(d.pop("token_kind"))




        app_version = d.pop("app_version", UNSET)

        managed_agents_register_push_device_request = cls(
            bundle_id=bundle_id,
            device_token=device_token,
            push_environment=push_environment,
            token_kind=token_kind,
            app_version=app_version,
        )


        managed_agents_register_push_device_request.additional_properties = d
        return managed_agents_register_push_device_request

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
