from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define


T = TypeVar("T", bound="ForwarderTypeTransform")


@_attrs_define
class ForwarderTypeTransform:
    """Default transform shipped with the type.

    Attributes:
        type_ (str): Engine name. Today only `JSONATA`.
        default (str): Default template; customers can override per forwarder.
    """

    type_: str
    default: str

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        default = self.default

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "default": default,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        default = d.pop("default")

        forwarder_type_transform = cls(
            type_=type_,
            default=default,
        )

        return forwarder_type_transform
