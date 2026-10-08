from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_type import JobType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.t_job_definition import TJobDefinition


T = TypeVar("T", bound="JobResponse")


@_attrs_define
class JobResponse:
    """The job as it stands after the deploy.

    Attributes:
        created_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        created_by (UUID): The ID of the identity who created the job
        id (UUID): The unique ID of the entity
        job_definition (TJobDefinition): Full job definition from dlt deployment manifest
        job_definition_engine_version (int): Manifest engine version for future migration
        job_definition_hash (str): Hash of the job definition for change detection
        job_ref (str): Canonical job reference, unique per workspace
        job_type (JobType | str): The type of the job: batch, interactive, or stream
        job_url (None | str): The URL where the job can be accessed if interactive
        profile (str): The profile the job runs under
        public_url (None | str): The public URL where the job can be accessed without authentication, is None if not
            enabled
        updated_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        version (int): The current version of the job
        workspace_id (UUID): The ID of the workspace the job belongs to
        default_trigger (None | str | Unset): Primary trigger string (computed from job_definition)
        deployment_module (None | str | Unset): Deployment module name (e.g. __deployment__)
        description (None | str | Unset): The description of the job
        freshness (list[str] | None | Unset): Freshness constraint strings (computed from job_definition)
        interval_end (datetime.datetime | None | Unset): Upper bound of the bounded work window (from
            job_definition.interval.end). None means no upper bound; the schedule halts once the next tick would exceed it.
        interval_start (datetime.datetime | None | Unset): Lower bound of the bounded work window (from
            job_definition.interval.start). None means the job has no bounded window.
        is_archived (bool | Unset): Whether the job is archived and hidden from default listings Default: False.
        is_paused (bool | Unset): Whether the job's scheduled runs are paused. The scheduler skips it, both on its own
            schedule and through a freshness cascade; manual runs, `trigger` and `job.success:`/`job.fail:` chains are
            unaffected. Only a job with `next_scheduled_run_at` can be paused, and losing that schedule on a deploy clears
            the pause. Default: False.
        name (None | str | Unset): Display name for the job
        next_scheduled_run_at (datetime.datetime | None | Unset): The next scheduled run of the job, is None if no
            schedule is set
        pipeline_name (None | str | Unset): Pipeline name this job operates on (computed from job_definition)
        public_secret (None | Unset | UUID): The secret UUID used to generate the public URL for this job
        triggers (list[str] | None | Unset): Trigger strings for this job (computed from job_definition)
    """

    created_at: datetime.datetime
    created_by: UUID
    id: UUID
    job_definition: TJobDefinition
    job_definition_engine_version: int
    job_definition_hash: str
    job_ref: str
    job_type: JobType | str
    job_url: None | str
    profile: str
    public_url: None | str
    updated_at: datetime.datetime
    version: int
    workspace_id: UUID
    default_trigger: None | str | Unset = UNSET
    deployment_module: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    freshness: list[str] | None | Unset = UNSET
    interval_end: datetime.datetime | None | Unset = UNSET
    interval_start: datetime.datetime | None | Unset = UNSET
    is_archived: bool | Unset = False
    is_paused: bool | Unset = False
    name: None | str | Unset = UNSET
    next_scheduled_run_at: datetime.datetime | None | Unset = UNSET
    pipeline_name: None | str | Unset = UNSET
    public_secret: None | Unset | UUID = UNSET
    triggers: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = str(self.created_by)

        id = str(self.id)

        job_definition = self.job_definition.to_dict()

        job_definition_engine_version = self.job_definition_engine_version

        job_definition_hash = self.job_definition_hash

        job_ref = self.job_ref

        job_type: str
        if isinstance(self.job_type, JobType):
            job_type = self.job_type.value
        else:
            job_type = self.job_type

        job_url: None | str
        job_url = self.job_url

        profile = self.profile

        public_url: None | str
        public_url = self.public_url

        updated_at = self.updated_at.isoformat()

        version = self.version

        workspace_id = str(self.workspace_id)

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

        is_archived = self.is_archived

        is_paused = self.is_paused

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        next_scheduled_run_at: None | str | Unset
        if isinstance(self.next_scheduled_run_at, Unset):
            next_scheduled_run_at = UNSET
        elif isinstance(self.next_scheduled_run_at, datetime.datetime):
            next_scheduled_run_at = self.next_scheduled_run_at.isoformat()
        else:
            next_scheduled_run_at = self.next_scheduled_run_at

        pipeline_name: None | str | Unset
        if isinstance(self.pipeline_name, Unset):
            pipeline_name = UNSET
        else:
            pipeline_name = self.pipeline_name

        public_secret: None | str | Unset
        if isinstance(self.public_secret, Unset):
            public_secret = UNSET
        elif isinstance(self.public_secret, UUID):
            public_secret = str(self.public_secret)
        else:
            public_secret = self.public_secret

        triggers: list[str] | None | Unset
        if isinstance(self.triggers, Unset):
            triggers = UNSET
        elif isinstance(self.triggers, list):
            triggers = self.triggers

        else:
            triggers = self.triggers

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
                "job_ref": job_ref,
                "job_type": job_type,
                "job_url": job_url,
                "profile": profile,
                "public_url": public_url,
                "updated_at": updated_at,
                "version": version,
                "workspace_id": workspace_id,
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
        if interval_end is not UNSET:
            field_dict["interval_end"] = interval_end
        if interval_start is not UNSET:
            field_dict["interval_start"] = interval_start
        if is_archived is not UNSET:
            field_dict["is_archived"] = is_archived
        if is_paused is not UNSET:
            field_dict["is_paused"] = is_paused
        if name is not UNSET:
            field_dict["name"] = name
        if next_scheduled_run_at is not UNSET:
            field_dict["next_scheduled_run_at"] = next_scheduled_run_at
        if pipeline_name is not UNSET:
            field_dict["pipeline_name"] = pipeline_name
        if public_secret is not UNSET:
            field_dict["public_secret"] = public_secret
        if triggers is not UNSET:
            field_dict["triggers"] = triggers

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

        def _parse_job_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        job_url = _parse_job_url(d.pop("job_url"))

        profile = d.pop("profile")

        def _parse_public_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        public_url = _parse_public_url(d.pop("public_url"))

        updated_at = isoparse(d.pop("updated_at"))

        version = d.pop("version")

        workspace_id = UUID(d.pop("workspace_id"))

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

        is_archived = d.pop("is_archived", UNSET)

        is_paused = d.pop("is_paused", UNSET)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_next_scheduled_run_at(
            data: object,
        ) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_scheduled_run_at_type_0 = isoparse(data)

                return next_scheduled_run_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        next_scheduled_run_at = _parse_next_scheduled_run_at(
            d.pop("next_scheduled_run_at", UNSET)
        )

        def _parse_pipeline_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pipeline_name = _parse_pipeline_name(d.pop("pipeline_name", UNSET))

        def _parse_public_secret(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                public_secret_type_0 = UUID(data)

                return public_secret_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        public_secret = _parse_public_secret(d.pop("public_secret", UNSET))

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

        job_response = cls(
            created_at=created_at,
            created_by=created_by,
            id=id,
            job_definition=job_definition,
            job_definition_engine_version=job_definition_engine_version,
            job_definition_hash=job_definition_hash,
            job_ref=job_ref,
            job_type=job_type,
            job_url=job_url,
            profile=profile,
            public_url=public_url,
            updated_at=updated_at,
            version=version,
            workspace_id=workspace_id,
            default_trigger=default_trigger,
            deployment_module=deployment_module,
            description=description,
            freshness=freshness,
            interval_end=interval_end,
            interval_start=interval_start,
            is_archived=is_archived,
            is_paused=is_paused,
            name=name,
            next_scheduled_run_at=next_scheduled_run_at,
            pipeline_name=pipeline_name,
            public_secret=public_secret,
            triggers=triggers,
        )

        job_response.additional_properties = d
        return job_response

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
