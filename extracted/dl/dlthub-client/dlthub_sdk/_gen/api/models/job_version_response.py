from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.instance_size import InstanceSize
from ..models.job_type import JobType
from ..models.run_provider import RunProvider
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.t_job_definition import TJobDefinition


T = TypeVar("T", bound="JobVersionResponse")


@_attrs_define
class JobVersionResponse:
    """
    Attributes:
        created_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        created_by (UUID): The ID of the identity who created the job
        id (UUID): The unique ID of the entity
        job_definition (TJobDefinition): Full job definition from dlt deployment manifest
        job_definition_engine_version (int): Manifest engine version for future migration
        job_definition_hash (str): Hash of the job definition for change detection
        job_id (UUID): The ID of the job the job version belongs to
        job_ref (str): Canonical job reference, unique per workspace
        job_type (JobType | str): The type of the job: batch, interactive, or stream
        max_run_time_seconds (int): Maximum allowed run duration in seconds for this job version
        profile (str): The profile the job runs under
        provider (RunProvider | str): Run provider for runs using this job version (e.g. 'tower', 'modal', 'local')
        updated_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        version (int): The current version of the job
        default_trigger (None | str | Unset): Primary trigger string (computed from job_definition)
        deployment_module (None | str | Unset): Deployment module name (e.g. __deployment__)
        description (None | str | Unset): The description of the job
        freshness (list[str] | None | Unset): Freshness constraint strings (computed from job_definition)
        instance_size (InstanceSize | None | Unset): Instance size this version runs on; None on a provider without
            instance sizing.
        interval_end (datetime.datetime | None | Unset): Upper bound of the bounded work window (from
            job_definition.interval.end). None means no upper bound; the schedule halts once the next tick would exceed it.
        interval_start (datetime.datetime | None | Unset): Lower bound of the bounded work window (from
            job_definition.interval.start). None means the job has no bounded window.
        memory_mib (int | None | Unset): Resolved memory in MiB; None when the version has no sized hardware.
        name (None | str | Unset): Display name for the job
        pipeline_name (None | str | Unset): Pipeline name this job operates on (computed from job_definition)
        triggers (list[str] | None | Unset): Trigger strings for this job (computed from job_definition)
        vcpu (float | None | Unset): Resolved virtual CPU cores; None when the version has no sized hardware.
    """

    created_at: datetime.datetime
    created_by: UUID
    id: UUID
    job_definition: TJobDefinition
    job_definition_engine_version: int
    job_definition_hash: str
    job_id: UUID
    job_ref: str
    job_type: JobType | str
    max_run_time_seconds: int
    profile: str
    provider: RunProvider | str
    updated_at: datetime.datetime
    version: int
    default_trigger: None | str | Unset = UNSET
    deployment_module: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    freshness: list[str] | None | Unset = UNSET
    instance_size: InstanceSize | None | Unset = UNSET
    interval_end: datetime.datetime | None | Unset = UNSET
    interval_start: datetime.datetime | None | Unset = UNSET
    memory_mib: int | None | Unset = UNSET
    name: None | str | Unset = UNSET
    pipeline_name: None | str | Unset = UNSET
    triggers: list[str] | None | Unset = UNSET
    vcpu: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = str(self.created_by)

        id = str(self.id)

        job_definition = self.job_definition.to_dict()

        job_definition_engine_version = self.job_definition_engine_version

        job_definition_hash = self.job_definition_hash

        job_id = str(self.job_id)

        job_ref = self.job_ref

        job_type: str
        if isinstance(self.job_type, JobType):
            job_type = self.job_type.value
        else:
            job_type = self.job_type

        max_run_time_seconds = self.max_run_time_seconds

        profile = self.profile

        provider: str
        if isinstance(self.provider, RunProvider):
            provider = self.provider.value
        else:
            provider = self.provider

        updated_at = self.updated_at.isoformat()

        version = self.version

        default_trigger: None | str | Unset
        if isinstance(self.default_trigger, Unset):
            default_trigger = UNSET
        else:
            default_trigger = self.default_trigger

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

        freshness: list[str] | None | Unset
        if isinstance(self.freshness, Unset):
            freshness = UNSET
        elif isinstance(self.freshness, list):
            freshness = self.freshness

        else:
            freshness = self.freshness

        instance_size: None | str | Unset
        if isinstance(self.instance_size, Unset):
            instance_size = UNSET
        elif isinstance(self.instance_size, InstanceSize):
            instance_size = self.instance_size.value
        else:
            instance_size = self.instance_size

        interval_end: None | str | Unset
        if isinstance(self.interval_end, Unset):
            interval_end = UNSET
        elif isinstance(self.interval_end, datetime.datetime):
            interval_end = self.interval_end.isoformat()
        else:
            interval_end = self.interval_end

        interval_start: None | str | Unset
        if isinstance(self.interval_start, Unset):
            interval_start = UNSET
        elif isinstance(self.interval_start, datetime.datetime):
            interval_start = self.interval_start.isoformat()
        else:
            interval_start = self.interval_start

        memory_mib: int | None | Unset
        if isinstance(self.memory_mib, Unset):
            memory_mib = UNSET
        else:
            memory_mib = self.memory_mib

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        pipeline_name: None | str | Unset
        if isinstance(self.pipeline_name, Unset):
            pipeline_name = UNSET
        else:
            pipeline_name = self.pipeline_name

        triggers: list[str] | None | Unset
        if isinstance(self.triggers, Unset):
            triggers = UNSET
        elif isinstance(self.triggers, list):
            triggers = self.triggers

        else:
            triggers = self.triggers

        vcpu: float | None | Unset
        if isinstance(self.vcpu, Unset):
            vcpu = UNSET
        else:
            vcpu = self.vcpu

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by": created_by,
                "id": id,
                "job_definition": job_definition,
                "job_definition_engine_version": job_definition_engine_version,
                "job_definition_hash": job_definition_hash,
                "job_id": job_id,
                "job_ref": job_ref,
                "job_type": job_type,
                "max_run_time_seconds": max_run_time_seconds,
                "profile": profile,
                "provider": provider,
                "updated_at": updated_at,
                "version": version,
            }
        )
        if default_trigger is not UNSET:
            field_dict["default_trigger"] = default_trigger
        if deployment_module is not UNSET:
            field_dict["deployment_module"] = deployment_module
        if description is not UNSET:
            field_dict["description"] = description
        if freshness is not UNSET:
            field_dict["freshness"] = freshness
        if instance_size is not UNSET:
            field_dict["instance_size"] = instance_size
        if interval_end is not UNSET:
            field_dict["interval_end"] = interval_end
        if interval_start is not UNSET:
            field_dict["interval_start"] = interval_start
        if memory_mib is not UNSET:
            field_dict["memory_mib"] = memory_mib
        if name is not UNSET:
            field_dict["name"] = name
        if pipeline_name is not UNSET:
            field_dict["pipeline_name"] = pipeline_name
        if triggers is not UNSET:
            field_dict["triggers"] = triggers
        if vcpu is not UNSET:
            field_dict["vcpu"] = vcpu

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.t_job_definition import TJobDefinition

        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        created_by = UUID(d.pop("created_by"))

        id = UUID(d.pop("id"))

        job_definition = TJobDefinition.from_dict(d.pop("job_definition"))

        job_definition_engine_version = d.pop("job_definition_engine_version")

        job_definition_hash = d.pop("job_definition_hash")

        job_id = UUID(d.pop("job_id"))

        job_ref = d.pop("job_ref")

        def _parse_job_type(data: object) -> JobType | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_type_type_0 = JobType(data)

                return job_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobType | str, data)

        job_type = _parse_job_type(d.pop("job_type"))

        max_run_time_seconds = d.pop("max_run_time_seconds")

        profile = d.pop("profile")

        def _parse_provider(data: object) -> RunProvider | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                provider_type_0 = RunProvider(data)

                return provider_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(RunProvider | str, data)

        provider = _parse_provider(d.pop("provider"))

        updated_at = isoparse(d.pop("updated_at"))

        version = d.pop("version")

        def _parse_default_trigger(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_trigger = _parse_default_trigger(d.pop("default_trigger", UNSET))

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

        def _parse_freshness(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                freshness_type_0 = cast(list[str], data)

                return freshness_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        freshness = _parse_freshness(d.pop("freshness", UNSET))

        def _parse_instance_size(data: object) -> InstanceSize | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                instance_size_type_0 = InstanceSize(data)

                return instance_size_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(InstanceSize | None | Unset, data)

        instance_size = _parse_instance_size(d.pop("instance_size", UNSET))

        def _parse_interval_end(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                interval_end_type_0 = isoparse(data)

                return interval_end_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        interval_end = _parse_interval_end(d.pop("interval_end", UNSET))

        def _parse_interval_start(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                interval_start_type_0 = isoparse(data)

                return interval_start_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        interval_start = _parse_interval_start(d.pop("interval_start", UNSET))

        def _parse_memory_mib(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        memory_mib = _parse_memory_mib(d.pop("memory_mib", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_pipeline_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pipeline_name = _parse_pipeline_name(d.pop("pipeline_name", UNSET))

        def _parse_triggers(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                triggers_type_0 = cast(list[str], data)

                return triggers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        triggers = _parse_triggers(d.pop("triggers", UNSET))

        def _parse_vcpu(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        vcpu = _parse_vcpu(d.pop("vcpu", UNSET))

        job_version_response = cls(
            created_at=created_at,
            created_by=created_by,
            id=id,
            job_definition=job_definition,
            job_definition_engine_version=job_definition_engine_version,
            job_definition_hash=job_definition_hash,
            job_id=job_id,
            job_ref=job_ref,
            job_type=job_type,
            max_run_time_seconds=max_run_time_seconds,
            profile=profile,
            provider=provider,
            updated_at=updated_at,
            version=version,
            default_trigger=default_trigger,
            deployment_module=deployment_module,
            description=description,
            freshness=freshness,
            instance_size=instance_size,
            interval_end=interval_end,
            interval_start=interval_start,
            memory_mib=memory_mib,
            name=name,
            pipeline_name=pipeline_name,
            triggers=triggers,
            vcpu=vcpu,
        )

        job_version_response.additional_properties = d
        return job_version_response

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
