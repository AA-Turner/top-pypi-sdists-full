from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResumeSuspendedJsonBody")


@_attrs_define
class ResumeSuspendedJsonBody:
    """
    Attributes:
        payload (Union[Unset, Any]): payload to send to the resumed job
        approval_token (Union[Unset, str]): approval token for unauthenticated access
        approved (Union[Unset, bool]): whether to approve (true) or cancel (false) the job Default: True.
    """

    payload: Union[Unset, Any] = UNSET
    approval_token: Union[Unset, str] = UNSET
    approved: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = self.payload
        approval_token = self.approval_token
        approved = self.approved

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if payload is not UNSET:
            field_dict["payload"] = payload
        if approval_token is not UNSET:
            field_dict["approval_token"] = approval_token
        if approved is not UNSET:
            field_dict["approved"] = approved

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        payload = d.pop("payload", UNSET)

        approval_token = d.pop("approval_token", UNSET)

        approved = d.pop("approved", UNSET)

        resume_suspended_json_body = cls(
            payload=payload,
            approval_token=approval_token,
            approved=approved,
        )

        resume_suspended_json_body.additional_properties = d
        return resume_suspended_json_body

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
