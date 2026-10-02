from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rancher_hpa_metric_target_request import RancherHPAMetricTargetRequest


T = TypeVar("T", bound="RancherHPAMetricRequest")


@_attrs_define
class RancherHPAMetricRequest:
    """
    Attributes:
        name (str):
        type_ (str):
        target (RancherHPAMetricTargetRequest):
    """

    name: str
    type_: str
    target: "RancherHPAMetricTargetRequest"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_

        target = self.target.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "target": target,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_hpa_metric_target_request import RancherHPAMetricTargetRequest

        d = dict(src_dict)
        name = d.pop("name")

        type_ = d.pop("type")

        target = RancherHPAMetricTargetRequest.from_dict(d.pop("target"))

        rancher_hpa_metric_request = cls(
            name=name,
            type_=type_,
            target=target,
        )

        rancher_hpa_metric_request.additional_properties = d
        return rancher_hpa_metric_request

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
