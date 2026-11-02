from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.secret_injection_action import SecretInjectionAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="SecretEgressInjection")


@_attrs_define
class SecretEgressInjection:
    """HTTP egress credential populated from a secret.

    Attributes:
        host_pattern (str):
        action (SecretInjectionAction): Where an egress secret is injected.
        name (str):
        value_template (str):
        path_pattern (None | str | Unset):
    """

    host_pattern: str
    action: SecretInjectionAction
    name: str
    value_template: str
    path_pattern: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        host_pattern = self.host_pattern

        action = self.action.value

        name = self.name

        value_template = self.value_template

        path_pattern: None | str | Unset
        if isinstance(self.path_pattern, Unset):
            path_pattern = UNSET
        else:
            path_pattern = self.path_pattern

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "host_pattern": host_pattern,
                "action": action,
                "name": name,
                "value_template": value_template,
            }
        )
        if path_pattern is not UNSET:
            field_dict["path_pattern"] = path_pattern

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        host_pattern = d.pop("host_pattern")

        action = SecretInjectionAction(d.pop("action"))

        name = d.pop("name")

        value_template = d.pop("value_template")

        def _parse_path_pattern(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        path_pattern = _parse_path_pattern(d.pop("path_pattern", UNSET))

        secret_egress_injection = cls(
            host_pattern=host_pattern,
            action=action,
            name=name,
            value_template=value_template,
            path_pattern=path_pattern,
        )

        return secret_egress_injection
