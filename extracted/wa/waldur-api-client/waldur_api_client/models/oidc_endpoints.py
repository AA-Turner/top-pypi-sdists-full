from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OidcEndpoints")


@_attrs_define
class OidcEndpoints:
    """
    Attributes:
        authorization_endpoint (str): OIDC authorization endpoint
        token_endpoint (str): OIDC token endpoint
        userinfo_endpoint (str): OIDC userinfo endpoint
        end_session_endpoint (Union[None, Unset, str]): OIDC end session endpoint
        jwks_uri (Union[None, Unset, str]): OIDC JWKS URI
    """

    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    end_session_endpoint: Union[None, Unset, str] = UNSET
    jwks_uri: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        authorization_endpoint = self.authorization_endpoint

        token_endpoint = self.token_endpoint

        userinfo_endpoint = self.userinfo_endpoint

        end_session_endpoint: Union[None, Unset, str]
        if isinstance(self.end_session_endpoint, Unset):
            end_session_endpoint = UNSET
        else:
            end_session_endpoint = self.end_session_endpoint

        jwks_uri: Union[None, Unset, str]
        if isinstance(self.jwks_uri, Unset):
            jwks_uri = UNSET
        else:
            jwks_uri = self.jwks_uri

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "authorization_endpoint": authorization_endpoint,
                "token_endpoint": token_endpoint,
                "userinfo_endpoint": userinfo_endpoint,
            }
        )
        if end_session_endpoint is not UNSET:
            field_dict["end_session_endpoint"] = end_session_endpoint
        if jwks_uri is not UNSET:
            field_dict["jwks_uri"] = jwks_uri

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        authorization_endpoint = d.pop("authorization_endpoint")

        token_endpoint = d.pop("token_endpoint")

        userinfo_endpoint = d.pop("userinfo_endpoint")

        def _parse_end_session_endpoint(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        end_session_endpoint = _parse_end_session_endpoint(d.pop("end_session_endpoint", UNSET))

        def _parse_jwks_uri(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        jwks_uri = _parse_jwks_uri(d.pop("jwks_uri", UNSET))

        oidc_endpoints = cls(
            authorization_endpoint=authorization_endpoint,
            token_endpoint=token_endpoint,
            userinfo_endpoint=userinfo_endpoint,
            end_session_endpoint=end_session_endpoint,
            jwks_uri=jwks_uri,
        )

        oidc_endpoints.additional_properties = d
        return oidc_endpoints

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
