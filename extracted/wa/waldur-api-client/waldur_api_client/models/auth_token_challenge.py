from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthTokenChallenge")


@_attrs_define
class AuthTokenChallenge:
    """
    Attributes:
        detail (str): Human-readable reason the token was not issued.
        passkey_required (Union[Unset, bool]): True when the password was accepted but a passkey assertion is still
            outstanding. Discriminates this case from a rejected password, which is also a 401.
        pending_passkey_ceremony (Union[Unset, UUID]): Handle for the passkey challenge that must be satisfied before a
            token is issued. Not a credential: it grants nothing on its own and cannot be used for authentication.
    """

    detail: str
    passkey_required: Union[Unset, bool] = UNSET
    pending_passkey_ceremony: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        passkey_required = self.passkey_required

        pending_passkey_ceremony: Union[Unset, str] = UNSET
        if not isinstance(self.pending_passkey_ceremony, Unset):
            pending_passkey_ceremony = str(self.pending_passkey_ceremony)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detail": detail,
            }
        )
        if passkey_required is not UNSET:
            field_dict["passkey_required"] = passkey_required
        if pending_passkey_ceremony is not UNSET:
            field_dict["pending_passkey_ceremony"] = pending_passkey_ceremony

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        detail = d.pop("detail")

        passkey_required = d.pop("passkey_required", UNSET)

        _pending_passkey_ceremony = d.pop("pending_passkey_ceremony", UNSET)
        pending_passkey_ceremony: Union[Unset, UUID]
        if isinstance(_pending_passkey_ceremony, Unset):
            pending_passkey_ceremony = UNSET
        else:
            pending_passkey_ceremony = UUID(_pending_passkey_ceremony)

        auth_token_challenge = cls(
            detail=detail,
            passkey_required=passkey_required,
            pending_passkey_ceremony=pending_passkey_ceremony,
        )

        auth_token_challenge.additional_properties = d
        return auth_token_challenge

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
