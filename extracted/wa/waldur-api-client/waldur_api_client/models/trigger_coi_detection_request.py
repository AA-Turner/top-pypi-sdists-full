from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.trigger_coi_detection_job_type_enum import TriggerCOIDetectionJobTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="TriggerCOIDetectionRequest")


@_attrs_define
class TriggerCOIDetectionRequest:
    """
    Attributes:
        job_type (Union[Unset, TriggerCOIDetectionJobTypeEnum]):  Default: TriggerCOIDetectionJobTypeEnum.FULL_CALL.
    """

    job_type: Union[Unset, TriggerCOIDetectionJobTypeEnum] = TriggerCOIDetectionJobTypeEnum.FULL_CALL
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_type: Union[Unset, str] = UNSET
        if not isinstance(self.job_type, Unset):
            job_type = self.job_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_type is not UNSET:
            field_dict["job_type"] = job_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _job_type = d.pop("job_type", UNSET)
        job_type: Union[Unset, TriggerCOIDetectionJobTypeEnum]
        if isinstance(_job_type, Unset):
            job_type = UNSET
        else:
            job_type = TriggerCOIDetectionJobTypeEnum(_job_type)

        trigger_coi_detection_request = cls(
            job_type=job_type,
        )

        trigger_coi_detection_request.additional_properties = d
        return trigger_coi_detection_request

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
