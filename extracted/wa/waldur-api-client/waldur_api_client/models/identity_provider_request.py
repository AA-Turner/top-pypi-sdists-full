from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IdentityProviderRequest")


@_attrs_define
class IdentityProviderRequest:
    """
    Attributes:
        provider (str):
        client_id (str): ID of application used for OAuth authentication.
        client_secret (str): Application secret key.
        discovery_url (str): The endpoint for endpoint discovery.
        label (str): Human-readable identity provider is label.
        is_active (Union[Unset, bool]):
        verify_ssl (Union[Unset, bool]):
        enable_post_logout_redirect (Union[Unset, bool]):
        enable_pkce (Union[Unset, bool]):
        management_url (Union[Unset, str]): The endpoint for user details management.
        protected_fields (Union[Unset, Any]):
        extra_scope (Union[None, Unset, str]): Space-separated list of scopes to request during authentication.
        user_field (Union[Unset, str]): The field in Waldur User model to be used for looking up the user
        user_claim (Union[Unset, str]): The OIDC claim from the userinfo endpoint to be used as the value for the lookup
            field.
        attribute_mapping (Union[Unset, Any]): A JSON object mapping Waldur User model fields to OIDC claims. Example:
            {"first_name": "given_name", "last_name": "family_name", "email": "email"}
        extra_fields (Union[None, Unset, str]): Space-separated list of extra fields to persist.
        allowed_redirects (Union[Unset, Any]): List of allowed redirect URLs for OAuth authentication. URLs must be
            exact matches (origin only: scheme + domain + port). HTTPS required except for localhost. No wildcards, paths,
            query params, or fragments. Example: ["https://portal1.example.com", "https://portal2.example.com:8443"]. If
            empty, falls back to HOMEPORT_URL setting.
    """

    provider: str
    client_id: str
    client_secret: str
    discovery_url: str
    label: str
    is_active: Union[Unset, bool] = UNSET
    verify_ssl: Union[Unset, bool] = UNSET
    enable_post_logout_redirect: Union[Unset, bool] = UNSET
    enable_pkce: Union[Unset, bool] = UNSET
    management_url: Union[Unset, str] = UNSET
    protected_fields: Union[Unset, Any] = UNSET
    extra_scope: Union[None, Unset, str] = UNSET
    user_field: Union[Unset, str] = UNSET
    user_claim: Union[Unset, str] = UNSET
    attribute_mapping: Union[Unset, Any] = UNSET
    extra_fields: Union[None, Unset, str] = UNSET
    allowed_redirects: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        client_id = self.client_id

        client_secret = self.client_secret

        discovery_url = self.discovery_url

        label = self.label

        is_active = self.is_active

        verify_ssl = self.verify_ssl

        enable_post_logout_redirect = self.enable_post_logout_redirect

        enable_pkce = self.enable_pkce

        management_url = self.management_url

        protected_fields = self.protected_fields

        extra_scope: Union[None, Unset, str]
        if isinstance(self.extra_scope, Unset):
            extra_scope = UNSET
        else:
            extra_scope = self.extra_scope

        user_field = self.user_field

        user_claim = self.user_claim

        attribute_mapping = self.attribute_mapping

        extra_fields: Union[None, Unset, str]
        if isinstance(self.extra_fields, Unset):
            extra_fields = UNSET
        else:
            extra_fields = self.extra_fields

        allowed_redirects = self.allowed_redirects

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "client_id": client_id,
                "client_secret": client_secret,
                "discovery_url": discovery_url,
                "label": label,
            }
        )
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if verify_ssl is not UNSET:
            field_dict["verify_ssl"] = verify_ssl
        if enable_post_logout_redirect is not UNSET:
            field_dict["enable_post_logout_redirect"] = enable_post_logout_redirect
        if enable_pkce is not UNSET:
            field_dict["enable_pkce"] = enable_pkce
        if management_url is not UNSET:
            field_dict["management_url"] = management_url
        if protected_fields is not UNSET:
            field_dict["protected_fields"] = protected_fields
        if extra_scope is not UNSET:
            field_dict["extra_scope"] = extra_scope
        if user_field is not UNSET:
            field_dict["user_field"] = user_field
        if user_claim is not UNSET:
            field_dict["user_claim"] = user_claim
        if attribute_mapping is not UNSET:
            field_dict["attribute_mapping"] = attribute_mapping
        if extra_fields is not UNSET:
            field_dict["extra_fields"] = extra_fields
        if allowed_redirects is not UNSET:
            field_dict["allowed_redirects"] = allowed_redirects

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = d.pop("provider")

        client_id = d.pop("client_id")

        client_secret = d.pop("client_secret")

        discovery_url = d.pop("discovery_url")

        label = d.pop("label")

        is_active = d.pop("is_active", UNSET)

        verify_ssl = d.pop("verify_ssl", UNSET)

        enable_post_logout_redirect = d.pop("enable_post_logout_redirect", UNSET)

        enable_pkce = d.pop("enable_pkce", UNSET)

        management_url = d.pop("management_url", UNSET)

        protected_fields = d.pop("protected_fields", UNSET)

        def _parse_extra_scope(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        extra_scope = _parse_extra_scope(d.pop("extra_scope", UNSET))

        user_field = d.pop("user_field", UNSET)

        user_claim = d.pop("user_claim", UNSET)

        attribute_mapping = d.pop("attribute_mapping", UNSET)

        def _parse_extra_fields(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        extra_fields = _parse_extra_fields(d.pop("extra_fields", UNSET))

        allowed_redirects = d.pop("allowed_redirects", UNSET)

        identity_provider_request = cls(
            provider=provider,
            client_id=client_id,
            client_secret=client_secret,
            discovery_url=discovery_url,
            label=label,
            is_active=is_active,
            verify_ssl=verify_ssl,
            enable_post_logout_redirect=enable_post_logout_redirect,
            enable_pkce=enable_pkce,
            management_url=management_url,
            protected_fields=protected_fields,
            extra_scope=extra_scope,
            user_field=user_field,
            user_claim=user_claim,
            attribute_mapping=attribute_mapping,
            extra_fields=extra_fields,
            allowed_redirects=allowed_redirects,
        )

        identity_provider_request.additional_properties = d
        return identity_provider_request

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
