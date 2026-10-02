from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherHPAMetricTargetRequest")


@_attrs_define
class RancherHPAMetricTargetRequest:
    """
    Attributes:
        type_ (str):
        utilization (Union[None, Unset, int]):
        average_value (Union[None, Unset, str]):
    """

    type_: str
    utilization: Union[None, Unset, int] = UNSET
    average_value: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        utilization: Union[None, Unset, int]
        if isinstance(self.utilization, Unset):
            utilization = UNSET
        else:
            utilization = self.utilization

        average_value: Union[None, Unset, str]
        if isinstance(self.average_value, Unset):
            average_value = UNSET
        else:
            average_value = self.average_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if utilization is not UNSET:
            field_dict["utilization"] = utilization
        if average_value is not UNSET:
            field_dict["averageValue"] = average_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        def _parse_utilization(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        utilization = _parse_utilization(d.pop("utilization", UNSET))

        def _parse_average_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        average_value = _parse_average_value(d.pop("averageValue", UNSET))

        rancher_hpa_metric_target_request = cls(
            type_=type_,
            utilization=utilization,
            average_value=average_value,
        )

        rancher_hpa_metric_target_request.additional_properties = d
        return rancher_hpa_metric_target_request

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
