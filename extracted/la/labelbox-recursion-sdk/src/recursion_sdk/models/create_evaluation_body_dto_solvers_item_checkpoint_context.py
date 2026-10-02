from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_evaluation_body_dto_solvers_item_checkpoint_context_context import CreateEvaluationBodyDtoSolversItemCheckpointContextContext





T = TypeVar("T", bound="CreateEvaluationBodyDtoSolversItemCheckpointContext")



@_attrs_define
class CreateEvaluationBodyDtoSolversItemCheckpointContext:
    """ Optional training-checkpoint context for this solver. When present, the solver container receives
    /input/checkpoint.json. A present checkpointContext with a null checkpointRef fails the evaluation fast, before any
    dispatch -- never silently runs the solver without its checkpoint.

        Attributes:
            checkpoint_ref (None | str): Opaque training-checkpoint reference the solver container should load. Never parsed
                by the platform.
            step (int): Training step the checkpoint was taken at.
            context (CreateEvaluationBodyDtoSolversItemCheckpointContextContext | Unset): Opaque, provider-owned payload
                relayed byte-identical from the source checkpoint announcement's own context -- never parsed by the platform.
     """

    checkpoint_ref: None | str
    step: int
    context: CreateEvaluationBodyDtoSolversItemCheckpointContextContext | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_evaluation_body_dto_solvers_item_checkpoint_context_context import CreateEvaluationBodyDtoSolversItemCheckpointContextContext # noqa: PLC0415
        checkpoint_ref: None | str
        checkpoint_ref = self.checkpoint_ref

        step = self.step

        context: dict[str, Any] | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "checkpointRef": checkpoint_ref,
            "step": step,
        })
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_evaluation_body_dto_solvers_item_checkpoint_context_context import CreateEvaluationBodyDtoSolversItemCheckpointContextContext # noqa: PLC0415
        d = dict(src_dict)
        def _parse_checkpoint_ref(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        checkpoint_ref = _parse_checkpoint_ref(d.pop("checkpointRef"))


        step = d.pop("step")

        _context = d.pop("context", UNSET)
        context: CreateEvaluationBodyDtoSolversItemCheckpointContextContext | Unset
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = CreateEvaluationBodyDtoSolversItemCheckpointContextContext.from_dict(_context)




        create_evaluation_body_dto_solvers_item_checkpoint_context = cls(
            checkpoint_ref=checkpoint_ref,
            step=step,
            context=context,
        )


        create_evaluation_body_dto_solvers_item_checkpoint_context.additional_properties = d
        return create_evaluation_body_dto_solvers_item_checkpoint_context

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
