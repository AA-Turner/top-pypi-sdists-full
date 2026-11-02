from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetQueueStatusResponse200Item")


@_attrs_define
class GetQueueStatusResponse200Item:
    """
    Attributes:
        tag (str):
        waiting (int): jobs due for more than 3 seconds that no worker has picked up
        running (int):
        workers (int): workers that pinged in the last minute and pull this tag
        delay (Union[Unset, float]): seconds the job the next pull would take has been waiting, absent when none is
    """

    tag: str
    waiting: int
    running: int
    workers: int
    delay: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tag = self.tag
        waiting = self.waiting
        running = self.running
        workers = self.workers
        delay = self.delay

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tag": tag,
                "waiting": waiting,
                "running": running,
                "workers": workers,
            }
        )
        if delay is not UNSET:
            field_dict["delay"] = delay

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tag = d.pop("tag")

        waiting = d.pop("waiting")

        running = d.pop("running")

        workers = d.pop("workers")

        delay = d.pop("delay", UNSET)

        get_queue_status_response_200_item = cls(
            tag=tag,
            waiting=waiting,
            running=running,
            workers=workers,
            delay=delay,
        )

        get_queue_status_response_200_item.additional_properties = d
        return get_queue_status_response_200_item

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
