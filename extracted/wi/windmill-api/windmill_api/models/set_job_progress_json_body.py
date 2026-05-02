from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetJobProgressJsonBody")


@_attrs_define
class SetJobProgressJsonBody:
    """
    Attributes:
        percent (Union[Unset, int]):
        flow_job_id (Union[Unset, str]):
    """

    percent: Union[Unset, int] = UNSET
    flow_job_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        percent = self.percent
        flow_job_id = self.flow_job_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if percent is not UNSET:
            field_dict["percent"] = percent
        if flow_job_id is not UNSET:
            field_dict["flow_job_id"] = flow_job_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        percent = d.pop("percent", UNSET)

        flow_job_id = d.pop("flow_job_id", UNSET)

        set_job_progress_json_body = cls(
            percent=percent,
            flow_job_id=flow_job_id,
        )

        set_job_progress_json_body.additional_properties = d
        return set_job_progress_json_body

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
