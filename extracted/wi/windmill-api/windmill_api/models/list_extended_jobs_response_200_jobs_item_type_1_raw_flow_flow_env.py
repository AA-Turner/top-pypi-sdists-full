from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListExtendedJobsResponse200JobsItemType1RawFlowFlowEnv")


@_attrs_define
class ListExtendedJobsResponse200JobsItemType1RawFlowFlowEnv:
    """Environment variables available to all steps"""

    additional_properties: Dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        list_extended_jobs_response_200_jobs_item_type_1_raw_flow_flow_env = cls()

        list_extended_jobs_response_200_jobs_item_type_1_raw_flow_flow_env.additional_properties = d
        return list_extended_jobs_response_200_jobs_item_type_1_raw_flow_flow_env

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
