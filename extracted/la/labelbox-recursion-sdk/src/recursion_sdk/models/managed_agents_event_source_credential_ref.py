from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEventSourceCredentialRef")



@_attrs_define
class ManagedAgentsEventSourceCredentialRef:
    """ Reference to a managed credential; secret material is never returned.

        Example:
            {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            credential_id (UUID): Credential within the vault that contains the verification secret.
            vault_id (UUID): Vault containing the secret used to verify inbound deliveries.
     """

    credential_id: UUID
    vault_id: UUID





    def to_dict(self) -> dict[str, Any]:
        credential_id = str(self.credential_id)

        vault_id = str(self.vault_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "credentialId": credential_id,
            "vaultId": vault_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credential_id = UUID(d.pop("credentialId"))




        vault_id = UUID(d.pop("vaultId"))




        managed_agents_event_source_credential_ref = cls(
            credential_id=credential_id,
            vault_id=vault_id,
        )

        return managed_agents_event_source_credential_ref

