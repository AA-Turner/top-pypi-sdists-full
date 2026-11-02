from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.managed_model_provider_reference_type import (
    ManagedModelProviderReferenceType,
)

T = TypeVar("T", bound="ManagedModelProviderReference")


@_attrs_define
class ManagedModelProviderReference:
    """
    Attributes:
        type_ (ManagedModelProviderReferenceType):
        id (str):
    """

    type_: ManagedModelProviderReferenceType
    id: str

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        id = self.id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ManagedModelProviderReferenceType(d.pop("type"))

        id = d.pop("id")

        managed_model_provider_reference = cls(
            type_=type_,
            id=id,
        )

        return managed_model_provider_reference
