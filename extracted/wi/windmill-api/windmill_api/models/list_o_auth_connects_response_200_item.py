from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListOAuthConnectsResponse200Item")


@_attrs_define
class ListOAuthConnectsResponse200Item:
    """
    Attributes:
        name (str):
        supports_client_credentials (bool):
        has_shared_credentials (bool):
    """

    name: str
    supports_client_credentials: bool
    has_shared_credentials: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        supports_client_credentials = self.supports_client_credentials
        has_shared_credentials = self.has_shared_credentials

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "supports_client_credentials": supports_client_credentials,
                "has_shared_credentials": has_shared_credentials,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        supports_client_credentials = d.pop("supports_client_credentials")

        has_shared_credentials = d.pop("has_shared_credentials")

        list_o_auth_connects_response_200_item = cls(
            name=name,
            supports_client_credentials=supports_client_credentials,
            has_shared_credentials=has_shared_credentials,
        )

        list_o_auth_connects_response_200_item.additional_properties = d
        return list_o_auth_connects_response_200_item

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
