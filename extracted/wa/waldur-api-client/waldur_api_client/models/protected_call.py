import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.call_states import CallStates
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_document import CallDocument
    from ..models.call_resource_template import CallResourceTemplate
    from ..models.nested_requested_offering import NestedRequestedOffering
    from ..models.nested_round import NestedRound


T = TypeVar("T", bound="ProtectedCall")


@_attrs_define
class ProtectedCall:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        state (Union[Unset, CallStates]):
        manager (Union[Unset, str]):
        manager_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        offerings (Union[Unset, list['NestedRequestedOffering']]):
        rounds (Union[Unset, list['NestedRound']]):
        documents (Union[Unset, list['CallDocument']]):
        resource_templates (Union[Unset, list['CallResourceTemplate']]):
        fixed_duration_in_days (Union[None, Unset, int]):
        backend_id (Union[Unset, str]):
        external_url (Union[None, Unset, str]):
        reviewer_identity_visible_to_submitters (Union[Unset, bool]): Whether proposal applicants can see reviewer
            identities
        reviews_visible_to_submitters (Union[Unset, bool]): Whether proposal applicants can see review comments and
            scores
        has_eligibility_restrictions (Union[Unset, bool]): Check if call has any eligibility restrictions configured.
        created_by (Union[None, Unset, str]):
        reference_code (Union[Unset, str]):
        compliance_checklist (Union[None, UUID, Unset]): Compliance checklist that proposals must complete before
            submission
        compliance_checklist_name (Union[Unset, str]):
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

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    slug: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    state: Union[Unset, CallStates] = UNSET
    manager: Union[Unset, str] = UNSET
    manager_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    offerings: Union[Unset, list["NestedRequestedOffering"]] = UNSET
    rounds: Union[Unset, list["NestedRound"]] = UNSET
    documents: Union[Unset, list["CallDocument"]] = UNSET
    resource_templates: Union[Unset, list["CallResourceTemplate"]] = UNSET
    fixed_duration_in_days: Union[None, Unset, int] = UNSET
    backend_id: Union[Unset, str] = UNSET
    external_url: Union[None, Unset, str] = UNSET
    reviewer_identity_visible_to_submitters: Union[Unset, bool] = UNSET
    reviews_visible_to_submitters: Union[Unset, bool] = UNSET
    has_eligibility_restrictions: Union[Unset, bool] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    reference_code: Union[Unset, str] = UNSET
    compliance_checklist: Union[None, UUID, Unset] = UNSET
    compliance_checklist_name: Union[Unset, str] = UNSET
    proposal_slug_template: Union[None, Unset, str] = UNSET
    user_email_patterns: Union[Unset, Any] = UNSET
    user_affiliations: Union[Unset, Any] = UNSET
    user_identity_sources: Union[Unset, Any] = UNSET
    user_nationalities: Union[Unset, Any] = UNSET
    user_organization_types: Union[Unset, Any] = UNSET
    user_assurance_levels: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        slug = self.slug

        name = self.name

        description = self.description

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        manager = self.manager

        manager_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.manager_uuid, Unset):
            manager_uuid = str(self.manager_uuid)

        customer_name = self.customer_name

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        offerings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.offerings, Unset):
            offerings = []
            for offerings_item_data in self.offerings:
                offerings_item = offerings_item_data.to_dict()
                offerings.append(offerings_item)

        rounds: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rounds, Unset):
            rounds = []
            for rounds_item_data in self.rounds:
                rounds_item = rounds_item_data.to_dict()
                rounds.append(rounds_item)

        documents: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.documents, Unset):
            documents = []
            for documents_item_data in self.documents:
                documents_item = documents_item_data.to_dict()
                documents.append(documents_item)

        resource_templates: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.resource_templates, Unset):
            resource_templates = []
            for resource_templates_item_data in self.resource_templates:
                resource_templates_item = resource_templates_item_data.to_dict()
                resource_templates.append(resource_templates_item)

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

        has_eligibility_restrictions = self.has_eligibility_restrictions

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

        compliance_checklist_name = self.compliance_checklist_name

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
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if slug is not UNSET:
            field_dict["slug"] = slug
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if state is not UNSET:
            field_dict["state"] = state
        if manager is not UNSET:
            field_dict["manager"] = manager
        if manager_uuid is not UNSET:
            field_dict["manager_uuid"] = manager_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if offerings is not UNSET:
            field_dict["offerings"] = offerings
        if rounds is not UNSET:
            field_dict["rounds"] = rounds
        if documents is not UNSET:
            field_dict["documents"] = documents
        if resource_templates is not UNSET:
            field_dict["resource_templates"] = resource_templates
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
        if has_eligibility_restrictions is not UNSET:
            field_dict["has_eligibility_restrictions"] = has_eligibility_restrictions
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if reference_code is not UNSET:
            field_dict["reference_code"] = reference_code
        if compliance_checklist is not UNSET:
            field_dict["compliance_checklist"] = compliance_checklist
        if compliance_checklist_name is not UNSET:
            field_dict["compliance_checklist_name"] = compliance_checklist_name
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
        from ..models.call_document import CallDocument
        from ..models.call_resource_template import CallResourceTemplate
        from ..models.nested_requested_offering import NestedRequestedOffering
        from ..models.nested_round import NestedRound

        d = dict(src_dict)
        url = d.pop("url", UNSET)

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

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        _end_date = d.pop("end_date", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        slug = d.pop("slug", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, CallStates]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = CallStates(_state)

        manager = d.pop("manager", UNSET)

        _manager_uuid = d.pop("manager_uuid", UNSET)
        manager_uuid: Union[Unset, UUID]
        if isinstance(_manager_uuid, Unset):
            manager_uuid = UNSET
        else:
            manager_uuid = UUID(_manager_uuid)

        customer_name = d.pop("customer_name", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        offerings = []
        _offerings = d.pop("offerings", UNSET)
        for offerings_item_data in _offerings or []:
            offerings_item = NestedRequestedOffering.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        rounds = []
        _rounds = d.pop("rounds", UNSET)
        for rounds_item_data in _rounds or []:
            rounds_item = NestedRound.from_dict(rounds_item_data)

            rounds.append(rounds_item)

        documents = []
        _documents = d.pop("documents", UNSET)
        for documents_item_data in _documents or []:
            documents_item = CallDocument.from_dict(documents_item_data)

            documents.append(documents_item)

        resource_templates = []
        _resource_templates = d.pop("resource_templates", UNSET)
        for resource_templates_item_data in _resource_templates or []:
            resource_templates_item = CallResourceTemplate.from_dict(resource_templates_item_data)

            resource_templates.append(resource_templates_item)

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

        has_eligibility_restrictions = d.pop("has_eligibility_restrictions", UNSET)

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

        compliance_checklist_name = d.pop("compliance_checklist_name", UNSET)

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

        protected_call = cls(
            url=url,
            uuid=uuid,
            created=created,
            start_date=start_date,
            end_date=end_date,
            slug=slug,
            name=name,
            description=description,
            state=state,
            manager=manager,
            manager_uuid=manager_uuid,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            offerings=offerings,
            rounds=rounds,
            documents=documents,
            resource_templates=resource_templates,
            fixed_duration_in_days=fixed_duration_in_days,
            backend_id=backend_id,
            external_url=external_url,
            reviewer_identity_visible_to_submitters=reviewer_identity_visible_to_submitters,
            reviews_visible_to_submitters=reviews_visible_to_submitters,
            has_eligibility_restrictions=has_eligibility_restrictions,
            created_by=created_by,
            reference_code=reference_code,
            compliance_checklist=compliance_checklist,
            compliance_checklist_name=compliance_checklist_name,
            proposal_slug_template=proposal_slug_template,
            user_email_patterns=user_email_patterns,
            user_affiliations=user_affiliations,
            user_identity_sources=user_identity_sources,
            user_nationalities=user_nationalities,
            user_organization_types=user_organization_types,
            user_assurance_levels=user_assurance_levels,
        )

        protected_call.additional_properties = d
        return protected_call

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
