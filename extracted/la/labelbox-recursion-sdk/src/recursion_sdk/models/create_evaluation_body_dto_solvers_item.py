from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_evaluation_body_dto_solvers_item_checkpoint_context import CreateEvaluationBodyDtoSolversItemCheckpointContext





T = TypeVar("T", bound="CreateEvaluationBodyDtoSolversItem")



@_attrs_define
class CreateEvaluationBodyDtoSolversItem:
    """ Configuration for one solver to include in a new evaluation.

        Attributes:
            display_name (str): Human-readable label distinguishing this solver in evaluation results.
            run_config_version_id (UUID): Locked run-config version (kind "solver") that governs this solver's invocation.
            concurrency (int | Unset): Maximum solver runs this solver keeps alive on the agent service at once (1-2000).
                Omitted means the platform default applies.
            checkpoint_context (CreateEvaluationBodyDtoSolversItemCheckpointContext | Unset): Optional training-checkpoint
                context for this solver. When present, the solver container receives /input/checkpoint.json. A present
                checkpointContext with a null checkpointRef fails the evaluation fast, before any dispatch -- never silently
                runs the solver without its checkpoint.
     """

    display_name: str
    run_config_version_id: UUID
    concurrency: int | Unset = UNSET
    checkpoint_context: CreateEvaluationBodyDtoSolversItemCheckpointContext | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_evaluation_body_dto_solvers_item_checkpoint_context import CreateEvaluationBodyDtoSolversItemCheckpointContext # noqa: PLC0415
        display_name = self.display_name

        run_config_version_id = str(self.run_config_version_id)

        concurrency = self.concurrency

        checkpoint_context: dict[str, Any] | Unset = UNSET
        if not isinstance(self.checkpoint_context, Unset):
            checkpoint_context = self.checkpoint_context.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "displayName": display_name,
            "runConfigVersionId": run_config_version_id,
        })
        if concurrency is not UNSET:
            field_dict["concurrency"] = concurrency
        if checkpoint_context is not UNSET:
            field_dict["checkpointContext"] = checkpoint_context

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_evaluation_body_dto_solvers_item_checkpoint_context import CreateEvaluationBodyDtoSolversItemCheckpointContext # noqa: PLC0415
        d = dict(src_dict)
        display_name = d.pop("displayName")

        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        concurrency = d.pop("concurrency", UNSET)

        _checkpoint_context = d.pop("checkpointContext", UNSET)
        checkpoint_context: CreateEvaluationBodyDtoSolversItemCheckpointContext | Unset
        if isinstance(_checkpoint_context,  Unset):
            checkpoint_context = UNSET
        else:
            checkpoint_context = CreateEvaluationBodyDtoSolversItemCheckpointContext.from_dict(_checkpoint_context)




        create_evaluation_body_dto_solvers_item = cls(
            display_name=display_name,
            run_config_version_id=run_config_version_id,
            concurrency=concurrency,
            checkpoint_context=checkpoint_context,
        )


        create_evaluation_body_dto_solvers_item.additional_properties = d
        return create_evaluation_body_dto_solvers_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
