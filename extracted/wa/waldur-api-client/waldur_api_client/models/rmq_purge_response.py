from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RmqPurgeResponse")


@_attrs_define
class RmqPurgeResponse:
    """
    Attributes:
        purged_queues (int): Number of queues that were purged
        purged_messages (int): Total number of messages that were purged
        deleted_queues (int): Number of queues that were deleted
    """

    purged_queues: int
    purged_messages: int
    deleted_queues: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        purged_queues = self.purged_queues

        purged_messages = self.purged_messages

        deleted_queues = self.deleted_queues

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "purged_queues": purged_queues,
                "purged_messages": purged_messages,
                "deleted_queues": deleted_queues,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        purged_queues = d.pop("purged_queues")

        purged_messages = d.pop("purged_messages")

        deleted_queues = d.pop("deleted_queues")

        rmq_purge_response = cls(
            purged_queues=purged_queues,
            purged_messages=purged_messages,
            deleted_queues=deleted_queues,
        )

        rmq_purge_response.additional_properties = d
        return rmq_purge_response

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
