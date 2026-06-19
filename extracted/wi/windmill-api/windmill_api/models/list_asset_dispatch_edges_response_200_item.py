import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_asset_dispatch_edges_response_200_item_asset_kind import (
    ListAssetDispatchEdgesResponse200ItemAssetKind,
)
from ..models.list_asset_dispatch_edges_response_200_item_outcome import ListAssetDispatchEdgesResponse200ItemOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAssetDispatchEdgesResponse200Item")


@_attrs_define
class ListAssetDispatchEdgesResponse200Item:
    """
    Attributes:
        producer_job_id (str):
        subscriber_path (str):
        outcome (ListAssetDispatchEdgesResponse200ItemOutcome):
        asset_kind (ListAssetDispatchEdgesResponse200ItemAssetKind):
        asset_path (str):
        created_at (datetime.datetime):
        child_job_id (Union[Unset, str]): Set for `dispatched`; absent for `join_pending` inputs.
    """

    producer_job_id: str
    subscriber_path: str
    outcome: ListAssetDispatchEdgesResponse200ItemOutcome
    asset_kind: ListAssetDispatchEdgesResponse200ItemAssetKind
    asset_path: str
    created_at: datetime.datetime
    child_job_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        producer_job_id = self.producer_job_id
        subscriber_path = self.subscriber_path
        outcome = self.outcome.value

        asset_kind = self.asset_kind.value

        asset_path = self.asset_path
        created_at = self.created_at.isoformat()

        child_job_id = self.child_job_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "producer_job_id": producer_job_id,
                "subscriber_path": subscriber_path,
                "outcome": outcome,
                "asset_kind": asset_kind,
                "asset_path": asset_path,
                "created_at": created_at,
            }
        )
        if child_job_id is not UNSET:
            field_dict["child_job_id"] = child_job_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        producer_job_id = d.pop("producer_job_id")

        subscriber_path = d.pop("subscriber_path")

        outcome = ListAssetDispatchEdgesResponse200ItemOutcome(d.pop("outcome"))

        asset_kind = ListAssetDispatchEdgesResponse200ItemAssetKind(d.pop("asset_kind"))

        asset_path = d.pop("asset_path")

        created_at = isoparse(d.pop("created_at"))

        child_job_id = d.pop("child_job_id", UNSET)

        list_asset_dispatch_edges_response_200_item = cls(
            producer_job_id=producer_job_id,
            subscriber_path=subscriber_path,
            outcome=outcome,
            asset_kind=asset_kind,
            asset_path=asset_path,
            created_at=created_at,
            child_job_id=child_job_id,
        )

        list_asset_dispatch_edges_response_200_item.additional_properties = d
        return list_asset_dispatch_edges_response_200_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
