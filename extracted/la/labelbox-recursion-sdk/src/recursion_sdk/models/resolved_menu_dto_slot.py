from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.resolved_menu_dto_slot_role import ResolvedMenuDtoSlotRole
from uuid import UUID






T = TypeVar("T", bound="ResolvedMenuDtoSlot")



@_attrs_define
class ResolvedMenuDtoSlot:
    """ An environment + role binding point for a curated run-config menu.

        Attributes:
            environment_id (UUID): Stable environment identifier (UUID).
            role (ResolvedMenuDtoSlotRole): The role a run config plays at a binding slot: solver, grader, qa, or
                synthesizer.
     """

    environment_id: UUID
    role: ResolvedMenuDtoSlotRole





    def to_dict(self) -> dict[str, Any]:
        environment_id = str(self.environment_id)

        role = self.role.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "environmentId": environment_id,
            "role": role,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        environment_id = UUID(d.pop("environmentId"))




        role = ResolvedMenuDtoSlotRole(d.pop("role"))




        resolved_menu_dto_slot = cls(
            environment_id=environment_id,
            role=role,
        )

        return resolved_menu_dto_slot

