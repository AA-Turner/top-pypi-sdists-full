import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.blank_enum import BlankEnum
from ..models.gender_enum import GenderEnum
from ..models.oecd_fos_2007_code_enum import OecdFos2007CodeEnum
from ..models.proposal_states import ProposalStates
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_round import NestedRound
    from ..models.proposal_can_submit import ProposalCanSubmit
    from ..models.proposal_compliance_status_type_0 import ProposalComplianceStatusType0
    from ..models.proposal_documentation import ProposalDocumentation


T = TypeVar("T", bound="Proposal")


@_attrs_define
class Proposal:
    """
    Attributes:
        uuid (UUID):
        url (str):
        slug (str):
        name (str):
        project_name (str):
        supporting_documentation (list['ProposalDocumentation']):
        state (ProposalStates):
        approved_by (Union[None, str]):
        created_by (Union[None, str]):
        created_by_name (str):
        created_by_uuid (UUID):
        applicant_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        applicant_full_name (str):
        applicant_first_name (str):
        applicant_last_name (str):
        applicant_email (str):
        applicant_registration_method (str): Indicates what registration method was used.
        applicant_phone_number (str):
        applicant_organization (str):
        applicant_organization_country (str):
        applicant_organization_type (str): SCHAC URN (e.g., urn:schac:homeOrganizationType:int:university)
        applicant_organization_registry_code (str): Company registration code of the user's organization, if known
        applicant_job_title (str):
        applicant_affiliations (Any): Person's affiliation within organization such as student, faculty, staff.
        applicant_gender (Union[BlankEnum, GenderEnum, None]): User's gender (male, female, or unknown)
        applicant_personal_title (str): Honorific title (Mr, Ms, Dr, Prof, etc.)
        applicant_place_of_birth (str):
        applicant_address (str):
        applicant_country_of_residence (str):
        applicant_nationality (str): Primary citizenship (ISO 3166-1 alpha-2 code)
        applicant_nationalities (Any): List of all citizenships (ISO 3166-1 alpha-2 codes)
        applicant_eduperson_assurance (Any): REFEDS assurance profile URIs from identity provider
        applicant_identity_source (str): Indicates what identity provider was used.
        applicant_civil_number (Union[None, str]):
        applicant_birth_date (Union[None, datetime.date]):
        applicant_active_isds (Any): List of ISDs that have asserted this user exists. User is deactivated when this
            becomes empty.
        project (Union[None, str]):
        round_ (NestedRound):
        call_uuid (UUID):
        call_name (str):
        call_managing_organisation_uuid (UUID):
        oecd_fos_2007_label (str):
        science_sub_domain_name (str):
        science_domain_uuid (UUID):
        science_domain_name (str):
        allocation_comment (Union[None, str]):
        created (datetime.datetime):
        compliance_status (Union['ProposalComplianceStatusType0', None]):
        can_submit (ProposalCanSubmit):
        description (Union[Unset, str]):
        project_summary (Union[Unset, str]):
        project_is_confidential (Union[Unset, bool]):
        project_has_civilian_purpose (Union[Unset, bool]):
        duration_in_days (Union[None, Unset, int]): Duration in days after provisioning of resources.
        oecd_fos_2007_code (Union[BlankEnum, None, OecdFos2007CodeEnum, Unset]):
        science_sub_domain (Union[None, UUID, Unset]):
    """

    uuid: UUID
    url: str
    slug: str
    name: str
    project_name: str
    supporting_documentation: list["ProposalDocumentation"]
    state: ProposalStates
    approved_by: Union[None, str]
    created_by: Union[None, str]
    created_by_name: str
    created_by_uuid: UUID
    applicant_username: str
    applicant_full_name: str
    applicant_first_name: str
    applicant_last_name: str
    applicant_email: str
    applicant_registration_method: str
    applicant_phone_number: str
    applicant_organization: str
    applicant_organization_country: str
    applicant_organization_type: str
    applicant_organization_registry_code: str
    applicant_job_title: str
    applicant_affiliations: Any
    applicant_gender: Union[BlankEnum, GenderEnum, None]
    applicant_personal_title: str
    applicant_place_of_birth: str
    applicant_address: str
    applicant_country_of_residence: str
    applicant_nationality: str
    applicant_nationalities: Any
    applicant_eduperson_assurance: Any
    applicant_identity_source: str
    applicant_civil_number: Union[None, str]
    applicant_birth_date: Union[None, datetime.date]
    applicant_active_isds: Any
    project: Union[None, str]
    round_: "NestedRound"
    call_uuid: UUID
    call_name: str
    call_managing_organisation_uuid: UUID
    oecd_fos_2007_label: str
    science_sub_domain_name: str
    science_domain_uuid: UUID
    science_domain_name: str
    allocation_comment: Union[None, str]
    created: datetime.datetime
    compliance_status: Union["ProposalComplianceStatusType0", None]
    can_submit: "ProposalCanSubmit"
    description: Union[Unset, str] = UNSET
    project_summary: Union[Unset, str] = UNSET
    project_is_confidential: Union[Unset, bool] = UNSET
    project_has_civilian_purpose: Union[Unset, bool] = UNSET
    duration_in_days: Union[None, Unset, int] = UNSET
    oecd_fos_2007_code: Union[BlankEnum, None, OecdFos2007CodeEnum, Unset] = UNSET
    science_sub_domain: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.proposal_compliance_status_type_0 import ProposalComplianceStatusType0

        uuid = str(self.uuid)

        url = self.url

        slug = self.slug

        name = self.name

        project_name = self.project_name

        supporting_documentation = []
        for supporting_documentation_item_data in self.supporting_documentation:
            supporting_documentation_item = supporting_documentation_item_data.to_dict()
            supporting_documentation.append(supporting_documentation_item)

        state = self.state.value

        approved_by: Union[None, str]
        approved_by = self.approved_by

        created_by: Union[None, str]
        created_by = self.created_by

        created_by_name = self.created_by_name

        created_by_uuid = str(self.created_by_uuid)

        applicant_username = self.applicant_username

        applicant_full_name = self.applicant_full_name

        applicant_first_name = self.applicant_first_name

        applicant_last_name = self.applicant_last_name

        applicant_email = self.applicant_email

        applicant_registration_method = self.applicant_registration_method

        applicant_phone_number = self.applicant_phone_number

        applicant_organization = self.applicant_organization

        applicant_organization_country = self.applicant_organization_country

        applicant_organization_type = self.applicant_organization_type

        applicant_organization_registry_code = self.applicant_organization_registry_code

        applicant_job_title = self.applicant_job_title

        applicant_affiliations = self.applicant_affiliations

        applicant_gender: Union[None, str]
        if isinstance(self.applicant_gender, GenderEnum):
            applicant_gender = self.applicant_gender.value
        elif isinstance(self.applicant_gender, BlankEnum):
            applicant_gender = self.applicant_gender.value
        else:
            applicant_gender = self.applicant_gender

        applicant_personal_title = self.applicant_personal_title

        applicant_place_of_birth = self.applicant_place_of_birth

        applicant_address = self.applicant_address

        applicant_country_of_residence = self.applicant_country_of_residence

        applicant_nationality = self.applicant_nationality

        applicant_nationalities = self.applicant_nationalities

        applicant_eduperson_assurance = self.applicant_eduperson_assurance

        applicant_identity_source = self.applicant_identity_source

        applicant_civil_number: Union[None, str]
        applicant_civil_number = self.applicant_civil_number

        applicant_birth_date: Union[None, str]
        if isinstance(self.applicant_birth_date, datetime.date):
            applicant_birth_date = self.applicant_birth_date.isoformat()
        else:
            applicant_birth_date = self.applicant_birth_date

        applicant_active_isds = self.applicant_active_isds

        project: Union[None, str]
        project = self.project

        round_ = self.round_.to_dict()

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        call_managing_organisation_uuid = str(self.call_managing_organisation_uuid)

        oecd_fos_2007_label = self.oecd_fos_2007_label

        science_sub_domain_name = self.science_sub_domain_name

        science_domain_uuid = str(self.science_domain_uuid)

        science_domain_name = self.science_domain_name

        allocation_comment: Union[None, str]
        allocation_comment = self.allocation_comment

        created = self.created.isoformat()

        compliance_status: Union[None, dict[str, Any]]
        if isinstance(self.compliance_status, ProposalComplianceStatusType0):
            compliance_status = self.compliance_status.to_dict()
        else:
            compliance_status = self.compliance_status

        can_submit = self.can_submit.to_dict()

        description = self.description

        project_summary = self.project_summary

        project_is_confidential = self.project_is_confidential

        project_has_civilian_purpose = self.project_has_civilian_purpose

        duration_in_days: Union[None, Unset, int]
        if isinstance(self.duration_in_days, Unset):
            duration_in_days = UNSET
        else:
            duration_in_days = self.duration_in_days

        oecd_fos_2007_code: Union[None, Unset, str]
        if isinstance(self.oecd_fos_2007_code, Unset):
            oecd_fos_2007_code = UNSET
        elif isinstance(self.oecd_fos_2007_code, OecdFos2007CodeEnum):
            oecd_fos_2007_code = self.oecd_fos_2007_code.value
        elif isinstance(self.oecd_fos_2007_code, BlankEnum):
            oecd_fos_2007_code = self.oecd_fos_2007_code.value
        else:
            oecd_fos_2007_code = self.oecd_fos_2007_code

        science_sub_domain: Union[None, Unset, str]
        if isinstance(self.science_sub_domain, Unset):
            science_sub_domain = UNSET
        elif isinstance(self.science_sub_domain, UUID):
            science_sub_domain = str(self.science_sub_domain)
        else:
            science_sub_domain = self.science_sub_domain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "slug": slug,
                "name": name,
                "project_name": project_name,
                "supporting_documentation": supporting_documentation,
                "state": state,
                "approved_by": approved_by,
                "created_by": created_by,
                "created_by_name": created_by_name,
                "created_by_uuid": created_by_uuid,
                "applicant_username": applicant_username,
                "applicant_full_name": applicant_full_name,
                "applicant_first_name": applicant_first_name,
                "applicant_last_name": applicant_last_name,
                "applicant_email": applicant_email,
                "applicant_registration_method": applicant_registration_method,
                "applicant_phone_number": applicant_phone_number,
                "applicant_organization": applicant_organization,
                "applicant_organization_country": applicant_organization_country,
                "applicant_organization_type": applicant_organization_type,
                "applicant_organization_registry_code": applicant_organization_registry_code,
                "applicant_job_title": applicant_job_title,
                "applicant_affiliations": applicant_affiliations,
                "applicant_gender": applicant_gender,
                "applicant_personal_title": applicant_personal_title,
                "applicant_place_of_birth": applicant_place_of_birth,
                "applicant_address": applicant_address,
                "applicant_country_of_residence": applicant_country_of_residence,
                "applicant_nationality": applicant_nationality,
                "applicant_nationalities": applicant_nationalities,
                "applicant_eduperson_assurance": applicant_eduperson_assurance,
                "applicant_identity_source": applicant_identity_source,
                "applicant_civil_number": applicant_civil_number,
                "applicant_birth_date": applicant_birth_date,
                "applicant_active_isds": applicant_active_isds,
                "project": project,
                "round": round_,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "call_managing_organisation_uuid": call_managing_organisation_uuid,
                "oecd_fos_2007_label": oecd_fos_2007_label,
                "science_sub_domain_name": science_sub_domain_name,
                "science_domain_uuid": science_domain_uuid,
                "science_domain_name": science_domain_name,
                "allocation_comment": allocation_comment,
                "created": created,
                "compliance_status": compliance_status,
                "can_submit": can_submit,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if project_summary is not UNSET:
            field_dict["project_summary"] = project_summary
        if project_is_confidential is not UNSET:
            field_dict["project_is_confidential"] = project_is_confidential
        if project_has_civilian_purpose is not UNSET:
            field_dict["project_has_civilian_purpose"] = project_has_civilian_purpose
        if duration_in_days is not UNSET:
            field_dict["duration_in_days"] = duration_in_days
        if oecd_fos_2007_code is not UNSET:
            field_dict["oecd_fos_2007_code"] = oecd_fos_2007_code
        if science_sub_domain is not UNSET:
            field_dict["science_sub_domain"] = science_sub_domain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_round import NestedRound
        from ..models.proposal_can_submit import ProposalCanSubmit
        from ..models.proposal_compliance_status_type_0 import ProposalComplianceStatusType0
        from ..models.proposal_documentation import ProposalDocumentation

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        slug = d.pop("slug")

        name = d.pop("name")

        project_name = d.pop("project_name")

        supporting_documentation = []
        _supporting_documentation = d.pop("supporting_documentation")
        for supporting_documentation_item_data in _supporting_documentation:
            supporting_documentation_item = ProposalDocumentation.from_dict(supporting_documentation_item_data)

            supporting_documentation.append(supporting_documentation_item)

        state = ProposalStates(d.pop("state"))

        def _parse_approved_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        approved_by = _parse_approved_by(d.pop("approved_by"))

        def _parse_created_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by = _parse_created_by(d.pop("created_by"))

        created_by_name = d.pop("created_by_name")

        created_by_uuid = UUID(d.pop("created_by_uuid"))

        applicant_username = d.pop("applicant_username")

        applicant_full_name = d.pop("applicant_full_name")

        applicant_first_name = d.pop("applicant_first_name")

        applicant_last_name = d.pop("applicant_last_name")

        applicant_email = d.pop("applicant_email")

        applicant_registration_method = d.pop("applicant_registration_method")

        applicant_phone_number = d.pop("applicant_phone_number")

        applicant_organization = d.pop("applicant_organization")

        applicant_organization_country = d.pop("applicant_organization_country")

        applicant_organization_type = d.pop("applicant_organization_type")

        applicant_organization_registry_code = d.pop("applicant_organization_registry_code")

        applicant_job_title = d.pop("applicant_job_title")

        applicant_affiliations = d.pop("applicant_affiliations")

        def _parse_applicant_gender(data: object) -> Union[BlankEnum, GenderEnum, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                applicant_gender_type_0 = GenderEnum(data)

                return applicant_gender_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                applicant_gender_type_1 = BlankEnum(data)

                return applicant_gender_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, GenderEnum, None], data)

        applicant_gender = _parse_applicant_gender(d.pop("applicant_gender"))

        applicant_personal_title = d.pop("applicant_personal_title")

        applicant_place_of_birth = d.pop("applicant_place_of_birth")

        applicant_address = d.pop("applicant_address")

        applicant_country_of_residence = d.pop("applicant_country_of_residence")

        applicant_nationality = d.pop("applicant_nationality")

        applicant_nationalities = d.pop("applicant_nationalities")

        applicant_eduperson_assurance = d.pop("applicant_eduperson_assurance")

        applicant_identity_source = d.pop("applicant_identity_source")

        def _parse_applicant_civil_number(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        applicant_civil_number = _parse_applicant_civil_number(d.pop("applicant_civil_number"))

        def _parse_applicant_birth_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                applicant_birth_date_type_0 = isoparse(data).date()

                return applicant_birth_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        applicant_birth_date = _parse_applicant_birth_date(d.pop("applicant_birth_date"))

        applicant_active_isds = d.pop("applicant_active_isds")

        def _parse_project(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        project = _parse_project(d.pop("project"))

        round_ = NestedRound.from_dict(d.pop("round"))

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        call_managing_organisation_uuid = UUID(d.pop("call_managing_organisation_uuid"))

        oecd_fos_2007_label = d.pop("oecd_fos_2007_label")

        science_sub_domain_name = d.pop("science_sub_domain_name")

        science_domain_uuid = UUID(d.pop("science_domain_uuid"))

        science_domain_name = d.pop("science_domain_name")

        def _parse_allocation_comment(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        allocation_comment = _parse_allocation_comment(d.pop("allocation_comment"))

        created = isoparse(d.pop("created"))

        def _parse_compliance_status(data: object) -> Union["ProposalComplianceStatusType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                compliance_status_type_0 = ProposalComplianceStatusType0.from_dict(data)

                return compliance_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ProposalComplianceStatusType0", None], data)

        compliance_status = _parse_compliance_status(d.pop("compliance_status"))

        can_submit = ProposalCanSubmit.from_dict(d.pop("can_submit"))

        description = d.pop("description", UNSET)

        project_summary = d.pop("project_summary", UNSET)

        project_is_confidential = d.pop("project_is_confidential", UNSET)

        project_has_civilian_purpose = d.pop("project_has_civilian_purpose", UNSET)

        def _parse_duration_in_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        duration_in_days = _parse_duration_in_days(d.pop("duration_in_days", UNSET))

        def _parse_oecd_fos_2007_code(data: object) -> Union[BlankEnum, None, OecdFos2007CodeEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                oecd_fos_2007_code_type_0 = OecdFos2007CodeEnum(data)

                return oecd_fos_2007_code_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                oecd_fos_2007_code_type_1 = BlankEnum(data)

                return oecd_fos_2007_code_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, None, OecdFos2007CodeEnum, Unset], data)

        oecd_fos_2007_code = _parse_oecd_fos_2007_code(d.pop("oecd_fos_2007_code", UNSET))

        def _parse_science_sub_domain(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                science_sub_domain_type_0 = UUID(data)

                return science_sub_domain_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        science_sub_domain = _parse_science_sub_domain(d.pop("science_sub_domain", UNSET))

        proposal = cls(
            uuid=uuid,
            url=url,
            slug=slug,
            name=name,
            project_name=project_name,
            supporting_documentation=supporting_documentation,
            state=state,
            approved_by=approved_by,
            created_by=created_by,
            created_by_name=created_by_name,
            created_by_uuid=created_by_uuid,
            applicant_username=applicant_username,
            applicant_full_name=applicant_full_name,
            applicant_first_name=applicant_first_name,
            applicant_last_name=applicant_last_name,
            applicant_email=applicant_email,
            applicant_registration_method=applicant_registration_method,
            applicant_phone_number=applicant_phone_number,
            applicant_organization=applicant_organization,
            applicant_organization_country=applicant_organization_country,
            applicant_organization_type=applicant_organization_type,
            applicant_organization_registry_code=applicant_organization_registry_code,
            applicant_job_title=applicant_job_title,
            applicant_affiliations=applicant_affiliations,
            applicant_gender=applicant_gender,
            applicant_personal_title=applicant_personal_title,
            applicant_place_of_birth=applicant_place_of_birth,
            applicant_address=applicant_address,
            applicant_country_of_residence=applicant_country_of_residence,
            applicant_nationality=applicant_nationality,
            applicant_nationalities=applicant_nationalities,
            applicant_eduperson_assurance=applicant_eduperson_assurance,
            applicant_identity_source=applicant_identity_source,
            applicant_civil_number=applicant_civil_number,
            applicant_birth_date=applicant_birth_date,
            applicant_active_isds=applicant_active_isds,
            project=project,
            round_=round_,
            call_uuid=call_uuid,
            call_name=call_name,
            call_managing_organisation_uuid=call_managing_organisation_uuid,
            oecd_fos_2007_label=oecd_fos_2007_label,
            science_sub_domain_name=science_sub_domain_name,
            science_domain_uuid=science_domain_uuid,
            science_domain_name=science_domain_name,
            allocation_comment=allocation_comment,
            created=created,
            compliance_status=compliance_status,
            can_submit=can_submit,
            description=description,
            project_summary=project_summary,
            project_is_confidential=project_is_confidential,
            project_has_civilian_purpose=project_has_civilian_purpose,
            duration_in_days=duration_in_days,
            oecd_fos_2007_code=oecd_fos_2007_code,
            science_sub_domain=science_sub_domain,
        )

        proposal.additional_properties = d
        return proposal

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
