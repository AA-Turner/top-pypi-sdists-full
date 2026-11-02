from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_queue_metrics_response_200_item_values_item import GetQueueMetricsResponse200ItemValuesItem


T = TypeVar("T", bound="GetQueueMetricsResponse200Item")


@_attrs_define
class GetQueueMetricsResponse200Item:
    """
    Attributes:
        id (str):
        values (List['GetQueueMetricsResponse200ItemValuesItem']):
    """

    id: str
    values: List["GetQueueMetricsResponse200ItemValuesItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        values = []
        for values_item_data in self.values:
            values_item = values_item_data.to_dict()

            values.append(values_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_queue_metrics_response_200_item_values_item import GetQueueMetricsResponse200ItemValuesItem

        d = src_dict.copy()
        id = d.pop("id")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = GetQueueMetricsResponse200ItemValuesItem.from_dict(values_item_data)

            values.append(values_item)

        get_queue_metrics_response_200_item = cls(
            id=id,
            values=values,
        )

        get_queue_metrics_response_200_item.additional_properties = d
        return get_queue_metrics_response_200_item

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
