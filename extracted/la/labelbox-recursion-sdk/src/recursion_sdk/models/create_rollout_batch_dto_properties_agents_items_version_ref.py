from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_rollout_batch_dto_properties_agents_items_version_ref_kind import CreateRolloutBatchDtoPropertiesAgentsItemsVersionRefKind
from uuid import UUID






T = TypeVar("T", bound="CreateRolloutBatchDtoPropertiesAgentsItemsVersionRef")



@_attrs_define
class CreateRolloutBatchDtoPropertiesAgentsItemsVersionRef:
    """ 
        Attributes:
            kind (CreateRolloutBatchDtoPropertiesAgentsItemsVersionRefKind): Reuse an existing locked run-config version as-
                is.
            run_config_version_id (UUID): Existing locked, agent-harness type run-config version to reuse as-is.
     """

    kind: CreateRolloutBatchDtoPropertiesAgentsItemsVersionRefKind
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
        kind = CreateRolloutBatchDtoPropertiesAgentsItemsVersionRefKind(d.pop("kind"))




        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        create_rollout_batch_dto_properties_agents_items_version_ref = cls(
            kind=kind,
            run_config_version_id=run_config_version_id,
        )

        return create_rollout_batch_dto_properties_agents_items_version_ref

