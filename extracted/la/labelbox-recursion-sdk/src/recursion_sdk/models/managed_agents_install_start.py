from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsInstallStart")



@_attrs_define
class ManagedAgentsInstallStart:
    """ Where to send a user to authorize an integration, plus the one-time state nonce that ties the provider's callback
    back to this attempt. Returned when an authorization flow is started.

        Example:
            {'state': 'example', 'url': 'https://example.com'}

        Attributes:
            state (str): Single-use CSRF nonce identifying this install attempt, not a lifecycle status. The provider must
                echo it in the callback; completion consumes the server-held record that binds it to the provider, organization,
                and user.
            url (str): Absolute provider-hosted authorization page to redirect the user to. Carries the state nonce as a
                query parameter; send the user here rather than fetching it server-side.
     """

    state: str
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        state = self.state

        url = self.url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "state": state,
            "url": url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = d.pop("state")

        url = d.pop("url")

        managed_agents_install_start = cls(
            state=state,
            url=url,
        )


        managed_agents_install_start.additional_properties = d
        return managed_agents_install_start

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
