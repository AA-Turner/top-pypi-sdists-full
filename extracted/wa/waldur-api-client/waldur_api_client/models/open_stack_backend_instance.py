import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackBackendInstance")


@_attrs_define
class OpenStackBackendInstance:
    """
    Attributes:
        name (str):
        state (str):
        created (datetime.datetime):
        availability_zone (str):
        key_name (Union[Unset, str]):
        start_time (Union[None, Unset, datetime.datetime]):
        runtime_state (Union[Unset, str]):
        backend_id (Union[None, Unset, str]): Instance ID in the OpenStack backend
        hypervisor_hostname (Union[Unset, str]): Name of the hypervisor hosting this instance
    """

    name: str
    state: str
    created: datetime.datetime
    availability_zone: str
    key_name: Union[Unset, str] = UNSET
    start_time: Union[None, Unset, datetime.datetime] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    backend_id: Union[None, Unset, str] = UNSET
    hypervisor_hostname: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        state = self.state

        created = self.created.isoformat()

        availability_zone = self.availability_zone

        key_name = self.key_name

        start_time: Union[None, Unset, str]
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        runtime_state = self.runtime_state

        backend_id: Union[None, Unset, str]
        if isinstance(self.backend_id, Unset):
            backend_id = UNSET
        else:
            backend_id = self.backend_id

        hypervisor_hostname = self.hypervisor_hostname

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "state": state,
                "created": created,
                "availability_zone": availability_zone,
            }
        )
        if key_name is not UNSET:
            field_dict["key_name"] = key_name
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if hypervisor_hostname is not UNSET:
            field_dict["hypervisor_hostname"] = hypervisor_hostname

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        state = d.pop("state")

        created = isoparse(d.pop("created"))

        availability_zone = d.pop("availability_zone")

        key_name = d.pop("key_name", UNSET)

        def _parse_start_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        runtime_state = d.pop("runtime_state", UNSET)

        def _parse_backend_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id", UNSET))

        hypervisor_hostname = d.pop("hypervisor_hostname", UNSET)

        open_stack_backend_instance = cls(
            name=name,
            state=state,
            created=created,
            availability_zone=availability_zone,
            key_name=key_name,
            start_time=start_time,
            runtime_state=runtime_state,
            backend_id=backend_id,
            hypervisor_hostname=hypervisor_hostname,
        )

        open_stack_backend_instance.additional_properties = d
        return open_stack_backend_instance

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
