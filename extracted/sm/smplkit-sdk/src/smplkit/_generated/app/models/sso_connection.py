from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sso_connection_default_role import check_sso_connection_default_role
from ..models.sso_connection_default_role import SSOConnectionDefaultRole
from ..models.sso_connection_protocol import check_sso_connection_protocol
from ..models.sso_connection_protocol import SSOConnectionProtocol
from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.sso_connection_group_role_mappings import SSOConnectionGroupRoleMappings


T = TypeVar("T", bound="SSOConnection")


@_attrs_define
class SSOConnection:
    """An account's Single Sign-On connection to a customer-controlled
    identity provider. Configuring a connection lets the account federate
    authentication to its own SAML or OIDC IdP; with `enforced` enabled,
    password and social sign-in are disabled for users on the account's
    verified domains.

    Each account has at most one SSO connection. The Service Provider
    metadata fields (`sp_entity_id`, `acs_url`, `slo_url`) are computed
    on every read from the connection identifier and never stored.

        Example:
            {'acs_url': 'https://app.smplkit.com/api/v1/auth/sso/acs', 'created_at': '2026-05-25T11:02:16.616Z',
                'default_role': 'MEMBER', 'enforced': True, 'group_role_mappings': {'smplkit-admins': 'ADMIN'},
                'oidc_client_id': 'smplkit-acme', 'oidc_issuer': 'https://login.acme.com', 'protocol': 'oidc', 'slo_url':
                'https://app.smplkit.com/api/v1/auth/sso/slo', 'sp_entity_id': 'https://app.smplkit.com/sso/sp', 'updated_at':
                '2026-05-25T11:02:16.616Z'}

        Attributes:
            protocol (SSOConnectionProtocol): Federation protocol. `oidc` for OpenID Connect; `saml` for SAML 2.0.
                Determines which set of IdP fields below are required.
            oidc_issuer (None | str | Unset): OIDC issuer URL — the base from which `.well-known/openid-configuration` is
                discovered. Required when `protocol` is `oidc`; ignored when `protocol` is `saml`.
            oidc_client_id (None | str | Unset): OIDC client identifier issued by the IdP for smplkit. Required when
                `protocol` is `oidc`; ignored otherwise.
            oidc_client_secret (None | str | Unset): OIDC client secret. Write-only — supplied on PUT, never returned by the
                API. Stored envelope-encrypted at rest. Required on first creation of an OIDC connection; on subsequent PUTs,
                omit to retain the existing value.
            saml_idp_entity_id (None | str | Unset): SAML IdP EntityID (typically a URI). Required when `protocol` is
                `saml`; ignored otherwise.
            saml_idp_sso_url (None | str | Unset): SAML IdP single sign-on URL (HTTP-Redirect or HTTP-POST endpoint).
                Required when `protocol` is `saml`.
            saml_idp_slo_url (None | str | Unset): SAML IdP single logout URL. Optional — when present, smplkit will issue
                LogoutRequests on user sign-out.
            saml_idp_x509_cert (None | str | Unset): SAML IdP X.509 signing certificate (PEM-encoded). Required when
                `protocol` is `saml`.
            default_role (SSOConnectionDefaultRole | Unset): Role granted to a user provisioned just-in-time on their first
                SSO login when no group mapping applies. `OWNER` values are downgraded to `ADMIN` for JIT — owner promotion
                remains an explicit account action. Default: 'MEMBER'.
            group_role_mappings (SSOConnectionGroupRoleMappings | Unset): Mapping of IdP group claim values to smplkit
                roles. The first key matching the user's group claims (in declaration order) decides the JIT role; if none
                match, `default_role` applies. Example: `{"smplkit-admins": "ADMIN"}`.
            enforced (bool | Unset): When `true`, password and social sign-in are rejected for users whose email domain
                matches one of the account's verified domains. The account owner is exempt (break-glass). Default: False.
            sp_entity_id (None | str | Unset): Service Provider EntityID to register with the IdP. Computed from the
                connection — paste this value into the IdP's smplkit configuration.
            acs_url (None | str | Unset): Assertion Consumer Service URL (SAML) or redirect URI (OIDC) to register with the
                IdP. Computed.
            slo_url (None | str | Unset): Single Logout URL to register with the IdP. Computed; smplkit accepts logout
                requests here for the SAML case.
            created_at (datetime.datetime | None | Unset): When the connection was created.
            updated_at (datetime.datetime | None | Unset): When the connection was last modified.
    """

    protocol: SSOConnectionProtocol
    oidc_issuer: None | str | Unset = UNSET
    oidc_client_id: None | str | Unset = UNSET
    oidc_client_secret: None | str | Unset = UNSET
    saml_idp_entity_id: None | str | Unset = UNSET
    saml_idp_sso_url: None | str | Unset = UNSET
    saml_idp_slo_url: None | str | Unset = UNSET
    saml_idp_x509_cert: None | str | Unset = UNSET
    default_role: SSOConnectionDefaultRole | Unset = "MEMBER"
    group_role_mappings: SSOConnectionGroupRoleMappings | Unset = UNSET
    enforced: bool | Unset = False
    sp_entity_id: None | str | Unset = UNSET
    acs_url: None | str | Unset = UNSET
    slo_url: None | str | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        protocol: str = self.protocol

        oidc_issuer: None | str | Unset
        if isinstance(self.oidc_issuer, Unset):
            oidc_issuer = UNSET
        else:
            oidc_issuer = self.oidc_issuer

        oidc_client_id: None | str | Unset
        if isinstance(self.oidc_client_id, Unset):
            oidc_client_id = UNSET
        else:
            oidc_client_id = self.oidc_client_id

        oidc_client_secret: None | str | Unset
        if isinstance(self.oidc_client_secret, Unset):
            oidc_client_secret = UNSET
        else:
            oidc_client_secret = self.oidc_client_secret

        saml_idp_entity_id: None | str | Unset
        if isinstance(self.saml_idp_entity_id, Unset):
            saml_idp_entity_id = UNSET
        else:
            saml_idp_entity_id = self.saml_idp_entity_id

        saml_idp_sso_url: None | str | Unset
        if isinstance(self.saml_idp_sso_url, Unset):
            saml_idp_sso_url = UNSET
        else:
            saml_idp_sso_url = self.saml_idp_sso_url

        saml_idp_slo_url: None | str | Unset
        if isinstance(self.saml_idp_slo_url, Unset):
            saml_idp_slo_url = UNSET
        else:
            saml_idp_slo_url = self.saml_idp_slo_url

        saml_idp_x509_cert: None | str | Unset
        if isinstance(self.saml_idp_x509_cert, Unset):
            saml_idp_x509_cert = UNSET
        else:
            saml_idp_x509_cert = self.saml_idp_x509_cert

        default_role: str | Unset = UNSET
        if not isinstance(self.default_role, Unset):
            default_role = self.default_role

        group_role_mappings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.group_role_mappings, Unset):
            group_role_mappings = self.group_role_mappings.to_dict()

        enforced = self.enforced

        sp_entity_id: None | str | Unset
        if isinstance(self.sp_entity_id, Unset):
            sp_entity_id = UNSET
        else:
            sp_entity_id = self.sp_entity_id

        acs_url: None | str | Unset
        if isinstance(self.acs_url, Unset):
            acs_url = UNSET
        else:
            acs_url = self.acs_url

        slo_url: None | str | Unset
        if isinstance(self.slo_url, Unset):
            slo_url = UNSET
        else:
            slo_url = self.slo_url

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "protocol": protocol,
            }
        )
        if oidc_issuer is not UNSET:
            field_dict["oidc_issuer"] = oidc_issuer
        if oidc_client_id is not UNSET:
            field_dict["oidc_client_id"] = oidc_client_id
        if oidc_client_secret is not UNSET:
            field_dict["oidc_client_secret"] = oidc_client_secret
        if saml_idp_entity_id is not UNSET:
            field_dict["saml_idp_entity_id"] = saml_idp_entity_id
        if saml_idp_sso_url is not UNSET:
            field_dict["saml_idp_sso_url"] = saml_idp_sso_url
        if saml_idp_slo_url is not UNSET:
            field_dict["saml_idp_slo_url"] = saml_idp_slo_url
        if saml_idp_x509_cert is not UNSET:
            field_dict["saml_idp_x509_cert"] = saml_idp_x509_cert
        if default_role is not UNSET:
            field_dict["default_role"] = default_role
        if group_role_mappings is not UNSET:
            field_dict["group_role_mappings"] = group_role_mappings
        if enforced is not UNSET:
            field_dict["enforced"] = enforced
        if sp_entity_id is not UNSET:
            field_dict["sp_entity_id"] = sp_entity_id
        if acs_url is not UNSET:
            field_dict["acs_url"] = acs_url
        if slo_url is not UNSET:
            field_dict["slo_url"] = slo_url
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sso_connection_group_role_mappings import SSOConnectionGroupRoleMappings

        d = dict(src_dict)
        protocol = check_sso_connection_protocol(d.pop("protocol"))

        def _parse_oidc_issuer(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        oidc_issuer = _parse_oidc_issuer(d.pop("oidc_issuer", UNSET))

        def _parse_oidc_client_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        oidc_client_id = _parse_oidc_client_id(d.pop("oidc_client_id", UNSET))

        def _parse_oidc_client_secret(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        oidc_client_secret = _parse_oidc_client_secret(d.pop("oidc_client_secret", UNSET))

        def _parse_saml_idp_entity_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        saml_idp_entity_id = _parse_saml_idp_entity_id(d.pop("saml_idp_entity_id", UNSET))

        def _parse_saml_idp_sso_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        saml_idp_sso_url = _parse_saml_idp_sso_url(d.pop("saml_idp_sso_url", UNSET))

        def _parse_saml_idp_slo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        saml_idp_slo_url = _parse_saml_idp_slo_url(d.pop("saml_idp_slo_url", UNSET))

        def _parse_saml_idp_x509_cert(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        saml_idp_x509_cert = _parse_saml_idp_x509_cert(d.pop("saml_idp_x509_cert", UNSET))

        _default_role = d.pop("default_role", UNSET)
        default_role: SSOConnectionDefaultRole | Unset
        if isinstance(_default_role, Unset):
            default_role = UNSET
        else:
            default_role = check_sso_connection_default_role(_default_role)

        _group_role_mappings = d.pop("group_role_mappings", UNSET)
        group_role_mappings: SSOConnectionGroupRoleMappings | Unset
        if isinstance(_group_role_mappings, Unset):
            group_role_mappings = UNSET
        else:
            group_role_mappings = SSOConnectionGroupRoleMappings.from_dict(_group_role_mappings)

        enforced = d.pop("enforced", UNSET)

        def _parse_sp_entity_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sp_entity_id = _parse_sp_entity_id(d.pop("sp_entity_id", UNSET))

        def _parse_acs_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        acs_url = _parse_acs_url(d.pop("acs_url", UNSET))

        def _parse_slo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        slo_url = _parse_slo_url(d.pop("slo_url", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        sso_connection = cls(
            protocol=protocol,
            oidc_issuer=oidc_issuer,
            oidc_client_id=oidc_client_id,
            oidc_client_secret=oidc_client_secret,
            saml_idp_entity_id=saml_idp_entity_id,
            saml_idp_sso_url=saml_idp_sso_url,
            saml_idp_slo_url=saml_idp_slo_url,
            saml_idp_x509_cert=saml_idp_x509_cert,
            default_role=default_role,
            group_role_mappings=group_role_mappings,
            enforced=enforced,
            sp_entity_id=sp_entity_id,
            acs_url=acs_url,
            slo_url=slo_url,
            created_at=created_at,
            updated_at=updated_at,
        )

        sso_connection.additional_properties = d
        return sso_connection

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
