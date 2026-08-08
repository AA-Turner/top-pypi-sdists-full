from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.script_type import ScriptType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_response import RunResponse
    from ..models.script_version_response import ScriptVersionResponse
    from ..models.t_job_definition import TJobDefinition


T = TypeVar("T", bound="DetailedScriptResponse")


@_attrs_define
class DetailedScriptResponse:
    """
    Attributes:
        created_by (UUID): The ID of the identity who created the script
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        id (UUID): The unique ID of the entity
        job_definition (TJobDefinition):
        job_definition_engine_version (int): Manifest engine version for future migration
        job_definition_hash (str): Hash of the job definition for change detection
        job_ref (str): Canonical job reference, unique per workspace
        profile (str): The profile the script runs under
        public_url (None | str): The public URL where the script can be accessed without authentication, is None if not
            enabled
        script_type (ScriptType): The type of the script: batch, interactive, or stream
        script_url (None | str): The URL where the script can be accessed if interactive
        version (int): The current version of the script
        workspace_id (UUID): The ID of the workspace the script belongs to
        archived (bool | Unset): Whether the script is archived and hidden from default listings Default: False.
        current_version (None | ScriptVersionResponse | Unset): The active script version, carrying its provider,
            instance size, and resolved hardware.
        default_trigger (None | str | Unset): Primary trigger string (computed from job_definition)
        deployment_module (None | str | Unset): Deployment module name (e.g. __deployment__)
        description (None | str | Unset): The description of the script
        freshness (list[str] | None | Unset): Freshness constraint strings (computed from job_definition)
        interval_end (datetime.datetime | None | Unset): Upper bound of the bounded work window (from
            job_definition.interval.end). None means no upper bound; the schedule halts once the next tick would exceed it.
        interval_start (datetime.datetime | None | Unset): Lower bound of the bounded work window (from
            job_definition.interval.start). None means the job has no bounded window.
        last_run (None | RunResponse | Unset): The last run of the script, is None if no run has been made
        name (None | str | Unset): Display name for the job
        next_scheduled_run (datetime.datetime | None | Unset): The next scheduled run of the script, is None if no
            schedule is set
        paused (bool | Unset): Whether the job's scheduled runs are paused. The scheduler skips it, both on its own
            schedule and through a freshness cascade; manual runs, `trigger` and `job.success:`/`job.fail:` chains are
            unaffected. Only a job with `next_scheduled_run` can be paused, and losing that schedule on a deploy clears the
            pause. Default: False.
        pipeline_name (None | str | Unset): Pipeline name this job operates on (computed from job_definition)
        public_secret (None | Unset | UUID): The secret UUID used to generate the public URL for this script
        triggers (list[str] | None | Unset): Trigger strings for this job (computed from job_definition)
    """

    created_by: UUID
    date_added: datetime.datetime
    date_updated: datetime.datetime
    id: UUID
    job_definition: TJobDefinition
    job_definition_engine_version: int
    job_definition_hash: str
    job_ref: str
    profile: str
    public_url: None | str
    script_type: ScriptType
    script_url: None | str
    version: int
    workspace_id: UUID
    archived: bool | Unset = False
    current_version: None | ScriptVersionResponse | Unset = UNSET
    default_trigger: None | str | Unset = UNSET
    deployment_module: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    freshness: list[str] | None | Unset = UNSET
    interval_end: datetime.datetime | None | Unset = UNSET
    interval_start: datetime.datetime | None | Unset = UNSET
    last_run: None | RunResponse | Unset = UNSET
    name: None | str | Unset = UNSET
    next_scheduled_run: datetime.datetime | None | Unset = UNSET
    paused: bool | Unset = False
    pipeline_name: None | str | Unset = UNSET
    public_secret: None | Unset | UUID = UNSET
    triggers: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.run_response import RunResponse
        from ..models.script_version_response import ScriptVersionResponse

        created_by = str(self.created_by)

        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        id = str(self.id)

        job_definition = self.job_definition.to_dict()

        job_definition_engine_version = self.job_definition_engine_version

        job_definition_hash = self.job_definition_hash

        job_ref = self.job_ref

        profile = self.profile

        public_url: None | str
        public_url = self.public_url

        script_type = self.script_type.value

        script_url: None | str
        script_url = self.script_url

        version = self.version

        workspace_id = str(self.workspace_id)

        archived = self.archived

        current_version: dict[str, Any] | None | Unset
        if isinstance(self.current_version, Unset):
            current_version = UNSET
        elif isinstance(self.current_version, ScriptVersionResponse):
            current_version = self.current_version.to_dict()
        else:
            current_version = self.current_version

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

        last_run: dict[str, Any] | None | Unset
        if isinstance(self.last_run, Unset):
            last_run = UNSET
        elif isinstance(self.last_run, RunResponse):
            last_run = self.last_run.to_dict()
        else:
            last_run = self.last_run

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        next_scheduled_run: None | str | Unset
        if isinstance(self.next_scheduled_run, Unset):
            next_scheduled_run = UNSET
        elif isinstance(self.next_scheduled_run, datetime.datetime):
            next_scheduled_run = self.next_scheduled_run.isoformat()
        else:
            next_scheduled_run = self.next_scheduled_run

        paused = self.paused

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
                "created_by": created_by,
                "date_added": date_added,
                "date_updated": date_updated,
                "id": id,
                "job_definition": job_definition,
                "job_definition_engine_version": job_definition_engine_version,
                "job_definition_hash": job_definition_hash,
                "job_ref": job_ref,
                "profile": profile,
                "public_url": public_url,
                "script_type": script_type,
                "script_url": script_url,
                "version": version,
                "workspace_id": workspace_id,
            }
        )
        if archived is not UNSET:
            field_dict["archived"] = archived
        if current_version is not UNSET:
            field_dict["current_version"] = current_version
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
        if last_run is not UNSET:
            field_dict["last_run"] = last_run
        if name is not UNSET:
            field_dict["name"] = name
        if next_scheduled_run is not UNSET:
            field_dict["next_scheduled_run"] = next_scheduled_run
        if paused is not UNSET:
            field_dict["paused"] = paused
        if pipeline_name is not UNSET:
            field_dict["pipeline_name"] = pipeline_name
        if public_secret is not UNSET:
            field_dict["public_secret"] = public_secret
        if triggers is not UNSET:
            field_dict["triggers"] = triggers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_response import RunResponse
        from ..models.script_version_response import ScriptVersionResponse
        from ..models.t_job_definition import TJobDefinition

        d = dict(src_dict)
        created_by = UUID(d.pop("created_by"))

        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        id = UUID(d.pop("id"))

        job_definition = TJobDefinition.from_dict(d.pop("job_definition"))

        job_definition_engine_version = d.pop("job_definition_engine_version")

        job_definition_hash = d.pop("job_definition_hash")

        job_ref = d.pop("job_ref")

        profile = d.pop("profile")

        def _parse_public_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        public_url = _parse_public_url(d.pop("public_url"))

        script_type = ScriptType(d.pop("script_type"))

        def _parse_script_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        script_url = _parse_script_url(d.pop("script_url"))

        version = d.pop("version")

        workspace_id = UUID(d.pop("workspace_id"))

        archived = d.pop("archived", UNSET)

        def _parse_current_version(
            data: object,
        ) -> None | ScriptVersionResponse | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                current_version_type_0 = ScriptVersionResponse.from_dict(data)

                return current_version_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ScriptVersionResponse | Unset, data)

        current_version = _parse_current_version(d.pop("current_version", UNSET))

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

        def _parse_last_run(data: object) -> None | RunResponse | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_run_type_0 = RunResponse.from_dict(data)

                return last_run_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunResponse | Unset, data)

        last_run = _parse_last_run(d.pop("last_run", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_next_scheduled_run(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_scheduled_run_type_0 = isoparse(data)

                return next_scheduled_run_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        next_scheduled_run = _parse_next_scheduled_run(
            d.pop("next_scheduled_run", UNSET)
        )

        paused = d.pop("paused", UNSET)

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

        detailed_script_response = cls(
            created_by=created_by,
            date_added=date_added,
            date_updated=date_updated,
            id=id,
            job_definition=job_definition,
            job_definition_engine_version=job_definition_engine_version,
            job_definition_hash=job_definition_hash,
            job_ref=job_ref,
            profile=profile,
            public_url=public_url,
            script_type=script_type,
            script_url=script_url,
            version=version,
            workspace_id=workspace_id,
            archived=archived,
            current_version=current_version,
            default_trigger=default_trigger,
            deployment_module=deployment_module,
            description=description,
            freshness=freshness,
            interval_end=interval_end,
            interval_start=interval_start,
            last_run=last_run,
            name=name,
            next_scheduled_run=next_scheduled_run,
            paused=paused,
            pipeline_name=pipeline_name,
            public_secret=public_secret,
            triggers=triggers,
        )

        detailed_script_response.additional_properties = d
        return detailed_script_response

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
