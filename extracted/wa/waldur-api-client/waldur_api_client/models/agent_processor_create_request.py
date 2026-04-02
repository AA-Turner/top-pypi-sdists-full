from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentProcessorCreateRequest")


@_attrs_define
class AgentProcessorCreateRequest:
    """
    Attributes:
        name (str):
        backend_type (str): Type of the backend, for example SLURM.
        backend_version (Union[None, Unset, str]):
    """

    name: str
    backend_type: str
    backend_version: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        backend_type = self.backend_type

        backend_version: Union[None, Unset, str]
        if isinstance(self.backend_version, Unset):
            backend_version = UNSET
        else:
            backend_version = self.backend_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "backend_type": backend_type,
            }
        )
        if backend_version is not UNSET:
            field_dict["backend_version"] = backend_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        backend_type = d.pop("backend_type")

        def _parse_backend_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_version = _parse_backend_version(d.pop("backend_version", UNSET))

        agent_processor_create_request = cls(
            name=name,
            backend_type=backend_type,
            backend_version=backend_version,
        )

        agent_processor_create_request.additional_properties = d
        return agent_processor_create_request

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
