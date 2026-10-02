from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_with_version_list_dto_items_properties_scope_problem_level import RunConfigWithVersionListDtoItemsPropertiesScopeProblemLevel
from uuid import UUID






T = TypeVar("T", bound="RunConfigWithVersionListDtoItemsPropertiesScopeProblem")



@_attrs_define
class RunConfigWithVersionListDtoItemsPropertiesScopeProblem:
    """ Problem-level scope — visible only on the specific problem.

        Attributes:
            level (RunConfigWithVersionListDtoItemsPropertiesScopeProblemLevel): Discriminator: scope is a problem.
            id (UUID): Problem that owns this scope.
     """

    level: RunConfigWithVersionListDtoItemsPropertiesScopeProblemLevel
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
        level = RunConfigWithVersionListDtoItemsPropertiesScopeProblemLevel(d.pop("level"))




        id = UUID(d.pop("id"))




        run_config_with_version_list_dto_items_properties_scope_problem = cls(
            level=level,
            id=id,
        )

        return run_config_with_version_list_dto_items_properties_scope_problem

