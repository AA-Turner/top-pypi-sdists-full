from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_vault_credential_network_mode import ManagedAgentsVaultCredentialNetworkMode
from ..models.managed_agents_vault_credential_platform_mcp_service import ManagedAgentsVaultCredentialPlatformMcpService
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_labelbox_tools_scope import ManagedAgentsLabelboxToolsScope
  from ..models.managed_agents_vault_credential_metadata import ManagedAgentsVaultCredentialMetadata





T = TypeVar("T", bound="ManagedAgentsVaultCredential")



@_attrs_define
class ManagedAgentsVaultCredential:
    """ One credential in a vault, described without its secret value — no field on this shape can carry secret material,
    which is what makes it safe to list over the API. Returned when managing a vault's contents; the value itself is
    opened only inside a running session.

        Example:
            {'allowed_hosts': ['example'], 'created_at': '2026-02-18T09:30:00Z', 'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'credential_type': 'example', 'display_name': 'example-name',
                'injection_locations': ['example'], 'integration_connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'integration_permission': 'example', 'integration_resources': ['example'], 'labelbox_scope': {'mode':
                'projects', 'organization_id': 'organization-id', 'project_ids': ['project-id']}, 'mcp_server_url':
                'https://example.com', 'metadata': {'key': 'example'}, 'network_mode': 'limited', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'platform_mcp_service': 'slack_tools', 'secret_name': 'example',
                'secret_ref': 'example', 'updated_at': '2026-02-18T09:30:00Z', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            created_at (datetime.datetime): RFC 3339 timestamp of when this record was created. Server-assigned.
            credential_id (str): Identifier for this credential (UUID). Server-assigned, and unique only within its vault.
            credential_type (str): How the credential is used: bearer_token, env_var, or webhook_secret. Legacy rows may
                report mcp_oauth or integration, so this remains a string rather than a closed response enum.
            organization_id (str): Organization that owns this record. Resolved from the API key; never accepted from the
                caller.
            updated_at (datetime.datetime): RFC 3339 timestamp of the last change to this record. Server-assigned.
            vault_id (str): Vault this credential belongs to (UUID).
            allowed_hosts (list[str] | Unset): Hosts the credential may be sent to when network_mode is limited. Ignored
                under unrestricted.
            display_name (str | Unset): Operator-facing label for the credential. Optional: a credential is identifiable by
                its secret_name or MCP server without one.
            injection_locations (list[str] | Unset): Where the credential is attached to an outbound request: headers, body,
                or both. Headers alone is recommended; a secret in a request body is far easier to log by accident. Meaningful
                only for the MCP OAuth and bearer-token kinds: env_var is injected into the sandbox environment, and integration
                mints its own token per session.
            integration_connection_id (str | Unset): Organization integration connection this credential grants a session
                (UUID). Set only for the integration kind, where it replaces sealed material: the provider mints a short-lived
                token per session.
            integration_permission (str | Unset): Permission preset applied when a token is minted for this grant; see the
                provider's scope table. An unknown value is rejected on write rather than at mint time.
            integration_resources (list[str] | Unset): Resources within the connection the grant is narrowed to —
                repositories, for GitHub. Empty means every resource the connection itself can reach, which is broader than most
                grants should be.
            labelbox_scope (ManagedAgentsLabelboxToolsScope | Unset): Labelbox product-state authorization ceiling. The
                organization always equals the credential's owner. Projects mode permits one exact project set; organization
                mode permits organization-wide reads only from one exact Slack binding whose internal or Slack Connect
                classification is explicit. Example: {'mode': 'projects', 'organization_id': 'organization-id', 'project_ids':
                ['project-id']}.
            mcp_server_url (str | Unset): MCP server this credential may be sent to. Required for bearer_token and immutable
                afterwards, so a stored secret cannot be repointed at a different service.
            metadata (ManagedAgentsVaultCredentialMetadata | Unset): Free-form caller-supplied key/value labels. Stored
                verbatim and never interpreted by the service. The key labelbox_scope is reserved for the typed field of that
                name.
            network_mode (ManagedAgentsVaultCredentialNetworkMode | Unset): How far the credential may travel: limited
                confines it to allowed_hosts, unrestricted permits any host. limited is the safe default.
            platform_mcp_service (ManagedAgentsVaultCredentialPlatformMcpService | Unset): Deployment-derived identity of
                the exact platform MCP service this credential targets. Present as slack_tools only when mcp_server_url matches
                the configured Slack tools endpoint; never caller-controlled or stored.
            secret_name (str | Unset): Environment variable or header name the secret binds to inside the sandbox. Required
                for the env_var kind.
            secret_ref (str | Unset): Pointer to material stored in an external secret manager, carrying a provider prefix
                such as kms: or vault:. Opaque to this service, and empty on the normal path where the value is sealed into the
                credential itself.
     """

    created_at: datetime.datetime
    credential_id: str
    credential_type: str
    organization_id: str
    updated_at: datetime.datetime
    vault_id: str
    allowed_hosts: list[str] | Unset = UNSET
    display_name: str | Unset = UNSET
    injection_locations: list[str] | Unset = UNSET
    integration_connection_id: str | Unset = UNSET
    integration_permission: str | Unset = UNSET
    integration_resources: list[str] | Unset = UNSET
    labelbox_scope: ManagedAgentsLabelboxToolsScope | Unset = UNSET
    mcp_server_url: str | Unset = UNSET
    metadata: ManagedAgentsVaultCredentialMetadata | Unset = UNSET
    network_mode: ManagedAgentsVaultCredentialNetworkMode | Unset = UNSET
    platform_mcp_service: ManagedAgentsVaultCredentialPlatformMcpService | Unset = UNSET
    secret_name: str | Unset = UNSET
    secret_ref: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_labelbox_tools_scope import ManagedAgentsLabelboxToolsScope # noqa: PLC0415
        from ..models.managed_agents_vault_credential_metadata import ManagedAgentsVaultCredentialMetadata # noqa: PLC0415
        created_at = self.created_at.isoformat()

        credential_id = self.credential_id

        credential_type = self.credential_type

        organization_id = self.organization_id

        updated_at = self.updated_at.isoformat()

        vault_id = self.vault_id

        allowed_hosts: list[str] | Unset = UNSET
        if not isinstance(self.allowed_hosts, Unset):
            allowed_hosts = self.allowed_hosts



        display_name = self.display_name

        injection_locations: list[str] | Unset = UNSET
        if not isinstance(self.injection_locations, Unset):
            injection_locations = self.injection_locations



        integration_connection_id = self.integration_connection_id

        integration_permission = self.integration_permission

        integration_resources: list[str] | Unset = UNSET
        if not isinstance(self.integration_resources, Unset):
            integration_resources = self.integration_resources



        labelbox_scope: dict[str, Any] | Unset = UNSET
        if not isinstance(self.labelbox_scope, Unset):
            labelbox_scope = self.labelbox_scope.to_dict()

        mcp_server_url = self.mcp_server_url

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        network_mode: str | Unset = UNSET
        if not isinstance(self.network_mode, Unset):
            network_mode = self.network_mode.value


        platform_mcp_service: str | Unset = UNSET
        if not isinstance(self.platform_mcp_service, Unset):
            platform_mcp_service = self.platform_mcp_service.value


        secret_name = self.secret_name

        secret_ref = self.secret_ref


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "credential_id": credential_id,
            "credential_type": credential_type,
            "organization_id": organization_id,
            "updated_at": updated_at,
            "vault_id": vault_id,
        })
        if allowed_hosts is not UNSET:
            field_dict["allowed_hosts"] = allowed_hosts
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if injection_locations is not UNSET:
            field_dict["injection_locations"] = injection_locations
        if integration_connection_id is not UNSET:
            field_dict["integration_connection_id"] = integration_connection_id
        if integration_permission is not UNSET:
            field_dict["integration_permission"] = integration_permission
        if integration_resources is not UNSET:
            field_dict["integration_resources"] = integration_resources
        if labelbox_scope is not UNSET:
            field_dict["labelbox_scope"] = labelbox_scope
        if mcp_server_url is not UNSET:
            field_dict["mcp_server_url"] = mcp_server_url
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if network_mode is not UNSET:
            field_dict["network_mode"] = network_mode
        if platform_mcp_service is not UNSET:
            field_dict["platform_mcp_service"] = platform_mcp_service
        if secret_name is not UNSET:
            field_dict["secret_name"] = secret_name
        if secret_ref is not UNSET:
            field_dict["secret_ref"] = secret_ref

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_labelbox_tools_scope import ManagedAgentsLabelboxToolsScope # noqa: PLC0415
        from ..models.managed_agents_vault_credential_metadata import ManagedAgentsVaultCredentialMetadata # noqa: PLC0415
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        credential_id = d.pop("credential_id")

        credential_type = d.pop("credential_type")

        organization_id = d.pop("organization_id")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        vault_id = d.pop("vault_id")

        allowed_hosts = cast(list[str], d.pop("allowed_hosts", UNSET))


        display_name = d.pop("display_name", UNSET)

        injection_locations = cast(list[str], d.pop("injection_locations", UNSET))


        integration_connection_id = d.pop("integration_connection_id", UNSET)

        integration_permission = d.pop("integration_permission", UNSET)

        integration_resources = cast(list[str], d.pop("integration_resources", UNSET))


        _labelbox_scope = d.pop("labelbox_scope", UNSET)
        labelbox_scope: ManagedAgentsLabelboxToolsScope | Unset
        if isinstance(_labelbox_scope,  Unset):
            labelbox_scope = UNSET
        else:
            labelbox_scope = ManagedAgentsLabelboxToolsScope.from_dict(_labelbox_scope)




        mcp_server_url = d.pop("mcp_server_url", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsVaultCredentialMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsVaultCredentialMetadata.from_dict(_metadata)




        _network_mode = d.pop("network_mode", UNSET)
        network_mode: ManagedAgentsVaultCredentialNetworkMode | Unset
        if isinstance(_network_mode,  Unset):
            network_mode = UNSET
        else:
            network_mode = ManagedAgentsVaultCredentialNetworkMode(_network_mode)




        _platform_mcp_service = d.pop("platform_mcp_service", UNSET)
        platform_mcp_service: ManagedAgentsVaultCredentialPlatformMcpService | Unset
        if isinstance(_platform_mcp_service,  Unset):
            platform_mcp_service = UNSET
        else:
            platform_mcp_service = ManagedAgentsVaultCredentialPlatformMcpService(_platform_mcp_service)




        secret_name = d.pop("secret_name", UNSET)

        secret_ref = d.pop("secret_ref", UNSET)

        managed_agents_vault_credential = cls(
            created_at=created_at,
            credential_id=credential_id,
            credential_type=credential_type,
            organization_id=organization_id,
            updated_at=updated_at,
            vault_id=vault_id,
            allowed_hosts=allowed_hosts,
            display_name=display_name,
            injection_locations=injection_locations,
            integration_connection_id=integration_connection_id,
            integration_permission=integration_permission,
            integration_resources=integration_resources,
            labelbox_scope=labelbox_scope,
            mcp_server_url=mcp_server_url,
            metadata=metadata,
            network_mode=network_mode,
            platform_mcp_service=platform_mcp_service,
            secret_name=secret_name,
            secret_ref=secret_ref,
        )


        managed_agents_vault_credential.additional_properties = d
        return managed_agents_vault_credential

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
