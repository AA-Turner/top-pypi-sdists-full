from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.resolved_menu_dto_properties_effective_selection_versioned_kind import ResolvedMenuDtoPropertiesEffectiveSelectionVersionedKind
from uuid import UUID






T = TypeVar("T", bound="ResolvedMenuDtoPropertiesEffectiveSelectionVersioned")



@_attrs_define
class ResolvedMenuDtoPropertiesEffectiveSelectionVersioned:
    """ A locked run-config version that would resolve at launch.

        Attributes:
            kind (ResolvedMenuDtoPropertiesEffectiveSelectionVersionedKind): A locked run-config version resolves at launch.
            run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver / grader / QA / synthesizer
                config.
            run_config_version_id (UUID): Stable run-config-version identifier (UUID). Points at one specific version of a
                run config.
            name (str): Display name of the run config.
            version_number (int): Version number of the effective run-config version.
     """

    kind: ResolvedMenuDtoPropertiesEffectiveSelectionVersionedKind
    run_config_id: UUID
    run_config_version_id: UUID
    name: str
    version_number: int





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        run_config_id = str(self.run_config_id)

        run_config_version_id = str(self.run_config_version_id)

        name = self.name

        version_number = self.version_number


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "runConfigId": run_config_id,
            "runConfigVersionId": run_config_version_id,
            "name": name,
            "versionNumber": version_number,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = ResolvedMenuDtoPropertiesEffectiveSelectionVersionedKind(d.pop("kind"))




        run_config_id = UUID(d.pop("runConfigId"))




        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        name = d.pop("name")

        version_number = d.pop("versionNumber")

        resolved_menu_dto_properties_effective_selection_versioned = cls(
            kind=kind,
            run_config_id=run_config_id,
            run_config_version_id=run_config_version_id,
            name=name,
            version_number=version_number,
        )

        return resolved_menu_dto_properties_effective_selection_versioned

