from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_ai_usage_response_200_buckets_item import ListAiUsageResponse200BucketsItem


T = TypeVar("T", bound="ListAiUsageResponse200")


@_attrs_define
class ListAiUsageResponse200:
    """
    Attributes:
        buckets (List['ListAiUsageResponse200BucketsItem']):
        truncated (bool): more buckets matched than were returned, so summing them under-reports
    """

    buckets: List["ListAiUsageResponse200BucketsItem"]
    truncated: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        buckets = []
        for buckets_item_data in self.buckets:
            buckets_item = buckets_item_data.to_dict()

            buckets.append(buckets_item)

        truncated = self.truncated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "buckets": buckets,
                "truncated": truncated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_ai_usage_response_200_buckets_item import ListAiUsageResponse200BucketsItem

        d = src_dict.copy()
        buckets = []
        _buckets = d.pop("buckets")
        for buckets_item_data in _buckets:
            buckets_item = ListAiUsageResponse200BucketsItem.from_dict(buckets_item_data)

            buckets.append(buckets_item)

        truncated = d.pop("truncated")

        list_ai_usage_response_200 = cls(
            buckets=buckets,
            truncated=truncated,
        )

        list_ai_usage_response_200.additional_properties = d
        return list_ai_usage_response_200

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
