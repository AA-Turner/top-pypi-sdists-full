from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_rule_request_plan_attributes import PatchedRuleRequestPlanAttributes
    from ..models.patched_rule_request_plan_limits import PatchedRuleRequestPlanLimits


T = TypeVar("T", bound="PatchedRuleRequest")


@_attrs_define
class PatchedRuleRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        user_affiliations (Union[Unset, list[str]]):
        user_email_patterns (Union[Unset, list[str]]):
        customer (Union[None, Unset, str]):
        use_user_organization_as_customer_name (Union[Unset, bool]):
        project_role (Union[None, Unset, str]):
        project_role_name (Union[None, Unset, str]):
        plan (Union[None, Unset, str]):
        plan_attributes (Union[Unset, PatchedRuleRequestPlanAttributes]):
        plan_limits (Union[Unset, PatchedRuleRequestPlanLimits]):
    """

    name: Union[Unset, str] = UNSET
    user_affiliations: Union[Unset, list[str]] = UNSET
    user_email_patterns: Union[Unset, list[str]] = UNSET
    customer: Union[None, Unset, str] = UNSET
    use_user_organization_as_customer_name: Union[Unset, bool] = UNSET
    project_role: Union[None, Unset, str] = UNSET
    project_role_name: Union[None, Unset, str] = UNSET
    plan: Union[None, Unset, str] = UNSET
    plan_attributes: Union[Unset, "PatchedRuleRequestPlanAttributes"] = UNSET
    plan_limits: Union[Unset, "PatchedRuleRequestPlanLimits"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        user_affiliations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_affiliations, Unset):
            user_affiliations = self.user_affiliations

        user_email_patterns: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_email_patterns, Unset):
            user_email_patterns = self.user_email_patterns

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        else:
            customer = self.customer

        use_user_organization_as_customer_name = self.use_user_organization_as_customer_name

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
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if user_affiliations is not UNSET:
            field_dict["user_affiliations"] = user_affiliations
        if user_email_patterns is not UNSET:
            field_dict["user_email_patterns"] = user_email_patterns
        if customer is not UNSET:
            field_dict["customer"] = customer
        if use_user_organization_as_customer_name is not UNSET:
            field_dict["use_user_organization_as_customer_name"] = use_user_organization_as_customer_name
        if project_role is not UNSET:
            field_dict["project_role"] = project_role
        if project_role_name is not UNSET:
            field_dict["project_role_name"] = project_role_name
        if plan is not UNSET:
            field_dict["plan"] = plan
        if plan_attributes is not UNSET:
            field_dict["plan_attributes"] = plan_attributes
        if plan_limits is not UNSET:
            field_dict["plan_limits"] = plan_limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.patched_rule_request_plan_attributes import PatchedRuleRequestPlanAttributes
        from ..models.patched_rule_request_plan_limits import PatchedRuleRequestPlanLimits

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        user_affiliations = cast(list[str], d.pop("user_affiliations", UNSET))

        user_email_patterns = cast(list[str], d.pop("user_email_patterns", UNSET))

        def _parse_customer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        use_user_organization_as_customer_name = d.pop("use_user_organization_as_customer_name", UNSET)

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

        def _parse_plan(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        _plan_attributes = d.pop("plan_attributes", UNSET)
        plan_attributes: Union[Unset, PatchedRuleRequestPlanAttributes]
        if isinstance(_plan_attributes, Unset):
            plan_attributes = UNSET
        else:
            plan_attributes = PatchedRuleRequestPlanAttributes.from_dict(_plan_attributes)

        _plan_limits = d.pop("plan_limits", UNSET)
        plan_limits: Union[Unset, PatchedRuleRequestPlanLimits]
        if isinstance(_plan_limits, Unset):
            plan_limits = UNSET
        else:
            plan_limits = PatchedRuleRequestPlanLimits.from_dict(_plan_limits)

        patched_rule_request = cls(
            name=name,
            user_affiliations=user_affiliations,
            user_email_patterns=user_email_patterns,
            customer=customer,
            use_user_organization_as_customer_name=use_user_organization_as_customer_name,
            project_role=project_role,
            project_role_name=project_role_name,
            plan=plan,
            plan_attributes=plan_attributes,
            plan_limits=plan_limits,
        )

        patched_rule_request.additional_properties = d
        return patched_rule_request

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
