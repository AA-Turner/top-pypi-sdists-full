from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_nested_approvals_response_200_approvals_item_approvers_item import (
        ListNestedApprovalsResponse200ApprovalsItemApproversItem,
    )


T = TypeVar("T", bound="ListNestedApprovalsResponse200ApprovalsItem")


@_attrs_define
class ListNestedApprovalsResponse200ApprovalsItem:
    """
    Attributes:
        job_id (str): the nested run the step belongs to
        subflows (List[str]): ids of the subflow steps leading to the nested run, outermost first. Step ids are unique
            across a flow, loop and branch steps included, so the first one (or the step itself) is a step of the flow run's
            own graph
        step_id (str):
        required_events (int): approvals the step required; fewer approvers means it timed out and the flow continued
        approvers (List['ListNestedApprovalsResponse200ApprovalsItemApproversItem']):
        step_summary (Union[Unset, str]):
    """

    job_id: str
    subflows: List[str]
    step_id: str
    required_events: int
    approvers: List["ListNestedApprovalsResponse200ApprovalsItemApproversItem"]
    step_summary: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id
        subflows = self.subflows

        step_id = self.step_id
        required_events = self.required_events
        approvers = []
        for approvers_item_data in self.approvers:
            approvers_item = approvers_item_data.to_dict()

            approvers.append(approvers_item)

        step_summary = self.step_summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "subflows": subflows,
                "step_id": step_id,
                "required_events": required_events,
                "approvers": approvers,
            }
        )
        if step_summary is not UNSET:
            field_dict["step_summary"] = step_summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_nested_approvals_response_200_approvals_item_approvers_item import (
            ListNestedApprovalsResponse200ApprovalsItemApproversItem,
        )

        d = src_dict.copy()
        job_id = d.pop("job_id")

        subflows = cast(List[str], d.pop("subflows"))

        step_id = d.pop("step_id")

        required_events = d.pop("required_events")

        approvers = []
        _approvers = d.pop("approvers")
        for approvers_item_data in _approvers:
            approvers_item = ListNestedApprovalsResponse200ApprovalsItemApproversItem.from_dict(approvers_item_data)

            approvers.append(approvers_item)

        step_summary = d.pop("step_summary", UNSET)

        list_nested_approvals_response_200_approvals_item = cls(
            job_id=job_id,
            subflows=subflows,
            step_id=step_id,
            required_events=required_events,
            approvers=approvers,
            step_summary=step_summary,
        )

        list_nested_approvals_response_200_approvals_item.additional_properties = d
        return list_nested_approvals_response_200_approvals_item

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
