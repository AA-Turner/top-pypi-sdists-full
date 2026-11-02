from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RuntimeImageDiskCapability")


@_attrs_define
class RuntimeImageDiskCapability:
    """
    Attributes:
        minimum_gib (int):
        maximum_gib (int):
        default_gib (int):
        step_gib (int):
    """

    minimum_gib: int
    maximum_gib: int
    default_gib: int
    step_gib: int

    def to_dict(self) -> dict[str, Any]:
        minimum_gib = self.minimum_gib

        maximum_gib = self.maximum_gib

        default_gib = self.default_gib

        step_gib = self.step_gib

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "minimum_gib": minimum_gib,
                "maximum_gib": maximum_gib,
                "default_gib": default_gib,
                "step_gib": step_gib,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        minimum_gib = d.pop("minimum_gib")

        maximum_gib = d.pop("maximum_gib")

        default_gib = d.pop("default_gib")

        step_gib = d.pop("step_gib")

        runtime_image_disk_capability = cls(
            minimum_gib=minimum_gib,
            maximum_gib=maximum_gib,
            default_gib=default_gib,
            step_gib=step_gib,
        )

        return runtime_image_disk_capability
