from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetApprovalInfoResponse200ApprovalConditions")


@_attrs_define
class GetApprovalInfoResponse200ApprovalConditions:
    """
    Attributes:
        user_auth_required (bool):
        user_groups_required (List[str]):
        self_approval_disabled (bool):
    """

    user_auth_required: bool
    user_groups_required: List[str]
    self_approval_disabled: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_auth_required = self.user_auth_required
        user_groups_required = self.user_groups_required

        self_approval_disabled = self.self_approval_disabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_auth_required": user_auth_required,
                "user_groups_required": user_groups_required,
                "self_approval_disabled": self_approval_disabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_auth_required = d.pop("user_auth_required")

        user_groups_required = cast(List[str], d.pop("user_groups_required"))

        self_approval_disabled = d.pop("self_approval_disabled")

        get_approval_info_response_200_approval_conditions = cls(
            user_auth_required=user_auth_required,
            user_groups_required=user_groups_required,
            self_approval_disabled=self_approval_disabled,
        )

        get_approval_info_response_200_approval_conditions.additional_properties = d
        return get_approval_info_response_200_approval_conditions

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
