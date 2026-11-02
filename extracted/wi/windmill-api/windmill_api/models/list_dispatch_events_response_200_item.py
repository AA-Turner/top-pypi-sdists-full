import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_dispatch_events_response_200_item_asset_kind import ListDispatchEventsResponse200ItemAssetKind
from ..models.list_dispatch_events_response_200_item_outcome import ListDispatchEventsResponse200ItemOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListDispatchEventsResponse200Item")


@_attrs_define
class ListDispatchEventsResponse200Item:
    """
    Attributes:
        subscriber_path (str):
        asset_kind (ListDispatchEventsResponse200ItemAssetKind):
        asset_path (str):
        outcome (ListDispatchEventsResponse200ItemOutcome):
        created_at (datetime.datetime):
        child_job_id (Union[Unset, str]):
        partition (Union[Unset, str]):
        received_inputs (Union[Unset, int]):
        required_inputs (Union[Unset, int]):
        debounce_s (Union[Unset, int]):
        reason (Union[Unset, str]):
    """

    subscriber_path: str
    asset_kind: ListDispatchEventsResponse200ItemAssetKind
    asset_path: str
    outcome: ListDispatchEventsResponse200ItemOutcome
    created_at: datetime.datetime
    child_job_id: Union[Unset, str] = UNSET
    partition: Union[Unset, str] = UNSET
    received_inputs: Union[Unset, int] = UNSET
    required_inputs: Union[Unset, int] = UNSET
    debounce_s: Union[Unset, int] = UNSET
    reason: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subscriber_path = self.subscriber_path
        asset_kind = self.asset_kind.value

        asset_path = self.asset_path
        outcome = self.outcome.value

        created_at = self.created_at.isoformat()

        child_job_id = self.child_job_id
        partition = self.partition
        received_inputs = self.received_inputs
        required_inputs = self.required_inputs
        debounce_s = self.debounce_s
        reason = self.reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subscriber_path": subscriber_path,
                "asset_kind": asset_kind,
                "asset_path": asset_path,
                "outcome": outcome,
                "created_at": created_at,
            }
        )
        if child_job_id is not UNSET:
            field_dict["child_job_id"] = child_job_id
        if partition is not UNSET:
            field_dict["partition"] = partition
        if received_inputs is not UNSET:
            field_dict["received_inputs"] = received_inputs
        if required_inputs is not UNSET:
            field_dict["required_inputs"] = required_inputs
        if debounce_s is not UNSET:
            field_dict["debounce_s"] = debounce_s
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subscriber_path = d.pop("subscriber_path")

        asset_kind = ListDispatchEventsResponse200ItemAssetKind(d.pop("asset_kind"))

        asset_path = d.pop("asset_path")

        outcome = ListDispatchEventsResponse200ItemOutcome(d.pop("outcome"))

        created_at = isoparse(d.pop("created_at"))

        child_job_id = d.pop("child_job_id", UNSET)

        partition = d.pop("partition", UNSET)

        received_inputs = d.pop("received_inputs", UNSET)

        required_inputs = d.pop("required_inputs", UNSET)

        debounce_s = d.pop("debounce_s", UNSET)

        reason = d.pop("reason", UNSET)

        list_dispatch_events_response_200_item = cls(
            subscriber_path=subscriber_path,
            asset_kind=asset_kind,
            asset_path=asset_path,
            outcome=outcome,
            created_at=created_at,
            child_job_id=child_job_id,
            partition=partition,
            received_inputs=received_inputs,
            required_inputs=required_inputs,
            debounce_s=debounce_s,
            reason=reason,
        )

        list_dispatch_events_response_200_item.additional_properties = d
        return list_dispatch_events_response_200_item

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
