from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_connection_setup import ManagedAgentsConnectionSetup
  from ..models.managed_agents_integration_connection import ManagedAgentsIntegrationConnection





T = TypeVar("T", bound="ManagedAgentsConnectionRegistration")



@_attrs_define
class ManagedAgentsConnectionRegistration:
    """ A directly registered integration connection together with the trust the customer still has to grant. The connection
    starts pending and becomes active when a probe mints through the granted trust.

        Example:
            {'connection': {'account_login': 'example', 'account_type': 'example', 'connected_by': 'example',
                'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z', 'external_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'permissions': {'key': 'example'}, 'provider': 'example', 'resource_selection': 'example', 'state': 'example',
                'updated_at': '2026-02-18T09:30:00Z', 'usage': {'agents': 1, 'automations': 1}}, 'created': True,
                'delegate_prepared': True, 'setup': {'delegate_principal': 'example', 'grant_command': 'example', 'role':
                'user', 'target_principal': 'example'}}

        Attributes:
            connection (ManagedAgentsIntegrationConnection): An organization's link to a third-party account, created by
                installing an integration such as the GitHub App. It holds no secret itself; grant it to an agent so sessions
                can mint short-lived provider credentials from it. Example: {'account_login': 'example', 'account_type':
                'example', 'connected_by': 'example', 'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at':
                '2026-02-18T09:30:00Z', 'external_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permissions': {'key': 'example'}, 'provider': 'example',
                'resource_selection': 'example', 'state': 'example', 'updated_at': '2026-02-18T09:30:00Z', 'usage': {'agents':
                1, 'automations': 1}}.
            created (bool): True when this call created the row. False when a live connection for the same principal already
                existed and was returned instead.
            delegate_prepared (bool): True only when this request confirmed the organization delegate through the isolated
                provisioner.
            setup (ManagedAgentsConnectionSetup): The trust a customer must grant at the provider before a directly
                registered connection can activate. Regenerated on every registration call, so a lost response is recovered by
                registering the same identifier again. Example: {'delegate_principal': 'example', 'grant_command': 'example',
                'role': 'user', 'target_principal': 'example'}.
     """

    connection: ManagedAgentsIntegrationConnection
    created: bool
    delegate_prepared: bool
    setup: ManagedAgentsConnectionSetup
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_connection_setup import ManagedAgentsConnectionSetup # noqa: PLC0415
        from ..models.managed_agents_integration_connection import ManagedAgentsIntegrationConnection # noqa: PLC0415
        connection = self.connection.to_dict()

        created = self.created

        delegate_prepared = self.delegate_prepared

        setup = self.setup.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connection": connection,
            "created": created,
            "delegate_prepared": delegate_prepared,
            "setup": setup,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_connection_setup import ManagedAgentsConnectionSetup # noqa: PLC0415
        from ..models.managed_agents_integration_connection import ManagedAgentsIntegrationConnection # noqa: PLC0415
        d = dict(src_dict)
        connection = ManagedAgentsIntegrationConnection.from_dict(d.pop("connection"))




        created = d.pop("created")

        delegate_prepared = d.pop("delegate_prepared")

        setup = ManagedAgentsConnectionSetup.from_dict(d.pop("setup"))




        managed_agents_connection_registration = cls(
            connection=connection,
            created=created,
            delegate_prepared=delegate_prepared,
            setup=setup,
        )


        managed_agents_connection_registration.additional_properties = d
        return managed_agents_connection_registration

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
