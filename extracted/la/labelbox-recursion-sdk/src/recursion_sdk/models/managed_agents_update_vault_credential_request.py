from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_injection_location import ManagedAgentsInjectionLocation
from ..models.managed_agents_update_vault_credential_request_network_mode import ManagedAgentsUpdateVaultCredentialRequestNetworkMode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_labelbox_scope_request import ManagedAgentsLabelboxScopeRequest
  from ..models.managed_agents_update_vault_credential_request_metadata import ManagedAgentsUpdateVaultCredentialRequestMetadata





T = TypeVar("T", bound="ManagedAgentsUpdateVaultCredentialRequest")



@_attrs_define
class ManagedAgentsUpdateVaultCredentialRequest:
    """ Request body for updating one vault credential. Every field is optional and omitted fields keep their current value;
    the MCP server URL and an integration connection are deliberately not changeable here.

        Example:
            {'allowed_hosts': ['example'], 'display_name': 'example-name', 'injection_locations': ['headers'],
                'integration_permission': 'example', 'integration_resources': ['example'], 'labelbox_scope': {'mode':
                'projects', 'project_ids': ['project-id']}, 'metadata': {'key': 'example'}, 'network_mode': 'limited',
                'secret_name': 'example', 'secret_ref': 'example', 'secret_value': 'example'}

        Attributes:
            allowed_hosts (list[str] | Unset): Replacement host allowlist for limited networking, supporting wildcards such
                as *.example.com. Sent as a whole list, not merged; omit to keep the current one.
            display_name (str | Unset): Replacement operator-facing label. Omit to keep the current one.
            injection_locations (list[ManagedAgentsInjectionLocation] | Unset): Replacement list of where the credential is
                applied. Sent as a whole list, not merged; omit to keep the current one.
            integration_permission (str | Unset): Replacement permission preset for an integration grant. The connection
                itself is not repointable: that would change which account the agent acts as.
            integration_resources (list[str] | Unset): Replacement resource allowlist for an integration grant.
            labelbox_scope (ManagedAgentsLabelboxScopeRequest | Unset): Labelbox product-state authorization ceiling.
                Projects mode permits one exact project set. Organization mode permits organization-wide access, optionally
                pinned to one exact Slack binding whose internal or Slack Connect classification is explicit. The organization
                always equals the credential's owner. Example: {'mode': 'projects', 'project_ids': ['project-id']}.
            metadata (ManagedAgentsUpdateVaultCredentialRequestMetadata | Unset): Replacement free-form caller-owned JSON.
                Sent as a whole object, not merged; omit to keep the current value. The key labelbox_scope is reserved for the
                typed field.
            network_mode (ManagedAgentsUpdateVaultCredentialRequestNetworkMode | Unset): Replacement network mode. limited
                confines the credential to allowed_hosts; unrestricted removes that confinement. Omit to keep the current one.
            secret_name (str | Unset): Replacement environment variable or header name the secret binds to inside the
                sandbox. Omit to keep the current one.
            secret_ref (str | Unset): New secret-manager reference, for material stored elsewhere. Not supported for
                webhook_secret. Omit to keep the current secret.
            secret_value (str | Unset): Replacement credential material. Stored as a new secret version so the previous
                value stays revocable. Omit to keep the current secret.
     """

    allowed_hosts: list[str] | Unset = UNSET
    display_name: str | Unset = UNSET
    injection_locations: list[ManagedAgentsInjectionLocation] | Unset = UNSET
    integration_permission: str | Unset = UNSET
    integration_resources: list[str] | Unset = UNSET
    labelbox_scope: ManagedAgentsLabelboxScopeRequest | Unset = UNSET
    metadata: ManagedAgentsUpdateVaultCredentialRequestMetadata | Unset = UNSET
    network_mode: ManagedAgentsUpdateVaultCredentialRequestNetworkMode | Unset = UNSET
    secret_name: str | Unset = UNSET
    secret_ref: str | Unset = UNSET
    secret_value: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_labelbox_scope_request import ManagedAgentsLabelboxScopeRequest # noqa: PLC0415
        from ..models.managed_agents_update_vault_credential_request_metadata import ManagedAgentsUpdateVaultCredentialRequestMetadata # noqa: PLC0415
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



        integration_permission = self.integration_permission

        integration_resources: list[str] | Unset = UNSET
        if not isinstance(self.integration_resources, Unset):
            integration_resources = self.integration_resources



        labelbox_scope: dict[str, Any] | Unset = UNSET
        if not isinstance(self.labelbox_scope, Unset):
            labelbox_scope = self.labelbox_scope.to_dict()

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
        })
        if allowed_hosts is not UNSET:
            field_dict["allowed_hosts"] = allowed_hosts
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if injection_locations is not UNSET:
            field_dict["injection_locations"] = injection_locations
        if integration_permission is not UNSET:
            field_dict["integration_permission"] = integration_permission
        if integration_resources is not UNSET:
            field_dict["integration_resources"] = integration_resources
        if labelbox_scope is not UNSET:
            field_dict["labelbox_scope"] = labelbox_scope
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
        from ..models.managed_agents_labelbox_scope_request import ManagedAgentsLabelboxScopeRequest # noqa: PLC0415
        from ..models.managed_agents_update_vault_credential_request_metadata import ManagedAgentsUpdateVaultCredentialRequestMetadata # noqa: PLC0415
        d = dict(src_dict)
        allowed_hosts = cast(list[str], d.pop("allowed_hosts", UNSET))


        display_name = d.pop("display_name", UNSET)

        _injection_locations = d.pop("injection_locations", UNSET)
        injection_locations: list[ManagedAgentsInjectionLocation] | Unset = UNSET
        if _injection_locations is not UNSET:
            injection_locations = []
            for injection_locations_item_data in _injection_locations:
                injection_locations_item = ManagedAgentsInjectionLocation(injection_locations_item_data)



                injection_locations.append(injection_locations_item)


        integration_permission = d.pop("integration_permission", UNSET)

        integration_resources = cast(list[str], d.pop("integration_resources", UNSET))


        _labelbox_scope = d.pop("labelbox_scope", UNSET)
        labelbox_scope: ManagedAgentsLabelboxScopeRequest | Unset
        if isinstance(_labelbox_scope,  Unset):
            labelbox_scope = UNSET
        else:
            labelbox_scope = ManagedAgentsLabelboxScopeRequest.from_dict(_labelbox_scope)




        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsUpdateVaultCredentialRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsUpdateVaultCredentialRequestMetadata.from_dict(_metadata)




        _network_mode = d.pop("network_mode", UNSET)
        network_mode: ManagedAgentsUpdateVaultCredentialRequestNetworkMode | Unset
        if isinstance(_network_mode,  Unset):
            network_mode = UNSET
        else:
            network_mode = ManagedAgentsUpdateVaultCredentialRequestNetworkMode(_network_mode)




        secret_name = d.pop("secret_name", UNSET)

        secret_ref = d.pop("secret_ref", UNSET)

        secret_value = d.pop("secret_value", UNSET)

        managed_agents_update_vault_credential_request = cls(
            allowed_hosts=allowed_hosts,
            display_name=display_name,
            injection_locations=injection_locations,
            integration_permission=integration_permission,
            integration_resources=integration_resources,
            labelbox_scope=labelbox_scope,
            metadata=metadata,
            network_mode=network_mode,
            secret_name=secret_name,
            secret_ref=secret_ref,
            secret_value=secret_value,
        )


        managed_agents_update_vault_credential_request.additional_properties = d
        return managed_agents_update_vault_credential_request

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
