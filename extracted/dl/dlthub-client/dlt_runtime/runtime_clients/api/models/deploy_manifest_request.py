from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.t_job_definition import TJobDefinition


T = TypeVar("T", bound="DeployManifestRequest")


@_attrs_define
class DeployManifestRequest:
    """
    Attributes:
        job_definition_engine_version (int): Manifest engine version.
        job_definition_hash (str): Content hash of the deployment manifest for change detection.
        jobs (list[TJobDefinition]): Job definitions from the deployment manifest.
        deployment_module (None | str | Unset): Deployment module name. None = ad-hoc (no archival). '__deployment__' =
            standard deploy.
        description (None | str | Unset): Workspace description (from __deployment__ docstring). Only applied when
            deployment_module='__deployment__'.
        dry_run (bool | Unset): If true, return preview of changes without persisting. Default: False.
    """

    job_definition_engine_version: int
    job_definition_hash: str
    jobs: list[TJobDefinition]
    deployment_module: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    dry_run: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_definition_engine_version = self.job_definition_engine_version

        job_definition_hash = self.job_definition_hash

        jobs = []
        for jobs_item_data in self.jobs:
            jobs_item = jobs_item_data.to_dict()
            jobs.append(jobs_item)

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

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_definition_engine_version": job_definition_engine_version,
                "job_definition_hash": job_definition_hash,
                "jobs": jobs,
            }
        )
        if deployment_module is not UNSET:
            field_dict["deployment_module"] = deployment_module
        if description is not UNSET:
            field_dict["description"] = description
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.t_job_definition import TJobDefinition

        d = dict(src_dict)
        job_definition_engine_version = d.pop("job_definition_engine_version")

        job_definition_hash = d.pop("job_definition_hash")

        jobs = []
        _jobs = d.pop("jobs")
        for jobs_item_data in _jobs:
            jobs_item = TJobDefinition.from_dict(jobs_item_data)

            jobs.append(jobs_item)

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

        dry_run = d.pop("dry_run", UNSET)

        deploy_manifest_request = cls(
            job_definition_engine_version=job_definition_engine_version,
            job_definition_hash=job_definition_hash,
            jobs=jobs,
            deployment_module=deployment_module,
            description=description,
            dry_run=dry_run,
        )

        deploy_manifest_request.additional_properties = d
        return deploy_manifest_request

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
