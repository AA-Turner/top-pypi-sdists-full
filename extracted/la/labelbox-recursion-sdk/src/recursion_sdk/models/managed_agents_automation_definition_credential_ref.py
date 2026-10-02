from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionCredentialRef")



@_attrs_define
class ManagedAgentsAutomationDefinitionCredentialRef:
    """ An exact credential grant within a selected vault.

        Example:
            {'credentialId': 'example', 'vaultId': 'example'}

        Attributes:
            credential_id (str): Credential to grant to the session.
            vault_id (str): Selected vault containing the credential.
     """

    credential_id: str
    vault_id: str





    def to_dict(self) -> dict[str, Any]:
        credential_id = self.credential_id

        vault_id = self.vault_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "credentialId": credential_id,
            "vaultId": vault_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credential_id = d.pop("credentialId")

        vault_id = d.pop("vaultId")

        managed_agents_automation_definition_credential_ref = cls(
            credential_id=credential_id,
            vault_id=vault_id,
        )

        return managed_agents_automation_definition_credential_ref

