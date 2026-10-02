from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsUpdateEnvironmentRequestEnvVars")



@_attrs_define
class ManagedAgentsUpdateEnvironmentRequestEnvVars:
    """ Plaintext environment variables exported in the sandbox. They become the whole container environment, including the
    runner entrypoint's, so PATH is refused (env_vars.PATH): managed images select /workspace/.venv themselves. A Runs
    session using one-time setup after its runner changes also refuses startup-hook names such as BASH_ENV, HOME,
    PYTHONPATH, and LD_PRELOAD; re-test to capture a compatible image instead. Never put secrets here; use secrets
    instead. On update, omit to keep the current variables; send {} to clear them.

     """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        managed_agents_update_environment_request_env_vars = cls(
        )


        managed_agents_update_environment_request_env_vars.additional_properties = d
        return managed_agents_update_environment_request_env_vars

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
