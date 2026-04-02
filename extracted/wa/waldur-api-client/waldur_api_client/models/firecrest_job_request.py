from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="FirecrestJobRequest")


@_attrs_define
class FirecrestJobRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        file (File):
        description (Union[Unset, str]):
        runtime_state (Union[Unset, str]):
    """

    name: str
    service_settings: str
    project: str
    file: File
    description: Union[Unset, str] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        file = self.file.to_tuple()

        description = self.description

        runtime_state = self.runtime_state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
                "file": file,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        file = File(payload=BytesIO(d.pop("file")))

        description = d.pop("description", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        firecrest_job_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            file=file,
            description=description,
            runtime_state=runtime_state,
        )

        firecrest_job_request.additional_properties = d
        return firecrest_job_request

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
