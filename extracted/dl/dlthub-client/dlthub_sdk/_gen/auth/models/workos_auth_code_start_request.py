from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkosAuthCodeStartRequest")


@_attrs_define
class WorkosAuthCodeStartRequest:
    """
    Attributes:
        code_challenge (str):
        redirect_uri (str):
        state (str):
    """

    code_challenge: str
    redirect_uri: str
    state: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code_challenge = self.code_challenge

        redirect_uri = self.redirect_uri

        state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code_challenge": code_challenge,
                "redirect_uri": redirect_uri,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code_challenge = d.pop("code_challenge")

        redirect_uri = d.pop("redirect_uri")

        state = d.pop("state")

        workos_auth_code_start_request = cls(
            code_challenge=code_challenge,
            redirect_uri=redirect_uri,
            state=state,
        )

        workos_auth_code_start_request.additional_properties = d
        return workos_auth_code_start_request

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
