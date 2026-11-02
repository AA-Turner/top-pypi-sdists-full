from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetJobResponse200Type1FlowStatusPreprocessorModuleFlowJobsDuration")


@_attrs_define
class GetJobResponse200Type1FlowStatusPreprocessorModuleFlowJobsDuration:
    """
    Attributes:
        started_at (Union[Unset, List[str]]):
        duration_ms (Union[Unset, List[int]]):
    """

    started_at: Union[Unset, List[str]] = UNSET
    duration_ms: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        started_at: Union[Unset, List[str]] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at

        duration_ms: Union[Unset, List[int]] = UNSET
        if not isinstance(self.duration_ms, Unset):
            duration_ms = self.duration_ms

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        started_at = cast(List[str], d.pop("started_at", UNSET))

        duration_ms = cast(List[int], d.pop("duration_ms", UNSET))

        get_job_response_200_type_1_flow_status_preprocessor_module_flow_jobs_duration = cls(
            started_at=started_at,
            duration_ms=duration_ms,
        )

        get_job_response_200_type_1_flow_status_preprocessor_module_flow_jobs_duration.additional_properties = d
        return get_job_response_200_type_1_flow_status_preprocessor_module_flow_jobs_duration

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
