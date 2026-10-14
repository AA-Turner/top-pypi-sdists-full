from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rule_plan_attributes import RulePlanAttributes
    from ..models.rule_plan_limits import RulePlanLimits
    from ..models.rule_user_claims import RuleUserClaims


T = TypeVar("T", bound="Rule")


@_attrs_define
class Rule:
    """
    Attributes:
        name (str):
        uuid (UUID):
        url (str):
        customer_name (str):
        customer_uuid (str):
        project_role_display_name (str):
        project_role_description (str):
        customer_role_display_name (str):
        customer_role_description (str):
        plan_name (str):
        offering_name (str):
        offering_uuid (UUID):
        category_title (str):
        category_url (str):
        user_affiliations (Union[Unset, list[str]]):
        user_email_patterns (Union[Unset, list[str]]):
        user_identity_sources (Union[Unset, list[str]]):
        user_nationalities (Union[Unset, list[str]]):
        user_organization_types (Union[Unset, list[str]]):
        user_assurance_levels (Union[Unset, list[str]]):
        user_claims (Union[Unset, RuleUserClaims]): Identity provider claims the user must carry, as {"claim":
            ["accepted", "values"]}. All claims must match; within one claim any value matches. A value ending in '*'
            matches by prefix.
        customer (Union[None, Unset, str]):
        use_user_organization_as_customer_name (Union[Unset, bool]):
        create_project (Union[Unset, bool]): Create (or join) a project for the matched user. Disable to grant only the
            organization-level role.
        project_name_template (Union[None, Unset, str]): Template for project name. Supports {username}, {email},
            {full_name} variables
        revoke_when_unmatched (Union[Unset, bool]): Revoke the roles this rule granted once the user stops matching it.
            Off by default so enabling a rule cannot silently strip access that is already in use.
        project_role (Union[None, Unset, str]):
        customer_role (Union[None, Unset, str]):
        plan (Union[None, Unset, str]):
        plan_attributes (Union[Unset, RulePlanAttributes]):
        plan_limits (Union[Unset, RulePlanLimits]):
    """

    name: str
    uuid: UUID
    url: str
    customer_name: str
    customer_uuid: str
    project_role_display_name: str
    project_role_description: str
    customer_role_display_name: str
    customer_role_description: str
    plan_name: str
    offering_name: str
    offering_uuid: UUID
    category_title: str
    category_url: str
    user_affiliations: Union[Unset, list[str]] = UNSET
    user_email_patterns: Union[Unset, list[str]] = UNSET
    user_identity_sources: Union[Unset, list[str]] = UNSET
    user_nationalities: Union[Unset, list[str]] = UNSET
    user_organization_types: Union[Unset, list[str]] = UNSET
    user_assurance_levels: Union[Unset, list[str]] = UNSET
    user_claims: Union[Unset, "RuleUserClaims"] = UNSET
    customer: Union[None, Unset, str] = UNSET
    use_user_organization_as_customer_name: Union[Unset, bool] = UNSET
    create_project: Union[Unset, bool] = UNSET
    project_name_template: Union[None, Unset, str] = UNSET
    revoke_when_unmatched: Union[Unset, bool] = UNSET
    project_role: Union[None, Unset, str] = UNSET
    customer_role: Union[None, Unset, str] = UNSET
    plan: Union[None, Unset, str] = UNSET
    plan_attributes: Union[Unset, "RulePlanAttributes"] = UNSET
    plan_limits: Union[Unset, "RulePlanLimits"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uuid = str(self.uuid)

        url = self.url

        customer_name = self.customer_name

        customer_uuid = self.customer_uuid

        project_role_display_name = self.project_role_display_name

        project_role_description = self.project_role_description

        customer_role_display_name = self.customer_role_display_name

        customer_role_description = self.customer_role_description

        plan_name = self.plan_name

        offering_name = self.offering_name

        offering_uuid = str(self.offering_uuid)

        category_title = self.category_title

        category_url = self.category_url

        user_affiliations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_affiliations, Unset):
            user_affiliations = self.user_affiliations

        user_email_patterns: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_email_patterns, Unset):
            user_email_patterns = self.user_email_patterns

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

        user_claims: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_claims, Unset):
            user_claims = self.user_claims.to_dict()

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        else:
            customer = self.customer

        use_user_organization_as_customer_name = self.use_user_organization_as_customer_name

        create_project = self.create_project

        project_name_template: Union[None, Unset, str]
        if isinstance(self.project_name_template, Unset):
            project_name_template = UNSET
        else:
            project_name_template = self.project_name_template

        revoke_when_unmatched = self.revoke_when_unmatched

        project_role: Union[None, Unset, str]
        if isinstance(self.project_role, Unset):
            project_role = UNSET
        else:
            project_role = self.project_role

        customer_role: Union[None, Unset, str]
        if isinstance(self.customer_role, Unset):
            customer_role = UNSET
        else:
            customer_role = self.customer_role

        plan: Union[None, Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        else:
            plan = self.plan

        plan_attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plan_attributes, Unset):
            plan_attributes = self.plan_attributes.to_dict()

        plan_limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plan_limits, Unset):
            plan_limits = self.plan_limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "uuid": uuid,
                "url": url,
                "customer_name": customer_name,
                "customer_uuid": customer_uuid,
                "project_role_display_name": project_role_display_name,
                "project_role_description": project_role_description,
                "customer_role_display_name": customer_role_display_name,
                "customer_role_description": customer_role_description,
                "plan_name": plan_name,
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
                "category_title": category_title,
                "category_url": category_url,
            }
        )
        if user_affiliations is not UNSET:
            field_dict["user_affiliations"] = user_affiliations
        if user_email_patterns is not UNSET:
            field_dict["user_email_patterns"] = user_email_patterns
        if user_identity_sources is not UNSET:
            field_dict["user_identity_sources"] = user_identity_sources
        if user_nationalities is not UNSET:
            field_dict["user_nationalities"] = user_nationalities
        if user_organization_types is not UNSET:
            field_dict["user_organization_types"] = user_organization_types
        if user_assurance_levels is not UNSET:
            field_dict["user_assurance_levels"] = user_assurance_levels
        if user_claims is not UNSET:
            field_dict["user_claims"] = user_claims
        if customer is not UNSET:
            field_dict["customer"] = customer
        if use_user_organization_as_customer_name is not UNSET:
            field_dict["use_user_organization_as_customer_name"] = use_user_organization_as_customer_name
        if create_project is not UNSET:
            field_dict["create_project"] = create_project
        if project_name_template is not UNSET:
            field_dict["project_name_template"] = project_name_template
        if revoke_when_unmatched is not UNSET:
            field_dict["revoke_when_unmatched"] = revoke_when_unmatched
        if project_role is not UNSET:
            field_dict["project_role"] = project_role
        if customer_role is not UNSET:
            field_dict["customer_role"] = customer_role
        if plan is not UNSET:
            field_dict["plan"] = plan
        if plan_attributes is not UNSET:
            field_dict["plan_attributes"] = plan_attributes
        if plan_limits is not UNSET:
            field_dict["plan_limits"] = plan_limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rule_plan_attributes import RulePlanAttributes
        from ..models.rule_plan_limits import RulePlanLimits
        from ..models.rule_user_claims import RuleUserClaims

        d = dict(src_dict)
        name = d.pop("name")

        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        customer_name = d.pop("customer_name")

        customer_uuid = d.pop("customer_uuid")

        project_role_display_name = d.pop("project_role_display_name")

        project_role_description = d.pop("project_role_description")

        customer_role_display_name = d.pop("customer_role_display_name")

        customer_role_description = d.pop("customer_role_description")

        plan_name = d.pop("plan_name")

        offering_name = d.pop("offering_name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        category_title = d.pop("category_title")

        category_url = d.pop("category_url")

        user_affiliations = cast(list[str], d.pop("user_affiliations", UNSET))

        user_email_patterns = cast(list[str], d.pop("user_email_patterns", UNSET))

        user_identity_sources = cast(list[str], d.pop("user_identity_sources", UNSET))

        user_nationalities = cast(list[str], d.pop("user_nationalities", UNSET))

        user_organization_types = cast(list[str], d.pop("user_organization_types", UNSET))

        user_assurance_levels = cast(list[str], d.pop("user_assurance_levels", UNSET))

        _user_claims = d.pop("user_claims", UNSET)
        user_claims: Union[Unset, RuleUserClaims]
        if isinstance(_user_claims, Unset):
            user_claims = UNSET
        else:
            user_claims = RuleUserClaims.from_dict(_user_claims)

        def _parse_customer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        use_user_organization_as_customer_name = d.pop("use_user_organization_as_customer_name", UNSET)

        create_project = d.pop("create_project", UNSET)

        def _parse_project_name_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_name_template = _parse_project_name_template(d.pop("project_name_template", UNSET))

        revoke_when_unmatched = d.pop("revoke_when_unmatched", UNSET)

        def _parse_project_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_role = _parse_project_role(d.pop("project_role", UNSET))

        def _parse_customer_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer_role = _parse_customer_role(d.pop("customer_role", UNSET))

        def _parse_plan(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        _plan_attributes = d.pop("plan_attributes", UNSET)
        plan_attributes: Union[Unset, RulePlanAttributes]
        if isinstance(_plan_attributes, Unset):
            plan_attributes = UNSET
        else:
            plan_attributes = RulePlanAttributes.from_dict(_plan_attributes)

        _plan_limits = d.pop("plan_limits", UNSET)
        plan_limits: Union[Unset, RulePlanLimits]
        if isinstance(_plan_limits, Unset):
            plan_limits = UNSET
        else:
            plan_limits = RulePlanLimits.from_dict(_plan_limits)

        rule = cls(
            name=name,
            uuid=uuid,
            url=url,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            project_role_display_name=project_role_display_name,
            project_role_description=project_role_description,
            customer_role_display_name=customer_role_display_name,
            customer_role_description=customer_role_description,
            plan_name=plan_name,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            category_title=category_title,
            category_url=category_url,
            user_affiliations=user_affiliations,
            user_email_patterns=user_email_patterns,
            user_identity_sources=user_identity_sources,
            user_nationalities=user_nationalities,
            user_organization_types=user_organization_types,
            user_assurance_levels=user_assurance_levels,
            user_claims=user_claims,
            customer=customer,
            use_user_organization_as_customer_name=use_user_organization_as_customer_name,
            create_project=create_project,
            project_name_template=project_name_template,
            revoke_when_unmatched=revoke_when_unmatched,
            project_role=project_role,
            customer_role=customer_role,
            plan=plan,
            plan_attributes=plan_attributes,
            plan_limits=plan_limits,
        )

        rule.additional_properties = d
        return rule

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
