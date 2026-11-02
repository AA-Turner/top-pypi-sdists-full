from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="WebAuthnCeremonyOptions")



@_attrs_define
class WebAuthnCeremonyOptions:
    """ The WebAuthn specification's own JSON shape for
    `PublicKeyCredentialCreationOptions`/`PublicKeyCredentialRequestOptions`
    (the begin responses) and `PublicKeyCredential`
    (the finish request bodies) — passed through to and from the
    browser's own `navigator.credentials` API untouched, so this
    contract intentionally doesn't re-model WebAuthn's own schema.

     """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        web_authn_ceremony_options = cls(
        )


        web_authn_ceremony_options.additional_properties = d
        return web_authn_ceremony_options

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
