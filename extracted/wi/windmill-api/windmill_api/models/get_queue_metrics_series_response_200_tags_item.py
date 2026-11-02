from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetQueueMetricsSeriesResponse200TagsItem")


@_attrs_define
class GetQueueMetricsSeriesResponse200TagsItem:
    """
    Attributes:
        tag (str):
        count (List[List[float]]): [epoch ms, jobs waiting more than 3 seconds] vertices
        delay (List[List[float]]): [epoch ms, seconds the next job has waited] vertices
    """

    tag: str
    count: List[List[float]]
    delay: List[List[float]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tag = self.tag
        count = []
        for count_item_data in self.count:
            count_item = count_item_data

            count.append(count_item)

        delay = []
        for delay_item_data in self.delay:
            delay_item = delay_item_data

            delay.append(delay_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tag": tag,
                "count": count,
                "delay": delay,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tag = d.pop("tag")

        count = []
        _count = d.pop("count")
        for count_item_data in _count:
            count_item = cast(List[float], count_item_data)

            count.append(count_item)

        delay = []
        _delay = d.pop("delay")
        for delay_item_data in _delay:
            delay_item = cast(List[float], delay_item_data)

            delay.append(delay_item)

        get_queue_metrics_series_response_200_tags_item = cls(
            tag=tag,
            count=count,
            delay=delay,
        )

        get_queue_metrics_series_response_200_tags_item.additional_properties = d
        return get_queue_metrics_series_response_200_tags_item

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
