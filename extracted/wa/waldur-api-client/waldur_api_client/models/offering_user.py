import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.gender_enum import GenderEnum
from ..models.offering_user_state import OfferingUserState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offering_user_consent_data_type_0 import OfferingUserConsentDataType0


T = TypeVar("T", bound="OfferingUser")


@_attrs_define
class OfferingUser:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        user (Union[Unset, str]):
        offering (Union[Unset, str]):
        username (Union[None, Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        offering_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        user_username (Union[Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        user_full_name (Union[Unset, str]):
        user_first_name (Union[Unset, str]):
        user_last_name (Union[Unset, str]):
        user_email (Union[Unset, str]):
        user_phone_number (Union[Unset, str]):
        user_organization (Union[Unset, str]):
        user_job_title (Union[Unset, str]):
        user_affiliations (Union[Unset, Any]): Person's affiliation within organization such as student, faculty, staff.
        user_gender (Union[GenderEnum, None, Unset]): ISO 5218 gender code
        user_personal_title (Union[Unset, str]): Honorific title (Mr, Ms, Dr, Prof, etc.)
        user_place_of_birth (Union[Unset, str]):
        user_country_of_residence (Union[Unset, str]):
        user_nationality (Union[Unset, str]): Primary citizenship (ISO 3166-1 alpha-2 code)
        user_nationalities (Union[Unset, Any]): List of all citizenships (ISO 3166-1 alpha-2 codes)
        user_organization_country (Union[Unset, str]):
        user_organization_type (Union[Unset, str]): SCHAC URN (e.g., urn:schac:homeOrganizationType:int:university)
        user_organization_registry_code (Union[Unset, str]): Company registration code of the user's organization, if
            known
        user_eduperson_assurance (Union[Unset, Any]): REFEDS assurance profile URIs from identity provider
        user_civil_number (Union[None, Unset, str]):
        user_birth_date (Union[None, Unset, datetime.date]):
        user_identity_source (Union[Unset, str]): Indicates what identity provider was used.
        user_active_isds (Union[Unset, Any]): List of ISDs that have asserted this user exists. User is deactivated when
            this becomes empty.
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        is_restricted (Union[Unset, bool]): Signal to service if the user account is restricted or not
        state (Union[Unset, OfferingUserState]):
        service_provider_comment (Union[Unset, str]): Additional comment for pending states like validation or account
            linking
        service_provider_comment_url (Union[Unset, str]): URL link for additional information or actions related to
            service provider comment
        has_consent (Union[Unset, bool]): Check if the user has active consent for this offering.
        requires_reconsent (Union[Unset, bool]): Check if the user needs to re-consent due to ToS changes.
        has_compliance_checklist (Union[Unset, bool]): Check if the offering user has a connected compliance checklist
            completion.
        consent_data (Union['OfferingUserConsentDataType0', None, Unset]): User consent data including uuid, version,
            and agreement_date
        is_profile_complete (Union[Unset, bool]):
        missing_profile_attributes (Union[Unset, list[str]]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    user: Union[Unset, str] = UNSET
    offering: Union[Unset, str] = UNSET
    username: Union[None, Unset, str] = UNSET
    offering_uuid: Union[Unset, UUID] = UNSET
    offering_name: Union[Unset, str] = UNSET
    user_uuid: Union[Unset, UUID] = UNSET
    user_username: Union[Unset, str] = UNSET
    user_full_name: Union[Unset, str] = UNSET
    user_first_name: Union[Unset, str] = UNSET
    user_last_name: Union[Unset, str] = UNSET
    user_email: Union[Unset, str] = UNSET
    user_phone_number: Union[Unset, str] = UNSET
    user_organization: Union[Unset, str] = UNSET
    user_job_title: Union[Unset, str] = UNSET
    user_affiliations: Union[Unset, Any] = UNSET
    user_gender: Union[GenderEnum, None, Unset] = UNSET
    user_personal_title: Union[Unset, str] = UNSET
    user_place_of_birth: Union[Unset, str] = UNSET
    user_country_of_residence: Union[Unset, str] = UNSET
    user_nationality: Union[Unset, str] = UNSET
    user_nationalities: Union[Unset, Any] = UNSET
    user_organization_country: Union[Unset, str] = UNSET
    user_organization_type: Union[Unset, str] = UNSET
    user_organization_registry_code: Union[Unset, str] = UNSET
    user_eduperson_assurance: Union[Unset, Any] = UNSET
    user_civil_number: Union[None, Unset, str] = UNSET
    user_birth_date: Union[None, Unset, datetime.date] = UNSET
    user_identity_source: Union[Unset, str] = UNSET
    user_active_isds: Union[Unset, Any] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    is_restricted: Union[Unset, bool] = UNSET
    state: Union[Unset, OfferingUserState] = UNSET
    service_provider_comment: Union[Unset, str] = UNSET
    service_provider_comment_url: Union[Unset, str] = UNSET
    has_consent: Union[Unset, bool] = UNSET
    requires_reconsent: Union[Unset, bool] = UNSET
    has_compliance_checklist: Union[Unset, bool] = UNSET
    consent_data: Union["OfferingUserConsentDataType0", None, Unset] = UNSET
    is_profile_complete: Union[Unset, bool] = UNSET
    missing_profile_attributes: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.offering_user_consent_data_type_0 import OfferingUserConsentDataType0

        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        user = self.user

        offering = self.offering

        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        user_username = self.user_username

        user_full_name = self.user_full_name

        user_first_name = self.user_first_name

        user_last_name = self.user_last_name

        user_email = self.user_email

        user_phone_number = self.user_phone_number

        user_organization = self.user_organization

        user_job_title = self.user_job_title

        user_affiliations = self.user_affiliations

        user_gender: Union[None, Unset, int]
        if isinstance(self.user_gender, Unset):
            user_gender = UNSET
        elif isinstance(self.user_gender, GenderEnum):
            user_gender = self.user_gender.value
        else:
            user_gender = self.user_gender

        user_personal_title = self.user_personal_title

        user_place_of_birth = self.user_place_of_birth

        user_country_of_residence = self.user_country_of_residence

        user_nationality = self.user_nationality

        user_nationalities = self.user_nationalities

        user_organization_country = self.user_organization_country

        user_organization_type = self.user_organization_type

        user_organization_registry_code = self.user_organization_registry_code

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

        user_active_isds = self.user_active_isds

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        is_restricted = self.is_restricted

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        service_provider_comment = self.service_provider_comment

        service_provider_comment_url = self.service_provider_comment_url

        has_consent = self.has_consent

        requires_reconsent = self.requires_reconsent

        has_compliance_checklist = self.has_compliance_checklist

        consent_data: Union[None, Unset, dict[str, Any]]
        if isinstance(self.consent_data, Unset):
            consent_data = UNSET
        elif isinstance(self.consent_data, OfferingUserConsentDataType0):
            consent_data = self.consent_data.to_dict()
        else:
            consent_data = self.consent_data

        is_profile_complete = self.is_profile_complete

        missing_profile_attributes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.missing_profile_attributes, Unset):
            missing_profile_attributes = self.missing_profile_attributes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if user is not UNSET:
            field_dict["user"] = user
        if offering is not UNSET:
            field_dict["offering"] = offering
        if username is not UNSET:
            field_dict["username"] = username
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if offering_name is not UNSET:
            field_dict["offering_name"] = offering_name
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if user_username is not UNSET:
            field_dict["user_username"] = user_username
        if user_full_name is not UNSET:
            field_dict["user_full_name"] = user_full_name
        if user_first_name is not UNSET:
            field_dict["user_first_name"] = user_first_name
        if user_last_name is not UNSET:
            field_dict["user_last_name"] = user_last_name
        if user_email is not UNSET:
            field_dict["user_email"] = user_email
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
        if user_eduperson_assurance is not UNSET:
            field_dict["user_eduperson_assurance"] = user_eduperson_assurance
        if user_civil_number is not UNSET:
            field_dict["user_civil_number"] = user_civil_number
        if user_birth_date is not UNSET:
            field_dict["user_birth_date"] = user_birth_date
        if user_identity_source is not UNSET:
            field_dict["user_identity_source"] = user_identity_source
        if user_active_isds is not UNSET:
            field_dict["user_active_isds"] = user_active_isds
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if is_restricted is not UNSET:
            field_dict["is_restricted"] = is_restricted
        if state is not UNSET:
            field_dict["state"] = state
        if service_provider_comment is not UNSET:
            field_dict["service_provider_comment"] = service_provider_comment
        if service_provider_comment_url is not UNSET:
            field_dict["service_provider_comment_url"] = service_provider_comment_url
        if has_consent is not UNSET:
            field_dict["has_consent"] = has_consent
        if requires_reconsent is not UNSET:
            field_dict["requires_reconsent"] = requires_reconsent
        if has_compliance_checklist is not UNSET:
            field_dict["has_compliance_checklist"] = has_compliance_checklist
        if consent_data is not UNSET:
            field_dict["consent_data"] = consent_data
        if is_profile_complete is not UNSET:
            field_dict["is_profile_complete"] = is_profile_complete
        if missing_profile_attributes is not UNSET:
            field_dict["missing_profile_attributes"] = missing_profile_attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_user_consent_data_type_0 import OfferingUserConsentDataType0

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        user = d.pop("user", UNSET)

        offering = d.pop("offering", UNSET)

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        _offering_uuid = d.pop("offering_uuid", UNSET)
        offering_uuid: Union[Unset, UUID]
        if isinstance(_offering_uuid, Unset):
            offering_uuid = UNSET
        else:
            offering_uuid = UUID(_offering_uuid)

        offering_name = d.pop("offering_name", UNSET)

        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        user_username = d.pop("user_username", UNSET)

        user_full_name = d.pop("user_full_name", UNSET)

        user_first_name = d.pop("user_first_name", UNSET)

        user_last_name = d.pop("user_last_name", UNSET)

        user_email = d.pop("user_email", UNSET)

        user_phone_number = d.pop("user_phone_number", UNSET)

        user_organization = d.pop("user_organization", UNSET)

        user_job_title = d.pop("user_job_title", UNSET)

        user_affiliations = d.pop("user_affiliations", UNSET)

        def _parse_user_gender(data: object) -> Union[GenderEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                user_gender_type_0 = GenderEnum(data)

                return user_gender_type_0
            except:  # noqa: E722
                pass
            return cast(Union[GenderEnum, None, Unset], data)

        user_gender = _parse_user_gender(d.pop("user_gender", UNSET))

        user_personal_title = d.pop("user_personal_title", UNSET)

        user_place_of_birth = d.pop("user_place_of_birth", UNSET)

        user_country_of_residence = d.pop("user_country_of_residence", UNSET)

        user_nationality = d.pop("user_nationality", UNSET)

        user_nationalities = d.pop("user_nationalities", UNSET)

        user_organization_country = d.pop("user_organization_country", UNSET)

        user_organization_type = d.pop("user_organization_type", UNSET)

        user_organization_registry_code = d.pop("user_organization_registry_code", UNSET)

        user_eduperson_assurance = d.pop("user_eduperson_assurance", UNSET)

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

        user_active_isds = d.pop("user_active_isds", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_name = d.pop("customer_name", UNSET)

        is_restricted = d.pop("is_restricted", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, OfferingUserState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = OfferingUserState(_state)

        service_provider_comment = d.pop("service_provider_comment", UNSET)

        service_provider_comment_url = d.pop("service_provider_comment_url", UNSET)

        has_consent = d.pop("has_consent", UNSET)

        requires_reconsent = d.pop("requires_reconsent", UNSET)

        has_compliance_checklist = d.pop("has_compliance_checklist", UNSET)

        def _parse_consent_data(data: object) -> Union["OfferingUserConsentDataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                consent_data_type_0 = OfferingUserConsentDataType0.from_dict(data)

                return consent_data_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OfferingUserConsentDataType0", None, Unset], data)

        consent_data = _parse_consent_data(d.pop("consent_data", UNSET))

        is_profile_complete = d.pop("is_profile_complete", UNSET)

        missing_profile_attributes = cast(list[str], d.pop("missing_profile_attributes", UNSET))

        offering_user = cls(
            url=url,
            uuid=uuid,
            user=user,
            offering=offering,
            username=username,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            user_uuid=user_uuid,
            user_username=user_username,
            user_full_name=user_full_name,
            user_first_name=user_first_name,
            user_last_name=user_last_name,
            user_email=user_email,
            user_phone_number=user_phone_number,
            user_organization=user_organization,
            user_job_title=user_job_title,
            user_affiliations=user_affiliations,
            user_gender=user_gender,
            user_personal_title=user_personal_title,
            user_place_of_birth=user_place_of_birth,
            user_country_of_residence=user_country_of_residence,
            user_nationality=user_nationality,
            user_nationalities=user_nationalities,
            user_organization_country=user_organization_country,
            user_organization_type=user_organization_type,
            user_organization_registry_code=user_organization_registry_code,
            user_eduperson_assurance=user_eduperson_assurance,
            user_civil_number=user_civil_number,
            user_birth_date=user_birth_date,
            user_identity_source=user_identity_source,
            user_active_isds=user_active_isds,
            created=created,
            modified=modified,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            is_restricted=is_restricted,
            state=state,
            service_provider_comment=service_provider_comment,
            service_provider_comment_url=service_provider_comment_url,
            has_consent=has_consent,
            requires_reconsent=requires_reconsent,
            has_compliance_checklist=has_compliance_checklist,
            consent_data=consent_data,
            is_profile_complete=is_profile_complete,
            missing_profile_attributes=missing_profile_attributes,
        )

        offering_user.additional_properties = d
        return offering_user

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
