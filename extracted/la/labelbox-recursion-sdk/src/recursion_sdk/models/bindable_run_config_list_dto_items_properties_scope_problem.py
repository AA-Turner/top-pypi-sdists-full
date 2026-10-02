from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.bindable_run_config_list_dto_items_properties_scope_problem_level import BindableRunConfigListDtoItemsPropertiesScopeProblemLevel
from uuid import UUID






T = TypeVar("T", bound="BindableRunConfigListDtoItemsPropertiesScopeProblem")



@_attrs_define
class BindableRunConfigListDtoItemsPropertiesScopeProblem:
    """ Problem-level scope — visible only on the specific problem.

        Attributes:
            level (BindableRunConfigListDtoItemsPropertiesScopeProblemLevel): Discriminator: scope is a problem.
            id (UUID): Problem that owns this scope.
     """

    level: BindableRunConfigListDtoItemsPropertiesScopeProblemLevel
    id: UUID





    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        id = str(self.id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "level": level,
            "id": id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        level = BindableRunConfigListDtoItemsPropertiesScopeProblemLevel(d.pop("level"))




        id = UUID(d.pop("id"))




        bindable_run_config_list_dto_items_properties_scope_problem = cls(
            level=level,
            id=id,
        )

        return bindable_run_config_list_dto_items_properties_scope_problem

