from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_queue_metrics_series_response_200_tags_item import GetQueueMetricsSeriesResponse200TagsItem


T = TypeVar("T", bound="GetQueueMetricsSeriesResponse200")


@_attrs_define
class GetQueueMetricsSeriesResponse200:
    """
    Attributes:
        from_ (int): start of the window, in epoch milliseconds
        to (int): end of the window, in epoch milliseconds
        tags (List['GetQueueMetricsSeriesResponse200TagsItem']):
    """

    from_: int
    to: int
    tags: List["GetQueueMetricsSeriesResponse200TagsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from_ = self.from_
        to = self.to
        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()

            tags.append(tags_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
                "tags": tags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_queue_metrics_series_response_200_tags_item import GetQueueMetricsSeriesResponse200TagsItem

        d = src_dict.copy()
        from_ = d.pop("from")

        to = d.pop("to")

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = GetQueueMetricsSeriesResponse200TagsItem.from_dict(tags_item_data)

            tags.append(tags_item)

        get_queue_metrics_series_response_200 = cls(
            from_=from_,
            to=to,
            tags=tags,
        )

        get_queue_metrics_series_response_200.additional_properties = d
        return get_queue_metrics_series_response_200

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
