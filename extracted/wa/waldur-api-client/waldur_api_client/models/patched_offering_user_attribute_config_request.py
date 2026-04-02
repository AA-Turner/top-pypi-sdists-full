from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedOfferingUserAttributeConfigRequest")


@_attrs_define
class PatchedOfferingUserAttributeConfigRequest:
    """
    Attributes:
        offering (Union[Unset, UUID]):
        expose_username (Union[Unset, bool]):
        expose_full_name (Union[Unset, bool]):
        expose_email (Union[Unset, bool]):
        expose_phone_number (Union[Unset, bool]):
        expose_organization (Union[Unset, bool]):
        expose_job_title (Union[Unset, bool]):
        expose_affiliations (Union[Unset, bool]):
        expose_gender (Union[Unset, bool]):
        expose_personal_title (Union[Unset, bool]):
        expose_place_of_birth (Union[Unset, bool]):
        expose_country_of_residence (Union[Unset, bool]):
        expose_nationality (Union[Unset, bool]):
        expose_nationalities (Union[Unset, bool]):
        expose_organization_country (Union[Unset, bool]):
        expose_organization_type (Union[Unset, bool]):
        expose_organization_registry_code (Union[Unset, bool]):
        expose_eduperson_assurance (Union[Unset, bool]):
        expose_civil_number (Union[Unset, bool]):
        expose_birth_date (Union[Unset, bool]):
        expose_identity_source (Union[Unset, bool]):
        expose_active_isds (Union[Unset, bool]):
    """

    offering: Union[Unset, UUID] = UNSET
    expose_username: Union[Unset, bool] = UNSET
    expose_full_name: Union[Unset, bool] = UNSET
    expose_email: Union[Unset, bool] = UNSET
    expose_phone_number: Union[Unset, bool] = UNSET
    expose_organization: Union[Unset, bool] = UNSET
    expose_job_title: Union[Unset, bool] = UNSET
    expose_affiliations: Union[Unset, bool] = UNSET
    expose_gender: Union[Unset, bool] = UNSET
    expose_personal_title: Union[Unset, bool] = UNSET
    expose_place_of_birth: Union[Unset, bool] = UNSET
    expose_country_of_residence: Union[Unset, bool] = UNSET
    expose_nationality: Union[Unset, bool] = UNSET
    expose_nationalities: Union[Unset, bool] = UNSET
    expose_organization_country: Union[Unset, bool] = UNSET
    expose_organization_type: Union[Unset, bool] = UNSET
    expose_organization_registry_code: Union[Unset, bool] = UNSET
    expose_eduperson_assurance: Union[Unset, bool] = UNSET
    expose_civil_number: Union[Unset, bool] = UNSET
    expose_birth_date: Union[Unset, bool] = UNSET
    expose_identity_source: Union[Unset, bool] = UNSET
    expose_active_isds: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering: Union[Unset, str] = UNSET
        if not isinstance(self.offering, Unset):
            offering = str(self.offering)

        expose_username = self.expose_username

        expose_full_name = self.expose_full_name

        expose_email = self.expose_email

        expose_phone_number = self.expose_phone_number

        expose_organization = self.expose_organization

        expose_job_title = self.expose_job_title

        expose_affiliations = self.expose_affiliations

        expose_gender = self.expose_gender

        expose_personal_title = self.expose_personal_title

        expose_place_of_birth = self.expose_place_of_birth

        expose_country_of_residence = self.expose_country_of_residence

        expose_nationality = self.expose_nationality

        expose_nationalities = self.expose_nationalities

        expose_organization_country = self.expose_organization_country

        expose_organization_type = self.expose_organization_type

        expose_organization_registry_code = self.expose_organization_registry_code

        expose_eduperson_assurance = self.expose_eduperson_assurance

        expose_civil_number = self.expose_civil_number

        expose_birth_date = self.expose_birth_date

        expose_identity_source = self.expose_identity_source

        expose_active_isds = self.expose_active_isds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if offering is not UNSET:
            field_dict["offering"] = offering
        if expose_username is not UNSET:
            field_dict["expose_username"] = expose_username
        if expose_full_name is not UNSET:
            field_dict["expose_full_name"] = expose_full_name
        if expose_email is not UNSET:
            field_dict["expose_email"] = expose_email
        if expose_phone_number is not UNSET:
            field_dict["expose_phone_number"] = expose_phone_number
        if expose_organization is not UNSET:
            field_dict["expose_organization"] = expose_organization
        if expose_job_title is not UNSET:
            field_dict["expose_job_title"] = expose_job_title
        if expose_affiliations is not UNSET:
            field_dict["expose_affiliations"] = expose_affiliations
        if expose_gender is not UNSET:
            field_dict["expose_gender"] = expose_gender
        if expose_personal_title is not UNSET:
            field_dict["expose_personal_title"] = expose_personal_title
        if expose_place_of_birth is not UNSET:
            field_dict["expose_place_of_birth"] = expose_place_of_birth
        if expose_country_of_residence is not UNSET:
            field_dict["expose_country_of_residence"] = expose_country_of_residence
        if expose_nationality is not UNSET:
            field_dict["expose_nationality"] = expose_nationality
        if expose_nationalities is not UNSET:
            field_dict["expose_nationalities"] = expose_nationalities
        if expose_organization_country is not UNSET:
            field_dict["expose_organization_country"] = expose_organization_country
        if expose_organization_type is not UNSET:
            field_dict["expose_organization_type"] = expose_organization_type
        if expose_organization_registry_code is not UNSET:
            field_dict["expose_organization_registry_code"] = expose_organization_registry_code
        if expose_eduperson_assurance is not UNSET:
            field_dict["expose_eduperson_assurance"] = expose_eduperson_assurance
        if expose_civil_number is not UNSET:
            field_dict["expose_civil_number"] = expose_civil_number
        if expose_birth_date is not UNSET:
            field_dict["expose_birth_date"] = expose_birth_date
        if expose_identity_source is not UNSET:
            field_dict["expose_identity_source"] = expose_identity_source
        if expose_active_isds is not UNSET:
            field_dict["expose_active_isds"] = expose_active_isds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _offering = d.pop("offering", UNSET)
        offering: Union[Unset, UUID]
        if isinstance(_offering, Unset):
            offering = UNSET
        else:
            offering = UUID(_offering)

        expose_username = d.pop("expose_username", UNSET)

        expose_full_name = d.pop("expose_full_name", UNSET)

        expose_email = d.pop("expose_email", UNSET)

        expose_phone_number = d.pop("expose_phone_number", UNSET)

        expose_organization = d.pop("expose_organization", UNSET)

        expose_job_title = d.pop("expose_job_title", UNSET)

        expose_affiliations = d.pop("expose_affiliations", UNSET)

        expose_gender = d.pop("expose_gender", UNSET)

        expose_personal_title = d.pop("expose_personal_title", UNSET)

        expose_place_of_birth = d.pop("expose_place_of_birth", UNSET)

        expose_country_of_residence = d.pop("expose_country_of_residence", UNSET)

        expose_nationality = d.pop("expose_nationality", UNSET)

        expose_nationalities = d.pop("expose_nationalities", UNSET)

        expose_organization_country = d.pop("expose_organization_country", UNSET)

        expose_organization_type = d.pop("expose_organization_type", UNSET)

        expose_organization_registry_code = d.pop("expose_organization_registry_code", UNSET)

        expose_eduperson_assurance = d.pop("expose_eduperson_assurance", UNSET)

        expose_civil_number = d.pop("expose_civil_number", UNSET)

        expose_birth_date = d.pop("expose_birth_date", UNSET)

        expose_identity_source = d.pop("expose_identity_source", UNSET)

        expose_active_isds = d.pop("expose_active_isds", UNSET)

        patched_offering_user_attribute_config_request = cls(
            offering=offering,
            expose_username=expose_username,
            expose_full_name=expose_full_name,
            expose_email=expose_email,
            expose_phone_number=expose_phone_number,
            expose_organization=expose_organization,
            expose_job_title=expose_job_title,
            expose_affiliations=expose_affiliations,
            expose_gender=expose_gender,
            expose_personal_title=expose_personal_title,
            expose_place_of_birth=expose_place_of_birth,
            expose_country_of_residence=expose_country_of_residence,
            expose_nationality=expose_nationality,
            expose_nationalities=expose_nationalities,
            expose_organization_country=expose_organization_country,
            expose_organization_type=expose_organization_type,
            expose_organization_registry_code=expose_organization_registry_code,
            expose_eduperson_assurance=expose_eduperson_assurance,
            expose_civil_number=expose_civil_number,
            expose_birth_date=expose_birth_date,
            expose_identity_source=expose_identity_source,
            expose_active_isds=expose_active_isds,
        )

        patched_offering_user_attribute_config_request.additional_properties = d
        return patched_offering_user_attribute_config_request

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
