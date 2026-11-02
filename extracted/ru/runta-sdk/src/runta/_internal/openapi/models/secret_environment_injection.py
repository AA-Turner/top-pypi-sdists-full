from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SecretEnvironmentInjection")


@_attrs_define
class SecretEnvironmentInjection:
    """Environment variable populated from a secret.

    Attributes:
        name (str):
        value_template (str):
    """

    name: str
    value_template: str

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value_template = self.value_template

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "value_template": value_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        value_template = d.pop("value_template")

        secret_environment_injection = cls(
            name=name,
            value_template=value_template,
        )

        return secret_environment_injection
