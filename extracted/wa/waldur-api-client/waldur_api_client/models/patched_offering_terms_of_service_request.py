from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedOfferingTermsOfServiceRequest")


@_attrs_define
class PatchedOfferingTermsOfServiceRequest:
    """
    Attributes:
        terms_of_service (Union[Unset, str]):
        terms_of_service_link (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        grace_period_days (Union[Unset, int]): Number of days before outdated consents are automatically revoked. Only
            applies when requires_reconsent=True.
    """

    terms_of_service: Union[Unset, str] = UNSET
    terms_of_service_link: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    grace_period_days: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        terms_of_service = self.terms_of_service

        terms_of_service_link = self.terms_of_service_link

        is_active = self.is_active

        grace_period_days = self.grace_period_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if terms_of_service is not UNSET:
            field_dict["terms_of_service"] = terms_of_service
        if terms_of_service_link is not UNSET:
            field_dict["terms_of_service_link"] = terms_of_service_link
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if grace_period_days is not UNSET:
            field_dict["grace_period_days"] = grace_period_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terms_of_service = d.pop("terms_of_service", UNSET)

        terms_of_service_link = d.pop("terms_of_service_link", UNSET)

        is_active = d.pop("is_active", UNSET)

        grace_period_days = d.pop("grace_period_days", UNSET)

        patched_offering_terms_of_service_request = cls(
            terms_of_service=terms_of_service,
            terms_of_service_link=terms_of_service_link,
            is_active=is_active,
            grace_period_days=grace_period_days,
        )

        patched_offering_terms_of_service_request.additional_properties = d
        return patched_offering_terms_of_service_request

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
