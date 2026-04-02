import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.gender_enum import GenderEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="MarketplaceServiceProviderUser")


@_attrs_define
class MarketplaceServiceProviderUser:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        username (Union[Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        full_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        last_name (Union[Unset, str]):
        organization (Union[Unset, str]):
        email (Union[Unset, str]):
        phone_number (Union[Unset, str]):
        projects_count (Union[Unset, int]):
        registration_method (Union[Unset, str]): Indicates what registration method was used.
        affiliations (Union[Unset, Any]): Person's affiliation within organization such as student, faculty, staff.
        is_active (Union[Unset, bool]): Designates whether this user should be treated as active. Unselect this instead
            of deleting accounts.
        job_title (Union[Unset, str]):
        gender (Union[GenderEnum, None, Unset]): ISO 5218 gender code
        personal_title (Union[Unset, str]): Honorific title (Mr, Ms, Dr, Prof, etc.)
        place_of_birth (Union[Unset, str]):
        country_of_residence (Union[Unset, str]):
        nationality (Union[Unset, str]): Primary citizenship (ISO 3166-1 alpha-2 code)
        nationalities (Union[Unset, Any]): List of all citizenships (ISO 3166-1 alpha-2 codes)
        organization_country (Union[Unset, str]):
        organization_type (Union[Unset, str]): SCHAC URN (e.g., urn:schac:homeOrganizationType:int:university)
        organization_registry_code (Union[Unset, str]): Company registration code of the user's organization, if known
        eduperson_assurance (Union[Unset, Any]): REFEDS assurance profile URIs from identity provider
        civil_number (Union[None, Unset, str]):
        birth_date (Union[None, Unset, datetime.date]):
        identity_source (Union[Unset, str]): Indicates what identity provider was used.
        active_isds (Union[Unset, Any]): List of ISDs that have asserted this user exists. User is deactivated when this
            becomes empty.
    """

    uuid: Union[Unset, UUID] = UNSET
    username: Union[Unset, str] = UNSET
    full_name: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    projects_count: Union[Unset, int] = UNSET
    registration_method: Union[Unset, str] = UNSET
    affiliations: Union[Unset, Any] = UNSET
    is_active: Union[Unset, bool] = UNSET
    job_title: Union[Unset, str] = UNSET
    gender: Union[GenderEnum, None, Unset] = UNSET
    personal_title: Union[Unset, str] = UNSET
    place_of_birth: Union[Unset, str] = UNSET
    country_of_residence: Union[Unset, str] = UNSET
    nationality: Union[Unset, str] = UNSET
    nationalities: Union[Unset, Any] = UNSET
    organization_country: Union[Unset, str] = UNSET
    organization_type: Union[Unset, str] = UNSET
    organization_registry_code: Union[Unset, str] = UNSET
    eduperson_assurance: Union[Unset, Any] = UNSET
    civil_number: Union[None, Unset, str] = UNSET
    birth_date: Union[None, Unset, datetime.date] = UNSET
    identity_source: Union[Unset, str] = UNSET
    active_isds: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        username = self.username

        full_name = self.full_name

        first_name = self.first_name

        last_name = self.last_name

        organization = self.organization

        email = self.email

        phone_number = self.phone_number

        projects_count = self.projects_count

        registration_method = self.registration_method

        affiliations = self.affiliations

        is_active = self.is_active

        job_title = self.job_title

        gender: Union[None, Unset, int]
        if isinstance(self.gender, Unset):
            gender = UNSET
        elif isinstance(self.gender, GenderEnum):
            gender = self.gender.value
        else:
            gender = self.gender

        personal_title = self.personal_title

        place_of_birth = self.place_of_birth

        country_of_residence = self.country_of_residence

        nationality = self.nationality

        nationalities = self.nationalities

        organization_country = self.organization_country

        organization_type = self.organization_type

        organization_registry_code = self.organization_registry_code

        eduperson_assurance = self.eduperson_assurance

        civil_number: Union[None, Unset, str]
        if isinstance(self.civil_number, Unset):
            civil_number = UNSET
        else:
            civil_number = self.civil_number

        birth_date: Union[None, Unset, str]
        if isinstance(self.birth_date, Unset):
            birth_date = UNSET
        elif isinstance(self.birth_date, datetime.date):
            birth_date = self.birth_date.isoformat()
        else:
            birth_date = self.birth_date

        identity_source = self.identity_source

        active_isds = self.active_isds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if username is not UNSET:
            field_dict["username"] = username
        if full_name is not UNSET:
            field_dict["full_name"] = full_name
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if organization is not UNSET:
            field_dict["organization"] = organization
        if email is not UNSET:
            field_dict["email"] = email
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if projects_count is not UNSET:
            field_dict["projects_count"] = projects_count
        if registration_method is not UNSET:
            field_dict["registration_method"] = registration_method
        if affiliations is not UNSET:
            field_dict["affiliations"] = affiliations
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if job_title is not UNSET:
            field_dict["job_title"] = job_title
        if gender is not UNSET:
            field_dict["gender"] = gender
        if personal_title is not UNSET:
            field_dict["personal_title"] = personal_title
        if place_of_birth is not UNSET:
            field_dict["place_of_birth"] = place_of_birth
        if country_of_residence is not UNSET:
            field_dict["country_of_residence"] = country_of_residence
        if nationality is not UNSET:
            field_dict["nationality"] = nationality
        if nationalities is not UNSET:
            field_dict["nationalities"] = nationalities
        if organization_country is not UNSET:
            field_dict["organization_country"] = organization_country
        if organization_type is not UNSET:
            field_dict["organization_type"] = organization_type
        if organization_registry_code is not UNSET:
            field_dict["organization_registry_code"] = organization_registry_code
        if eduperson_assurance is not UNSET:
            field_dict["eduperson_assurance"] = eduperson_assurance
        if civil_number is not UNSET:
            field_dict["civil_number"] = civil_number
        if birth_date is not UNSET:
            field_dict["birth_date"] = birth_date
        if identity_source is not UNSET:
            field_dict["identity_source"] = identity_source
        if active_isds is not UNSET:
            field_dict["active_isds"] = active_isds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        username = d.pop("username", UNSET)

        full_name = d.pop("full_name", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        organization = d.pop("organization", UNSET)

        email = d.pop("email", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        projects_count = d.pop("projects_count", UNSET)

        registration_method = d.pop("registration_method", UNSET)

        affiliations = d.pop("affiliations", UNSET)

        is_active = d.pop("is_active", UNSET)

        job_title = d.pop("job_title", UNSET)

        def _parse_gender(data: object) -> Union[GenderEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                gender_type_0 = GenderEnum(data)

                return gender_type_0
            except:  # noqa: E722
                pass
            return cast(Union[GenderEnum, None, Unset], data)

        gender = _parse_gender(d.pop("gender", UNSET))

        personal_title = d.pop("personal_title", UNSET)

        place_of_birth = d.pop("place_of_birth", UNSET)

        country_of_residence = d.pop("country_of_residence", UNSET)

        nationality = d.pop("nationality", UNSET)

        nationalities = d.pop("nationalities", UNSET)

        organization_country = d.pop("organization_country", UNSET)

        organization_type = d.pop("organization_type", UNSET)

        organization_registry_code = d.pop("organization_registry_code", UNSET)

        eduperson_assurance = d.pop("eduperson_assurance", UNSET)

        def _parse_civil_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        civil_number = _parse_civil_number(d.pop("civil_number", UNSET))

        def _parse_birth_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                birth_date_type_0 = isoparse(data).date()

                return birth_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        birth_date = _parse_birth_date(d.pop("birth_date", UNSET))

        identity_source = d.pop("identity_source", UNSET)

        active_isds = d.pop("active_isds", UNSET)

        marketplace_service_provider_user = cls(
            uuid=uuid,
            username=username,
            full_name=full_name,
            first_name=first_name,
            last_name=last_name,
            organization=organization,
            email=email,
            phone_number=phone_number,
            projects_count=projects_count,
            registration_method=registration_method,
            affiliations=affiliations,
            is_active=is_active,
            job_title=job_title,
            gender=gender,
            personal_title=personal_title,
            place_of_birth=place_of_birth,
            country_of_residence=country_of_residence,
            nationality=nationality,
            nationalities=nationalities,
            organization_country=organization_country,
            organization_type=organization_type,
            organization_registry_code=organization_registry_code,
            eduperson_assurance=eduperson_assurance,
            civil_number=civil_number,
            birth_date=birth_date,
            identity_source=identity_source,
            active_isds=active_isds,
        )

        marketplace_service_provider_user.additional_properties = d
        return marketplace_service_provider_user

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
