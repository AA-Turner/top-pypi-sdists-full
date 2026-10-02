import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.policy_period_enum import PolicyPeriodEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_price_estimate import NestedPriceEstimate
    from ..models.project_estimated_cost_policy_options import ProjectEstimatedCostPolicyOptions


T = TypeVar("T", bound="ProjectEstimatedCostPolicy")


@_attrs_define
class ProjectEstimatedCostPolicy:
    """
    Attributes:
        uuid (UUID):
        url (str):
        scope (str):
        scope_name (str):
        scope_uuid (UUID):
        actions (str):
        created (datetime.datetime):
        created_by_full_name (str):
        created_by_username (str):
        has_fired (bool):
        fired_datetime (datetime.datetime):
        affected_resources_count (int):
        limit_cost (int):
        period_name (str):
        project_credit (Union[None, str]):
        customer_credit (Union[None, str]):
        resource_name (str):
        billing_price_estimate (NestedPriceEstimate):
        options (Union[Unset, ProjectEstimatedCostPolicyOptions]): Fields for saving actions extra data. Keys are name
            of actions.
        period (Union[Unset, PolicyPeriodEnum]):
        resource (Union[None, UUID, Unset]):
        use_credit (Union[Unset, bool]):
    """

    uuid: UUID
    url: str
    scope: str
    scope_name: str
    scope_uuid: UUID
    actions: str
    created: datetime.datetime
    created_by_full_name: str
    created_by_username: str
    has_fired: bool
    fired_datetime: datetime.datetime
    affected_resources_count: int
    limit_cost: int
    period_name: str
    project_credit: Union[None, str]
    customer_credit: Union[None, str]
    resource_name: str
    billing_price_estimate: "NestedPriceEstimate"
    options: Union[Unset, "ProjectEstimatedCostPolicyOptions"] = UNSET
    period: Union[Unset, PolicyPeriodEnum] = UNSET
    resource: Union[None, UUID, Unset] = UNSET
    use_credit: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        scope = self.scope

        scope_name = self.scope_name

        scope_uuid = str(self.scope_uuid)

        actions = self.actions

        created = self.created.isoformat()

        created_by_full_name = self.created_by_full_name

        created_by_username = self.created_by_username

        has_fired = self.has_fired

        fired_datetime = self.fired_datetime.isoformat()

        affected_resources_count = self.affected_resources_count

        limit_cost = self.limit_cost

        period_name = self.period_name

        project_credit: Union[None, str]
        project_credit = self.project_credit

        customer_credit: Union[None, str]
        customer_credit = self.customer_credit

        resource_name = self.resource_name

        billing_price_estimate = self.billing_price_estimate.to_dict()

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        period: Union[Unset, int] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        resource: Union[None, Unset, str]
        if isinstance(self.resource, Unset):
            resource = UNSET
        elif isinstance(self.resource, UUID):
            resource = str(self.resource)
        else:
            resource = self.resource

        use_credit = self.use_credit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "scope": scope,
                "scope_name": scope_name,
                "scope_uuid": scope_uuid,
                "actions": actions,
                "created": created,
                "created_by_full_name": created_by_full_name,
                "created_by_username": created_by_username,
                "has_fired": has_fired,
                "fired_datetime": fired_datetime,
                "affected_resources_count": affected_resources_count,
                "limit_cost": limit_cost,
                "period_name": period_name,
                "project_credit": project_credit,
                "customer_credit": customer_credit,
                "resource_name": resource_name,
                "billing_price_estimate": billing_price_estimate,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options
        if period is not UNSET:
            field_dict["period"] = period
        if resource is not UNSET:
            field_dict["resource"] = resource
        if use_credit is not UNSET:
            field_dict["use_credit"] = use_credit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_price_estimate import NestedPriceEstimate
        from ..models.project_estimated_cost_policy_options import ProjectEstimatedCostPolicyOptions

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        scope = d.pop("scope")

        scope_name = d.pop("scope_name")

        scope_uuid = UUID(d.pop("scope_uuid"))

        actions = d.pop("actions")

        created = isoparse(d.pop("created"))

        created_by_full_name = d.pop("created_by_full_name")

        created_by_username = d.pop("created_by_username")

        has_fired = d.pop("has_fired")

        fired_datetime = isoparse(d.pop("fired_datetime"))

        affected_resources_count = d.pop("affected_resources_count")

        limit_cost = d.pop("limit_cost")

        period_name = d.pop("period_name")

        def _parse_project_credit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        project_credit = _parse_project_credit(d.pop("project_credit"))

        def _parse_customer_credit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_credit = _parse_customer_credit(d.pop("customer_credit"))

        resource_name = d.pop("resource_name")

        billing_price_estimate = NestedPriceEstimate.from_dict(d.pop("billing_price_estimate"))

        _options = d.pop("options", UNSET)
        options: Union[Unset, ProjectEstimatedCostPolicyOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = ProjectEstimatedCostPolicyOptions.from_dict(_options)

        _period = d.pop("period", UNSET)
        period: Union[Unset, PolicyPeriodEnum]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = PolicyPeriodEnum(_period)

        def _parse_resource(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_type_0 = UUID(data)

                return resource_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        resource = _parse_resource(d.pop("resource", UNSET))

        use_credit = d.pop("use_credit", UNSET)

        project_estimated_cost_policy = cls(
            uuid=uuid,
            url=url,
            scope=scope,
            scope_name=scope_name,
            scope_uuid=scope_uuid,
            actions=actions,
            created=created,
            created_by_full_name=created_by_full_name,
            created_by_username=created_by_username,
            has_fired=has_fired,
            fired_datetime=fired_datetime,
            affected_resources_count=affected_resources_count,
            limit_cost=limit_cost,
            period_name=period_name,
            project_credit=project_credit,
            customer_credit=customer_credit,
            resource_name=resource_name,
            billing_price_estimate=billing_price_estimate,
            options=options,
            period=period,
            resource=resource,
            use_credit=use_credit,
        )

        project_estimated_cost_policy.additional_properties = d
        return project_estimated_cost_policy

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
