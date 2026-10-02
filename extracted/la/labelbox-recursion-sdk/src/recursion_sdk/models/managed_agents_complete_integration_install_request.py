from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsCompleteIntegrationInstallRequest")



@_attrs_define
class ManagedAgentsCompleteIntegrationInstallRequest:
    """ Request body completing integration authorization after the provider redirects the user back. Sent from an
    authenticated session so the provider and organization come from the single-use state record rather than from
    callback parameters or browser-local storage.

        Example:
            {'code': 'example', 'selection': 'example', 'state': 'example'}

        Attributes:
            state (str): The nonce returned when authorization was started. Single-use and short-lived.
            code (str | Unset): Provider authorization code, proving which user authorized this connection. Required by
                OAuth providers (GitHub, Jira, Confluence, Loom), which refuse a completion without one; a built-in integration
                link (provider merge) returns a single-use code that the service exchanges with Merge before verifying the link,
                so a completion without it fails.
            selection (str | Unset): Which account the operator chose on the provider's own page, in the opaque form that
                provider returned. Providers with an account chooser may require it; GitHub returns an installation id. A
                selector only: the server verifies the choice against the accounts the authorizing user can reach and refuses
                one they cannot.
     """

    state: str
    code: str | Unset = UNSET
    selection: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        state = self.state

        code = self.code

        selection = self.selection


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "state": state,
        })
        if code is not UNSET:
            field_dict["code"] = code
        if selection is not UNSET:
            field_dict["selection"] = selection

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = d.pop("state")

        code = d.pop("code", UNSET)

        selection = d.pop("selection", UNSET)

        managed_agents_complete_integration_install_request = cls(
            state=state,
            code=code,
            selection=selection,
        )


        managed_agents_complete_integration_install_request.additional_properties = d
        return managed_agents_complete_integration_install_request

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
