from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.message_state_cache_filter import MessageStateCacheFilter


T = TypeVar("T", bound="MessageStateCache")


@_attrs_define
class MessageStateCache:
    """
    Attributes:
        cache_ttl (int): Cache TTL in seconds
        description (str): Cache description
        filter_ (MessageStateCacheFilter):
    """

    cache_ttl: int
    description: str
    filter_: "MessageStateCacheFilter"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cache_ttl = self.cache_ttl

        description = self.description

        filter_ = self.filter_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cache_ttl": cache_ttl,
                "description": description,
                "filter": filter_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_state_cache_filter import MessageStateCacheFilter

        d = dict(src_dict)
        cache_ttl = d.pop("cache_ttl")

        description = d.pop("description")

        filter_ = MessageStateCacheFilter.from_dict(d.pop("filter"))

        message_state_cache = cls(
            cache_ttl=cache_ttl,
            description=description,
            filter_=filter_,
        )

        message_state_cache.additional_properties = d
        return message_state_cache

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
