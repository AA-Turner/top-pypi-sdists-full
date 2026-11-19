from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListQueueResponse200ItemFlowStatusContinuedOnErrorItem")


@_attrs_define
class ListQueueResponse200ItemFlowStatusContinuedOnErrorItem:
    """
    Attributes:
        id (str):
        job (str):
    """

    id: str
    job: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        job = self.job

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "job": job,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        job = d.pop("job")

        list_queue_response_200_item_flow_status_continued_on_error_item = cls(
            id=id,
            job=job,
        )

        list_queue_response_200_item_flow_status_continued_on_error_item.additional_properties = d
        return list_queue_response_200_item_flow_status_continued_on_error_item

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
