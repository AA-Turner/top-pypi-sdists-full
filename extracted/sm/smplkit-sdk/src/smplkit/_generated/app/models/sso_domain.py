from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sso_domain_status import check_sso_domain_status
from ..models.sso_domain_status import SSODomainStatus
from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="SSODomain")


@_attrs_define
class SSODomain:
    """An email domain claimed by an account for SSO routing. A domain is
    not active until it has been verified by publishing a DNS TXT record
    containing the `dns_txt_token`. Once verified, sign-in attempts on
    that domain route to this account's SSO connection.

    Verified-domain ownership is global across accounts — two accounts
    cannot both hold the same verified domain.

        Example:
            {'created_at': '2026-05-25T11:00:00.000Z', 'dns_txt_token': 'smplkit-domain-verification=8c91e7d2a3b4f6e0',
                'status': 'verified', 'updated_at': '2026-05-25T11:02:16.616Z', 'verified_at': '2026-05-25T11:02:16.616Z'}

        Attributes:
            dns_txt_token (None | str | Unset): Token to publish on the domain's DNS as a TXT record to prove ownership. The
                full record value is `smplkit-domain-verification=<token>`.
            verified_at (datetime.datetime | None | Unset): When the domain was verified. Null until verification succeeds.
            status (SSODomainStatus | Unset): Verification status. `pending` means a claim has been registered but DNS TXT
                verification has not yet succeeded. `verified` means the domain is in use for SSO routing.
            created_at (datetime.datetime | None | Unset): When the claim was created.
            updated_at (datetime.datetime | None | Unset): When the claim was last modified.
    """

    dns_txt_token: None | str | Unset = UNSET
    verified_at: datetime.datetime | None | Unset = UNSET
    status: SSODomainStatus | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dns_txt_token: None | str | Unset
        if isinstance(self.dns_txt_token, Unset):
            dns_txt_token = UNSET
        else:
            dns_txt_token = self.dns_txt_token

        verified_at: None | str | Unset
        if isinstance(self.verified_at, Unset):
            verified_at = UNSET
        elif isinstance(self.verified_at, datetime.datetime):
            verified_at = self.verified_at.isoformat()
        else:
            verified_at = self.verified_at

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status

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
        field_dict.update({})
        if dns_txt_token is not UNSET:
            field_dict["dns_txt_token"] = dns_txt_token
        if verified_at is not UNSET:
            field_dict["verified_at"] = verified_at
        if status is not UNSET:
            field_dict["status"] = status
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_dns_txt_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dns_txt_token = _parse_dns_txt_token(d.pop("dns_txt_token", UNSET))

        def _parse_verified_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                verified_at_type_0 = isoparse(data)

                return verified_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        verified_at = _parse_verified_at(d.pop("verified_at", UNSET))

        _status = d.pop("status", UNSET)
        status: SSODomainStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = check_sso_domain_status(_status)

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

        sso_domain = cls(
            dns_txt_token=dns_txt_token,
            verified_at=verified_at,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

        sso_domain.additional_properties = d
        return sso_domain

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
