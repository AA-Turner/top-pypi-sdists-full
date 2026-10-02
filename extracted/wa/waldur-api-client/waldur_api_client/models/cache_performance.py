from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CachePerformance")


@_attrs_define
class CachePerformance:
    """
    Attributes:
        buffer_cache_hit_ratio (Union[None, float]): Buffer cache hit ratio percentage (should be >99%)
        index_hit_ratio (Union[None, float]): Index cache hit ratio percentage
        shared_buffers (str): Configured shared_buffers setting
        effective_cache_size (str): Configured effective_cache_size setting
    """

    buffer_cache_hit_ratio: Union[None, float]
    index_hit_ratio: Union[None, float]
    shared_buffers: str
    effective_cache_size: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        buffer_cache_hit_ratio: Union[None, float]
        buffer_cache_hit_ratio = self.buffer_cache_hit_ratio

        index_hit_ratio: Union[None, float]
        index_hit_ratio = self.index_hit_ratio

        shared_buffers = self.shared_buffers

        effective_cache_size = self.effective_cache_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "buffer_cache_hit_ratio": buffer_cache_hit_ratio,
                "index_hit_ratio": index_hit_ratio,
                "shared_buffers": shared_buffers,
                "effective_cache_size": effective_cache_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_buffer_cache_hit_ratio(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        buffer_cache_hit_ratio = _parse_buffer_cache_hit_ratio(d.pop("buffer_cache_hit_ratio"))

        def _parse_index_hit_ratio(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        index_hit_ratio = _parse_index_hit_ratio(d.pop("index_hit_ratio"))

        shared_buffers = d.pop("shared_buffers")

        effective_cache_size = d.pop("effective_cache_size")

        cache_performance = cls(
            buffer_cache_hit_ratio=buffer_cache_hit_ratio,
            index_hit_ratio=index_hit_ratio,
            shared_buffers=shared_buffers,
            effective_cache_size=effective_cache_size,
        )

        cache_performance.additional_properties = d
        return cache_performance

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
