from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rancher_nested_workload_request import RancherNestedWorkloadRequest
    from ..models.rancher_service_request_selector_type_0 import RancherServiceRequestSelectorType0


T = TypeVar("T", bound="RancherServiceRequest")


@_attrs_define
class RancherServiceRequest:
    """
    Attributes:
        name (str):
        target_workloads (list['RancherNestedWorkloadRequest']):
        description (Union[Unset, str]):
        cluster_ip (Union[None, Unset, str]):
        selector (Union['RancherServiceRequestSelectorType0', None, Unset]):
    """

    name: str
    target_workloads: list["RancherNestedWorkloadRequest"]
    description: Union[Unset, str] = UNSET
    cluster_ip: Union[None, Unset, str] = UNSET
    selector: Union["RancherServiceRequestSelectorType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.rancher_service_request_selector_type_0 import RancherServiceRequestSelectorType0

        name = self.name

        target_workloads = []
        for target_workloads_item_data in self.target_workloads:
            target_workloads_item = target_workloads_item_data.to_dict()
            target_workloads.append(target_workloads_item)

        description = self.description

        cluster_ip: Union[None, Unset, str]
        if isinstance(self.cluster_ip, Unset):
            cluster_ip = UNSET
        else:
            cluster_ip = self.cluster_ip

        selector: Union[None, Unset, dict[str, Any]]
        if isinstance(self.selector, Unset):
            selector = UNSET
        elif isinstance(self.selector, RancherServiceRequestSelectorType0):
            selector = self.selector.to_dict()
        else:
            selector = self.selector

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "target_workloads": target_workloads,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if cluster_ip is not UNSET:
            field_dict["cluster_ip"] = cluster_ip
        if selector is not UNSET:
            field_dict["selector"] = selector

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_nested_workload_request import RancherNestedWorkloadRequest
        from ..models.rancher_service_request_selector_type_0 import RancherServiceRequestSelectorType0

        d = dict(src_dict)
        name = d.pop("name")

        target_workloads = []
        _target_workloads = d.pop("target_workloads")
        for target_workloads_item_data in _target_workloads:
            target_workloads_item = RancherNestedWorkloadRequest.from_dict(target_workloads_item_data)

            target_workloads.append(target_workloads_item)

        description = d.pop("description", UNSET)

        def _parse_cluster_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cluster_ip = _parse_cluster_ip(d.pop("cluster_ip", UNSET))

        def _parse_selector(data: object) -> Union["RancherServiceRequestSelectorType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                selector_type_0 = RancherServiceRequestSelectorType0.from_dict(data)

                return selector_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RancherServiceRequestSelectorType0", None, Unset], data)

        selector = _parse_selector(d.pop("selector", UNSET))

        rancher_service_request = cls(
            name=name,
            target_workloads=target_workloads,
            description=description,
            cluster_ip=cluster_ip,
            selector=selector,
        )

        rancher_service_request.additional_properties = d
        return rancher_service_request

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
