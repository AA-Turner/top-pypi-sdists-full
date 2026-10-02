import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.proposal_workflow_step_instance_status_enum import ProposalWorkflowStepInstanceStatusEnum
from ..models.step_enum import StepEnum

if TYPE_CHECKING:
    from ..models.step_checklist_status import StepChecklistStatus


T = TypeVar("T", bound="ProposalWorkflowStepInstance")


@_attrs_define
class ProposalWorkflowStepInstance:
    """
    Attributes:
        uuid (UUID):
        step (StepEnum):
        step_name (str):
        step_description (str):
        responsible_role (Union[None, str]):
        status (ProposalWorkflowStepInstanceStatusEnum):
        outcome (Union[None, str]): Step-specific outcome (e.g., eligible, feasible, approved).
        outcome_reason (str): Explanation for the outcome (e.g., rejection reason).
        rejection_reason (Union[None, str]):
        internal_notes (Union[None, str]):
        started_at (Union[None, datetime.datetime]): When this step became active.
        completed_at (Union[None, datetime.datetime]):
        completed_by (Union[None, UUID]):
        deadline (Union[None, datetime.datetime]): Computed from started_at + step duration_in_days.
        applicant_visible (bool):
        duration_in_days (Union[None, int]):
        is_required (bool):
        checklist_status (Union['StepChecklistStatus', None]):
    """

    uuid: UUID
    step: StepEnum
    step_name: str
    step_description: str
    responsible_role: Union[None, str]
    status: ProposalWorkflowStepInstanceStatusEnum
    outcome: Union[None, str]
    outcome_reason: str
    rejection_reason: Union[None, str]
    internal_notes: Union[None, str]
    started_at: Union[None, datetime.datetime]
    completed_at: Union[None, datetime.datetime]
    completed_by: Union[None, UUID]
    deadline: Union[None, datetime.datetime]
    applicant_visible: bool
    duration_in_days: Union[None, int]
    is_required: bool
    checklist_status: Union["StepChecklistStatus", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.step_checklist_status import StepChecklistStatus

        uuid = str(self.uuid)

        step = self.step.value

        step_name = self.step_name

        step_description = self.step_description

        responsible_role: Union[None, str]
        responsible_role = self.responsible_role

        status = self.status.value

        outcome: Union[None, str]
        outcome = self.outcome

        outcome_reason = self.outcome_reason

        rejection_reason: Union[None, str]
        rejection_reason = self.rejection_reason

        internal_notes: Union[None, str]
        internal_notes = self.internal_notes

        started_at: Union[None, str]
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: Union[None, str]
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        completed_by: Union[None, str]
        if isinstance(self.completed_by, UUID):
            completed_by = str(self.completed_by)
        else:
            completed_by = self.completed_by

        deadline: Union[None, str]
        if isinstance(self.deadline, datetime.datetime):
            deadline = self.deadline.isoformat()
        else:
            deadline = self.deadline

        applicant_visible = self.applicant_visible

        duration_in_days: Union[None, int]
        duration_in_days = self.duration_in_days

        is_required = self.is_required

        checklist_status: Union[None, dict[str, Any]]
        if isinstance(self.checklist_status, StepChecklistStatus):
            checklist_status = self.checklist_status.to_dict()
        else:
            checklist_status = self.checklist_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "step": step,
                "step_name": step_name,
                "step_description": step_description,
                "responsible_role": responsible_role,
                "status": status,
                "outcome": outcome,
                "outcome_reason": outcome_reason,
                "rejection_reason": rejection_reason,
                "internal_notes": internal_notes,
                "started_at": started_at,
                "completed_at": completed_at,
                "completed_by": completed_by,
                "deadline": deadline,
                "applicant_visible": applicant_visible,
                "duration_in_days": duration_in_days,
                "is_required": is_required,
                "checklist_status": checklist_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.step_checklist_status import StepChecklistStatus

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        step = StepEnum(d.pop("step"))

        step_name = d.pop("step_name")

        step_description = d.pop("step_description")

        def _parse_responsible_role(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        responsible_role = _parse_responsible_role(d.pop("responsible_role"))

        status = ProposalWorkflowStepInstanceStatusEnum(d.pop("status"))

        def _parse_outcome(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        outcome = _parse_outcome(d.pop("outcome"))

        outcome_reason = d.pop("outcome_reason")

        def _parse_rejection_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        rejection_reason = _parse_rejection_reason(d.pop("rejection_reason"))

        def _parse_internal_notes(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        internal_notes = _parse_internal_notes(d.pop("internal_notes"))

        def _parse_started_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        started_at = _parse_started_at(d.pop("started_at"))

        def _parse_completed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        def _parse_completed_by(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_by_type_0 = UUID(data)

                return completed_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        completed_by = _parse_completed_by(d.pop("completed_by"))

        def _parse_deadline(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deadline_type_0 = isoparse(data)

                return deadline_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        deadline = _parse_deadline(d.pop("deadline"))

        applicant_visible = d.pop("applicant_visible")

        def _parse_duration_in_days(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        duration_in_days = _parse_duration_in_days(d.pop("duration_in_days"))

        is_required = d.pop("is_required")

        def _parse_checklist_status(data: object) -> Union["StepChecklistStatus", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                checklist_status_type_1 = StepChecklistStatus.from_dict(data)

                return checklist_status_type_1
            except:  # noqa: E722
                pass
            return cast(Union["StepChecklistStatus", None], data)

        checklist_status = _parse_checklist_status(d.pop("checklist_status"))

        proposal_workflow_step_instance = cls(
            uuid=uuid,
            step=step,
            step_name=step_name,
            step_description=step_description,
            responsible_role=responsible_role,
            status=status,
            outcome=outcome,
            outcome_reason=outcome_reason,
            rejection_reason=rejection_reason,
            internal_notes=internal_notes,
            started_at=started_at,
            completed_at=completed_at,
            completed_by=completed_by,
            deadline=deadline,
            applicant_visible=applicant_visible,
            duration_in_days=duration_in_days,
            is_required=is_required,
            checklist_status=checklist_status,
        )

        proposal_workflow_step_instance.additional_properties = d
        return proposal_workflow_step_instance

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
