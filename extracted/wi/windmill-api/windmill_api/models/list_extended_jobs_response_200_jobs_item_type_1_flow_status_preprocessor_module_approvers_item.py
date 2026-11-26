import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListExtendedJobsResponse200JobsItemType1FlowStatusPreprocessorModuleApproversItem")


@_attrs_define
class ListExtendedJobsResponse200JobsItemType1FlowStatusPreprocessorModuleApproversItem:
    """
    Attributes:
        resume_id (int):
        approver (str):
        approved_at (Union[Unset, datetime.datetime]): absent for approvals recorded before it was kept
        approved (Union[Unset, bool]): false for a rejection the flow continued past; absent for approvals recorded
            before it was kept
    """

    resume_id: int
    approver: str
    approved_at: Union[Unset, datetime.datetime] = UNSET
    approved: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resume_id = self.resume_id
        approver = self.approver
        approved_at: Union[Unset, str] = UNSET
        if not isinstance(self.approved_at, Unset):
            approved_at = self.approved_at.isoformat()

        approved = self.approved

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resume_id": resume_id,
                "approver": approver,
            }
        )
        if approved_at is not UNSET:
            field_dict["approved_at"] = approved_at
        if approved is not UNSET:
            field_dict["approved"] = approved

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        resume_id = d.pop("resume_id")

        approver = d.pop("approver")

        _approved_at = d.pop("approved_at", UNSET)
        approved_at: Union[Unset, datetime.datetime]
        if isinstance(_approved_at, Unset):
            approved_at = UNSET
        else:
            approved_at = isoparse(_approved_at)

        approved = d.pop("approved", UNSET)

        list_extended_jobs_response_200_jobs_item_type_1_flow_status_preprocessor_module_approvers_item = cls(
            resume_id=resume_id,
            approver=approver,
            approved_at=approved_at,
            approved=approved,
        )

        list_extended_jobs_response_200_jobs_item_type_1_flow_status_preprocessor_module_approvers_item.additional_properties = (
            d
        )
        return list_extended_jobs_response_200_jobs_item_type_1_flow_status_preprocessor_module_approvers_item

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
