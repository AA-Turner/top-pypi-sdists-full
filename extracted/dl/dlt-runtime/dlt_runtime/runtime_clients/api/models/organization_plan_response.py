import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.organization_plan_type import OrganizationPlanType
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationPlanResponse")


@_attrs_define
class OrganizationPlanResponse:
    """
    Attributes:
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        id (UUID): The unique ID of the entity
        plan (OrganizationPlanType): The plan type (trial, paid)
        trial_days_remaining (Union[None, Unset, int]): Days remaining in trial. Positive when active, zero or negative
            when expired. Null for non-trial plans.
    """

    date_added: datetime.datetime
    date_updated: datetime.datetime
    id: UUID
    plan: OrganizationPlanType
    trial_days_remaining: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        id = str(self.id)

        plan = self.plan.value

        trial_days_remaining: Union[None, Unset, int]
        if isinstance(self.trial_days_remaining, Unset):
            trial_days_remaining = UNSET
        else:
            trial_days_remaining = self.trial_days_remaining

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date_added": date_added,
                "date_updated": date_updated,
                "id": id,
                "plan": plan,
            }
        )
        if trial_days_remaining is not UNSET:
            field_dict["trial_days_remaining"] = trial_days_remaining

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        id = UUID(d.pop("id"))

        plan = OrganizationPlanType(d.pop("plan"))

        def _parse_trial_days_remaining(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        trial_days_remaining = _parse_trial_days_remaining(
            d.pop("trial_days_remaining", UNSET)
        )

        organization_plan_response = cls(
            date_added=date_added,
            date_updated=date_updated,
            id=id,
            plan=plan,
            trial_days_remaining=trial_days_remaining,
        )

        organization_plan_response.additional_properties = d
        return organization_plan_response

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
