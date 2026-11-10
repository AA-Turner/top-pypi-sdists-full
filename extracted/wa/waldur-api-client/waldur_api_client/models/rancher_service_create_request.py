from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rancher_service_create_request_selector_type_0 import RancherServiceCreateRequestSelectorType0
    from ..models.rancher_workload_create_request import RancherWorkloadCreateRequest


T = TypeVar("T", bound="RancherServiceCreateRequest")


@_attrs_define
class RancherServiceCreateRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        description (Union[Unset, str]):
        namespace (Union[Unset, str]):
        cluster_ip (Union[None, Unset, str]):
        selector (Union['RancherServiceCreateRequestSelectorType0', None, Unset]):
        target_workloads (Union[Unset, list['RancherWorkloadCreateRequest']]):
    """

    name: str
    service_settings: str
    project: str
    description: Union[Unset, str] = UNSET
    namespace: Union[Unset, str] = UNSET
    cluster_ip: Union[None, Unset, str] = UNSET
    selector: Union["RancherServiceCreateRequestSelectorType0", None, Unset] = UNSET
    target_workloads: Union[Unset, list["RancherWorkloadCreateRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.rancher_service_create_request_selector_type_0 import RancherServiceCreateRequestSelectorType0

        name = self.name

        service_settings = self.service_settings

        project = self.project

        description = self.description

        namespace = self.namespace

        cluster_ip: Union[None, Unset, str]
        if isinstance(self.cluster_ip, Unset):
            cluster_ip = UNSET
        else:
            cluster_ip = self.cluster_ip

        selector: Union[None, Unset, dict[str, Any]]
        if isinstance(self.selector, Unset):
            selector = UNSET
        elif isinstance(self.selector, RancherServiceCreateRequestSelectorType0):
            selector = self.selector.to_dict()
        else:
            selector = self.selector

        target_workloads: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.target_workloads, Unset):
            target_workloads = []
            for target_workloads_item_data in self.target_workloads:
                target_workloads_item = target_workloads_item_data.to_dict()
                target_workloads.append(target_workloads_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if cluster_ip is not UNSET:
            field_dict["cluster_ip"] = cluster_ip
        if selector is not UNSET:
            field_dict["selector"] = selector
        if target_workloads is not UNSET:
            field_dict["target_workloads"] = target_workloads

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_service_create_request_selector_type_0 import RancherServiceCreateRequestSelectorType0
        from ..models.rancher_workload_create_request import RancherWorkloadCreateRequest

        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        description = d.pop("description", UNSET)

        namespace = d.pop("namespace", UNSET)

        def _parse_cluster_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cluster_ip = _parse_cluster_ip(d.pop("cluster_ip", UNSET))

        def _parse_selector(data: object) -> Union["RancherServiceCreateRequestSelectorType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                selector_type_0 = RancherServiceCreateRequestSelectorType0.from_dict(data)

                return selector_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RancherServiceCreateRequestSelectorType0", None, Unset], data)

        selector = _parse_selector(d.pop("selector", UNSET))

        target_workloads = []
        _target_workloads = d.pop("target_workloads", UNSET)
        for target_workloads_item_data in _target_workloads or []:
            target_workloads_item = RancherWorkloadCreateRequest.from_dict(target_workloads_item_data)

            target_workloads.append(target_workloads_item)

        rancher_service_create_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            description=description,
            namespace=namespace,
            cluster_ip=cluster_ip,
            selector=selector,
            target_workloads=target_workloads,
        )

        rancher_service_create_request.additional_properties = d
        return rancher_service_create_request

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
