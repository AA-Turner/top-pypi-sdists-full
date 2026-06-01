from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.sso_domain_resource import SSODomainResource


T = TypeVar("T", bound="SSODomainResponse")


@_attrs_define
class SSODomainResponse:
    """JSON:API single-resource response envelope for an SSO domain.

    Attributes:
        data (SSODomainResource): JSON:API resource envelope for an SSO domain.

            The resource `id` is the domain string itself per ADR-035 (e.g.
            `"acme.com"`). The domain is normalised to lower-case on write. Example: {'attributes': {'created_at':
            '2026-05-25T11:00:00.000Z', 'dns_txt_token': 'smplkit-domain-verification=8c91e7d2a3b4f6e0', 'status':
            'verified', 'updated_at': '2026-05-25T11:02:16.616Z', 'verified_at': '2026-05-25T11:02:16.616Z'}, 'id':
            'acme.com', 'type': 'sso_domain'}.
    """

    data: SSODomainResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sso_domain_resource import SSODomainResource

        d = dict(src_dict)
        data = SSODomainResource.from_dict(d.pop("data"))

        sso_domain_response = cls(
            data=data,
        )

        sso_domain_response.additional_properties = d
        return sso_domain_response

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
