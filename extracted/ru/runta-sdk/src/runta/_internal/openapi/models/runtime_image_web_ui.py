from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RuntimeImageWebUi")


@_attrs_define
class RuntimeImageWebUi:
    """A browser surface the image serves. It is published through the runtime's ingress on demand, behind a session
    gateway, rather than being exposed for the lifetime of the runtime.

        Attributes:
            port (int): Guest-local port the gateway listens on.
    """

    port: int

    def to_dict(self) -> dict[str, Any]:
        port = self.port

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "port": port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        port = d.pop("port")

        runtime_image_web_ui = cls(
            port=port,
        )

        return runtime_image_web_ui
