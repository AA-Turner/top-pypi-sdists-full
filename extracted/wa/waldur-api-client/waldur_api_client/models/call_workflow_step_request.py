from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.allocation_time_enum import AllocationTimeEnum
from ..models.blank_enum import BlankEnum
from ..models.responsible_role_enum import ResponsibleRoleEnum
from ..models.step_enum import StepEnum
from ..models.transition_mode_enum import TransitionModeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_criterion_request import WorkflowCriterionRequest


T = TypeVar("T", bound="CallWorkflowStepRequest")


@_attrs_define
class CallWorkflowStepRequest:
    """
    Attributes:
        step (StepEnum):
        is_enabled (Union[Unset, bool]): Whether this step is enabled. Disabled steps are skipped.
        duration_in_days (Union[None, Unset, int]): Duration in days. Used to calculate deadlines.
        checklist (Union[None, UUID, Unset]):
        checklist_required (Union[Unset, bool]): When the step has a checklist, block completion until its required
            questions are answered. Set False to make the checklist advisory.
        blind_review (Union[Unset, bool]): Evaluators cannot see each other's assessments.
        requires_coi_confirmation (Union[Unset, bool]): Evaluator must confirm absence of conflict of interest.
        min_reviewers (Union[None, Unset, int]): Minimum reviews required before step can complete.
        min_score_threshold (Union[None, Unset, str]): Minimum average score required before this step can complete (a
            completion gate; it does not auto-reject lower scores).
        applicant_visible (Union[Unset, bool]): Whether the applicant can see step details (not just status).
        responsible_role (Union[BlankEnum, None, ResponsibleRoleEnum, Unset]): Role expected to act on this step.
        transition_mode (Union[Unset, TransitionModeEnum]):
        include_award_response (Union[Unset, bool]): Allocation decision: require applicant award response after
            decision.
        allocation_time (Union[Unset, AllocationTimeEnum]):
        display_order (Union[None, Unset, int]): Optional override of catalog ordering.
        criteria (Union[Unset, list['WorkflowCriterionRequest']]):
    """

    step: StepEnum
    is_enabled: Union[Unset, bool] = UNSET
    duration_in_days: Union[None, Unset, int] = UNSET
    checklist: Union[None, UUID, Unset] = UNSET
    checklist_required: Union[Unset, bool] = UNSET
    blind_review: Union[Unset, bool] = UNSET
    requires_coi_confirmation: Union[Unset, bool] = UNSET
    min_reviewers: Union[None, Unset, int] = UNSET
    min_score_threshold: Union[None, Unset, str] = UNSET
    applicant_visible: Union[Unset, bool] = UNSET
    responsible_role: Union[BlankEnum, None, ResponsibleRoleEnum, Unset] = UNSET
    transition_mode: Union[Unset, TransitionModeEnum] = UNSET
    include_award_response: Union[Unset, bool] = UNSET
    allocation_time: Union[Unset, AllocationTimeEnum] = UNSET
    display_order: Union[None, Unset, int] = UNSET
    criteria: Union[Unset, list["WorkflowCriterionRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        step = self.step.value

        is_enabled = self.is_enabled

        duration_in_days: Union[None, Unset, int]
        if isinstance(self.duration_in_days, Unset):
            duration_in_days = UNSET
        else:
            duration_in_days = self.duration_in_days

        checklist: Union[None, Unset, str]
        if isinstance(self.checklist, Unset):
            checklist = UNSET
        elif isinstance(self.checklist, UUID):
            checklist = str(self.checklist)
        else:
            checklist = self.checklist

        checklist_required = self.checklist_required

        blind_review = self.blind_review

        requires_coi_confirmation = self.requires_coi_confirmation

        min_reviewers: Union[None, Unset, int]
        if isinstance(self.min_reviewers, Unset):
            min_reviewers = UNSET
        else:
            min_reviewers = self.min_reviewers

        min_score_threshold: Union[None, Unset, str]
        if isinstance(self.min_score_threshold, Unset):
            min_score_threshold = UNSET
        else:
            min_score_threshold = self.min_score_threshold

        applicant_visible = self.applicant_visible

        responsible_role: Union[None, Unset, str]
        if isinstance(self.responsible_role, Unset):
            responsible_role = UNSET
        elif isinstance(self.responsible_role, ResponsibleRoleEnum):
            responsible_role = self.responsible_role.value
        elif isinstance(self.responsible_role, BlankEnum):
            responsible_role = self.responsible_role.value
        else:
            responsible_role = self.responsible_role

        transition_mode: Union[Unset, str] = UNSET
        if not isinstance(self.transition_mode, Unset):
            transition_mode = self.transition_mode.value

        include_award_response = self.include_award_response

        allocation_time: Union[Unset, str] = UNSET
        if not isinstance(self.allocation_time, Unset):
            allocation_time = self.allocation_time.value

        display_order: Union[None, Unset, int]
        if isinstance(self.display_order, Unset):
            display_order = UNSET
        else:
            display_order = self.display_order

        criteria: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.criteria, Unset):
            criteria = []
            for criteria_item_data in self.criteria:
                criteria_item = criteria_item_data.to_dict()
                criteria.append(criteria_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step": step,
            }
        )
        if is_enabled is not UNSET:
            field_dict["is_enabled"] = is_enabled
        if duration_in_days is not UNSET:
            field_dict["duration_in_days"] = duration_in_days
        if checklist is not UNSET:
            field_dict["checklist"] = checklist
        if checklist_required is not UNSET:
            field_dict["checklist_required"] = checklist_required
        if blind_review is not UNSET:
            field_dict["blind_review"] = blind_review
        if requires_coi_confirmation is not UNSET:
            field_dict["requires_coi_confirmation"] = requires_coi_confirmation
        if min_reviewers is not UNSET:
            field_dict["min_reviewers"] = min_reviewers
        if min_score_threshold is not UNSET:
            field_dict["min_score_threshold"] = min_score_threshold
        if applicant_visible is not UNSET:
            field_dict["applicant_visible"] = applicant_visible
        if responsible_role is not UNSET:
            field_dict["responsible_role"] = responsible_role
        if transition_mode is not UNSET:
            field_dict["transition_mode"] = transition_mode
        if include_award_response is not UNSET:
            field_dict["include_award_response"] = include_award_response
        if allocation_time is not UNSET:
            field_dict["allocation_time"] = allocation_time
        if display_order is not UNSET:
            field_dict["display_order"] = display_order
        if criteria is not UNSET:
            field_dict["criteria"] = criteria

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workflow_criterion_request import WorkflowCriterionRequest

        d = dict(src_dict)
        step = StepEnum(d.pop("step"))

        is_enabled = d.pop("is_enabled", UNSET)

        def _parse_duration_in_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        duration_in_days = _parse_duration_in_days(d.pop("duration_in_days", UNSET))

        def _parse_checklist(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                checklist_type_0 = UUID(data)

                return checklist_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        checklist = _parse_checklist(d.pop("checklist", UNSET))

        checklist_required = d.pop("checklist_required", UNSET)

        blind_review = d.pop("blind_review", UNSET)

        requires_coi_confirmation = d.pop("requires_coi_confirmation", UNSET)

        def _parse_min_reviewers(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_reviewers = _parse_min_reviewers(d.pop("min_reviewers", UNSET))

        def _parse_min_score_threshold(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        min_score_threshold = _parse_min_score_threshold(d.pop("min_score_threshold", UNSET))

        applicant_visible = d.pop("applicant_visible", UNSET)

        def _parse_responsible_role(data: object) -> Union[BlankEnum, None, ResponsibleRoleEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                responsible_role_type_0 = ResponsibleRoleEnum(data)

                return responsible_role_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                responsible_role_type_1 = BlankEnum(data)

                return responsible_role_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, None, ResponsibleRoleEnum, Unset], data)

        responsible_role = _parse_responsible_role(d.pop("responsible_role", UNSET))

        _transition_mode = d.pop("transition_mode", UNSET)
        transition_mode: Union[Unset, TransitionModeEnum]
        if isinstance(_transition_mode, Unset):
            transition_mode = UNSET
        else:
            transition_mode = TransitionModeEnum(_transition_mode)

        include_award_response = d.pop("include_award_response", UNSET)

        _allocation_time = d.pop("allocation_time", UNSET)
        allocation_time: Union[Unset, AllocationTimeEnum]
        if isinstance(_allocation_time, Unset):
            allocation_time = UNSET
        else:
            allocation_time = AllocationTimeEnum(_allocation_time)

        def _parse_display_order(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        display_order = _parse_display_order(d.pop("display_order", UNSET))

        criteria = []
        _criteria = d.pop("criteria", UNSET)
        for criteria_item_data in _criteria or []:
            criteria_item = WorkflowCriterionRequest.from_dict(criteria_item_data)

            criteria.append(criteria_item)

        call_workflow_step_request = cls(
            step=step,
            is_enabled=is_enabled,
            duration_in_days=duration_in_days,
            checklist=checklist,
            checklist_required=checklist_required,
            blind_review=blind_review,
            requires_coi_confirmation=requires_coi_confirmation,
            min_reviewers=min_reviewers,
            min_score_threshold=min_score_threshold,
            applicant_visible=applicant_visible,
            responsible_role=responsible_role,
            transition_mode=transition_mode,
            include_award_response=include_award_response,
            allocation_time=allocation_time,
            display_order=display_order,
            criteria=criteria,
        )

        call_workflow_step_request.additional_properties = d
        return call_workflow_step_request

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
