from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListDeploymentRequestEligibleDeployersResponse200Item")


@_attrs_define
class ListDeploymentRequestEligibleDeployersResponse200Item:
    """
    Attributes:
        username (str):
        email (str):
        is_admin (bool):
    """

    username: str
    email: str
    is_admin: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        email = self.email
        is_admin = self.is_admin

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "email": email,
                "is_admin": is_admin,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        email = d.pop("email")

        is_admin = d.pop("is_admin")

        list_deployment_request_eligible_deployers_response_200_item = cls(
            username=username,
            email=email,
            is_admin=is_admin,
        )

        list_deployment_request_eligible_deployers_response_200_item.additional_properties = d
        return list_deployment_request_eligible_deployers_response_200_item

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
