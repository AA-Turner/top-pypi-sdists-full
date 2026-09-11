from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.script_type import ScriptType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.t_job_definition import TJobDefinition


T = TypeVar("T", bound="CreateScriptRequest")


@_attrs_define
class CreateScriptRequest:
    """
    Attributes:
        job_definition (TJobDefinition):
        job_definition_engine_version (int): Manifest engine version for future migration
        job_definition_hash (str): Hash of the job definition for change detection
        job_ref (str): Canonical job reference, unique per workspace
        script_type (ScriptType): The type of the script: batch, interactive, or stream
        deployment_module (None | str | Unset): Deployment module name (e.g. __deployment__)
        description (None | str | Unset): The description of the script
        name (None | str | Unset): Display name for the job
        profile (None | str | Unset): The name of the profile to use for the script
    """

    job_definition: TJobDefinition
    job_definition_engine_version: int
    job_definition_hash: str
    job_ref: str
    script_type: ScriptType
    deployment_module: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    profile: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_definition = self.job_definition.to_dict()

        job_definition_engine_version = self.job_definition_engine_version

        job_definition_hash = self.job_definition_hash

        job_ref = self.job_ref

        script_type = self.script_type.value

        deployment_module: None | str | Unset
        if isinstance(self.deployment_module, Unset):
            deployment_module = UNSET
        else:
            deployment_module = self.deployment_module

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        profile: None | str | Unset
        if isinstance(self.profile, Unset):
            profile = UNSET
        else:
            profile = self.profile

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_definition": job_definition,
                "job_definition_engine_version": job_definition_engine_version,
                "job_definition_hash": job_definition_hash,
                "job_ref": job_ref,
                "script_type": script_type,
            }
        )
        if deployment_module is not UNSET:
            field_dict["deployment_module"] = deployment_module
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.t_job_definition import TJobDefinition

        d = dict(src_dict)
        job_definition = TJobDefinition.from_dict(d.pop("job_definition"))

        job_definition_engine_version = d.pop("job_definition_engine_version")

        job_definition_hash = d.pop("job_definition_hash")

        job_ref = d.pop("job_ref")

        script_type = ScriptType(d.pop("script_type"))

        def _parse_deployment_module(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        deployment_module = _parse_deployment_module(d.pop("deployment_module", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_profile(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        profile = _parse_profile(d.pop("profile", UNSET))

        create_script_request = cls(
            job_definition=job_definition,
            job_definition_engine_version=job_definition_engine_version,
            job_definition_hash=job_definition_hash,
            job_ref=job_ref,
            script_type=script_type,
            deployment_module=deployment_module,
            description=description,
            name=name,
            profile=profile,
        )

        create_script_request.additional_properties = d
        return create_script_request

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
