import datetime
from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from .. import types
from ..models.gender_enum import GenderEnum
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="UserRequest")


@_attrs_define
class UserRequest:
    """
    Attributes:
        username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        email (str):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        native_name (Union[Unset, str]):
        job_title (Union[Unset, str]):
        phone_number (Union[Unset, str]):
        organization (Union[Unset, str]):
        description (Union[Unset, str]):
        is_staff (Union[Unset, bool]): Designates whether the user can log into this admin site.
        is_active (Union[Unset, bool]): Designates whether this user should be treated as active. Unselect this instead
            of deleting accounts.
        is_support (Union[Unset, bool]): Designates whether the user is a global support user.
        token_lifetime (Union[None, Unset, int]): Token lifetime in seconds.
        agree_with_policy (Union[Unset, bool]): User must agree with the policy to register.
        notifications_enabled (Union[Unset, bool]): Designates whether the user is allowed to receive email
            notifications.
        preferred_language (Union[Unset, str]):
        first_name (Union[Unset, str]):
        last_name (Union[Unset, str]):
        birth_date (Union[None, Unset, datetime.date]):
        image (Union[File, None, Unset]):
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
        is_identity_manager (Union[Unset, bool]): Designates whether the user is allowed to manage remote user
            identities.
        managed_isds (Union[Unset, Any]): List of ISD source identifiers this user can manage via Identity Bridge. E.g.,
            ['isd:puhuri', 'isd:fenix']. Non-empty list implies identity manager role.
    """

    username: str
    email: str
    slug: Union[Unset, str] = UNSET
    native_name: Union[Unset, str] = UNSET
    job_title: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    is_staff: Union[Unset, bool] = UNSET
    is_active: Union[Unset, bool] = UNSET
    is_support: Union[Unset, bool] = UNSET
    token_lifetime: Union[None, Unset, int] = UNSET
    agree_with_policy: Union[Unset, bool] = UNSET
    notifications_enabled: Union[Unset, bool] = UNSET
    preferred_language: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    birth_date: Union[None, Unset, datetime.date] = UNSET
    image: Union[File, None, Unset] = UNSET
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
    is_identity_manager: Union[Unset, bool] = UNSET
    managed_isds: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        email = self.email

        slug = self.slug

        native_name = self.native_name

        job_title = self.job_title

        phone_number = self.phone_number

        organization = self.organization

        description = self.description

        is_staff = self.is_staff

        is_active = self.is_active

        is_support = self.is_support

        token_lifetime: Union[None, Unset, int]
        if isinstance(self.token_lifetime, Unset):
            token_lifetime = UNSET
        else:
            token_lifetime = self.token_lifetime

        agree_with_policy = self.agree_with_policy

        notifications_enabled = self.notifications_enabled

        preferred_language = self.preferred_language

        first_name = self.first_name

        last_name = self.last_name

        birth_date: Union[None, Unset, str]
        if isinstance(self.birth_date, Unset):
            birth_date = UNSET
        elif isinstance(self.birth_date, datetime.date):
            birth_date = self.birth_date.isoformat()
        else:
            birth_date = self.birth_date

        image: Union[None, Unset, types.FileTypes]
        if isinstance(self.image, Unset):
            image = UNSET
        elif isinstance(self.image, File):
            image = self.image.to_tuple()

        else:
            image = self.image

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

        is_identity_manager = self.is_identity_manager

        managed_isds = self.managed_isds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "email": email,
            }
        )
        if slug is not UNSET:
            field_dict["slug"] = slug
        if native_name is not UNSET:
            field_dict["native_name"] = native_name
        if job_title is not UNSET:
            field_dict["job_title"] = job_title
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if organization is not UNSET:
            field_dict["organization"] = organization
        if description is not UNSET:
            field_dict["description"] = description
        if is_staff is not UNSET:
            field_dict["is_staff"] = is_staff
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if is_support is not UNSET:
            field_dict["is_support"] = is_support
        if token_lifetime is not UNSET:
            field_dict["token_lifetime"] = token_lifetime
        if agree_with_policy is not UNSET:
            field_dict["agree_with_policy"] = agree_with_policy
        if notifications_enabled is not UNSET:
            field_dict["notifications_enabled"] = notifications_enabled
        if preferred_language is not UNSET:
            field_dict["preferred_language"] = preferred_language
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if birth_date is not UNSET:
            field_dict["birth_date"] = birth_date
        if image is not UNSET:
            field_dict["image"] = image
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
        if is_identity_manager is not UNSET:
            field_dict["is_identity_manager"] = is_identity_manager
        if managed_isds is not UNSET:
            field_dict["managed_isds"] = managed_isds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        email = d.pop("email")

        slug = d.pop("slug", UNSET)

        native_name = d.pop("native_name", UNSET)

        job_title = d.pop("job_title", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        organization = d.pop("organization", UNSET)

        description = d.pop("description", UNSET)

        is_staff = d.pop("is_staff", UNSET)

        is_active = d.pop("is_active", UNSET)

        is_support = d.pop("is_support", UNSET)

        def _parse_token_lifetime(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        token_lifetime = _parse_token_lifetime(d.pop("token_lifetime", UNSET))

        agree_with_policy = d.pop("agree_with_policy", UNSET)

        notifications_enabled = d.pop("notifications_enabled", UNSET)

        preferred_language = d.pop("preferred_language", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

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

        def _parse_image(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                image_type_0 = File(payload=BytesIO(data))

                return image_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        image = _parse_image(d.pop("image", UNSET))

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

        is_identity_manager = d.pop("is_identity_manager", UNSET)

        managed_isds = d.pop("managed_isds", UNSET)

        user_request = cls(
            username=username,
            email=email,
            slug=slug,
            native_name=native_name,
            job_title=job_title,
            phone_number=phone_number,
            organization=organization,
            description=description,
            is_staff=is_staff,
            is_active=is_active,
            is_support=is_support,
            token_lifetime=token_lifetime,
            agree_with_policy=agree_with_policy,
            notifications_enabled=notifications_enabled,
            preferred_language=preferred_language,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            image=image,
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
            is_identity_manager=is_identity_manager,
            managed_isds=managed_isds,
        )

        user_request.additional_properties = d
        return user_request

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
