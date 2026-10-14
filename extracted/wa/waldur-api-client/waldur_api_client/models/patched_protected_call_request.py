from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.evaluation_start_enum import EvaluationStartEnum
from ..models.order_author_enum import OrderAuthorEnum
from ..models.publish_results_enum import PublishResultsEnum
from ..models.undecided_at_round_completion_enum import UndecidedAtRoundCompletionEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_applicant_visibility_config_request import CallApplicantVisibilityConfigRequest
    from ..models.call_proposal_field_config_request import CallProposalFieldConfigRequest


T = TypeVar("T", bound="PatchedProtectedCallRequest")


@_attrs_define
class PatchedProtectedCallRequest:
    """
    Attributes:
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        fixed_duration_in_days (Union[None, Unset, int]):
        backend_id (Union[Unset, str]):
        external_url (Union[None, Unset, str]):
        reviewer_identity_visible_to_submitters (Union[Unset, bool]): Whether proposal applicants can see reviewer
            identities
        reviews_visible_to_submitters (Union[Unset, bool]): Whether proposal applicants can see review comments and
            scores
        proposal_field_config (Union[Unset, CallProposalFieldConfigRequest]):
        evaluation_start (Union[Unset, EvaluationStartEnum]):
        publish_results (Union[Unset, PublishResultsEnum]):
        created_by (Union[None, Unset, str]):
        reference_code (Union[Unset, str]):
        compliance_checklist (Union[None, UUID, Unset]): Compliance checklist that proposals must complete before
            submission
        panel_chair (Union[None, UUID, Unset]):
        proposal_slug_template (Union[None, Unset, str]): Template for proposal slugs. Supports: {call_slug},
            {round_slug}, {org_slug}, {year}, {month}, {counter}, {counter_padded}. Default: {round_slug}-{counter_padded}
        user_email_patterns (Union[Unset, list[str]]): List of email regex patterns. User must match one.
        user_affiliations (Union[Unset, list[str]]): List of allowed affiliations. User must have one.
        user_identity_sources (Union[Unset, list[str]]): List of allowed identity sources (identity providers).
        user_nationalities (Union[Unset, list[str]]): List of allowed nationality codes (ISO 3166-1 alpha-2). User must
            have one.
        user_organization_types (Union[Unset, list[str]]): List of allowed organization type URNs (SCHAC). User must
            match one.
        user_assurance_levels (Union[Unset, list[str]]): List of required assurance URIs (REFEDS). User must have ALL of
            these.
        applicant_visibility_config (Union['CallApplicantVisibilityConfigRequest', None, Unset]):
        order_author (Union[Unset, OrderAuthorEnum]):
        order_author_user (Union[None, UUID, Unset]): The person orders are attributed to when the author is a named
            contact. Must hold a role on this call or on the organisation managing it.
        carry_over_drafts (Union[Unset, bool]): Whether a draft still open when its round's cut-off passes moves on to
            the call's next round instead of being cancelled. Without a later round the draft is cancelled either way.
        undecided_at_round_completion (Union[Unset, UndecidedAtRoundCompletionEnum]):
    """

    slug: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    fixed_duration_in_days: Union[None, Unset, int] = UNSET
    backend_id: Union[Unset, str] = UNSET
    external_url: Union[None, Unset, str] = UNSET
    reviewer_identity_visible_to_submitters: Union[Unset, bool] = UNSET
    reviews_visible_to_submitters: Union[Unset, bool] = UNSET
    proposal_field_config: Union[Unset, "CallProposalFieldConfigRequest"] = UNSET
    evaluation_start: Union[Unset, EvaluationStartEnum] = UNSET
    publish_results: Union[Unset, PublishResultsEnum] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    reference_code: Union[Unset, str] = UNSET
    compliance_checklist: Union[None, UUID, Unset] = UNSET
    panel_chair: Union[None, UUID, Unset] = UNSET
    proposal_slug_template: Union[None, Unset, str] = UNSET
    user_email_patterns: Union[Unset, list[str]] = UNSET
    user_affiliations: Union[Unset, list[str]] = UNSET
    user_identity_sources: Union[Unset, list[str]] = UNSET
    user_nationalities: Union[Unset, list[str]] = UNSET
    user_organization_types: Union[Unset, list[str]] = UNSET
    user_assurance_levels: Union[Unset, list[str]] = UNSET
    applicant_visibility_config: Union["CallApplicantVisibilityConfigRequest", None, Unset] = UNSET
    order_author: Union[Unset, OrderAuthorEnum] = UNSET
    order_author_user: Union[None, UUID, Unset] = UNSET
    carry_over_drafts: Union[Unset, bool] = UNSET
    undecided_at_round_completion: Union[Unset, UndecidedAtRoundCompletionEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.call_applicant_visibility_config_request import CallApplicantVisibilityConfigRequest

        slug = self.slug

        name = self.name

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

        proposal_field_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.proposal_field_config, Unset):
            proposal_field_config = self.proposal_field_config.to_dict()

        evaluation_start: Union[Unset, str] = UNSET
        if not isinstance(self.evaluation_start, Unset):
            evaluation_start = self.evaluation_start.value

        publish_results: Union[Unset, str] = UNSET
        if not isinstance(self.publish_results, Unset):
            publish_results = self.publish_results.value

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

        panel_chair: Union[None, Unset, str]
        if isinstance(self.panel_chair, Unset):
            panel_chair = UNSET
        elif isinstance(self.panel_chair, UUID):
            panel_chair = str(self.panel_chair)
        else:
            panel_chair = self.panel_chair

        proposal_slug_template: Union[None, Unset, str]
        if isinstance(self.proposal_slug_template, Unset):
            proposal_slug_template = UNSET
        else:
            proposal_slug_template = self.proposal_slug_template

        user_email_patterns: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_email_patterns, Unset):
            user_email_patterns = self.user_email_patterns

        user_affiliations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_affiliations, Unset):
            user_affiliations = self.user_affiliations

        user_identity_sources: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_identity_sources, Unset):
            user_identity_sources = self.user_identity_sources

        user_nationalities: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_nationalities, Unset):
            user_nationalities = self.user_nationalities

        user_organization_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_organization_types, Unset):
            user_organization_types = self.user_organization_types

        user_assurance_levels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_assurance_levels, Unset):
            user_assurance_levels = self.user_assurance_levels

        applicant_visibility_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.applicant_visibility_config, Unset):
            applicant_visibility_config = UNSET
        elif isinstance(self.applicant_visibility_config, CallApplicantVisibilityConfigRequest):
            applicant_visibility_config = self.applicant_visibility_config.to_dict()
        else:
            applicant_visibility_config = self.applicant_visibility_config

        order_author: Union[Unset, str] = UNSET
        if not isinstance(self.order_author, Unset):
            order_author = self.order_author.value

        order_author_user: Union[None, Unset, str]
        if isinstance(self.order_author_user, Unset):
            order_author_user = UNSET
        elif isinstance(self.order_author_user, UUID):
            order_author_user = str(self.order_author_user)
        else:
            order_author_user = self.order_author_user

        carry_over_drafts = self.carry_over_drafts

        undecided_at_round_completion: Union[Unset, str] = UNSET
        if not isinstance(self.undecided_at_round_completion, Unset):
            undecided_at_round_completion = self.undecided_at_round_completion.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if slug is not UNSET:
            field_dict["slug"] = slug
        if name is not UNSET:
            field_dict["name"] = name
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
        if proposal_field_config is not UNSET:
            field_dict["proposal_field_config"] = proposal_field_config
        if evaluation_start is not UNSET:
            field_dict["evaluation_start"] = evaluation_start
        if publish_results is not UNSET:
            field_dict["publish_results"] = publish_results
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if reference_code is not UNSET:
            field_dict["reference_code"] = reference_code
        if compliance_checklist is not UNSET:
            field_dict["compliance_checklist"] = compliance_checklist
        if panel_chair is not UNSET:
            field_dict["panel_chair"] = panel_chair
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
        if applicant_visibility_config is not UNSET:
            field_dict["applicant_visibility_config"] = applicant_visibility_config
        if order_author is not UNSET:
            field_dict["order_author"] = order_author
        if order_author_user is not UNSET:
            field_dict["order_author_user"] = order_author_user
        if carry_over_drafts is not UNSET:
            field_dict["carry_over_drafts"] = carry_over_drafts
        if undecided_at_round_completion is not UNSET:
            field_dict["undecided_at_round_completion"] = undecided_at_round_completion

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_applicant_visibility_config_request import CallApplicantVisibilityConfigRequest
        from ..models.call_proposal_field_config_request import CallProposalFieldConfigRequest

        d = dict(src_dict)
        slug = d.pop("slug", UNSET)

        name = d.pop("name", UNSET)

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

        _proposal_field_config = d.pop("proposal_field_config", UNSET)
        proposal_field_config: Union[Unset, CallProposalFieldConfigRequest]
        if isinstance(_proposal_field_config, Unset):
            proposal_field_config = UNSET
        else:
            proposal_field_config = CallProposalFieldConfigRequest.from_dict(_proposal_field_config)

        _evaluation_start = d.pop("evaluation_start", UNSET)
        evaluation_start: Union[Unset, EvaluationStartEnum]
        if isinstance(_evaluation_start, Unset):
            evaluation_start = UNSET
        else:
            evaluation_start = EvaluationStartEnum(_evaluation_start)

        _publish_results = d.pop("publish_results", UNSET)
        publish_results: Union[Unset, PublishResultsEnum]
        if isinstance(_publish_results, Unset):
            publish_results = UNSET
        else:
            publish_results = PublishResultsEnum(_publish_results)

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

        def _parse_panel_chair(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                panel_chair_type_0 = UUID(data)

                return panel_chair_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        panel_chair = _parse_panel_chair(d.pop("panel_chair", UNSET))

        def _parse_proposal_slug_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        proposal_slug_template = _parse_proposal_slug_template(d.pop("proposal_slug_template", UNSET))

        user_email_patterns = cast(list[str], d.pop("user_email_patterns", UNSET))

        user_affiliations = cast(list[str], d.pop("user_affiliations", UNSET))

        user_identity_sources = cast(list[str], d.pop("user_identity_sources", UNSET))

        user_nationalities = cast(list[str], d.pop("user_nationalities", UNSET))

        user_organization_types = cast(list[str], d.pop("user_organization_types", UNSET))

        user_assurance_levels = cast(list[str], d.pop("user_assurance_levels", UNSET))

        def _parse_applicant_visibility_config(
            data: object,
        ) -> Union["CallApplicantVisibilityConfigRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                applicant_visibility_config_type_1 = CallApplicantVisibilityConfigRequest.from_dict(data)

                return applicant_visibility_config_type_1
            except:  # noqa: E722
                pass
            return cast(Union["CallApplicantVisibilityConfigRequest", None, Unset], data)

        applicant_visibility_config = _parse_applicant_visibility_config(d.pop("applicant_visibility_config", UNSET))

        _order_author = d.pop("order_author", UNSET)
        order_author: Union[Unset, OrderAuthorEnum]
        if isinstance(_order_author, Unset):
            order_author = UNSET
        else:
            order_author = OrderAuthorEnum(_order_author)

        def _parse_order_author_user(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                order_author_user_type_0 = UUID(data)

                return order_author_user_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        order_author_user = _parse_order_author_user(d.pop("order_author_user", UNSET))

        carry_over_drafts = d.pop("carry_over_drafts", UNSET)

        _undecided_at_round_completion = d.pop("undecided_at_round_completion", UNSET)
        undecided_at_round_completion: Union[Unset, UndecidedAtRoundCompletionEnum]
        if isinstance(_undecided_at_round_completion, Unset):
            undecided_at_round_completion = UNSET
        else:
            undecided_at_round_completion = UndecidedAtRoundCompletionEnum(_undecided_at_round_completion)

        patched_protected_call_request = cls(
            slug=slug,
            name=name,
            description=description,
            fixed_duration_in_days=fixed_duration_in_days,
            backend_id=backend_id,
            external_url=external_url,
            reviewer_identity_visible_to_submitters=reviewer_identity_visible_to_submitters,
            reviews_visible_to_submitters=reviews_visible_to_submitters,
            proposal_field_config=proposal_field_config,
            evaluation_start=evaluation_start,
            publish_results=publish_results,
            created_by=created_by,
            reference_code=reference_code,
            compliance_checklist=compliance_checklist,
            panel_chair=panel_chair,
            proposal_slug_template=proposal_slug_template,
            user_email_patterns=user_email_patterns,
            user_affiliations=user_affiliations,
            user_identity_sources=user_identity_sources,
            user_nationalities=user_nationalities,
            user_organization_types=user_organization_types,
            user_assurance_levels=user_assurance_levels,
            applicant_visibility_config=applicant_visibility_config,
            order_author=order_author,
            order_author_user=order_author_user,
            carry_over_drafts=carry_over_drafts,
            undecided_at_round_completion=undecided_at_round_completion,
        )

        patched_protected_call_request.additional_properties = d
        return patched_protected_call_request

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
