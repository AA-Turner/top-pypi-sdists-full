import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.limit_type_enum import LimitTypeEnum
from ..models.policy_period_enum import PolicyPeriodEnum
from ..models.qos_strategy_enum import QosStrategyEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_offering_component_limit import NestedOfferingComponentLimit


T = TypeVar("T", bound="SlurmPeriodicUsagePolicy")


@_attrs_define
class SlurmPeriodicUsagePolicy:
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
        component_limits_set (list['NestedOfferingComponentLimit']):
        period_name (str):
        warnings (list[str]): Warnings about misconfiguration, e.g. missing site agent queue registration.
        options (Union[Unset, Any]): Fields for saving actions extra data. Keys are name of actions.
        organization_groups (Union[Unset, list[str]]):
        apply_to_all (Union[Unset, bool]): If True, policy applies to all customers. Mutually exclusive with
            organization_groups.
        period (Union[Unset, PolicyPeriodEnum]):
        limit_type (Union[Unset, LimitTypeEnum]):
        tres_billing_enabled (Union[Unset, bool]): Use TRES billing units instead of raw TRES values
        tres_billing_weights (Union[Unset, Any]): TRES billing weights (e.g., {"CPU": 0.015625, "Mem": 0.001953125,
            "GRES/gpu": 0.25})
        carryover_factor (Union[Unset, int]): Maximum percentage of base allocation that can carry over from unused
            previous period (0-100)
        grace_ratio (Union[Unset, float]): Grace period ratio (0.2 = 20% overconsumption allowed)
        carryover_enabled (Union[Unset, bool]): Enable unused allocation carryover to next period
        raw_usage_reset (Union[Unset, bool]): Reset raw usage at period transitions (PriorityUsageResetPeriod=None)
        qos_strategy (Union[Unset, QosStrategyEnum]):
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
    component_limits_set: list["NestedOfferingComponentLimit"]
    period_name: str
    warnings: list[str]
    options: Union[Unset, Any] = UNSET
    organization_groups: Union[Unset, list[str]] = UNSET
    apply_to_all: Union[Unset, bool] = UNSET
    period: Union[Unset, PolicyPeriodEnum] = UNSET
    limit_type: Union[Unset, LimitTypeEnum] = UNSET
    tres_billing_enabled: Union[Unset, bool] = UNSET
    tres_billing_weights: Union[Unset, Any] = UNSET
    carryover_factor: Union[Unset, int] = UNSET
    grace_ratio: Union[Unset, float] = UNSET
    carryover_enabled: Union[Unset, bool] = UNSET
    raw_usage_reset: Union[Unset, bool] = UNSET
    qos_strategy: Union[Unset, QosStrategyEnum] = UNSET
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

        component_limits_set = []
        for component_limits_set_item_data in self.component_limits_set:
            component_limits_set_item = component_limits_set_item_data.to_dict()
            component_limits_set.append(component_limits_set_item)

        period_name = self.period_name

        warnings = self.warnings

        options = self.options

        organization_groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.organization_groups, Unset):
            organization_groups = self.organization_groups

        apply_to_all = self.apply_to_all

        period: Union[Unset, int] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        limit_type: Union[Unset, str] = UNSET
        if not isinstance(self.limit_type, Unset):
            limit_type = self.limit_type.value

        tres_billing_enabled = self.tres_billing_enabled

        tres_billing_weights = self.tres_billing_weights

        carryover_factor = self.carryover_factor

        grace_ratio = self.grace_ratio

        carryover_enabled = self.carryover_enabled

        raw_usage_reset = self.raw_usage_reset

        qos_strategy: Union[Unset, str] = UNSET
        if not isinstance(self.qos_strategy, Unset):
            qos_strategy = self.qos_strategy.value

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
                "component_limits_set": component_limits_set,
                "period_name": period_name,
                "warnings": warnings,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options
        if organization_groups is not UNSET:
            field_dict["organization_groups"] = organization_groups
        if apply_to_all is not UNSET:
            field_dict["apply_to_all"] = apply_to_all
        if period is not UNSET:
            field_dict["period"] = period
        if limit_type is not UNSET:
            field_dict["limit_type"] = limit_type
        if tres_billing_enabled is not UNSET:
            field_dict["tres_billing_enabled"] = tres_billing_enabled
        if tres_billing_weights is not UNSET:
            field_dict["tres_billing_weights"] = tres_billing_weights
        if carryover_factor is not UNSET:
            field_dict["carryover_factor"] = carryover_factor
        if grace_ratio is not UNSET:
            field_dict["grace_ratio"] = grace_ratio
        if carryover_enabled is not UNSET:
            field_dict["carryover_enabled"] = carryover_enabled
        if raw_usage_reset is not UNSET:
            field_dict["raw_usage_reset"] = raw_usage_reset
        if qos_strategy is not UNSET:
            field_dict["qos_strategy"] = qos_strategy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_offering_component_limit import NestedOfferingComponentLimit

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

        component_limits_set = []
        _component_limits_set = d.pop("component_limits_set")
        for component_limits_set_item_data in _component_limits_set:
            component_limits_set_item = NestedOfferingComponentLimit.from_dict(component_limits_set_item_data)

            component_limits_set.append(component_limits_set_item)

        period_name = d.pop("period_name")

        warnings = cast(list[str], d.pop("warnings"))

        options = d.pop("options", UNSET)

        organization_groups = cast(list[str], d.pop("organization_groups", UNSET))

        apply_to_all = d.pop("apply_to_all", UNSET)

        _period = d.pop("period", UNSET)
        period: Union[Unset, PolicyPeriodEnum]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = PolicyPeriodEnum(_period)

        _limit_type = d.pop("limit_type", UNSET)
        limit_type: Union[Unset, LimitTypeEnum]
        if isinstance(_limit_type, Unset):
            limit_type = UNSET
        else:
            limit_type = LimitTypeEnum(_limit_type)

        tres_billing_enabled = d.pop("tres_billing_enabled", UNSET)

        tres_billing_weights = d.pop("tres_billing_weights", UNSET)

        carryover_factor = d.pop("carryover_factor", UNSET)

        grace_ratio = d.pop("grace_ratio", UNSET)

        carryover_enabled = d.pop("carryover_enabled", UNSET)

        raw_usage_reset = d.pop("raw_usage_reset", UNSET)

        _qos_strategy = d.pop("qos_strategy", UNSET)
        qos_strategy: Union[Unset, QosStrategyEnum]
        if isinstance(_qos_strategy, Unset):
            qos_strategy = UNSET
        else:
            qos_strategy = QosStrategyEnum(_qos_strategy)

        slurm_periodic_usage_policy = cls(
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
            component_limits_set=component_limits_set,
            period_name=period_name,
            warnings=warnings,
            options=options,
            organization_groups=organization_groups,
            apply_to_all=apply_to_all,
            period=period,
            limit_type=limit_type,
            tres_billing_enabled=tres_billing_enabled,
            tres_billing_weights=tres_billing_weights,
            carryover_factor=carryover_factor,
            grace_ratio=grace_ratio,
            carryover_enabled=carryover_enabled,
            raw_usage_reset=raw_usage_reset,
            qos_strategy=qos_strategy,
        )

        slurm_periodic_usage_policy.additional_properties = d
        return slurm_periodic_usage_policy

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
