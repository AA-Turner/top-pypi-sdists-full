from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.create_runtime_image_build_request_architecture import (
    CreateRuntimeImageBuildRequestArchitecture,
)

T = TypeVar("T", bound="CreateRuntimeImageBuildRequest")


@_attrs_define
class CreateRuntimeImageBuildRequest:
    """
    Attributes:
        name (str):
        dockerfile (str):
        architecture (CreateRuntimeImageBuildRequestArchitecture):  Default:
            CreateRuntimeImageBuildRequestArchitecture.X86_64.
    """

    name: str
    dockerfile: str
    architecture: CreateRuntimeImageBuildRequestArchitecture = (
        CreateRuntimeImageBuildRequestArchitecture.X86_64
    )

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        dockerfile = self.dockerfile

        architecture = self.architecture.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "dockerfile": dockerfile,
                "architecture": architecture,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        dockerfile = d.pop("dockerfile")

        architecture = CreateRuntimeImageBuildRequestArchitecture(d.pop("architecture"))

        create_runtime_image_build_request = cls(
            name=name,
            dockerfile=dockerfile,
            architecture=architecture,
        )

        return create_runtime_image_build_request
