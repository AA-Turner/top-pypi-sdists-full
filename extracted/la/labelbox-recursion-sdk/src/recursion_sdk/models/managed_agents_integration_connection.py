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
  from ..models.managed_agents_integration_connection_permissions import ManagedAgentsIntegrationConnectionPermissions
  from ..models.managed_agents_integration_connection_usage import ManagedAgentsIntegrationConnectionUsage





T = TypeVar("T", bound="ManagedAgentsIntegrationConnection")



@_attrs_define
class ManagedAgentsIntegrationConnection:
    """ An organization's link to a third-party account, created by installing an integration such as the GitHub App. It
    holds no secret itself; grant it to an agent so sessions can mint short-lived provider credentials from it.

        Example:
            {'account_login': 'example', 'account_type': 'example', 'connected_by': 'example', 'connection_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z', 'external_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'permissions': {'key': 'example'}, 'provider': 'example', 'resource_selection': 'example', 'state': 'example',
                'updated_at': '2026-02-18T09:30:00Z', 'usage': {'agents': 1, 'automations': 1}}

        Attributes:
            connection_id (str): Identifier for this connection (UUID). Server-assigned. Cite it when granting an agent
                access to the integration.
            created_at (datetime.datetime): RFC 3339 timestamp of when this record was created. Server-assigned.
            external_id (str): The provider's own identifier for the link, which token minting addresses. The installation
                id for GitHub; the composite {api_app_id}:{team_id} for Slack; the customer service-account email for Google
                Cloud.
            organization_id (str): Organization that owns this record. Resolved from the API key; never accepted from the
                caller.
            provider (str): Stable slug of the third-party integration adapter this connection uses.
            state (str): Lifecycle of the connection: pending was registered directly and waits for the customer to grant
                trust at the provider (a successful probe activates it), active can mint tokens, suspended is restorable at the
                provider and resolves to no credential, revoked was uninstalled and must be installed again.
            updated_at (datetime.datetime): RFC 3339 timestamp of the last change to this record. Server-assigned.
            account_login (str | Unset): Name of the connected third-party account, e.g. the GitHub org or user login.
                Cached at install time for display, so no provider call is needed to show it.
            account_type (str | Unset): Kind of account that was connected, as the provider reports it, e.g. Organization or
                User for GitHub and workspace for Slack.
            connected_by (str | Unset): User who completed the install, recorded for audit. Empty for connections created by
                an internal admin route.
            permissions (ManagedAgentsIntegrationConnectionPermissions | Unset): What the provider granted the install, as
                permission name to access level (e.g. contents: write). Used to narrow a minted token without a provider round
                trip and to explain why a permission preset is unavailable.
            resource_selection (str | Unset): Whether the install covers all of the account's resources or only chosen ones:
                all or selected. Informational only; the authoritative list stays at the provider.
            usage (ManagedAgentsIntegrationConnectionUsage | Unset): Current agent and pinned automation runtime usage of a
                connection. Example: {'agents': 1, 'automations': 1}.
     """

    connection_id: str
    created_at: datetime.datetime
    external_id: str
    organization_id: str
    provider: str
    state: str
    updated_at: datetime.datetime
    account_login: str | Unset = UNSET
    account_type: str | Unset = UNSET
    connected_by: str | Unset = UNSET
    permissions: ManagedAgentsIntegrationConnectionPermissions | Unset = UNSET
    resource_selection: str | Unset = UNSET
    usage: ManagedAgentsIntegrationConnectionUsage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_integration_connection_permissions import ManagedAgentsIntegrationConnectionPermissions # noqa: PLC0415
        from ..models.managed_agents_integration_connection_usage import ManagedAgentsIntegrationConnectionUsage # noqa: PLC0415
        connection_id = self.connection_id

        created_at = self.created_at.isoformat()

        external_id = self.external_id

        organization_id = self.organization_id

        provider = self.provider

        state = self.state

        updated_at = self.updated_at.isoformat()

        account_login = self.account_login

        account_type = self.account_type

        connected_by = self.connected_by

        permissions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions.to_dict()

        resource_selection = self.resource_selection

        usage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connection_id": connection_id,
            "created_at": created_at,
            "external_id": external_id,
            "organization_id": organization_id,
            "provider": provider,
            "state": state,
            "updated_at": updated_at,
        })
        if account_login is not UNSET:
            field_dict["account_login"] = account_login
        if account_type is not UNSET:
            field_dict["account_type"] = account_type
        if connected_by is not UNSET:
            field_dict["connected_by"] = connected_by
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if resource_selection is not UNSET:
            field_dict["resource_selection"] = resource_selection
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_integration_connection_permissions import ManagedAgentsIntegrationConnectionPermissions # noqa: PLC0415
        from ..models.managed_agents_integration_connection_usage import ManagedAgentsIntegrationConnectionUsage # noqa: PLC0415
        d = dict(src_dict)
        connection_id = d.pop("connection_id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        external_id = d.pop("external_id")

        organization_id = d.pop("organization_id")

        provider = d.pop("provider")

        state = d.pop("state")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        account_login = d.pop("account_login", UNSET)

        account_type = d.pop("account_type", UNSET)

        connected_by = d.pop("connected_by", UNSET)

        _permissions = d.pop("permissions", UNSET)
        permissions: ManagedAgentsIntegrationConnectionPermissions | Unset
        if isinstance(_permissions,  Unset):
            permissions = UNSET
        else:
            permissions = ManagedAgentsIntegrationConnectionPermissions.from_dict(_permissions)




        resource_selection = d.pop("resource_selection", UNSET)

        _usage = d.pop("usage", UNSET)
        usage: ManagedAgentsIntegrationConnectionUsage | Unset
        if isinstance(_usage,  Unset):
            usage = UNSET
        else:
            usage = ManagedAgentsIntegrationConnectionUsage.from_dict(_usage)




        managed_agents_integration_connection = cls(
            connection_id=connection_id,
            created_at=created_at,
            external_id=external_id,
            organization_id=organization_id,
            provider=provider,
            state=state,
            updated_at=updated_at,
            account_login=account_login,
            account_type=account_type,
            connected_by=connected_by,
            permissions=permissions,
            resource_selection=resource_selection,
            usage=usage,
        )


        managed_agents_integration_connection.additional_properties = d
        return managed_agents_integration_connection

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
