import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.hpc_monthly_usage import HpcMonthlyUsage
    from ..models.hpc_usage_point import HpcUsagePoint
    from ..models.hpc_user_usage import HpcUserUsage


T = TypeVar("T", bound="HpcComponentUsage")


@_attrs_define
class HpcComponentUsage:
    """
    Attributes:
        type_ (str):
        name (str):
        unit (str):
        limit (Union[None, float]):
        limit_period (str):
        period_start (datetime.date):
        period_end (Union[None, datetime.date]):
        consumed (float):
        percent (Union[None, float]):
        daily_rate (Union[None, float]):
        runs_out (Union[None, datetime.date]):
        runs_out_before_period_end (bool):
        cumulative (list['HpcUsagePoint']):
        monthly (list['HpcMonthlyUsage']):
        users (list['HpcUserUsage']):
    """

    type_: str
    name: str
    unit: str
    limit: Union[None, float]
    limit_period: str
    period_start: datetime.date
    period_end: Union[None, datetime.date]
    consumed: float
    percent: Union[None, float]
    daily_rate: Union[None, float]
    runs_out: Union[None, datetime.date]
    runs_out_before_period_end: bool
    cumulative: list["HpcUsagePoint"]
    monthly: list["HpcMonthlyUsage"]
    users: list["HpcUserUsage"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        name = self.name

        unit = self.unit

        limit: Union[None, float]
        limit = self.limit

        limit_period = self.limit_period

        period_start = self.period_start.isoformat()

        period_end: Union[None, str]
        if isinstance(self.period_end, datetime.date):
            period_end = self.period_end.isoformat()
        else:
            period_end = self.period_end

        consumed = self.consumed

        percent: Union[None, float]
        percent = self.percent

        daily_rate: Union[None, float]
        daily_rate = self.daily_rate

        runs_out: Union[None, str]
        if isinstance(self.runs_out, datetime.date):
            runs_out = self.runs_out.isoformat()
        else:
            runs_out = self.runs_out

        runs_out_before_period_end = self.runs_out_before_period_end

        cumulative = []
        for cumulative_item_data in self.cumulative:
            cumulative_item = cumulative_item_data.to_dict()
            cumulative.append(cumulative_item)

        monthly = []
        for monthly_item_data in self.monthly:
            monthly_item = monthly_item_data.to_dict()
            monthly.append(monthly_item)

        users = []
        for users_item_data in self.users:
            users_item = users_item_data.to_dict()
            users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "name": name,
                "unit": unit,
                "limit": limit,
                "limit_period": limit_period,
                "period_start": period_start,
                "period_end": period_end,
                "consumed": consumed,
                "percent": percent,
                "daily_rate": daily_rate,
                "runs_out": runs_out,
                "runs_out_before_period_end": runs_out_before_period_end,
                "cumulative": cumulative,
                "monthly": monthly,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hpc_monthly_usage import HpcMonthlyUsage
        from ..models.hpc_usage_point import HpcUsagePoint
        from ..models.hpc_user_usage import HpcUserUsage

        d = dict(src_dict)
        type_ = d.pop("type")

        name = d.pop("name")

        unit = d.pop("unit")

        def _parse_limit(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        limit = _parse_limit(d.pop("limit"))

        limit_period = d.pop("limit_period")

        period_start = isoparse(d.pop("period_start")).date()

        def _parse_period_end(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                period_end_type_0 = isoparse(data).date()

                return period_end_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        period_end = _parse_period_end(d.pop("period_end"))

        consumed = d.pop("consumed")

        def _parse_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        percent = _parse_percent(d.pop("percent"))

        def _parse_daily_rate(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        daily_rate = _parse_daily_rate(d.pop("daily_rate"))

        def _parse_runs_out(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                runs_out_type_0 = isoparse(data).date()

                return runs_out_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        runs_out = _parse_runs_out(d.pop("runs_out"))

        runs_out_before_period_end = d.pop("runs_out_before_period_end")

        cumulative = []
        _cumulative = d.pop("cumulative")
        for cumulative_item_data in _cumulative:
            cumulative_item = HpcUsagePoint.from_dict(cumulative_item_data)

            cumulative.append(cumulative_item)

        monthly = []
        _monthly = d.pop("monthly")
        for monthly_item_data in _monthly:
            monthly_item = HpcMonthlyUsage.from_dict(monthly_item_data)

            monthly.append(monthly_item)

        users = []
        _users = d.pop("users")
        for users_item_data in _users:
            users_item = HpcUserUsage.from_dict(users_item_data)

            users.append(users_item)

        hpc_component_usage = cls(
            type_=type_,
            name=name,
            unit=unit,
            limit=limit,
            limit_period=limit_period,
            period_start=period_start,
            period_end=period_end,
            consumed=consumed,
            percent=percent,
            daily_rate=daily_rate,
            runs_out=runs_out,
            runs_out_before_period_end=runs_out_before_period_end,
            cumulative=cumulative,
            monthly=monthly,
            users=users,
        )

        hpc_component_usage.additional_properties = d
        return hpc_component_usage

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
