from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_create_vault_credential_request_credential_type import ManagedAgentsCreateVaultCredentialRequestCredentialType
from ..models.managed_agents_create_vault_credential_request_network_mode import ManagedAgentsCreateVaultCredentialRequestNetworkMode
from ..models.managed_agents_injection_location import ManagedAgentsInjectionLocation
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_create_vault_credential_request_metadata import ManagedAgentsCreateVaultCredentialRequestMetadata
  from ..models.managed_agents_labelbox_scope_request import ManagedAgentsLabelboxScopeRequest





T = TypeVar("T", bound="ManagedAgentsCreateVaultCredentialRequest")



@_attrs_define
class ManagedAgentsCreateVaultCredentialRequest:
    """ Request body for adding one credential to a vault. Its shape depends on credential_type. bearer_token and env_var
    accept exactly one of secret_value or secret_ref; webhook_secret requires secret_value; integration accepts neither.
    Secret material is encrypted at rest and never returned.

        Example:
            {'allowed_hosts': ['example'], 'credential_type': 'bearer_token', 'display_name': 'example-name',
                'injection_locations': ['headers'], 'integration_connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'integration_permission': 'example', 'integration_resources': ['example'], 'labelbox_scope': {'mode':
                'projects', 'project_ids': ['project-id']}, 'mcp_server_url': 'https://example.com', 'metadata': {'key':
                'example'}, 'network_mode': 'limited', 'secret_name': 'example', 'secret_ref': 'example', 'secret_value':
                'example'}

        Attributes:
            credential_type (ManagedAgentsCreateVaultCredentialRequestCredentialType): bearer_token authenticates to an MCP
                server and requires mcp_server_url. env_var is exposed to the sandbox for CLIs and SDKs. webhook_secret is
                control-plane-only material used to verify inbound webhook signatures. integration references a connected
                provider account and carries no secret of its own.
            allowed_hosts (list[str] | Unset): Hosts the credential may be sent to under limited networking. Supports
                wildcards such as *.example.com.
            display_name (str | Unset): Operator-facing label.
            injection_locations (list[ManagedAgentsInjectionLocation] | Unset): Where a bearer or MCP credential attaches to
                a request. Defaults to headers, which is recommended unless the service reads the secret from the request body.
                Ignored for env_var, which is injected into the sandbox environment instead, and for integration.
            integration_connection_id (str | Unset): The connected account this grant uses. Required for the integration
                kind.
            integration_permission (str | Unset): Provider permission preset applied when minting. See the provider's list;
                defaults to the least-privileged one.
            integration_resources (list[str] | Unset): Resources within the connection this grant may reach, e.g. GitHub
                repository names. Empty means every resource the connection reaches, which is broader than most grants should
                be.
            labelbox_scope (ManagedAgentsLabelboxScopeRequest | Unset): Labelbox product-state authorization ceiling.
                Projects mode permits one exact project set. Organization mode permits organization-wide access, optionally
                pinned to one exact Slack binding whose internal or Slack Connect classification is explicit. The organization
                always equals the credential's owner. Example: {'mode': 'projects', 'project_ids': ['project-id']}.
            mcp_server_url (str | Unset): The MCP server this credential unlocks. Must be http or https and must not embed
                credentials. Required for the MCP kinds and immutable afterwards, so it is validated here rather than at the
                first connection.
            metadata (ManagedAgentsCreateVaultCredentialRequestMetadata | Unset): Free-form caller-owned JSON stored with
                the credential row and returned on reads. Not interpreted by the service; never put secret material here, since
                unlike secret_value it is returned verbatim. The key labelbox_scope is reserved for the typed field.
            network_mode (ManagedAgentsCreateVaultCredentialRequestNetworkMode | Unset): Where the credential may be sent.
                Defaults to limited, which restricts it to allowed_hosts.
            secret_name (str | Unset): Environment variable or header name the secret binds to inside the sandbox. Required
                for env_var.
            secret_ref (str | Unset): Reference to material stored outside this service, carrying a provider prefix. Not
                supported for webhook_secret because verification runs in this control plane. Requests carrying obvious inline
                secret material are rejected.
            secret_value (str | Unset): The credential material itself. Encrypted at rest and never returned or logged by
                this service. Supply this or secret_ref, not both.
     """

    credential_type: ManagedAgentsCreateVaultCredentialRequestCredentialType
    allowed_hosts: list[str] | Unset = UNSET
    display_name: str | Unset = UNSET
    injection_locations: list[ManagedAgentsInjectionLocation] | Unset = UNSET
    integration_connection_id: str | Unset = UNSET
    integration_permission: str | Unset = UNSET
    integration_resources: list[str] | Unset = UNSET
    labelbox_scope: ManagedAgentsLabelboxScopeRequest | Unset = UNSET
    mcp_server_url: str | Unset = UNSET
    metadata: ManagedAgentsCreateVaultCredentialRequestMetadata | Unset = UNSET
    network_mode: ManagedAgentsCreateVaultCredentialRequestNetworkMode | Unset = UNSET
    secret_name: str | Unset = UNSET
    secret_ref: str | Unset = UNSET
    secret_value: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_create_vault_credential_request_metadata import ManagedAgentsCreateVaultCredentialRequestMetadata # noqa: PLC0415
        from ..models.managed_agents_labelbox_scope_request import ManagedAgentsLabelboxScopeRequest # noqa: PLC0415
        credential_type = self.credential_type.value

        allowed_hosts: list[str] | Unset = UNSET
        if not isinstance(self.allowed_hosts, Unset):
            allowed_hosts = self.allowed_hosts



        display_name = self.display_name

        injection_locations: list[str] | Unset = UNSET
        if not isinstance(self.injection_locations, Unset):
            injection_locations = []
            for injection_locations_item_data in self.injection_locations:
                injection_locations_item = injection_locations_item_data.value
                injection_locations.append(injection_locations_item)



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


        secret_name = self.secret_name

        secret_ref = self.secret_ref

        secret_value = self.secret_value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "credential_type": credential_type,
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
        if secret_name is not UNSET:
            field_dict["secret_name"] = secret_name
        if secret_ref is not UNSET:
            field_dict["secret_ref"] = secret_ref
        if secret_value is not UNSET:
            field_dict["secret_value"] = secret_value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_create_vault_credential_request_metadata import ManagedAgentsCreateVaultCredentialRequestMetadata # noqa: PLC0415
        from ..models.managed_agents_labelbox_scope_request import ManagedAgentsLabelboxScopeRequest # noqa: PLC0415
        d = dict(src_dict)
        credential_type = ManagedAgentsCreateVaultCredentialRequestCredentialType(d.pop("credential_type"))




        allowed_hosts = cast(list[str], d.pop("allowed_hosts", UNSET))


        display_name = d.pop("display_name", UNSET)

        _injection_locations = d.pop("injection_locations", UNSET)
        injection_locations: list[ManagedAgentsInjectionLocation] | Unset = UNSET
        if _injection_locations is not UNSET:
            injection_locations = []
            for injection_locations_item_data in _injection_locations:
                injection_locations_item = ManagedAgentsInjectionLocation(injection_locations_item_data)



                injection_locations.append(injection_locations_item)


        integration_connection_id = d.pop("integration_connection_id", UNSET)

        integration_permission = d.pop("integration_permission", UNSET)

        integration_resources = cast(list[str], d.pop("integration_resources", UNSET))


        _labelbox_scope = d.pop("labelbox_scope", UNSET)
        labelbox_scope: ManagedAgentsLabelboxScopeRequest | Unset
        if isinstance(_labelbox_scope,  Unset):
            labelbox_scope = UNSET
        else:
            labelbox_scope = ManagedAgentsLabelboxScopeRequest.from_dict(_labelbox_scope)




        mcp_server_url = d.pop("mcp_server_url", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsCreateVaultCredentialRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsCreateVaultCredentialRequestMetadata.from_dict(_metadata)




        _network_mode = d.pop("network_mode", UNSET)
        network_mode: ManagedAgentsCreateVaultCredentialRequestNetworkMode | Unset
        if isinstance(_network_mode,  Unset):
            network_mode = UNSET
        else:
            network_mode = ManagedAgentsCreateVaultCredentialRequestNetworkMode(_network_mode)




        secret_name = d.pop("secret_name", UNSET)

        secret_ref = d.pop("secret_ref", UNSET)

        secret_value = d.pop("secret_value", UNSET)

        managed_agents_create_vault_credential_request = cls(
            credential_type=credential_type,
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
            secret_name=secret_name,
            secret_ref=secret_ref,
            secret_value=secret_value,
        )


        managed_agents_create_vault_credential_request.additional_properties = d
        return managed_agents_create_vault_credential_request

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
