from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedCallApplicantAttributeConfigRequest")


@_attrs_define
class PatchedCallApplicantAttributeConfigRequest:
    """
    Attributes:
        call (Union[Unset, UUID]):
        expose_full_name (Union[Unset, bool]):
        expose_email (Union[Unset, bool]):
        expose_organization (Union[Unset, bool]):
        expose_affiliations (Union[Unset, bool]):
        expose_organization_type (Union[Unset, bool]):
        expose_organization_country (Union[Unset, bool]):
        expose_nationality (Union[Unset, bool]):
        expose_nationalities (Union[Unset, bool]):
        expose_country_of_residence (Union[Unset, bool]):
        expose_eduperson_assurance (Union[Unset, bool]):
        expose_identity_source (Union[Unset, bool]):
        reviewers_see_applicant_details (Union[Unset, bool]): If True, reviewers see applicant identity. If False,
            proposals are anonymized for reviewers.
    """

    call: Union[Unset, UUID] = UNSET
    expose_full_name: Union[Unset, bool] = UNSET
    expose_email: Union[Unset, bool] = UNSET
    expose_organization: Union[Unset, bool] = UNSET
    expose_affiliations: Union[Unset, bool] = UNSET
    expose_organization_type: Union[Unset, bool] = UNSET
    expose_organization_country: Union[Unset, bool] = UNSET
    expose_nationality: Union[Unset, bool] = UNSET
    expose_nationalities: Union[Unset, bool] = UNSET
    expose_country_of_residence: Union[Unset, bool] = UNSET
    expose_eduperson_assurance: Union[Unset, bool] = UNSET
    expose_identity_source: Union[Unset, bool] = UNSET
    reviewers_see_applicant_details: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call: Union[Unset, str] = UNSET
        if not isinstance(self.call, Unset):
            call = str(self.call)

        expose_full_name = self.expose_full_name

        expose_email = self.expose_email

        expose_organization = self.expose_organization

        expose_affiliations = self.expose_affiliations

        expose_organization_type = self.expose_organization_type

        expose_organization_country = self.expose_organization_country

        expose_nationality = self.expose_nationality

        expose_nationalities = self.expose_nationalities

        expose_country_of_residence = self.expose_country_of_residence

        expose_eduperson_assurance = self.expose_eduperson_assurance

        expose_identity_source = self.expose_identity_source

        reviewers_see_applicant_details = self.reviewers_see_applicant_details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if call is not UNSET:
            field_dict["call"] = call
        if expose_full_name is not UNSET:
            field_dict["expose_full_name"] = expose_full_name
        if expose_email is not UNSET:
            field_dict["expose_email"] = expose_email
        if expose_organization is not UNSET:
            field_dict["expose_organization"] = expose_organization
        if expose_affiliations is not UNSET:
            field_dict["expose_affiliations"] = expose_affiliations
        if expose_organization_type is not UNSET:
            field_dict["expose_organization_type"] = expose_organization_type
        if expose_organization_country is not UNSET:
            field_dict["expose_organization_country"] = expose_organization_country
        if expose_nationality is not UNSET:
            field_dict["expose_nationality"] = expose_nationality
        if expose_nationalities is not UNSET:
            field_dict["expose_nationalities"] = expose_nationalities
        if expose_country_of_residence is not UNSET:
            field_dict["expose_country_of_residence"] = expose_country_of_residence
        if expose_eduperson_assurance is not UNSET:
            field_dict["expose_eduperson_assurance"] = expose_eduperson_assurance
        if expose_identity_source is not UNSET:
            field_dict["expose_identity_source"] = expose_identity_source
        if reviewers_see_applicant_details is not UNSET:
            field_dict["reviewers_see_applicant_details"] = reviewers_see_applicant_details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _call = d.pop("call", UNSET)
        call: Union[Unset, UUID]
        if isinstance(_call, Unset):
            call = UNSET
        else:
            call = UUID(_call)

        expose_full_name = d.pop("expose_full_name", UNSET)

        expose_email = d.pop("expose_email", UNSET)

        expose_organization = d.pop("expose_organization", UNSET)

        expose_affiliations = d.pop("expose_affiliations", UNSET)

        expose_organization_type = d.pop("expose_organization_type", UNSET)

        expose_organization_country = d.pop("expose_organization_country", UNSET)

        expose_nationality = d.pop("expose_nationality", UNSET)

        expose_nationalities = d.pop("expose_nationalities", UNSET)

        expose_country_of_residence = d.pop("expose_country_of_residence", UNSET)

        expose_eduperson_assurance = d.pop("expose_eduperson_assurance", UNSET)

        expose_identity_source = d.pop("expose_identity_source", UNSET)

        reviewers_see_applicant_details = d.pop("reviewers_see_applicant_details", UNSET)

        patched_call_applicant_attribute_config_request = cls(
            call=call,
            expose_full_name=expose_full_name,
            expose_email=expose_email,
            expose_organization=expose_organization,
            expose_affiliations=expose_affiliations,
            expose_organization_type=expose_organization_type,
            expose_organization_country=expose_organization_country,
            expose_nationality=expose_nationality,
            expose_nationalities=expose_nationalities,
            expose_country_of_residence=expose_country_of_residence,
            expose_eduperson_assurance=expose_eduperson_assurance,
            expose_identity_source=expose_identity_source,
            reviewers_see_applicant_details=reviewers_see_applicant_details,
        )

        patched_call_applicant_attribute_config_request.additional_properties = d
        return patched_call_applicant_attribute_config_request

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
