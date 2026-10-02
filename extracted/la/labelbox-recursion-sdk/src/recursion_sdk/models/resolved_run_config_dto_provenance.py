from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.resolved_run_config_dto_properties_provenance_properties_scope_env import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeEnv
  from ..models.resolved_run_config_dto_properties_provenance_properties_scope_org import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeOrg
  from ..models.resolved_run_config_dto_properties_provenance_properties_scope_problem import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeProblem
  from ..models.resolved_run_config_dto_properties_provenance_properties_scope_system import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeSystem





T = TypeVar("T", bound="ResolvedRunConfigDtoProvenance")



@_attrs_define
class ResolvedRunConfigDtoProvenance:
    """ Which run-config / version this resolved to, for "this run came from …" displays.

        Attributes:
            run_config_id (UUID): Owning run-config identity.
            run_config_version_id (UUID): Specific version that produced the selected pre-consumer payload.
            run_config_name (str): Display name of the resolved run-config identity.
            scope (ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeEnv |
                ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeOrg |
                ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeProblem |
                ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeSystem): Scope the resolved run-config lives at.
            version_number (int): Version number of the resolved version. Example: 3.
     """

    run_config_id: UUID
    run_config_version_id: UUID
    run_config_name: str
    scope: ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeEnv | ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeOrg | ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeProblem | ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeSystem
    version_number: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.resolved_run_config_dto_properties_provenance_properties_scope_env import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeEnv # noqa: PLC0415
        from ..models.resolved_run_config_dto_properties_provenance_properties_scope_org import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeOrg # noqa: PLC0415
        from ..models.resolved_run_config_dto_properties_provenance_properties_scope_problem import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeProblem # noqa: PLC0415
        from ..models.resolved_run_config_dto_properties_provenance_properties_scope_system import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeSystem # noqa: PLC0415
        run_config_id = str(self.run_config_id)

        run_config_version_id = str(self.run_config_version_id)

        run_config_name = self.run_config_name

        scope: dict[str, Any]
        if isinstance(self.scope, ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeSystem):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeOrg):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeEnv):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()


        version_number = self.version_number


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runConfigId": run_config_id,
            "runConfigVersionId": run_config_version_id,
            "runConfigName": run_config_name,
            "scope": scope,
            "versionNumber": version_number,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resolved_run_config_dto_properties_provenance_properties_scope_env import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeEnv # noqa: PLC0415
        from ..models.resolved_run_config_dto_properties_provenance_properties_scope_org import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeOrg # noqa: PLC0415
        from ..models.resolved_run_config_dto_properties_provenance_properties_scope_problem import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeProblem # noqa: PLC0415
        from ..models.resolved_run_config_dto_properties_provenance_properties_scope_system import ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeSystem # noqa: PLC0415
        d = dict(src_dict)
        run_config_id = UUID(d.pop("runConfigId"))




        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        run_config_name = d.pop("runConfigName")

        def _parse_scope(data: object) -> ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeEnv | ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeOrg | ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeProblem | ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeSystem:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_0 = ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeSystem.from_dict(data)



                return scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_1 = ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeOrg.from_dict(data)



                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_2 = ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeEnv.from_dict(data)



                return scope_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            scope_type_3 = ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeProblem.from_dict(data)



            return scope_type_3

        scope = _parse_scope(d.pop("scope"))


        version_number = d.pop("versionNumber")

        resolved_run_config_dto_provenance = cls(
            run_config_id=run_config_id,
            run_config_version_id=run_config_version_id,
            run_config_name=run_config_name,
            scope=scope,
            version_number=version_number,
        )

        return resolved_run_config_dto_provenance

