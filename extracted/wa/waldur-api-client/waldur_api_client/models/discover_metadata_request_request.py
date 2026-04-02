from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiscoverMetadataRequestRequest")


@_attrs_define
class DiscoverMetadataRequestRequest:
    """
    Attributes:
        discovery_url (str): OIDC discovery URL (e.g., https://idp.example.com/.well-known/openid-configuration)
        verify_ssl (Union[Unset, bool]): Whether to verify SSL certificate Default: True.
    """

    discovery_url: str
    verify_ssl: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        discovery_url = self.discovery_url

        verify_ssl = self.verify_ssl

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "discovery_url": discovery_url,
            }
        )
        if verify_ssl is not UNSET:
            field_dict["verify_ssl"] = verify_ssl

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        discovery_url = d.pop("discovery_url")

        verify_ssl = d.pop("verify_ssl", UNSET)

        discover_metadata_request_request = cls(
            discovery_url=discovery_url,
            verify_ssl=verify_ssl,
        )

        discover_metadata_request_request.additional_properties = d
        return discover_metadata_request_request

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
