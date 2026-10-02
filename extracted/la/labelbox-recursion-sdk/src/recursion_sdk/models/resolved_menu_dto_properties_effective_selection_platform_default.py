from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.resolved_menu_dto_properties_effective_selection_platform_default_kind import ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefaultKind






T = TypeVar("T", bound="ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefault")



@_attrs_define
class ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefault:
    """ The platform harness and model defaults would apply at launch.

        Attributes:
            kind (ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefaultKind): The platform harness and model defaults
                resolve at launch.
     """

    kind: ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefaultKind





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefaultKind(d.pop("kind"))




        resolved_menu_dto_properties_effective_selection_platform_default = cls(
            kind=kind,
        )

        return resolved_menu_dto_properties_effective_selection_platform_default

