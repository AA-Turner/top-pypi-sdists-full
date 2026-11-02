from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.token_response_resource_fields import TokenResponseResourceFields


T = TypeVar("T", bound="TokenResponse")


@_attrs_define
class TokenResponse:
    """
    Attributes:
        access_token (str):
        expires_in (Union[Unset, int]):
        refresh_token (Union[Unset, str]):
        scope (Union[Unset, List[str]]):
        grant_type (Union[Unset, str]):
        resource_fields (Union[Unset, TokenResponseResourceFields]): Resource fields the provider's `connect_fields`
            picked on connect (Salesforce's instance_url, Docusign's account_id and base_uri, QuickBooks' realmId), for the
            connect dialog to prefill.
    """

    access_token: str
    expires_in: Union[Unset, int] = UNSET
    refresh_token: Union[Unset, str] = UNSET
    scope: Union[Unset, List[str]] = UNSET
    grant_type: Union[Unset, str] = UNSET
    resource_fields: Union[Unset, "TokenResponseResourceFields"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        access_token = self.access_token
        expires_in = self.expires_in
        refresh_token = self.refresh_token
        scope: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope

        grant_type = self.grant_type
        resource_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource_fields, Unset):
            resource_fields = self.resource_fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access_token": access_token,
            }
        )
        if expires_in is not UNSET:
            field_dict["expires_in"] = expires_in
        if refresh_token is not UNSET:
            field_dict["refresh_token"] = refresh_token
        if scope is not UNSET:
            field_dict["scope"] = scope
        if grant_type is not UNSET:
            field_dict["grant_type"] = grant_type
        if resource_fields is not UNSET:
            field_dict["resource_fields"] = resource_fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_response_resource_fields import TokenResponseResourceFields

        d = src_dict.copy()
        access_token = d.pop("access_token")

        expires_in = d.pop("expires_in", UNSET)

        refresh_token = d.pop("refresh_token", UNSET)

        scope = cast(List[str], d.pop("scope", UNSET))

        grant_type = d.pop("grant_type", UNSET)

        _resource_fields = d.pop("resource_fields", UNSET)
        resource_fields: Union[Unset, TokenResponseResourceFields]
        if isinstance(_resource_fields, Unset):
            resource_fields = UNSET
        else:
            resource_fields = TokenResponseResourceFields.from_dict(_resource_fields)

        token_response = cls(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            scope=scope,
            grant_type=grant_type,
            resource_fields=resource_fields,
        )

        token_response.additional_properties = d
        return token_response

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
