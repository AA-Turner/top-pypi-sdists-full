from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.bindable_run_config_list_dto_items_properties_scope_env_level import BindableRunConfigListDtoItemsPropertiesScopeEnvLevel
from uuid import UUID






T = TypeVar("T", bound="BindableRunConfigListDtoItemsPropertiesScopeEnv")



@_attrs_define
class BindableRunConfigListDtoItemsPropertiesScopeEnv:
    """ Environment-level scope — visible only within the environment.

        Attributes:
            level (BindableRunConfigListDtoItemsPropertiesScopeEnvLevel): Discriminator: scope is an environment.
            id (UUID): Environment that owns this scope.
     """

    level: BindableRunConfigListDtoItemsPropertiesScopeEnvLevel
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
        level = BindableRunConfigListDtoItemsPropertiesScopeEnvLevel(d.pop("level"))




        id = UUID(d.pop("id"))




        bindable_run_config_list_dto_items_properties_scope_env = cls(
            level=level,
            id=id,
        )

        return bindable_run_config_list_dto_items_properties_scope_env

