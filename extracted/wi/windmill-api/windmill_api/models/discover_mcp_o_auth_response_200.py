from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiscoverMcpOAuthResponse200")


@_attrs_define
class DiscoverMcpOAuthResponse200:
    """
    Attributes:
        scopes_supported (Union[Unset, List[str]]):
        authorization_endpoint (Union[Unset, str]):
        token_endpoint (Union[Unset, str]):
        registration_endpoint (Union[Unset, str]):
        supports_dynamic_registration (Union[Unset, bool]):
    """

    scopes_supported: Union[Unset, List[str]] = UNSET
    authorization_endpoint: Union[Unset, str] = UNSET
    token_endpoint: Union[Unset, str] = UNSET
    registration_endpoint: Union[Unset, str] = UNSET
    supports_dynamic_registration: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scopes_supported: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes_supported, Unset):
            scopes_supported = self.scopes_supported

        authorization_endpoint = self.authorization_endpoint
        token_endpoint = self.token_endpoint
        registration_endpoint = self.registration_endpoint
        supports_dynamic_registration = self.supports_dynamic_registration

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scopes_supported is not UNSET:
            field_dict["scopes_supported"] = scopes_supported
        if authorization_endpoint is not UNSET:
            field_dict["authorization_endpoint"] = authorization_endpoint
        if token_endpoint is not UNSET:
            field_dict["token_endpoint"] = token_endpoint
        if registration_endpoint is not UNSET:
            field_dict["registration_endpoint"] = registration_endpoint
        if supports_dynamic_registration is not UNSET:
            field_dict["supports_dynamic_registration"] = supports_dynamic_registration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scopes_supported = cast(List[str], d.pop("scopes_supported", UNSET))

        authorization_endpoint = d.pop("authorization_endpoint", UNSET)

        token_endpoint = d.pop("token_endpoint", UNSET)

        registration_endpoint = d.pop("registration_endpoint", UNSET)

        supports_dynamic_registration = d.pop("supports_dynamic_registration", UNSET)

        discover_mcp_o_auth_response_200 = cls(
            scopes_supported=scopes_supported,
            authorization_endpoint=authorization_endpoint,
            token_endpoint=token_endpoint,
            registration_endpoint=registration_endpoint,
            supports_dynamic_registration=supports_dynamic_registration,
        )

        discover_mcp_o_auth_response_200.additional_properties = d
        return discover_mcp_o_auth_response_200

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
