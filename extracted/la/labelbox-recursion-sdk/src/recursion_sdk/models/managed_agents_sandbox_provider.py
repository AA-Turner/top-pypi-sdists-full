from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsSandboxProvider")



@_attrs_define
class ManagedAgentsSandboxProvider:
    """ One sandbox runtime this deployment can provision compute on. Listed so a caller can pick a sandbox_provider when
    creating an environment; this is static service capability, not organization data.

        Example:
            {'default': True, 'description': 'example', 'display_name': 'example-name', 'provider': 'example',
                'requires_credential': 'example'}

        Attributes:
            display_name (str): Human-readable name for this runtime, for pickers and listings.
            provider (str): Identifier of the sandbox runtime, used as the sandbox_provider value when creating an
                environment.
            default (bool | Unset): True on the runtime used when an environment does not name one. At most one provider is
                the default.
            description (str | Unset): Short explanation of what this runtime provides and when to choose it.
            requires_credential (str | Unset): Name of the deployment-level credential this runtime needs before it can
                provision sandboxes. Empty when the runtime needs none.
     """

    display_name: str
    provider: str
    default: bool | Unset = UNSET
    description: str | Unset = UNSET
    requires_credential: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        provider = self.provider

        default = self.default

        description = self.description

        requires_credential = self.requires_credential


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "display_name": display_name,
            "provider": provider,
        })
        if default is not UNSET:
            field_dict["default"] = default
        if description is not UNSET:
            field_dict["description"] = description
        if requires_credential is not UNSET:
            field_dict["requires_credential"] = requires_credential

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        display_name = d.pop("display_name")

        provider = d.pop("provider")

        default = d.pop("default", UNSET)

        description = d.pop("description", UNSET)

        requires_credential = d.pop("requires_credential", UNSET)

        managed_agents_sandbox_provider = cls(
            display_name=display_name,
            provider=provider,
            default=default,
            description=description,
            requires_credential=requires_credential,
        )


        managed_agents_sandbox_provider.additional_properties = d
        return managed_agents_sandbox_provider

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
