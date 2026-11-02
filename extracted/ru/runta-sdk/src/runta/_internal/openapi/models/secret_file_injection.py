from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SecretFileInjection")


@_attrs_define
class SecretFileInjection:
    """Managed credential file populated from a secret.

    Attributes:
        path (str): Delivery path, relative to the guest home directory.
        value_template (str):
    """

    path: str
    value_template: str

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        value_template = self.value_template

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "path": path,
                "value_template": value_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        value_template = d.pop("value_template")

        secret_file_injection = cls(
            path=path,
            value_template=value_template,
        )

        return secret_file_injection
