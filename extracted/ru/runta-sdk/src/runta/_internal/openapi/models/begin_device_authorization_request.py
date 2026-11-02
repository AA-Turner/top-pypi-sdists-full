from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.begin_device_authorization_request_client_id import (
    BeginDeviceAuthorizationRequestClientId,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BeginDeviceAuthorizationRequest")


@_attrs_define
class BeginDeviceAuthorizationRequest:
    """
    Attributes:
        client_id (BeginDeviceAuthorizationRequestClientId):
        device_name (str | Unset):
        app_url (str | Unset):
    """

    client_id: BeginDeviceAuthorizationRequestClientId
    device_name: str | Unset = UNSET
    app_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id.value

        device_name = self.device_name

        app_url = self.app_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_id": client_id,
            }
        )
        if device_name is not UNSET:
            field_dict["device_name"] = device_name
        if app_url is not UNSET:
            field_dict["app_url"] = app_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = BeginDeviceAuthorizationRequestClientId(d.pop("client_id"))

        device_name = d.pop("device_name", UNSET)

        app_url = d.pop("app_url", UNSET)

        begin_device_authorization_request = cls(
            client_id=client_id,
            device_name=device_name,
            app_url=app_url,
        )

        begin_device_authorization_request.additional_properties = d
        return begin_device_authorization_request

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
