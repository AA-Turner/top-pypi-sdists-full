from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.inherited_run_config_default_dto_scope_level import InheritedRunConfigDefaultDtoScopeLevel
from uuid import UUID






T = TypeVar("T", bound="InheritedRunConfigDefaultDto")



@_attrs_define
class InheritedRunConfigDefaultDto:
    """ Resolved scope-default lookup for the env-overview picker — what default would be inherited at this env (or at a
    specific problem beneath it) along with enough metadata to render an "inherited" label without a follow-up fetch.

        Attributes:
            run_config_version_id (UUID): Locked version that would be inherited at this scope.
            run_config_id (UUID): Run-config identity that owns the inherited version.
            run_config_name (str): Display name of the inherited run-config identity.
            version_number (int): Version number of the inherited version. Example: 2.
            scope_level (InheritedRunConfigDefaultDtoScopeLevel): Scope level the inherited default lives at.
     """

    run_config_version_id: UUID
    run_config_id: UUID
    run_config_name: str
    version_number: int
    scope_level: InheritedRunConfigDefaultDtoScopeLevel





    def to_dict(self) -> dict[str, Any]:
        run_config_version_id = str(self.run_config_version_id)

        run_config_id = str(self.run_config_id)

        run_config_name = self.run_config_name

        version_number = self.version_number

        scope_level = self.scope_level.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runConfigVersionId": run_config_version_id,
            "runConfigId": run_config_id,
            "runConfigName": run_config_name,
            "versionNumber": version_number,
            "scopeLevel": scope_level,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        run_config_id = UUID(d.pop("runConfigId"))




        run_config_name = d.pop("runConfigName")

        version_number = d.pop("versionNumber")

        scope_level = InheritedRunConfigDefaultDtoScopeLevel(d.pop("scopeLevel"))




        inherited_run_config_default_dto = cls(
            run_config_version_id=run_config_version_id,
            run_config_id=run_config_id,
            run_config_name=run_config_name,
            version_number=version_number,
            scope_level=scope_level,
        )

        return inherited_run_config_default_dto

