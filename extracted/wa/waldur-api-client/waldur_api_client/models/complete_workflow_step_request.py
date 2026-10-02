from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.outcome_enum import OutcomeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CompleteWorkflowStepRequest")


@_attrs_define
class CompleteWorkflowStepRequest:
    """
    Attributes:
        step_uuid (UUID): UUID of the workflow step instance the client believes is active. Used to detect concurrent
            step transitions.
        outcome (OutcomeEnum):
        outcome_reason (Union[Unset, str]): Explanation for the outcome. Default: ''.
        internal_notes (Union[Unset, str]): Internal notes captured by the call-management team. Stored on the step
            instance and never returned to applicants. Default: ''.
    """

    step_uuid: UUID
    outcome: OutcomeEnum
    outcome_reason: Union[Unset, str] = ""
    internal_notes: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        step_uuid = str(self.step_uuid)

        outcome = self.outcome.value

        outcome_reason = self.outcome_reason

        internal_notes = self.internal_notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step_uuid": step_uuid,
                "outcome": outcome,
            }
        )
        if outcome_reason is not UNSET:
            field_dict["outcome_reason"] = outcome_reason
        if internal_notes is not UNSET:
            field_dict["internal_notes"] = internal_notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        step_uuid = UUID(d.pop("step_uuid"))

        outcome = OutcomeEnum(d.pop("outcome"))

        outcome_reason = d.pop("outcome_reason", UNSET)

        internal_notes = d.pop("internal_notes", UNSET)

        complete_workflow_step_request = cls(
            step_uuid=step_uuid,
            outcome=outcome,
            outcome_reason=outcome_reason,
            internal_notes=internal_notes,
        )

        complete_workflow_step_request.additional_properties = d
        return complete_workflow_step_request

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
