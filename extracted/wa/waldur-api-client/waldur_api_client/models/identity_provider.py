from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.identity_provider_attribute_mapping import IdentityProviderAttributeMapping


T = TypeVar("T", bound="IdentityProvider")


@_attrs_define
class IdentityProvider:
    """
    Attributes:
        provider (str):
        label (str): Human-readable identity provider is label.
        protected_fields (Union[Unset, list[str]]):
        allowed_redirects (Union[Unset, list[str]]):
        is_active (Union[Unset, bool]):
        client_id (Union[Unset, str]): ID of application used for OAuth authentication.
        client_secret (Union[Unset, str]): Application secret key.
        verify_ssl (Union[Unset, bool]):
        enable_post_logout_redirect (Union[Unset, bool]):
        enable_pkce (Union[Unset, bool]):
        discovery_url (Union[Unset, str]): The endpoint for endpoint discovery.
        userinfo_url (Union[Unset, str]): The endpoint for fetching user info.
        token_url (Union[Unset, str]): The endpoint for obtaining auth token.
        auth_url (Union[Unset, str]): The endpoint for authorization request flow.
        logout_url (Union[Unset, str]): The endpoint used to redirect after sign-out.
        management_url (Union[Unset, str]): The endpoint for user details management.
        extra_scope (Union[None, Unset, str]): Space-separated list of scopes to request during authentication.
        user_field (Union[Unset, str]): The field in Waldur User model to be used for looking up the user
        user_claim (Union[Unset, str]): The OIDC claim from the userinfo endpoint to be used as the value for the lookup
            field.
        attribute_mapping (Union[Unset, IdentityProviderAttributeMapping]): A JSON object mapping Waldur User model
            fields to OIDC claims. Example: {"first_name": "given_name", "last_name": "family_name", "email": "email"}
        extra_fields (Union[None, Unset, str]): Space-separated list of extra fields to persist.
    """

    provider: str
    label: str
    protected_fields: Union[Unset, list[str]] = UNSET
    allowed_redirects: Union[Unset, list[str]] = UNSET
    is_active: Union[Unset, bool] = UNSET
    client_id: Union[Unset, str] = UNSET
    client_secret: Union[Unset, str] = UNSET
    verify_ssl: Union[Unset, bool] = UNSET
    enable_post_logout_redirect: Union[Unset, bool] = UNSET
    enable_pkce: Union[Unset, bool] = UNSET
    discovery_url: Union[Unset, str] = UNSET
    userinfo_url: Union[Unset, str] = UNSET
    token_url: Union[Unset, str] = UNSET
    auth_url: Union[Unset, str] = UNSET
    logout_url: Union[Unset, str] = UNSET
    management_url: Union[Unset, str] = UNSET
    extra_scope: Union[None, Unset, str] = UNSET
    user_field: Union[Unset, str] = UNSET
    user_claim: Union[Unset, str] = UNSET
    attribute_mapping: Union[Unset, "IdentityProviderAttributeMapping"] = UNSET
    extra_fields: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        label = self.label

        protected_fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.protected_fields, Unset):
            protected_fields = self.protected_fields

        allowed_redirects: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_redirects, Unset):
            allowed_redirects = self.allowed_redirects

        is_active = self.is_active

        client_id = self.client_id

        client_secret = self.client_secret

        verify_ssl = self.verify_ssl

        enable_post_logout_redirect = self.enable_post_logout_redirect

        enable_pkce = self.enable_pkce

        discovery_url = self.discovery_url

        userinfo_url = self.userinfo_url

        token_url = self.token_url

        auth_url = self.auth_url

        logout_url = self.logout_url

        management_url = self.management_url

        extra_scope: Union[None, Unset, str]
        if isinstance(self.extra_scope, Unset):
            extra_scope = UNSET
        else:
            extra_scope = self.extra_scope

        user_field = self.user_field

        user_claim = self.user_claim

        attribute_mapping: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attribute_mapping, Unset):
            attribute_mapping = self.attribute_mapping.to_dict()

        extra_fields: Union[None, Unset, str]
        if isinstance(self.extra_fields, Unset):
            extra_fields = UNSET
        else:
            extra_fields = self.extra_fields

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "label": label,
            }
        )
        if protected_fields is not UNSET:
            field_dict["protected_fields"] = protected_fields
        if allowed_redirects is not UNSET:
            field_dict["allowed_redirects"] = allowed_redirects
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if verify_ssl is not UNSET:
            field_dict["verify_ssl"] = verify_ssl
        if enable_post_logout_redirect is not UNSET:
            field_dict["enable_post_logout_redirect"] = enable_post_logout_redirect
        if enable_pkce is not UNSET:
            field_dict["enable_pkce"] = enable_pkce
        if discovery_url is not UNSET:
            field_dict["discovery_url"] = discovery_url
        if userinfo_url is not UNSET:
            field_dict["userinfo_url"] = userinfo_url
        if token_url is not UNSET:
            field_dict["token_url"] = token_url
        if auth_url is not UNSET:
            field_dict["auth_url"] = auth_url
        if logout_url is not UNSET:
            field_dict["logout_url"] = logout_url
        if management_url is not UNSET:
            field_dict["management_url"] = management_url
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.identity_provider_attribute_mapping import IdentityProviderAttributeMapping

        d = dict(src_dict)
        provider = d.pop("provider")

        label = d.pop("label")

        protected_fields = cast(list[str], d.pop("protected_fields", UNSET))

        allowed_redirects = cast(list[str], d.pop("allowed_redirects", UNSET))

        is_active = d.pop("is_active", UNSET)

        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        verify_ssl = d.pop("verify_ssl", UNSET)

        enable_post_logout_redirect = d.pop("enable_post_logout_redirect", UNSET)

        enable_pkce = d.pop("enable_pkce", UNSET)

        discovery_url = d.pop("discovery_url", UNSET)

        userinfo_url = d.pop("userinfo_url", UNSET)

        token_url = d.pop("token_url", UNSET)

        auth_url = d.pop("auth_url", UNSET)

        logout_url = d.pop("logout_url", UNSET)

        management_url = d.pop("management_url", UNSET)

        def _parse_extra_scope(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        extra_scope = _parse_extra_scope(d.pop("extra_scope", UNSET))

        user_field = d.pop("user_field", UNSET)

        user_claim = d.pop("user_claim", UNSET)

        _attribute_mapping = d.pop("attribute_mapping", UNSET)
        attribute_mapping: Union[Unset, IdentityProviderAttributeMapping]
        if isinstance(_attribute_mapping, Unset):
            attribute_mapping = UNSET
        else:
            attribute_mapping = IdentityProviderAttributeMapping.from_dict(_attribute_mapping)

        def _parse_extra_fields(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        extra_fields = _parse_extra_fields(d.pop("extra_fields", UNSET))

        identity_provider = cls(
            provider=provider,
            label=label,
            protected_fields=protected_fields,
            allowed_redirects=allowed_redirects,
            is_active=is_active,
            client_id=client_id,
            client_secret=client_secret,
            verify_ssl=verify_ssl,
            enable_post_logout_redirect=enable_post_logout_redirect,
            enable_pkce=enable_pkce,
            discovery_url=discovery_url,
            userinfo_url=userinfo_url,
            token_url=token_url,
            auth_url=auth_url,
            logout_url=logout_url,
            management_url=management_url,
            extra_scope=extra_scope,
            user_field=user_field,
            user_claim=user_claim,
            attribute_mapping=attribute_mapping,
            extra_fields=extra_fields,
        )

        identity_provider.additional_properties = d
        return identity_provider

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
