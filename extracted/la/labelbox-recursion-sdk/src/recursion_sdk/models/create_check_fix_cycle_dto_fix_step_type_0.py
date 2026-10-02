from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_check_fix_cycle_dto_fix_step_type_0_kind import CreateCheckFixCycleDtoFixStepType0Kind
from uuid import UUID






T = TypeVar("T", bound="CreateCheckFixCycleDtoFixStepType0")



@_attrs_define
class CreateCheckFixCycleDtoFixStepType0:
    """ 
        Attributes:
            kind (CreateCheckFixCycleDtoFixStepType0Kind): Discriminator for the run_config fix-step arm.
            run_config_version_id (UUID): Locked, agent-harness run-config version executed as the fix child.
     """

    kind: CreateCheckFixCycleDtoFixStepType0Kind
    run_config_version_id: UUID





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        run_config_version_id = str(self.run_config_version_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "runConfigVersionId": run_config_version_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = CreateCheckFixCycleDtoFixStepType0Kind(d.pop("kind"))




        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        create_check_fix_cycle_dto_fix_step_type_0 = cls(
            kind=kind,
            run_config_version_id=run_config_version_id,
        )

        return create_check_fix_cycle_dto_fix_step_type_0

