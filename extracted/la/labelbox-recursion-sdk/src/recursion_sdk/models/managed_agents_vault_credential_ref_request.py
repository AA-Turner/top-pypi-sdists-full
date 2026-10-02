from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsVaultCredentialRefRequest")



@_attrs_define
class ManagedAgentsVaultCredentialRefRequest:
    """ A pointer to one credential inside one vault. Used to grant a session specific credentials rather than every
    credential in a vault.

        Example:
            {'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            credential_id (str | Unset): Credential to select inside vault_id.
            vault_id (str | Unset): Vault holding the credential. Required, because credential ids are unique only within a
                vault.
     """

    credential_id: str | Unset = UNSET
    vault_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        credential_id = self.credential_id

        vault_id = self.vault_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if credential_id is not UNSET:
            field_dict["credential_id"] = credential_id
        if vault_id is not UNSET:
            field_dict["vault_id"] = vault_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credential_id = d.pop("credential_id", UNSET)

        vault_id = d.pop("vault_id", UNSET)

        managed_agents_vault_credential_ref_request = cls(
            credential_id=credential_id,
            vault_id=vault_id,
        )


        managed_agents_vault_credential_ref_request.additional_properties = d
        return managed_agents_vault_credential_ref_request

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
