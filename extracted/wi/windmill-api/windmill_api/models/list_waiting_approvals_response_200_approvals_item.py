import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListWaitingApprovalsResponse200ApprovalsItem")


@_attrs_define
class ListWaitingApprovalsResponse200ApprovalsItem:
    """
    Attributes:
        job_id (str): the suspended flow run, the one its approval page takes: the root run, or the branch, loop or
            subflow run holding the approval step
        started_by (str):
        created_at (datetime.datetime):
        approvals (int): approvals received so far
        required_approvals (int):
        flow_path (Union[Unset, str]):
        flow_summary (Union[Unset, str]):
        step_summary (Union[Unset, str]):
    """

    job_id: str
    started_by: str
    created_at: datetime.datetime
    approvals: int
    required_approvals: int
    flow_path: Union[Unset, str] = UNSET
    flow_summary: Union[Unset, str] = UNSET
    step_summary: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id
        started_by = self.started_by
        created_at = self.created_at.isoformat()

        approvals = self.approvals
        required_approvals = self.required_approvals
        flow_path = self.flow_path
        flow_summary = self.flow_summary
        step_summary = self.step_summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "started_by": started_by,
                "created_at": created_at,
                "approvals": approvals,
                "required_approvals": required_approvals,
            }
        )
        if flow_path is not UNSET:
            field_dict["flow_path"] = flow_path
        if flow_summary is not UNSET:
            field_dict["flow_summary"] = flow_summary
        if step_summary is not UNSET:
            field_dict["step_summary"] = step_summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_id = d.pop("job_id")

        started_by = d.pop("started_by")

        created_at = isoparse(d.pop("created_at"))

        approvals = d.pop("approvals")

        required_approvals = d.pop("required_approvals")

        flow_path = d.pop("flow_path", UNSET)

        flow_summary = d.pop("flow_summary", UNSET)

        step_summary = d.pop("step_summary", UNSET)

        list_waiting_approvals_response_200_approvals_item = cls(
            job_id=job_id,
            started_by=started_by,
            created_at=created_at,
            approvals=approvals,
            required_approvals=required_approvals,
            flow_path=flow_path,
            flow_summary=flow_summary,
            step_summary=step_summary,
        )

        list_waiting_approvals_response_200_approvals_item.additional_properties = d
        return list_waiting_approvals_response_200_approvals_item

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
