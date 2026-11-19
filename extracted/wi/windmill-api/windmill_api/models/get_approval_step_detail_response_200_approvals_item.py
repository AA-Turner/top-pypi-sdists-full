import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetApprovalStepDetailResponse200ApprovalsItem")


@_attrs_define
class GetApprovalStepDetailResponse200ApprovalsItem:
    """
    Attributes:
        resume_id (int):
        approver (str):
        approved (Union[Unset, bool]):
        value (Union[Unset, Any]):
        created_at (Union[Unset, datetime.datetime]):
    """

    resume_id: int
    approver: str
    approved: Union[Unset, bool] = UNSET
    value: Union[Unset, Any] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resume_id = self.resume_id
        approver = self.approver
        approved = self.approved
        value = self.value
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resume_id": resume_id,
                "approver": approver,
            }
        )
        if approved is not UNSET:
            field_dict["approved"] = approved
        if value is not UNSET:
            field_dict["value"] = value
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        resume_id = d.pop("resume_id")

        approver = d.pop("approver")

        approved = d.pop("approved", UNSET)

        value = d.pop("value", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        get_approval_step_detail_response_200_approvals_item = cls(
            resume_id=resume_id,
            approver=approver,
            approved=approved,
            value=value,
            created_at=created_at,
        )

        get_approval_step_detail_response_200_approvals_item.additional_properties = d
        return get_approval_step_detail_response_200_approvals_item

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
