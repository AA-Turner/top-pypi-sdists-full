from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProtectedCallRequest")


@_attrs_define
class ProtectedCallRequest:
    """
    Attributes:
        name (str):
        manager (str):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        description (Union[Unset, str]):
        fixed_duration_in_days (Union[None, Unset, int]):
        backend_id (Union[Unset, str]):
        external_url (Union[None, Unset, str]):
        reviewer_identity_visible_to_submitters (Union[Unset, bool]): Whether proposal applicants can see reviewer
            identities
        reviews_visible_to_submitters (Union[Unset, bool]): Whether proposal applicants can see review comments and
            scores
        created_by (Union[None, Unset, str]):
        reference_code (Union[Unset, str]):
        compliance_checklist (Union[None, UUID, Unset]): Compliance checklist that proposals must complete before
            submission
        proposal_slug_template (Union[None, Unset, str]): Template for proposal slugs. Supports: {call_slug},
            {round_slug}, {org_slug}, {year}, {month}, {counter}, {counter_padded}. Default: {round_slug}-{counter_padded}
        user_email_patterns (Union[Unset, Any]): List of email regex patterns. User must match one.
        user_affiliations (Union[Unset, Any]): List of allowed affiliations. User must have one.
        user_identity_sources (Union[Unset, Any]): List of allowed identity sources (identity providers).
        user_nationalities (Union[Unset, Any]): List of allowed nationality codes (ISO 3166-1 alpha-2). User must have
            one.
        user_organization_types (Union[Unset, Any]): List of allowed organization type URNs (SCHAC). User must match
            one.
        user_assurance_levels (Union[Unset, Any]): List of required assurance URIs (REFEDS). User must have ALL of
            these.
    """

    name: str
    manager: str
    slug: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    fixed_duration_in_days: Union[None, Unset, int] = UNSET
    backend_id: Union[Unset, str] = UNSET
    external_url: Union[None, Unset, str] = UNSET
    reviewer_identity_visible_to_submitters: Union[Unset, bool] = UNSET
    reviews_visible_to_submitters: Union[Unset, bool] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    reference_code: Union[Unset, str] = UNSET
    compliance_checklist: Union[None, UUID, Unset] = UNSET
    proposal_slug_template: Union[None, Unset, str] = UNSET
    user_email_patterns: Union[Unset, Any] = UNSET
    user_affiliations: Union[Unset, Any] = UNSET
    user_identity_sources: Union[Unset, Any] = UNSET
    user_nationalities: Union[Unset, Any] = UNSET
    user_organization_types: Union[Unset, Any] = UNSET
    user_assurance_levels: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        manager = self.manager

        slug = self.slug

        description = self.description

        fixed_duration_in_days: Union[None, Unset, int]
        if isinstance(self.fixed_duration_in_days, Unset):
            fixed_duration_in_days = UNSET
        else:
            fixed_duration_in_days = self.fixed_duration_in_days

        backend_id = self.backend_id

        external_url: Union[None, Unset, str]
        if isinstance(self.external_url, Unset):
            external_url = UNSET
        else:
            external_url = self.external_url

        reviewer_identity_visible_to_submitters = self.reviewer_identity_visible_to_submitters

        reviews_visible_to_submitters = self.reviews_visible_to_submitters

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        reference_code = self.reference_code

        compliance_checklist: Union[None, Unset, str]
        if isinstance(self.compliance_checklist, Unset):
            compliance_checklist = UNSET
        elif isinstance(self.compliance_checklist, UUID):
            compliance_checklist = str(self.compliance_checklist)
        else:
            compliance_checklist = self.compliance_checklist

        proposal_slug_template: Union[None, Unset, str]
        if isinstance(self.proposal_slug_template, Unset):
            proposal_slug_template = UNSET
        else:
            proposal_slug_template = self.proposal_slug_template

        user_email_patterns = self.user_email_patterns

        user_affiliations = self.user_affiliations

        user_identity_sources = self.user_identity_sources

        user_nationalities = self.user_nationalities

        user_organization_types = self.user_organization_types

        user_assurance_levels = self.user_assurance_levels

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "manager": manager,
            }
        )
        if slug is not UNSET:
            field_dict["slug"] = slug
        if description is not UNSET:
            field_dict["description"] = description
        if fixed_duration_in_days is not UNSET:
            field_dict["fixed_duration_in_days"] = fixed_duration_in_days
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if external_url is not UNSET:
            field_dict["external_url"] = external_url
        if reviewer_identity_visible_to_submitters is not UNSET:
            field_dict["reviewer_identity_visible_to_submitters"] = reviewer_identity_visible_to_submitters
        if reviews_visible_to_submitters is not UNSET:
            field_dict["reviews_visible_to_submitters"] = reviews_visible_to_submitters
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if reference_code is not UNSET:
            field_dict["reference_code"] = reference_code
        if compliance_checklist is not UNSET:
            field_dict["compliance_checklist"] = compliance_checklist
        if proposal_slug_template is not UNSET:
            field_dict["proposal_slug_template"] = proposal_slug_template
        if user_email_patterns is not UNSET:
            field_dict["user_email_patterns"] = user_email_patterns
        if user_affiliations is not UNSET:
            field_dict["user_affiliations"] = user_affiliations
        if user_identity_sources is not UNSET:
            field_dict["user_identity_sources"] = user_identity_sources
        if user_nationalities is not UNSET:
            field_dict["user_nationalities"] = user_nationalities
        if user_organization_types is not UNSET:
            field_dict["user_organization_types"] = user_organization_types
        if user_assurance_levels is not UNSET:
            field_dict["user_assurance_levels"] = user_assurance_levels

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        manager = d.pop("manager")

        slug = d.pop("slug", UNSET)

        description = d.pop("description", UNSET)

        def _parse_fixed_duration_in_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        fixed_duration_in_days = _parse_fixed_duration_in_days(d.pop("fixed_duration_in_days", UNSET))

        backend_id = d.pop("backend_id", UNSET)

        def _parse_external_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_url = _parse_external_url(d.pop("external_url", UNSET))

        reviewer_identity_visible_to_submitters = d.pop("reviewer_identity_visible_to_submitters", UNSET)

        reviews_visible_to_submitters = d.pop("reviews_visible_to_submitters", UNSET)

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        reference_code = d.pop("reference_code", UNSET)

        def _parse_compliance_checklist(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                compliance_checklist_type_0 = UUID(data)

                return compliance_checklist_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        compliance_checklist = _parse_compliance_checklist(d.pop("compliance_checklist", UNSET))

        def _parse_proposal_slug_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        proposal_slug_template = _parse_proposal_slug_template(d.pop("proposal_slug_template", UNSET))

        user_email_patterns = d.pop("user_email_patterns", UNSET)

        user_affiliations = d.pop("user_affiliations", UNSET)

        user_identity_sources = d.pop("user_identity_sources", UNSET)

        user_nationalities = d.pop("user_nationalities", UNSET)

        user_organization_types = d.pop("user_organization_types", UNSET)

        user_assurance_levels = d.pop("user_assurance_levels", UNSET)

        protected_call_request = cls(
            name=name,
            manager=manager,
            slug=slug,
            description=description,
            fixed_duration_in_days=fixed_duration_in_days,
            backend_id=backend_id,
            external_url=external_url,
            reviewer_identity_visible_to_submitters=reviewer_identity_visible_to_submitters,
            reviews_visible_to_submitters=reviews_visible_to_submitters,
            created_by=created_by,
            reference_code=reference_code,
            compliance_checklist=compliance_checklist,
            proposal_slug_template=proposal_slug_template,
            user_email_patterns=user_email_patterns,
            user_affiliations=user_affiliations,
            user_identity_sources=user_identity_sources,
            user_nationalities=user_nationalities,
            user_organization_types=user_organization_types,
            user_assurance_levels=user_assurance_levels,
        )

        protected_call_request.additional_properties = d
        return protected_call_request

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
