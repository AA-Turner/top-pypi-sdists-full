from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CountJobsByTagResponse200Item")


@_attrs_define
class CountJobsByTagResponse200Item:
    """
    Attributes:
        tag (str):
        count (int):
    """

    tag: str
    count: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tag = self.tag
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tag": tag,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tag = d.pop("tag")

        count = d.pop("count")

        count_jobs_by_tag_response_200_item = cls(
            tag=tag,
            count=count,
        )

        count_jobs_by_tag_response_200_item.additional_properties = d
        return count_jobs_by_tag_response_200_item

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
