from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_vault_metadata import ManagedAgentsVaultMetadata





T = TypeVar("T", bound="ManagedAgentsVault")



@_attrs_define
class ManagedAgentsVault:
    """ A named group of credentials an agent session may be granted. A session references vaults by id; the credential
    values inside are resolved at execution time and are never returned over the API.

        Example:
            {'created_at': '2026-02-18T09:30:00Z', 'credential_count': 1, 'display_name': 'example-name', 'metadata':
                {'key': 'example'}, 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at':
                '2026-02-18T09:30:00Z', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            created_at (datetime.datetime): RFC 3339 timestamp of when this record was created. Server-assigned.
            credential_count (int): How many credentials this vault currently holds, so a list view need not fetch each
                vault's credentials.
            display_name (str): Operator-facing label for the vault, shown wherever vaults are listed.
            organization_id (str): Organization that owns this record. Resolved from the API key; never accepted from the
                caller.
            updated_at (datetime.datetime): RFC 3339 timestamp of the last change to this record. Server-assigned.
            vault_id (str): Identifier for this vault (UUID). Server-assigned.
            metadata (ManagedAgentsVaultMetadata | Unset): Free-form caller-supplied key/value labels. Stored verbatim and
                never interpreted by the service.
     """

    created_at: datetime.datetime
    credential_count: int
    display_name: str
    organization_id: str
    updated_at: datetime.datetime
    vault_id: str
    metadata: ManagedAgentsVaultMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_vault_metadata import ManagedAgentsVaultMetadata # noqa: PLC0415
        created_at = self.created_at.isoformat()

        credential_count = self.credential_count

        display_name = self.display_name

        organization_id = self.organization_id

        updated_at = self.updated_at.isoformat()

        vault_id = self.vault_id

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "credential_count": credential_count,
            "display_name": display_name,
            "organization_id": organization_id,
            "updated_at": updated_at,
            "vault_id": vault_id,
        })
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_vault_metadata import ManagedAgentsVaultMetadata # noqa: PLC0415
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        credential_count = d.pop("credential_count")

        display_name = d.pop("display_name")

        organization_id = d.pop("organization_id")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        vault_id = d.pop("vault_id")

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsVaultMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsVaultMetadata.from_dict(_metadata)




        managed_agents_vault = cls(
            created_at=created_at,
            credential_count=credential_count,
            display_name=display_name,
            organization_id=organization_id,
            updated_at=updated_at,
            vault_id=vault_id,
            metadata=metadata,
        )


        managed_agents_vault.additional_properties = d
        return managed_agents_vault

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
