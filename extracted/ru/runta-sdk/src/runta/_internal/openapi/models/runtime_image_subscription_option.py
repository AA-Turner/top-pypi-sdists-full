from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="RuntimeImageSubscriptionOption")


@_attrs_define
class RuntimeImageSubscriptionOption:
    """
    Attributes:
        protocols (list[str]):
        secret_preset_ids (list[str]):
    """

    protocols: list[str]
    secret_preset_ids: list[str]

    def to_dict(self) -> dict[str, Any]:
        protocols = self.protocols

        secret_preset_ids = self.secret_preset_ids

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "protocols": protocols,
                "secret_preset_ids": secret_preset_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        protocols = cast(list[str], d.pop("protocols"))

        secret_preset_ids = cast(list[str], d.pop("secret_preset_ids"))

        runtime_image_subscription_option = cls(
            protocols=protocols,
            secret_preset_ids=secret_preset_ids,
        )

        return runtime_image_subscription_option
