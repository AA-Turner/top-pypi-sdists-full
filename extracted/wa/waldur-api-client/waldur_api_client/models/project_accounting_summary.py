import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ProjectAccountingSummary")


@_attrs_define
class ProjectAccountingSummary:
    """
    Attributes:
        project_uuid (UUID):
        project_name (str):
        customer_uuid (UUID):
        customer_name (str):
        start_date (Union[None, datetime.date]):
        end_date (Union[None, datetime.date]):
        total_credits (str):
        total_spend (str):
        current_month_spend (str):
    """

    project_uuid: UUID
    project_name: str
    customer_uuid: UUID
    customer_name: str
    start_date: Union[None, datetime.date]
    end_date: Union[None, datetime.date]
    total_credits: str
    total_spend: str
    current_month_spend: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        start_date: Union[None, str]
        if isinstance(self.start_date, datetime.date):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        end_date: Union[None, str]
        if isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        total_credits = self.total_credits

        total_spend = self.total_spend

        current_month_spend = self.current_month_spend

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_uuid": project_uuid,
                "project_name": project_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "start_date": start_date,
                "end_date": end_date,
                "total_credits": total_credits,
                "total_spend": total_spend,
                "current_month_spend": current_month_spend,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        def _parse_start_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data).date()

                return start_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        start_date = _parse_start_date(d.pop("start_date"))

        def _parse_end_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data).date()

                return end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        end_date = _parse_end_date(d.pop("end_date"))

        total_credits = d.pop("total_credits")

        total_spend = d.pop("total_spend")

        current_month_spend = d.pop("current_month_spend")

        project_accounting_summary = cls(
            project_uuid=project_uuid,
            project_name=project_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            start_date=start_date,
            end_date=end_date,
            total_credits=total_credits,
            total_spend=total_spend,
            current_month_spend=current_month_spend,
        )

        project_accounting_summary.additional_properties = d
        return project_accounting_summary

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
