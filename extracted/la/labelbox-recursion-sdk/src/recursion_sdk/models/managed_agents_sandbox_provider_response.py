from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ManagedAgentsSandboxProviderResponse")



@_attrs_define
class ManagedAgentsSandboxProviderResponse:
    """ One sandbox runtime this deployment can provision compute on.

        Example:
            {'default': True, 'description': 'example', 'displayName': 'example', 'provider': 'example',
                'requiresCredential': 'example'}

        Attributes:
            default (bool): Whether this runtime is the default. At most one provider is the default.
            description (str): Short explanation of this runtime and when to choose it.
            display_name (str): Human-readable name for this runtime.
            provider (str): Identifier of the sandbox runtime, used when creating an environment.
            requires_credential (None | str): Deployment credential name required by this runtime, or null if none is
                needed.
     """

    default: bool
    description: str
    display_name: str
    provider: str
    requires_credential: None | str





    def to_dict(self) -> dict[str, Any]:
        default = self.default

        description = self.description

        display_name = self.display_name

        provider = self.provider

        requires_credential: None | str
        requires_credential = self.requires_credential


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "default": default,
            "description": description,
            "displayName": display_name,
            "provider": provider,
            "requiresCredential": requires_credential,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default = d.pop("default")

        description = d.pop("description")

        display_name = d.pop("displayName")

        provider = d.pop("provider")

        def _parse_requires_credential(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        requires_credential = _parse_requires_credential(d.pop("requiresCredential"))


        managed_agents_sandbox_provider_response = cls(
            default=default,
            description=description,
            display_name=display_name,
            provider=provider,
            requires_credential=requires_credential,
        )

        return managed_agents_sandbox_provider_response

