from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BackendMetadata")


@_attrs_define
class BackendMetadata:
    """
    Attributes:
        state (Union[Unset, str]): Backend resource state
        runtime_state (Union[Unset, str]): Runtime state of the backend resource
        action (Union[Unset, str]): Current action being performed
        instance_name (Union[None, Unset, str]): Name of the backend instance
    """

    state: Union[Unset, str] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    action: Union[Unset, str] = UNSET
    instance_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state

        runtime_state = self.runtime_state

        action = self.action

        instance_name: Union[None, Unset, str]
        if isinstance(self.instance_name, Unset):
            instance_name = UNSET
        else:
            instance_name = self.instance_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state is not UNSET:
            field_dict["state"] = state
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if action is not UNSET:
            field_dict["action"] = action
        if instance_name is not UNSET:
            field_dict["instance_name"] = instance_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = d.pop("state", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        action = d.pop("action", UNSET)

        def _parse_instance_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instance_name = _parse_instance_name(d.pop("instance_name", UNSET))

        backend_metadata = cls(
            state=state,
            runtime_state=runtime_state,
            action=action,
            instance_name=instance_name,
        )

        backend_metadata.additional_properties = d
        return backend_metadata

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
