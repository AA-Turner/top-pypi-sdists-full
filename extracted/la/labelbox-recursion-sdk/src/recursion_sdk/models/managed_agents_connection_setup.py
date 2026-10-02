from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsConnectionSetup")



@_attrs_define
class ManagedAgentsConnectionSetup:
    """ The trust a customer must grant at the provider before a directly registered connection can activate. Regenerated on
    every registration call, so a lost response is recovered by registering the same identifier again.

        Example:
            {'delegate_principal': 'example', 'grant_command': 'example', 'role': 'user', 'target_principal': 'example'}

        Attributes:
            delegate_principal (str): The platform-side principal the customer grants trust to. For Google Cloud this is the
                organization's delegate service-account email; it is derived from the authenticated organization and is the only
                thing the customer is told to trust.
            grant_command (str): A ready-to-run provider CLI command that performs the grant described by the other fields.
                Convenience only; the identifiers are authoritative.
            role (str): The provider role the customer grants the delegate principal on the target, e.g.
                roles/iam.serviceAccountTokenCreator.
            target_principal (str): The customer-owned principal the connection represents, normalized. Matches the
                connection's external_id.
     """

    delegate_principal: str
    grant_command: str
    role: str
    target_principal: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        delegate_principal = self.delegate_principal

        grant_command = self.grant_command

        role = self.role

        target_principal = self.target_principal


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "delegate_principal": delegate_principal,
            "grant_command": grant_command,
            "role": role,
            "target_principal": target_principal,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        delegate_principal = d.pop("delegate_principal")

        grant_command = d.pop("grant_command")

        role = d.pop("role")

        target_principal = d.pop("target_principal")

        managed_agents_connection_setup = cls(
            delegate_principal=delegate_principal,
            grant_command=grant_command,
            role=role,
            target_principal=target_principal,
        )


        managed_agents_connection_setup.additional_properties = d
        return managed_agents_connection_setup

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
