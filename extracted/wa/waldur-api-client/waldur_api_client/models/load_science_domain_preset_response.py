from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LoadScienceDomainPresetResponse")


@_attrs_define
class LoadScienceDomainPresetResponse:
    """
    Attributes:
        created_domains (int):
        created_subdomains (int):
        skipped_domains (int):
        skipped_subdomains (int):
    """

    created_domains: int
    created_subdomains: int
    skipped_domains: int
    skipped_subdomains: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_domains = self.created_domains

        created_subdomains = self.created_subdomains

        skipped_domains = self.skipped_domains

        skipped_subdomains = self.skipped_subdomains

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_domains": created_domains,
                "created_subdomains": created_subdomains,
                "skipped_domains": skipped_domains,
                "skipped_subdomains": skipped_subdomains,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_domains = d.pop("created_domains")

        created_subdomains = d.pop("created_subdomains")

        skipped_domains = d.pop("skipped_domains")

        skipped_subdomains = d.pop("skipped_subdomains")

        load_science_domain_preset_response = cls(
            created_domains=created_domains,
            created_subdomains=created_subdomains,
            skipped_domains=skipped_domains,
            skipped_subdomains=skipped_subdomains,
        )

        load_science_domain_preset_response.additional_properties = d
        return load_science_domain_preset_response

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
