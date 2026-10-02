from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsCreateVaultCredentialRequestMetadata")



@_attrs_define
class ManagedAgentsCreateVaultCredentialRequestMetadata:
    """ Free-form caller-owned JSON stored with the credential row and returned on reads. Not interpreted by the service;
    never put secret material here, since unlike secret_value it is returned verbatim. The key labelbox_scope is
    reserved for the typed field.

     """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        managed_agents_create_vault_credential_request_metadata = cls(
        )


        managed_agents_create_vault_credential_request_metadata.additional_properties = d
        return managed_agents_create_vault_credential_request_metadata

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
