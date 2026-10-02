from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_identity_provider_request_attribute_mapping import (
        PatchedIdentityProviderRequestAttributeMapping,
    )


T = TypeVar("T", bound="PatchedIdentityProviderRequest")


@_attrs_define
class PatchedIdentityProviderRequest:
    """
    Attributes:
        protected_fields (Union[Unset, list[str]]):
        allowed_redirects (Union[Unset, list[str]]):
        provider (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        client_id (Union[Unset, str]): ID of application used for OAuth authentication.
        client_secret (Union[Unset, str]): Application secret key.
        verify_ssl (Union[Unset, bool]):
        enable_post_logout_redirect (Union[Unset, bool]):
        enable_pkce (Union[Unset, bool]):
        discovery_url (Union[Unset, str]): The endpoint for endpoint discovery.
        label (Union[Unset, str]): Human-readable identity provider is label.
        management_url (Union[Unset, str]): The endpoint for user details management.
        extra_scope (Union[None, Unset, str]): Space-separated list of scopes to request during authentication.
        user_field (Union[Unset, str]): The field in Waldur User model to be used for looking up the user
        user_claim (Union[Unset, str]): The OIDC claim from the userinfo endpoint to be used as the value for the lookup
            field.
        attribute_mapping (Union[Unset, PatchedIdentityProviderRequestAttributeMapping]): A JSON object mapping Waldur
            User model fields to OIDC claims. Example: {"first_name": "given_name", "last_name": "family_name", "email":
            "email"}
        extra_fields (Union[None, Unset, str]): Space-separated list of extra fields to persist.
    """

    protected_fields: Union[Unset, list[str]] = UNSET
    allowed_redirects: Union[Unset, list[str]] = UNSET
    provider: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    client_id: Union[Unset, str] = UNSET
    client_secret: Union[Unset, str] = UNSET
    verify_ssl: Union[Unset, bool] = UNSET
    enable_post_logout_redirect: Union[Unset, bool] = UNSET
    enable_pkce: Union[Unset, bool] = UNSET
    discovery_url: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    management_url: Union[Unset, str] = UNSET
    extra_scope: Union[None, Unset, str] = UNSET
    user_field: Union[Unset, str] = UNSET
    user_claim: Union[Unset, str] = UNSET
    attribute_mapping: Union[Unset, "PatchedIdentityProviderRequestAttributeMapping"] = UNSET
    extra_fields: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        protected_fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.protected_fields, Unset):
            protected_fields = self.protected_fields

        allowed_redirects: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_redirects, Unset):
            allowed_redirects = self.allowed_redirects

        provider = self.provider

        is_active = self.is_active

        client_id = self.client_id

        client_secret = self.client_secret

        verify_ssl = self.verify_ssl

        enable_post_logout_redirect = self.enable_post_logout_redirect

        enable_pkce = self.enable_pkce

        discovery_url = self.discovery_url

        label = self.label

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
        field_dict.update({})
        if protected_fields is not UNSET:
            field_dict["protected_fields"] = protected_fields
        if allowed_redirects is not UNSET:
            field_dict["allowed_redirects"] = allowed_redirects
        if provider is not UNSET:
            field_dict["provider"] = provider
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
        if label is not UNSET:
            field_dict["label"] = label
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
        from ..models.patched_identity_provider_request_attribute_mapping import (
            PatchedIdentityProviderRequestAttributeMapping,
        )

        d = dict(src_dict)
        protected_fields = cast(list[str], d.pop("protected_fields", UNSET))

        allowed_redirects = cast(list[str], d.pop("allowed_redirects", UNSET))

        provider = d.pop("provider", UNSET)

        is_active = d.pop("is_active", UNSET)

        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        verify_ssl = d.pop("verify_ssl", UNSET)

        enable_post_logout_redirect = d.pop("enable_post_logout_redirect", UNSET)

        enable_pkce = d.pop("enable_pkce", UNSET)

        discovery_url = d.pop("discovery_url", UNSET)

        label = d.pop("label", UNSET)

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
        attribute_mapping: Union[Unset, PatchedIdentityProviderRequestAttributeMapping]
        if isinstance(_attribute_mapping, Unset):
            attribute_mapping = UNSET
        else:
            attribute_mapping = PatchedIdentityProviderRequestAttributeMapping.from_dict(_attribute_mapping)

        def _parse_extra_fields(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        extra_fields = _parse_extra_fields(d.pop("extra_fields", UNSET))

        patched_identity_provider_request = cls(
            protected_fields=protected_fields,
            allowed_redirects=allowed_redirects,
            provider=provider,
            is_active=is_active,
            client_id=client_id,
            client_secret=client_secret,
            verify_ssl=verify_ssl,
            enable_post_logout_redirect=enable_post_logout_redirect,
            enable_pkce=enable_pkce,
            discovery_url=discovery_url,
            label=label,
            management_url=management_url,
            extra_scope=extra_scope,
            user_field=user_field,
            user_claim=user_claim,
            attribute_mapping=attribute_mapping,
            extra_fields=extra_fields,
        )

        patched_identity_provider_request.additional_properties = d
        return patched_identity_provider_request

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
