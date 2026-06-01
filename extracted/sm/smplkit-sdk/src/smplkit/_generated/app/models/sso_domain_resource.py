from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sso_domain_resource_type import check_sso_domain_resource_type
from ..models.sso_domain_resource_type import SSODomainResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.sso_domain import SSODomain


T = TypeVar("T", bound="SSODomainResource")


@_attrs_define
class SSODomainResource:
    """JSON:API resource envelope for an SSO domain.

    The resource `id` is the domain string itself per ADR-035 (e.g.
    `"acme.com"`). The domain is normalised to lower-case on write.

        Example:
            {'attributes': {'created_at': '2026-05-25T11:00:00.000Z', 'dns_txt_token': 'smplkit-domain-
                verification=8c91e7d2a3b4f6e0', 'status': 'verified', 'updated_at': '2026-05-25T11:02:16.616Z', 'verified_at':
                '2026-05-25T11:02:16.616Z'}, 'id': 'acme.com', 'type': 'sso_domain'}

        Attributes:
            type_ (SSODomainResourceType):
            attributes (SSODomain): An email domain claimed by an account for SSO routing. A domain is
                not active until it has been verified by publishing a DNS TXT record
                containing the `dns_txt_token`. Once verified, sign-in attempts on
                that domain route to this account's SSO connection.

                Verified-domain ownership is global across accounts — two accounts
                cannot both hold the same verified domain. Example: {'created_at': '2026-05-25T11:00:00.000Z', 'dns_txt_token':
                'smplkit-domain-verification=8c91e7d2a3b4f6e0', 'status': 'verified', 'updated_at': '2026-05-25T11:02:16.616Z',
                'verified_at': '2026-05-25T11:02:16.616Z'}.
            id (None | str | Unset):
    """

    type_: SSODomainResourceType
    attributes: SSODomain
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sso_domain import SSODomain

        d = dict(src_dict)
        type_ = check_sso_domain_resource_type(d.pop("type"))

        attributes = SSODomain.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        sso_domain_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        sso_domain_resource.additional_properties = d
        return sso_domain_resource

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
