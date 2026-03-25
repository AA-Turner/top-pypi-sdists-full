from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_approval_info_response_200_approval_conditions import GetApprovalInfoResponse200ApprovalConditions
    from ..models.get_approval_info_response_200_approvers_item import GetApprovalInfoResponse200ApproversItem


T = TypeVar("T", bound="GetApprovalInfoResponse200")


@_attrs_define
class GetApprovalInfoResponse200:
    """
    Attributes:
        flow_id (str):
        can_approve (bool): whether the current user/token holder can approve
        user_auth_required (bool): whether user authentication is required to approve
        approvers (List['GetApprovalInfoResponse200ApproversItem']):
        form_schema (Union[Unset, Any]): form schema for the approval step
        description (Union[Unset, Any]): description of the approval step
        approval_conditions (Union[Unset, GetApprovalInfoResponse200ApprovalConditions]):
        hide_cancel (Union[Unset, bool]): whether to hide the cancel button in the UI
    """

    flow_id: str
    can_approve: bool
    user_auth_required: bool
    approvers: List["GetApprovalInfoResponse200ApproversItem"]
    form_schema: Union[Unset, Any] = UNSET
    description: Union[Unset, Any] = UNSET
    approval_conditions: Union[Unset, "GetApprovalInfoResponse200ApprovalConditions"] = UNSET
    hide_cancel: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        flow_id = self.flow_id
        can_approve = self.can_approve
        user_auth_required = self.user_auth_required
        approvers = []
        for approvers_item_data in self.approvers:
            approvers_item = approvers_item_data.to_dict()

            approvers.append(approvers_item)

        form_schema = self.form_schema
        description = self.description
        approval_conditions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.approval_conditions, Unset):
            approval_conditions = self.approval_conditions.to_dict()

        hide_cancel = self.hide_cancel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flow_id": flow_id,
                "can_approve": can_approve,
                "user_auth_required": user_auth_required,
                "approvers": approvers,
            }
        )
        if form_schema is not UNSET:
            field_dict["form_schema"] = form_schema
        if description is not UNSET:
            field_dict["description"] = description
        if approval_conditions is not UNSET:
            field_dict["approval_conditions"] = approval_conditions
        if hide_cancel is not UNSET:
            field_dict["hide_cancel"] = hide_cancel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_approval_info_response_200_approval_conditions import (
            GetApprovalInfoResponse200ApprovalConditions,
        )
        from ..models.get_approval_info_response_200_approvers_item import GetApprovalInfoResponse200ApproversItem

        d = src_dict.copy()
        flow_id = d.pop("flow_id")

        can_approve = d.pop("can_approve")

        user_auth_required = d.pop("user_auth_required")

        approvers = []
        _approvers = d.pop("approvers")
        for approvers_item_data in _approvers:
            approvers_item = GetApprovalInfoResponse200ApproversItem.from_dict(approvers_item_data)

            approvers.append(approvers_item)

        form_schema = d.pop("form_schema", UNSET)

        description = d.pop("description", UNSET)

        _approval_conditions = d.pop("approval_conditions", UNSET)
        approval_conditions: Union[Unset, GetApprovalInfoResponse200ApprovalConditions]
        if isinstance(_approval_conditions, Unset):
            approval_conditions = UNSET
        else:
            approval_conditions = GetApprovalInfoResponse200ApprovalConditions.from_dict(_approval_conditions)

        hide_cancel = d.pop("hide_cancel", UNSET)

        get_approval_info_response_200 = cls(
            flow_id=flow_id,
            can_approve=can_approve,
            user_auth_required=user_auth_required,
            approvers=approvers,
            form_schema=form_schema,
            description=description,
            approval_conditions=approval_conditions,
            hide_cancel=hide_cancel,
        )

        get_approval_info_response_200.additional_properties = d
        return get_approval_info_response_200

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
