from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedOpenStackPoolRequest")


@_attrs_define
class PatchedOpenStackPoolRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        service_settings (Union[Unset, str]):
        project (Union[Unset, str]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        backend_id (Union[None, Unset, str]): Pool ID in Octavia
        load_balancer (Union[Unset, str]): Load balancer this pool belongs to
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    service_settings: Union[Unset, str] = UNSET
    project: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    backend_id: Union[None, Unset, str] = UNSET
    load_balancer: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        service_settings = self.service_settings

        project = self.project

        error_message = self.error_message

        error_traceback = self.error_traceback

        backend_id: Union[None, Unset, str]
        if isinstance(self.backend_id, Unset):
            backend_id = UNSET
        else:
            backend_id = self.backend_id

        load_balancer = self.load_balancer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if service_settings is not UNSET:
            field_dict["service_settings"] = service_settings
        if project is not UNSET:
            field_dict["project"] = project
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if load_balancer is not UNSET:
            field_dict["load_balancer"] = load_balancer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        service_settings = d.pop("service_settings", UNSET)

        project = d.pop("project", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        def _parse_backend_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id", UNSET))

        load_balancer = d.pop("load_balancer", UNSET)

        patched_open_stack_pool_request = cls(
            name=name,
            description=description,
            service_settings=service_settings,
            project=project,
            error_message=error_message,
            error_traceback=error_traceback,
            backend_id=backend_id,
            load_balancer=load_balancer,
        )

        patched_open_stack_pool_request.additional_properties = d
        return patched_open_stack_pool_request

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
