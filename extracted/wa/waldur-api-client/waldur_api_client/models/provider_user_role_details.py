import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.blank_enum import BlankEnum
from ..models.gender_enum import GenderEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProviderUserRoleDetails")


@_attrs_define
class ProviderUserRoleDetails:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[None, Unset, datetime.datetime]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        user_email (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        user_username (Union[Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        user_uuid (Union[Unset, UUID]):
        user_image (Union[Unset, str]):
        created_by_full_name (Union[Unset, str]):
        created_by_uuid (Union[Unset, UUID]):
        source (Union[Unset, str]):
        user_phone_number (Union[Unset, str]):
        user_organization (Union[Unset, str]):
        user_job_title (Union[Unset, str]):
        user_affiliations (Union[Unset, list[str]]): Person's affiliation within organization such as student, faculty,
            staff.
        user_gender (Union[BlankEnum, GenderEnum, None, Unset]): User's gender (male, female, or unknown)
        user_personal_title (Union[Unset, str]): Honorific title (Mr, Ms, Dr, Prof, etc.)
        user_place_of_birth (Union[Unset, str]):
        user_address (Union[Unset, str]):
        user_country_of_residence (Union[Unset, str]):
        user_nationality (Union[Unset, str]): Primary citizenship (ISO 3166-1 alpha-2 code)
        user_nationalities (Union[Unset, list[str]]): List of all citizenships (ISO 3166-1 alpha-2 codes)
        user_organization_country (Union[Unset, str]):
        user_organization_type (Union[Unset, str]): SCHAC URN (e.g., urn:schac:homeOrganizationType:int:university)
        user_organization_registry_code (Union[Unset, str]): Company registration code of the user's organization, if
            known
        user_organization_vat_code (Union[Unset, str]): VAT code of the user's organization
        user_organization_address (Union[Unset, str]): Postal address of the user's organization
        user_eduperson_assurance (Union[Unset, list[str]]): REFEDS assurance profile URIs from identity provider
        user_civil_number (Union[None, Unset, str]):
        user_birth_date (Union[None, Unset, datetime.date]):
        user_identity_source (Union[Unset, str]): Indicates what identity provider was used.
        user_uid_number (Union[None, Unset, int]): POSIX UID from the identity provider; used when an offering's
            uid_source is 'user_attribute'.
        user_primary_gid (Union[None, Unset, int]): POSIX primary GID from the identity provider; used when an
            offering's gid_source is 'user_attribute'.
        user_active_isds (Union[Unset, list[str]]): List of ISDs that have asserted this user exists. User is
            deactivated when this becomes empty.
    """

    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    expiration_time: Union[None, Unset, datetime.datetime] = UNSET
    role_name: Union[Unset, str] = UNSET
    role_uuid: Union[Unset, UUID] = UNSET
    user_email: Union[Unset, str] = UNSET
    user_full_name: Union[Unset, str] = UNSET
    user_username: Union[Unset, str] = UNSET
    user_uuid: Union[Unset, UUID] = UNSET
    user_image: Union[Unset, str] = UNSET
    created_by_full_name: Union[Unset, str] = UNSET
    created_by_uuid: Union[Unset, UUID] = UNSET
    source: Union[Unset, str] = UNSET
    user_phone_number: Union[Unset, str] = UNSET
    user_organization: Union[Unset, str] = UNSET
    user_job_title: Union[Unset, str] = UNSET
    user_affiliations: Union[Unset, list[str]] = UNSET
    user_gender: Union[BlankEnum, GenderEnum, None, Unset] = UNSET
    user_personal_title: Union[Unset, str] = UNSET
    user_place_of_birth: Union[Unset, str] = UNSET
    user_address: Union[Unset, str] = UNSET
    user_country_of_residence: Union[Unset, str] = UNSET
    user_nationality: Union[Unset, str] = UNSET
    user_nationalities: Union[Unset, list[str]] = UNSET
    user_organization_country: Union[Unset, str] = UNSET
    user_organization_type: Union[Unset, str] = UNSET
    user_organization_registry_code: Union[Unset, str] = UNSET
    user_organization_vat_code: Union[Unset, str] = UNSET
    user_organization_address: Union[Unset, str] = UNSET
    user_eduperson_assurance: Union[Unset, list[str]] = UNSET
    user_civil_number: Union[None, Unset, str] = UNSET
    user_birth_date: Union[None, Unset, datetime.date] = UNSET
    user_identity_source: Union[Unset, str] = UNSET
    user_uid_number: Union[None, Unset, int] = UNSET
    user_primary_gid: Union[None, Unset, int] = UNSET
    user_active_isds: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        expiration_time: Union[None, Unset, str]
        if isinstance(self.expiration_time, Unset):
            expiration_time = UNSET
        elif isinstance(self.expiration_time, datetime.datetime):
            expiration_time = self.expiration_time.isoformat()
        else:
            expiration_time = self.expiration_time

        role_name = self.role_name

        role_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.role_uuid, Unset):
            role_uuid = str(self.role_uuid)

        user_email = self.user_email

        user_full_name = self.user_full_name

        user_username = self.user_username

        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        user_image = self.user_image

        created_by_full_name = self.created_by_full_name

        created_by_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.created_by_uuid, Unset):
            created_by_uuid = str(self.created_by_uuid)

        source = self.source

        user_phone_number = self.user_phone_number

        user_organization = self.user_organization

        user_job_title = self.user_job_title

        user_affiliations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_affiliations, Unset):
            user_affiliations = self.user_affiliations

        user_gender: Union[None, Unset, str]
        if isinstance(self.user_gender, Unset):
            user_gender = UNSET
        elif isinstance(self.user_gender, GenderEnum):
            user_gender = self.user_gender.value
        elif isinstance(self.user_gender, BlankEnum):
            user_gender = self.user_gender.value
        else:
            user_gender = self.user_gender

        user_personal_title = self.user_personal_title

        user_place_of_birth = self.user_place_of_birth

        user_address = self.user_address

        user_country_of_residence = self.user_country_of_residence

        user_nationality = self.user_nationality

        user_nationalities: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_nationalities, Unset):
            user_nationalities = self.user_nationalities

        user_organization_country = self.user_organization_country

        user_organization_type = self.user_organization_type

        user_organization_registry_code = self.user_organization_registry_code

        user_organization_vat_code = self.user_organization_vat_code

        user_organization_address = self.user_organization_address

        user_eduperson_assurance: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_eduperson_assurance, Unset):
            user_eduperson_assurance = self.user_eduperson_assurance

        user_civil_number: Union[None, Unset, str]
        if isinstance(self.user_civil_number, Unset):
            user_civil_number = UNSET
        else:
            user_civil_number = self.user_civil_number

        user_birth_date: Union[None, Unset, str]
        if isinstance(self.user_birth_date, Unset):
            user_birth_date = UNSET
        elif isinstance(self.user_birth_date, datetime.date):
            user_birth_date = self.user_birth_date.isoformat()
        else:
            user_birth_date = self.user_birth_date

        user_identity_source = self.user_identity_source

        user_uid_number: Union[None, Unset, int]
        if isinstance(self.user_uid_number, Unset):
            user_uid_number = UNSET
        else:
            user_uid_number = self.user_uid_number

        user_primary_gid: Union[None, Unset, int]
        if isinstance(self.user_primary_gid, Unset):
            user_primary_gid = UNSET
        else:
            user_primary_gid = self.user_primary_gid

        user_active_isds: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_active_isds, Unset):
            user_active_isds = self.user_active_isds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if expiration_time is not UNSET:
            field_dict["expiration_time"] = expiration_time
        if role_name is not UNSET:
            field_dict["role_name"] = role_name
        if role_uuid is not UNSET:
            field_dict["role_uuid"] = role_uuid
        if user_email is not UNSET:
            field_dict["user_email"] = user_email
        if user_full_name is not UNSET:
            field_dict["user_full_name"] = user_full_name
        if user_username is not UNSET:
            field_dict["user_username"] = user_username
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if user_image is not UNSET:
            field_dict["user_image"] = user_image
        if created_by_full_name is not UNSET:
            field_dict["created_by_full_name"] = created_by_full_name
        if created_by_uuid is not UNSET:
            field_dict["created_by_uuid"] = created_by_uuid
        if source is not UNSET:
            field_dict["source"] = source
        if user_phone_number is not UNSET:
            field_dict["user_phone_number"] = user_phone_number
        if user_organization is not UNSET:
            field_dict["user_organization"] = user_organization
        if user_job_title is not UNSET:
            field_dict["user_job_title"] = user_job_title
        if user_affiliations is not UNSET:
            field_dict["user_affiliations"] = user_affiliations
        if user_gender is not UNSET:
            field_dict["user_gender"] = user_gender
        if user_personal_title is not UNSET:
            field_dict["user_personal_title"] = user_personal_title
        if user_place_of_birth is not UNSET:
            field_dict["user_place_of_birth"] = user_place_of_birth
        if user_address is not UNSET:
            field_dict["user_address"] = user_address
        if user_country_of_residence is not UNSET:
            field_dict["user_country_of_residence"] = user_country_of_residence
        if user_nationality is not UNSET:
            field_dict["user_nationality"] = user_nationality
        if user_nationalities is not UNSET:
            field_dict["user_nationalities"] = user_nationalities
        if user_organization_country is not UNSET:
            field_dict["user_organization_country"] = user_organization_country
        if user_organization_type is not UNSET:
            field_dict["user_organization_type"] = user_organization_type
        if user_organization_registry_code is not UNSET:
            field_dict["user_organization_registry_code"] = user_organization_registry_code
        if user_organization_vat_code is not UNSET:
            field_dict["user_organization_vat_code"] = user_organization_vat_code
        if user_organization_address is not UNSET:
            field_dict["user_organization_address"] = user_organization_address
        if user_eduperson_assurance is not UNSET:
            field_dict["user_eduperson_assurance"] = user_eduperson_assurance
        if user_civil_number is not UNSET:
            field_dict["user_civil_number"] = user_civil_number
        if user_birth_date is not UNSET:
            field_dict["user_birth_date"] = user_birth_date
        if user_identity_source is not UNSET:
            field_dict["user_identity_source"] = user_identity_source
        if user_uid_number is not UNSET:
            field_dict["user_uid_number"] = user_uid_number
        if user_primary_gid is not UNSET:
            field_dict["user_primary_gid"] = user_primary_gid
        if user_active_isds is not UNSET:
            field_dict["user_active_isds"] = user_active_isds

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

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        def _parse_expiration_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiration_time_type_0 = isoparse(data)

                return expiration_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expiration_time = _parse_expiration_time(d.pop("expiration_time", UNSET))

        role_name = d.pop("role_name", UNSET)

        _role_uuid = d.pop("role_uuid", UNSET)
        role_uuid: Union[Unset, UUID]
        if isinstance(_role_uuid, Unset):
            role_uuid = UNSET
        else:
            role_uuid = UUID(_role_uuid)

        user_email = d.pop("user_email", UNSET)

        user_full_name = d.pop("user_full_name", UNSET)

        user_username = d.pop("user_username", UNSET)

        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        user_image = d.pop("user_image", UNSET)

        created_by_full_name = d.pop("created_by_full_name", UNSET)

        _created_by_uuid = d.pop("created_by_uuid", UNSET)
        created_by_uuid: Union[Unset, UUID]
        if isinstance(_created_by_uuid, Unset):
            created_by_uuid = UNSET
        else:
            created_by_uuid = UUID(_created_by_uuid)

        source = d.pop("source", UNSET)

        user_phone_number = d.pop("user_phone_number", UNSET)

        user_organization = d.pop("user_organization", UNSET)

        user_job_title = d.pop("user_job_title", UNSET)

        user_affiliations = cast(list[str], d.pop("user_affiliations", UNSET))

        def _parse_user_gender(data: object) -> Union[BlankEnum, GenderEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_gender_type_0 = GenderEnum(data)

                return user_gender_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_gender_type_1 = BlankEnum(data)

                return user_gender_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, GenderEnum, None, Unset], data)

        user_gender = _parse_user_gender(d.pop("user_gender", UNSET))

        user_personal_title = d.pop("user_personal_title", UNSET)

        user_place_of_birth = d.pop("user_place_of_birth", UNSET)

        user_address = d.pop("user_address", UNSET)

        user_country_of_residence = d.pop("user_country_of_residence", UNSET)

        user_nationality = d.pop("user_nationality", UNSET)

        user_nationalities = cast(list[str], d.pop("user_nationalities", UNSET))

        user_organization_country = d.pop("user_organization_country", UNSET)

        user_organization_type = d.pop("user_organization_type", UNSET)

        user_organization_registry_code = d.pop("user_organization_registry_code", UNSET)

        user_organization_vat_code = d.pop("user_organization_vat_code", UNSET)

        user_organization_address = d.pop("user_organization_address", UNSET)

        user_eduperson_assurance = cast(list[str], d.pop("user_eduperson_assurance", UNSET))

        def _parse_user_civil_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_civil_number = _parse_user_civil_number(d.pop("user_civil_number", UNSET))

        def _parse_user_birth_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_birth_date_type_0 = isoparse(data).date()

                return user_birth_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        user_birth_date = _parse_user_birth_date(d.pop("user_birth_date", UNSET))

        user_identity_source = d.pop("user_identity_source", UNSET)

        def _parse_user_uid_number(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        user_uid_number = _parse_user_uid_number(d.pop("user_uid_number", UNSET))

        def _parse_user_primary_gid(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        user_primary_gid = _parse_user_primary_gid(d.pop("user_primary_gid", UNSET))

        user_active_isds = cast(list[str], d.pop("user_active_isds", UNSET))

        provider_user_role_details = cls(
            uuid=uuid,
            created=created,
            expiration_time=expiration_time,
            role_name=role_name,
            role_uuid=role_uuid,
            user_email=user_email,
            user_full_name=user_full_name,
            user_username=user_username,
            user_uuid=user_uuid,
            user_image=user_image,
            created_by_full_name=created_by_full_name,
            created_by_uuid=created_by_uuid,
            source=source,
            user_phone_number=user_phone_number,
            user_organization=user_organization,
            user_job_title=user_job_title,
            user_affiliations=user_affiliations,
            user_gender=user_gender,
            user_personal_title=user_personal_title,
            user_place_of_birth=user_place_of_birth,
            user_address=user_address,
            user_country_of_residence=user_country_of_residence,
            user_nationality=user_nationality,
            user_nationalities=user_nationalities,
            user_organization_country=user_organization_country,
            user_organization_type=user_organization_type,
            user_organization_registry_code=user_organization_registry_code,
            user_organization_vat_code=user_organization_vat_code,
            user_organization_address=user_organization_address,
            user_eduperson_assurance=user_eduperson_assurance,
            user_civil_number=user_civil_number,
            user_birth_date=user_birth_date,
            user_identity_source=user_identity_source,
            user_uid_number=user_uid_number,
            user_primary_gid=user_primary_gid,
            user_active_isds=user_active_isds,
        )

        provider_user_role_details.additional_properties = d
        return provider_user_role_details

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
