import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_approval_step_detail_response_200_skin import GetApprovalStepDetailResponse200Skin
from ..models.get_approval_step_detail_response_200_status import GetApprovalStepDetailResponse200Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_approval_step_detail_response_200_approval_conditions import (
        GetApprovalStepDetailResponse200ApprovalConditions,
    )
    from ..models.get_approval_step_detail_response_200_approvals_item import (
        GetApprovalStepDetailResponse200ApprovalsItem,
    )


T = TypeVar("T", bound="GetApprovalStepDetailResponse200")


@_attrs_define
class GetApprovalStepDetailResponse200:
    """
    Attributes:
        flow_id (str):
        step_id (str):
        status (GetApprovalStepDetailResponse200Status): not_reached: the step's own script has not finished yet.
            failed: the step failed before asking for approval. waiting: the run is suspended on this step. resumed: the run
            moved past this step. not_resumed: the run ended while waiting (denied, timed out or cancelled).
        required_events (int): number of approvals required to resume
        hide_cancel (bool):
        continue_on_disapprove_timeout (bool):
        skin (GetApprovalStepDetailResponse200Skin):
        approvals (List['GetApprovalStepDetailResponse200ApprovalsItem']): approvals received. approved and value are
            known only while the run is live; a finished run keeps approver names and, for approvals recorded since it was
            kept, created_at.
        step_job (Union[Unset, str]): the job of the approval step, once it ran
        step_summary (Union[Unset, str]):
        timeout (Union[Unset, int]): seconds the run waits for approvals
        suspended_until (Union[Unset, datetime.datetime]): when the wait times out, while waiting
        form_schema (Union[Unset, Any]): form schema for the approval step
        approval_conditions (Union[Unset, GetApprovalStepDetailResponse200ApprovalConditions]):
        can_approve (Union[Unset, bool]): whether the caller can approve, set only while waiting
        description (Union[Unset, Any]): description returned by the approval step's script
        default_args (Union[Unset, Any]): default form values returned by the approval step's script
        enums (Union[Unset, Any]): form enums returned by the approval step's script
        error (Union[Unset, Any]): the run's error, when status is not_resumed
    """

    flow_id: str
    step_id: str
    status: GetApprovalStepDetailResponse200Status
    required_events: int
    hide_cancel: bool
    continue_on_disapprove_timeout: bool
    skin: GetApprovalStepDetailResponse200Skin
    approvals: List["GetApprovalStepDetailResponse200ApprovalsItem"]
    step_job: Union[Unset, str] = UNSET
    step_summary: Union[Unset, str] = UNSET
    timeout: Union[Unset, int] = UNSET
    suspended_until: Union[Unset, datetime.datetime] = UNSET
    form_schema: Union[Unset, Any] = UNSET
    approval_conditions: Union[Unset, "GetApprovalStepDetailResponse200ApprovalConditions"] = UNSET
    can_approve: Union[Unset, bool] = UNSET
    description: Union[Unset, Any] = UNSET
    default_args: Union[Unset, Any] = UNSET
    enums: Union[Unset, Any] = UNSET
    error: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        flow_id = self.flow_id
        step_id = self.step_id
        status = self.status.value

        required_events = self.required_events
        hide_cancel = self.hide_cancel
        continue_on_disapprove_timeout = self.continue_on_disapprove_timeout
        skin = self.skin.value

        approvals = []
        for approvals_item_data in self.approvals:
            approvals_item = approvals_item_data.to_dict()

            approvals.append(approvals_item)

        step_job = self.step_job
        step_summary = self.step_summary
        timeout = self.timeout
        suspended_until: Union[Unset, str] = UNSET
        if not isinstance(self.suspended_until, Unset):
            suspended_until = self.suspended_until.isoformat()

        form_schema = self.form_schema
        approval_conditions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.approval_conditions, Unset):
            approval_conditions = self.approval_conditions.to_dict()

        can_approve = self.can_approve
        description = self.description
        default_args = self.default_args
        enums = self.enums
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flow_id": flow_id,
                "step_id": step_id,
                "status": status,
                "required_events": required_events,
                "hide_cancel": hide_cancel,
                "continue_on_disapprove_timeout": continue_on_disapprove_timeout,
                "skin": skin,
                "approvals": approvals,
            }
        )
        if step_job is not UNSET:
            field_dict["step_job"] = step_job
        if step_summary is not UNSET:
            field_dict["step_summary"] = step_summary
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if suspended_until is not UNSET:
            field_dict["suspended_until"] = suspended_until
        if form_schema is not UNSET:
            field_dict["form_schema"] = form_schema
        if approval_conditions is not UNSET:
            field_dict["approval_conditions"] = approval_conditions
        if can_approve is not UNSET:
            field_dict["can_approve"] = can_approve
        if description is not UNSET:
            field_dict["description"] = description
        if default_args is not UNSET:
            field_dict["default_args"] = default_args
        if enums is not UNSET:
            field_dict["enums"] = enums
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_approval_step_detail_response_200_approval_conditions import (
            GetApprovalStepDetailResponse200ApprovalConditions,
        )
        from ..models.get_approval_step_detail_response_200_approvals_item import (
            GetApprovalStepDetailResponse200ApprovalsItem,
        )

        d = src_dict.copy()
        flow_id = d.pop("flow_id")

        step_id = d.pop("step_id")

        status = GetApprovalStepDetailResponse200Status(d.pop("status"))

        required_events = d.pop("required_events")

        hide_cancel = d.pop("hide_cancel")

        continue_on_disapprove_timeout = d.pop("continue_on_disapprove_timeout")

        skin = GetApprovalStepDetailResponse200Skin(d.pop("skin"))

        approvals = []
        _approvals = d.pop("approvals")
        for approvals_item_data in _approvals:
            approvals_item = GetApprovalStepDetailResponse200ApprovalsItem.from_dict(approvals_item_data)

            approvals.append(approvals_item)

        step_job = d.pop("step_job", UNSET)

        step_summary = d.pop("step_summary", UNSET)

        timeout = d.pop("timeout", UNSET)

        _suspended_until = d.pop("suspended_until", UNSET)
        suspended_until: Union[Unset, datetime.datetime]
        if isinstance(_suspended_until, Unset):
            suspended_until = UNSET
        else:
            suspended_until = isoparse(_suspended_until)

        form_schema = d.pop("form_schema", UNSET)

        _approval_conditions = d.pop("approval_conditions", UNSET)
        approval_conditions: Union[Unset, GetApprovalStepDetailResponse200ApprovalConditions]
        if isinstance(_approval_conditions, Unset):
            approval_conditions = UNSET
        else:
            approval_conditions = GetApprovalStepDetailResponse200ApprovalConditions.from_dict(_approval_conditions)

        can_approve = d.pop("can_approve", UNSET)

        description = d.pop("description", UNSET)

        default_args = d.pop("default_args", UNSET)

        enums = d.pop("enums", UNSET)

        error = d.pop("error", UNSET)

        get_approval_step_detail_response_200 = cls(
            flow_id=flow_id,
            step_id=step_id,
            status=status,
            required_events=required_events,
            hide_cancel=hide_cancel,
            continue_on_disapprove_timeout=continue_on_disapprove_timeout,
            skin=skin,
            approvals=approvals,
            step_job=step_job,
            step_summary=step_summary,
            timeout=timeout,
            suspended_until=suspended_until,
            form_schema=form_schema,
            approval_conditions=approval_conditions,
            can_approve=can_approve,
            description=description,
            default_args=default_args,
            enums=enums,
            error=error,
        )

        get_approval_step_detail_response_200.additional_properties = d
        return get_approval_step_detail_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
