from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RmqPurgeRequestRequest")


@_attrs_define
class RmqPurgeRequestRequest:
    """
    Attributes:
        vhost (Union[Unset, str]): Virtual host name containing the queue(s)
        queue_name (Union[Unset, str]): Specific queue name (requires vhost)
        queue_pattern (Union[Unset, str]): Glob pattern to match queue names (e.g., '*_resource'). Requires vhost.
        purge_all_subscription_queues (Union[Unset, bool]): If true, purge all subscription queues across all vhosts
            Default: False.
        delete_queue (Union[Unset, bool]): If true, delete the queue(s) entirely instead of just purging messages
            Default: False.
        delete_all_subscription_queues (Union[Unset, bool]): If true, delete all subscription queues across all vhosts
            Default: False.
    """

    vhost: Union[Unset, str] = UNSET
    queue_name: Union[Unset, str] = UNSET
    queue_pattern: Union[Unset, str] = UNSET
    purge_all_subscription_queues: Union[Unset, bool] = False
    delete_queue: Union[Unset, bool] = False
    delete_all_subscription_queues: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vhost = self.vhost

        queue_name = self.queue_name

        queue_pattern = self.queue_pattern

        purge_all_subscription_queues = self.purge_all_subscription_queues

        delete_queue = self.delete_queue

        delete_all_subscription_queues = self.delete_all_subscription_queues

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if vhost is not UNSET:
            field_dict["vhost"] = vhost
        if queue_name is not UNSET:
            field_dict["queue_name"] = queue_name
        if queue_pattern is not UNSET:
            field_dict["queue_pattern"] = queue_pattern
        if purge_all_subscription_queues is not UNSET:
            field_dict["purge_all_subscription_queues"] = purge_all_subscription_queues
        if delete_queue is not UNSET:
            field_dict["delete_queue"] = delete_queue
        if delete_all_subscription_queues is not UNSET:
            field_dict["delete_all_subscription_queues"] = delete_all_subscription_queues

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vhost = d.pop("vhost", UNSET)

        queue_name = d.pop("queue_name", UNSET)

        queue_pattern = d.pop("queue_pattern", UNSET)

        purge_all_subscription_queues = d.pop("purge_all_subscription_queues", UNSET)

        delete_queue = d.pop("delete_queue", UNSET)

        delete_all_subscription_queues = d.pop("delete_all_subscription_queues", UNSET)

        rmq_purge_request_request = cls(
            vhost=vhost,
            queue_name=queue_name,
            queue_pattern=queue_pattern,
            purge_all_subscription_queues=purge_all_subscription_queues,
            delete_queue=delete_queue,
            delete_all_subscription_queues=delete_all_subscription_queues,
        )

        rmq_purge_request_request.additional_properties = d
        return rmq_purge_request_request

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
