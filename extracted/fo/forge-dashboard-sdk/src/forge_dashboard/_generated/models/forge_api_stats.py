from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.forge_api_bucket import ForgeApiBucket
  from ..models.forge_api_budget import ForgeApiBudget





T = TypeVar("T", bound="ForgeApiStats")



@_attrs_define
class ForgeApiStats:
    """ 
        Attributes:
            since (datetime.datetime): When counting began, which is when the server last started.
            buckets (list[ForgeApiBucket]): One row per forge, credential, kind and repository that made a request, ordered
                by forge, credential, kind and repo.
            budgets (list[ForgeApiBudget]): The rate limits each forge last reported, one row per forge.
     """

    since: datetime.datetime
    buckets: list[ForgeApiBucket]
    budgets: list[ForgeApiBudget]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.forge_api_bucket import ForgeApiBucket # noqa: PLC0415
        from ..models.forge_api_budget import ForgeApiBudget # noqa: PLC0415
        since = self.since.isoformat()

        buckets = []
        for buckets_item_data in self.buckets:
            buckets_item = buckets_item_data.to_dict()
            buckets.append(buckets_item)



        budgets = []
        for budgets_item_data in self.budgets:
            budgets_item = budgets_item_data.to_dict()
            budgets.append(budgets_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "since": since,
            "buckets": buckets,
            "budgets": budgets,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forge_api_bucket import ForgeApiBucket # noqa: PLC0415
        from ..models.forge_api_budget import ForgeApiBudget # noqa: PLC0415
        d = dict(src_dict)
        since = datetime.datetime.fromisoformat(d.pop("since"))




        buckets = []
        _buckets = d.pop("buckets")
        for buckets_item_data in (_buckets):
            buckets_item = ForgeApiBucket.from_dict(buckets_item_data)



            buckets.append(buckets_item)


        budgets = []
        _budgets = d.pop("budgets")
        for budgets_item_data in (_budgets):
            budgets_item = ForgeApiBudget.from_dict(budgets_item_data)



            budgets.append(budgets_item)


        forge_api_stats = cls(
            since=since,
            buckets=buckets,
            budgets=budgets,
        )


        forge_api_stats.additional_properties = d
        return forge_api_stats

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
