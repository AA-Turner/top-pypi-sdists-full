from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rule_request_plan_attributes import RuleRequestPlanAttributes
    from ..models.rule_request_plan_limits import RuleRequestPlanLimits
    from ..models.rule_request_user_claims import RuleRequestUserClaims


T = TypeVar("T", bound="RuleRequest")


@_attrs_define
class RuleRequest:
    """
    Attributes:
        name (str):
        user_affiliations (Union[Unset, list[str]]):
        user_email_patterns (Union[Unset, list[str]]):
        user_identity_sources (Union[Unset, list[str]]):
        user_nationalities (Union[Unset, list[str]]):
        user_organization_types (Union[Unset, list[str]]):
        user_assurance_levels (Union[Unset, list[str]]):
        user_claims (Union[Unset, RuleRequestUserClaims]): Identity provider claims the user must carry, as {"claim":
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
        project_role_name (Union[None, Unset, str]):
        customer_role (Union[None, Unset, str]):
        customer_role_name (Union[None, Unset, str]):
        plan (Union[None, Unset, str]):
        plan_attributes (Union[Unset, RuleRequestPlanAttributes]):
        plan_limits (Union[Unset, RuleRequestPlanLimits]):
    """

    name: str
    user_affiliations: Union[Unset, list[str]] = UNSET
    user_email_patterns: Union[Unset, list[str]] = UNSET
    user_identity_sources: Union[Unset, list[str]] = UNSET
    user_nationalities: Union[Unset, list[str]] = UNSET
    user_organization_types: Union[Unset, list[str]] = UNSET
    user_assurance_levels: Union[Unset, list[str]] = UNSET
    user_claims: Union[Unset, "RuleRequestUserClaims"] = UNSET
    customer: Union[None, Unset, str] = UNSET
    use_user_organization_as_customer_name: Union[Unset, bool] = UNSET
    create_project: Union[Unset, bool] = UNSET
    project_name_template: Union[None, Unset, str] = UNSET
    revoke_when_unmatched: Union[Unset, bool] = UNSET
    project_role: Union[None, Unset, str] = UNSET
    project_role_name: Union[None, Unset, str] = UNSET
    customer_role: Union[None, Unset, str] = UNSET
    customer_role_name: Union[None, Unset, str] = UNSET
    plan: Union[None, Unset, str] = UNSET
    plan_attributes: Union[Unset, "RuleRequestPlanAttributes"] = UNSET
    plan_limits: Union[Unset, "RuleRequestPlanLimits"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

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

        project_role_name: Union[None, Unset, str]
        if isinstance(self.project_role_name, Unset):
            project_role_name = UNSET
        else:
            project_role_name = self.project_role_name

        customer_role: Union[None, Unset, str]
        if isinstance(self.customer_role, Unset):
            customer_role = UNSET
        else:
            customer_role = self.customer_role

        customer_role_name: Union[None, Unset, str]
        if isinstance(self.customer_role_name, Unset):
            customer_role_name = UNSET
        else:
            customer_role_name = self.customer_role_name

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
        if project_role_name is not UNSET:
            field_dict["project_role_name"] = project_role_name
        if customer_role is not UNSET:
            field_dict["customer_role"] = customer_role
        if customer_role_name is not UNSET:
            field_dict["customer_role_name"] = customer_role_name
        if plan is not UNSET:
            field_dict["plan"] = plan
        if plan_attributes is not UNSET:
            field_dict["plan_attributes"] = plan_attributes
        if plan_limits is not UNSET:
            field_dict["plan_limits"] = plan_limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rule_request_plan_attributes import RuleRequestPlanAttributes
        from ..models.rule_request_plan_limits import RuleRequestPlanLimits
        from ..models.rule_request_user_claims import RuleRequestUserClaims

        d = dict(src_dict)
        name = d.pop("name")

        user_affiliations = cast(list[str], d.pop("user_affiliations", UNSET))

        user_email_patterns = cast(list[str], d.pop("user_email_patterns", UNSET))

        user_identity_sources = cast(list[str], d.pop("user_identity_sources", UNSET))

        user_nationalities = cast(list[str], d.pop("user_nationalities", UNSET))

        user_organization_types = cast(list[str], d.pop("user_organization_types", UNSET))

        user_assurance_levels = cast(list[str], d.pop("user_assurance_levels", UNSET))

        _user_claims = d.pop("user_claims", UNSET)
        user_claims: Union[Unset, RuleRequestUserClaims]
        if isinstance(_user_claims, Unset):
            user_claims = UNSET
        else:
            user_claims = RuleRequestUserClaims.from_dict(_user_claims)

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

        def _parse_project_role_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_role_name = _parse_project_role_name(d.pop("project_role_name", UNSET))

        def _parse_customer_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer_role = _parse_customer_role(d.pop("customer_role", UNSET))

        def _parse_customer_role_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer_role_name = _parse_customer_role_name(d.pop("customer_role_name", UNSET))

        def _parse_plan(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        _plan_attributes = d.pop("plan_attributes", UNSET)
        plan_attributes: Union[Unset, RuleRequestPlanAttributes]
        if isinstance(_plan_attributes, Unset):
            plan_attributes = UNSET
        else:
            plan_attributes = RuleRequestPlanAttributes.from_dict(_plan_attributes)

        _plan_limits = d.pop("plan_limits", UNSET)
        plan_limits: Union[Unset, RuleRequestPlanLimits]
        if isinstance(_plan_limits, Unset):
            plan_limits = UNSET
        else:
            plan_limits = RuleRequestPlanLimits.from_dict(_plan_limits)

        rule_request = cls(
            name=name,
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
            project_role_name=project_role_name,
            customer_role=customer_role,
            customer_role_name=customer_role_name,
            plan=plan,
            plan_attributes=plan_attributes,
            plan_limits=plan_limits,
        )

        rule_request.additional_properties = d
        return rule_request

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
