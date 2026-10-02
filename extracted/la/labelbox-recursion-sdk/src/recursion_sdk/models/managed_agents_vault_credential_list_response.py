from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_vault_credential import ManagedAgentsVaultCredential





T = TypeVar("T", bound="ManagedAgentsVaultCredentialListResponse")



@_attrs_define
class ManagedAgentsVaultCredentialListResponse:
    """ Response body of GET /v1/vaults/{vault_id}/credentials. Unlike the other list envelopes this one is deliberately
    lossy: each row describes a credential and points at its secret-manager reference, and the secret material is never
    returned by any read endpoint. To learn whether a credential actually works, probe with POST /v1/mcp/probe.

        Example:
            {'vault_credentials': [{'allowed_hosts': ['example'], 'created_at': '2026-02-18T09:30:00Z', 'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'credential_type': 'example', 'display_name': 'example-name',
                'injection_locations': ['example'], 'integration_connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'integration_permission': 'example', 'integration_resources': ['example'], 'labelbox_scope': {'mode':
                'projects', 'organization_id': 'organization-id', 'project_ids': ['project-id']}, 'mcp_server_url':
                'https://example.com', 'metadata': {'key': 'example'}, 'network_mode': 'limited', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'platform_mcp_service': 'slack_tools', 'secret_name': 'example',
                'secret_ref': 'example', 'updated_at': '2026-02-18T09:30:00Z', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}

        Attributes:
            vault_credentials (list[ManagedAgentsVaultCredential] | None): Credentials held by the vault named in the path,
                newest first. Null rather than an empty array when the vault is empty. Soft-deleted credentials are omitted, and
                no row carries a secret value.
     """

    vault_credentials: list[ManagedAgentsVaultCredential] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_vault_credential import ManagedAgentsVaultCredential # noqa: PLC0415
        vault_credentials: list[dict[str, Any]] | None
        if isinstance(self.vault_credentials, list):
            vault_credentials = []
            for vault_credentials_type_0_item_data in self.vault_credentials:
                vault_credentials_type_0_item = vault_credentials_type_0_item_data.to_dict()
                vault_credentials.append(vault_credentials_type_0_item)


        else:
            vault_credentials = self.vault_credentials


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "vault_credentials": vault_credentials,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_vault_credential import ManagedAgentsVaultCredential # noqa: PLC0415
        d = dict(src_dict)
        def _parse_vault_credentials(data: object) -> list[ManagedAgentsVaultCredential] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                vault_credentials_type_0 = []
                _vault_credentials_type_0 = data
                for vault_credentials_type_0_item_data in (_vault_credentials_type_0):
                    vault_credentials_type_0_item = ManagedAgentsVaultCredential.from_dict(vault_credentials_type_0_item_data)



                    vault_credentials_type_0.append(vault_credentials_type_0_item)

                return vault_credentials_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsVaultCredential] | None, data)

        vault_credentials = _parse_vault_credentials(d.pop("vault_credentials"))


        managed_agents_vault_credential_list_response = cls(
            vault_credentials=vault_credentials,
        )


        managed_agents_vault_credential_list_response.additional_properties = d
        return managed_agents_vault_credential_list_response

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
