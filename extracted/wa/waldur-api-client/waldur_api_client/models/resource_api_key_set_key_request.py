from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceApiKeySetKeyRequest")


@_attrs_define
class ResourceApiKeySetKeyRequest:
    """
    Attributes:
        api_key (str):
        client_id (Union[Unset, str]):
    """

    api_key: str
    client_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_key = self.api_key

        client_id = self.client_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_key": api_key,
            }
        )
        if client_id is not UNSET:
            field_dict["client_id"] = client_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_key = d.pop("api_key")

        client_id = d.pop("client_id", UNSET)

        resource_api_key_set_key_request = cls(
            api_key=api_key,
            client_id=client_id,
        )

        resource_api_key_set_key_request.additional_properties = d
        return resource_api_key_set_key_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
