from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackLoadBalancerRequest")


@_attrs_define
class OpenStackLoadBalancerRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        tenant (str): OpenStack tenant this load balancer belongs to
        description (Union[Unset, str]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        backend_id (Union[None, Unset, str]): Load balancer ID in Octavia
        attached_floating_ip (Union[None, Unset, str]): Floating IP attached to the VIP port
    """

    name: str
    service_settings: str
    project: str
    tenant: str
    description: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    backend_id: Union[None, Unset, str] = UNSET
    attached_floating_ip: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        tenant = self.tenant

        description = self.description

        error_message = self.error_message

        error_traceback = self.error_traceback

        backend_id: Union[None, Unset, str]
        if isinstance(self.backend_id, Unset):
            backend_id = UNSET
        else:
            backend_id = self.backend_id

        attached_floating_ip: Union[None, Unset, str]
        if isinstance(self.attached_floating_ip, Unset):
            attached_floating_ip = UNSET
        else:
            attached_floating_ip = self.attached_floating_ip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
                "tenant": tenant,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if attached_floating_ip is not UNSET:
            field_dict["attached_floating_ip"] = attached_floating_ip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        tenant = d.pop("tenant")

        description = d.pop("description", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        def _parse_backend_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id", UNSET))

        def _parse_attached_floating_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        attached_floating_ip = _parse_attached_floating_ip(d.pop("attached_floating_ip", UNSET))

        open_stack_load_balancer_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            tenant=tenant,
            description=description,
            error_message=error_message,
            error_traceback=error_traceback,
            backend_id=backend_id,
            attached_floating_ip=attached_floating_ip,
        )

        open_stack_load_balancer_request.additional_properties = d
        return open_stack_load_balancer_request

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
