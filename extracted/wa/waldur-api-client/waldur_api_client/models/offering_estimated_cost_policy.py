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
    from ..models.offering_estimated_cost_policy_options import OfferingEstimatedCostPolicyOptions


T = TypeVar("T", bound="OfferingEstimatedCostPolicy")


@_attrs_define
class OfferingEstimatedCostPolicy:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        url (Union[Unset, str]):
        scope (Union[Unset, str]):
        scope_name (Union[Unset, str]):
        scope_uuid (Union[Unset, UUID]):
        actions (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        created_by_full_name (Union[Unset, str]):
        created_by_username (Union[Unset, str]):
        has_fired (Union[Unset, bool]):
        fired_datetime (Union[Unset, datetime.datetime]):
        options (Union[Unset, OfferingEstimatedCostPolicyOptions]): Fields for saving actions extra data. Keys are name
            of actions.
        affected_resources_count (Union[Unset, int]):
        limit_cost (Union[Unset, int]):
        period (Union[Unset, PolicyPeriodEnum]):
        period_name (Union[Unset, str]):
        current_cost (Union[Unset, str]): The cost this policy compares against limit_cost right now: the period's
            invoice total, less the credit already applied and the credit still to be drawn. Do not re-derive it — only the
            server can simulate the pending draw, and a figure computed from the invoice alone will not match what the
            policy evaluates.
        eta_days (Union[None, Unset, int]): Days until the policy fires, or null when no projection exists. 0 means the
            threshold is already crossed and the policy is triggered — measured, not projected. Null must be rendered as no
            date, never as 'now': it is the common case, and it is also what an unprojectable or more-than-a-year-away
            policy reports. Nothing is projected beyond 365 days, because the rate comes from the current month's spend.
            Note that a cost policy does not fire on cost alone — it also waits for the credit balance to fall to limit_cost
            — so a policy far over its cap can still report a future date or null.
        eta_date (Union[None, Unset, datetime.date]): eta_days as a calendar date, so clients do not each re-derive it.
            Null whenever eta_days is null; today when eta_days is 0.
        organization_groups (Union[Unset, list[str]]):
        apply_to_all (Union[Unset, bool]): If True, policy applies to all customers. Mutually exclusive with
            organization_groups.
    """

    uuid: Union[Unset, UUID] = UNSET
    url: Union[Unset, str] = UNSET
    scope: Union[Unset, str] = UNSET
    scope_name: Union[Unset, str] = UNSET
    scope_uuid: Union[Unset, UUID] = UNSET
    actions: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    created_by_full_name: Union[Unset, str] = UNSET
    created_by_username: Union[Unset, str] = UNSET
    has_fired: Union[Unset, bool] = UNSET
    fired_datetime: Union[Unset, datetime.datetime] = UNSET
    options: Union[Unset, "OfferingEstimatedCostPolicyOptions"] = UNSET
    affected_resources_count: Union[Unset, int] = UNSET
    limit_cost: Union[Unset, int] = UNSET
    period: Union[Unset, PolicyPeriodEnum] = UNSET
    period_name: Union[Unset, str] = UNSET
    current_cost: Union[Unset, str] = UNSET
    eta_days: Union[None, Unset, int] = UNSET
    eta_date: Union[None, Unset, datetime.date] = UNSET
    organization_groups: Union[Unset, list[str]] = UNSET
    apply_to_all: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        url = self.url

        scope = self.scope

        scope_name = self.scope_name

        scope_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.scope_uuid, Unset):
            scope_uuid = str(self.scope_uuid)

        actions = self.actions

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        created_by_full_name = self.created_by_full_name

        created_by_username = self.created_by_username

        has_fired = self.has_fired

        fired_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.fired_datetime, Unset):
            fired_datetime = self.fired_datetime.isoformat()

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        affected_resources_count = self.affected_resources_count

        limit_cost = self.limit_cost

        period: Union[Unset, int] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        period_name = self.period_name

        current_cost = self.current_cost

        eta_days: Union[None, Unset, int]
        if isinstance(self.eta_days, Unset):
            eta_days = UNSET
        else:
            eta_days = self.eta_days

        eta_date: Union[None, Unset, str]
        if isinstance(self.eta_date, Unset):
            eta_date = UNSET
        elif isinstance(self.eta_date, datetime.date):
            eta_date = self.eta_date.isoformat()
        else:
            eta_date = self.eta_date

        organization_groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.organization_groups, Unset):
            organization_groups = self.organization_groups

        apply_to_all = self.apply_to_all

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if url is not UNSET:
            field_dict["url"] = url
        if scope is not UNSET:
            field_dict["scope"] = scope
        if scope_name is not UNSET:
            field_dict["scope_name"] = scope_name
        if scope_uuid is not UNSET:
            field_dict["scope_uuid"] = scope_uuid
        if actions is not UNSET:
            field_dict["actions"] = actions
        if created is not UNSET:
            field_dict["created"] = created
        if created_by_full_name is not UNSET:
            field_dict["created_by_full_name"] = created_by_full_name
        if created_by_username is not UNSET:
            field_dict["created_by_username"] = created_by_username
        if has_fired is not UNSET:
            field_dict["has_fired"] = has_fired
        if fired_datetime is not UNSET:
            field_dict["fired_datetime"] = fired_datetime
        if options is not UNSET:
            field_dict["options"] = options
        if affected_resources_count is not UNSET:
            field_dict["affected_resources_count"] = affected_resources_count
        if limit_cost is not UNSET:
            field_dict["limit_cost"] = limit_cost
        if period is not UNSET:
            field_dict["period"] = period
        if period_name is not UNSET:
            field_dict["period_name"] = period_name
        if current_cost is not UNSET:
            field_dict["current_cost"] = current_cost
        if eta_days is not UNSET:
            field_dict["eta_days"] = eta_days
        if eta_date is not UNSET:
            field_dict["eta_date"] = eta_date
        if organization_groups is not UNSET:
            field_dict["organization_groups"] = organization_groups
        if apply_to_all is not UNSET:
            field_dict["apply_to_all"] = apply_to_all

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_estimated_cost_policy_options import OfferingEstimatedCostPolicyOptions

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        url = d.pop("url", UNSET)

        scope = d.pop("scope", UNSET)

        scope_name = d.pop("scope_name", UNSET)

        _scope_uuid = d.pop("scope_uuid", UNSET)
        scope_uuid: Union[Unset, UUID]
        if isinstance(_scope_uuid, Unset):
            scope_uuid = UNSET
        else:
            scope_uuid = UUID(_scope_uuid)

        actions = d.pop("actions", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        created_by_full_name = d.pop("created_by_full_name", UNSET)

        created_by_username = d.pop("created_by_username", UNSET)

        has_fired = d.pop("has_fired", UNSET)

        _fired_datetime = d.pop("fired_datetime", UNSET)
        fired_datetime: Union[Unset, datetime.datetime]
        if isinstance(_fired_datetime, Unset):
            fired_datetime = UNSET
        else:
            fired_datetime = isoparse(_fired_datetime)

        _options = d.pop("options", UNSET)
        options: Union[Unset, OfferingEstimatedCostPolicyOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = OfferingEstimatedCostPolicyOptions.from_dict(_options)

        affected_resources_count = d.pop("affected_resources_count", UNSET)

        limit_cost = d.pop("limit_cost", UNSET)

        _period = d.pop("period", UNSET)
        period: Union[Unset, PolicyPeriodEnum]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = PolicyPeriodEnum(_period)

        period_name = d.pop("period_name", UNSET)

        current_cost = d.pop("current_cost", UNSET)

        def _parse_eta_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        eta_days = _parse_eta_days(d.pop("eta_days", UNSET))

        def _parse_eta_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                eta_date_type_0 = isoparse(data).date()

                return eta_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        eta_date = _parse_eta_date(d.pop("eta_date", UNSET))

        organization_groups = cast(list[str], d.pop("organization_groups", UNSET))

        apply_to_all = d.pop("apply_to_all", UNSET)

        offering_estimated_cost_policy = cls(
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
            options=options,
            affected_resources_count=affected_resources_count,
            limit_cost=limit_cost,
            period=period,
            period_name=period_name,
            current_cost=current_cost,
            eta_days=eta_days,
            eta_date=eta_date,
            organization_groups=organization_groups,
            apply_to_all=apply_to_all,
        )

        offering_estimated_cost_policy.additional_properties = d
        return offering_estimated_cost_policy

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
