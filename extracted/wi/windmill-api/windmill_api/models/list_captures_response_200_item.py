import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_captures_response_200_item_trigger_kind import ListCapturesResponse200ItemTriggerKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListCapturesResponse200Item")


@_attrs_define
class ListCapturesResponse200Item:
    """
    Attributes:
        trigger_kind (ListCapturesResponse200ItemTriggerKind):
        payload (Any):
        id (int):
        created_at (datetime.datetime):
        trigger_extra (Union[Unset, Any]):
    """

    trigger_kind: ListCapturesResponse200ItemTriggerKind
    payload: Any
    id: int
    created_at: datetime.datetime
    trigger_extra: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trigger_kind = self.trigger_kind.value

        payload = self.payload
        id = self.id
        created_at = self.created_at.isoformat()

        trigger_extra = self.trigger_extra

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trigger_kind": trigger_kind,
                "payload": payload,
                "id": id,
                "created_at": created_at,
            }
        )
        if trigger_extra is not UNSET:
            field_dict["trigger_extra"] = trigger_extra

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trigger_kind = ListCapturesResponse200ItemTriggerKind(d.pop("trigger_kind"))

        payload = d.pop("payload")

        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        trigger_extra = d.pop("trigger_extra", UNSET)

        list_captures_response_200_item = cls(
            trigger_kind=trigger_kind,
            payload=payload,
            id=id,
            created_at=created_at,
            trigger_extra=trigger_extra,
        )

        list_captures_response_200_item.additional_properties = d
        return list_captures_response_200_item

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
