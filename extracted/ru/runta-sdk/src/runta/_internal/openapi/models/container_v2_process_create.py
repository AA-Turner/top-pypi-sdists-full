from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.container_v2_process_create_spec import ContainerV2ProcessCreateSpec


T = TypeVar("T", bound="ContainerV2ProcessCreate")


@_attrs_define
class ContainerV2ProcessCreate:
    """
    Attributes:
        process_id (str):
        spec (ContainerV2ProcessCreateSpec):
    """

    process_id: str
    spec: ContainerV2ProcessCreateSpec
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        process_id = self.process_id

        spec = self.spec.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "process_id": process_id,
                "spec": spec,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_v2_process_create_spec import (
            ContainerV2ProcessCreateSpec,
        )

        d = dict(src_dict)
        process_id = d.pop("process_id")

        spec = ContainerV2ProcessCreateSpec.from_dict(d.pop("spec"))

        container_v2_process_create = cls(
            process_id=process_id,
            spec=spec,
        )

        container_v2_process_create.additional_properties = d
        return container_v2_process_create

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
