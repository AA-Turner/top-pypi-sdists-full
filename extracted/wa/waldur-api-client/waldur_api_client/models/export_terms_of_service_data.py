from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExportTermsOfServiceData")


@_attrs_define
class ExportTermsOfServiceData:
    """
    Attributes:
        terms_of_service (str):
        terms_of_service_link (str):
        version (str):
        is_active (bool):
        requires_reconsent (bool):
        grace_period_days (Union[None, int]):
    """

    terms_of_service: str
    terms_of_service_link: str
    version: str
    is_active: bool
    requires_reconsent: bool
    grace_period_days: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        terms_of_service = self.terms_of_service

        terms_of_service_link = self.terms_of_service_link

        version = self.version

        is_active = self.is_active

        requires_reconsent = self.requires_reconsent

        grace_period_days: Union[None, int]
        grace_period_days = self.grace_period_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terms_of_service": terms_of_service,
                "terms_of_service_link": terms_of_service_link,
                "version": version,
                "is_active": is_active,
                "requires_reconsent": requires_reconsent,
                "grace_period_days": grace_period_days,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terms_of_service = d.pop("terms_of_service")

        terms_of_service_link = d.pop("terms_of_service_link")

        version = d.pop("version")

        is_active = d.pop("is_active")

        requires_reconsent = d.pop("requires_reconsent")

        def _parse_grace_period_days(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        grace_period_days = _parse_grace_period_days(d.pop("grace_period_days"))

        export_terms_of_service_data = cls(
            terms_of_service=terms_of_service,
            terms_of_service_link=terms_of_service_link,
            version=version,
            is_active=is_active,
            requires_reconsent=requires_reconsent,
            grace_period_days=grace_period_days,
        )

        export_terms_of_service_data.additional_properties = d
        return export_terms_of_service_data

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
