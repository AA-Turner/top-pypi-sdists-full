import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.script_type import ScriptType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.t_job_definition import TJobDefinition


T = TypeVar("T", bound="ScriptVersionResponse")


@_attrs_define
class ScriptVersionResponse:
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
        max_run_time_seconds (int): Maximum allowed run duration in seconds for this script version
        provider (str): Compute provider for runs using this script version (e.g. 'tower', 'modal')
        script_id (UUID): The ID of the script the script version belongs to
        script_type (ScriptType): The type of the script: batch, interactive, or stream
        version (int): The current version of the script
        default_trigger (Union[None, Unset, str]): Primary trigger string (computed from job_definition)
        deployment_module (Union[None, Unset, str]): Deployment module name (e.g. __deployment__)
        description (Union[None, Unset, str]): The description of the script
        freshness (Union[None, Unset, list[str]]): Freshness constraint strings (computed from job_definition)
        interval_end (Union[None, Unset, datetime.datetime]): Upper bound of the bounded work window (from
            job_definition.interval.end). None means no upper bound; the schedule halts once the next tick would exceed it.
        interval_start (Union[None, Unset, datetime.datetime]): Lower bound of the bounded work window (from
            job_definition.interval.start). None means the job has no bounded window.
        name (Union[None, Unset, str]): Display name for the job
        pipeline_name (Union[None, Unset, str]): Pipeline name this job operates on (computed from job_definition)
        profile (Union[None, Unset, str]): The name of the profile to use for the script
        triggers (Union[None, Unset, list[str]]): Trigger strings for this job (computed from job_definition)
    """

    created_by: UUID
    date_added: datetime.datetime
    date_updated: datetime.datetime
    id: UUID
    job_definition: "TJobDefinition"
    job_definition_engine_version: int
    job_definition_hash: str
    job_ref: str
    max_run_time_seconds: int
    provider: str
    script_id: UUID
    script_type: ScriptType
    version: int
    default_trigger: Union[None, Unset, str] = UNSET
    deployment_module: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    freshness: Union[None, Unset, list[str]] = UNSET
    interval_end: Union[None, Unset, datetime.datetime] = UNSET
    interval_start: Union[None, Unset, datetime.datetime] = UNSET
    name: Union[None, Unset, str] = UNSET
    pipeline_name: Union[None, Unset, str] = UNSET
    profile: Union[None, Unset, str] = UNSET
    triggers: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_by = str(self.created_by)

        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        id = str(self.id)

        job_definition = self.job_definition.to_dict()

        job_definition_engine_version = self.job_definition_engine_version

        job_definition_hash = self.job_definition_hash

        job_ref = self.job_ref

        max_run_time_seconds = self.max_run_time_seconds

        provider = self.provider

        script_id = str(self.script_id)

        script_type = self.script_type.value

        version = self.version

        default_trigger: Union[None, Unset, str]
        if isinstance(self.default_trigger, Unset):
            default_trigger = UNSET
        else:
            default_trigger = self.default_trigger

        deployment_module: Union[None, Unset, str]
        if isinstance(self.deployment_module, Unset):
            deployment_module = UNSET
        else:
            deployment_module = self.deployment_module

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        freshness: Union[None, Unset, list[str]]
        if isinstance(self.freshness, Unset):
            freshness = UNSET
        elif isinstance(self.freshness, list):
            freshness = self.freshness

        else:
            freshness = self.freshness

        interval_end: Union[None, Unset, str]
        if isinstance(self.interval_end, Unset):
            interval_end = UNSET
        elif isinstance(self.interval_end, datetime.datetime):
            interval_end = self.interval_end.isoformat()
        else:
            interval_end = self.interval_end

        interval_start: Union[None, Unset, str]
        if isinstance(self.interval_start, Unset):
            interval_start = UNSET
        elif isinstance(self.interval_start, datetime.datetime):
            interval_start = self.interval_start.isoformat()
        else:
            interval_start = self.interval_start

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        pipeline_name: Union[None, Unset, str]
        if isinstance(self.pipeline_name, Unset):
            pipeline_name = UNSET
        else:
            pipeline_name = self.pipeline_name

        profile: Union[None, Unset, str]
        if isinstance(self.profile, Unset):
            profile = UNSET
        else:
            profile = self.profile

        triggers: Union[None, Unset, list[str]]
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
                "max_run_time_seconds": max_run_time_seconds,
                "provider": provider,
                "script_id": script_id,
                "script_type": script_type,
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
        if interval_end is not UNSET:
            field_dict["interval_end"] = interval_end
        if interval_start is not UNSET:
            field_dict["interval_start"] = interval_start
        if name is not UNSET:
            field_dict["name"] = name
        if pipeline_name is not UNSET:
            field_dict["pipeline_name"] = pipeline_name
        if profile is not UNSET:
            field_dict["profile"] = profile
        if triggers is not UNSET:
            field_dict["triggers"] = triggers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
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

        max_run_time_seconds = d.pop("max_run_time_seconds")

        provider = d.pop("provider")

        script_id = UUID(d.pop("script_id"))

        script_type = ScriptType(d.pop("script_type"))

        version = d.pop("version")

        def _parse_default_trigger(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_trigger = _parse_default_trigger(d.pop("default_trigger", UNSET))

        def _parse_deployment_module(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deployment_module = _parse_deployment_module(d.pop("deployment_module", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_freshness(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                freshness_type_0 = cast(list[str], data)

                return freshness_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        freshness = _parse_freshness(d.pop("freshness", UNSET))

        def _parse_interval_end(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                interval_end_type_0 = isoparse(data)

                return interval_end_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        interval_end = _parse_interval_end(d.pop("interval_end", UNSET))

        def _parse_interval_start(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                interval_start_type_0 = isoparse(data)

                return interval_start_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        interval_start = _parse_interval_start(d.pop("interval_start", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_pipeline_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pipeline_name = _parse_pipeline_name(d.pop("pipeline_name", UNSET))

        def _parse_profile(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profile = _parse_profile(d.pop("profile", UNSET))

        def _parse_triggers(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                triggers_type_0 = cast(list[str], data)

                return triggers_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        triggers = _parse_triggers(d.pop("triggers", UNSET))

        script_version_response = cls(
            created_by=created_by,
            date_added=date_added,
            date_updated=date_updated,
            id=id,
            job_definition=job_definition,
            job_definition_engine_version=job_definition_engine_version,
            job_definition_hash=job_definition_hash,
            job_ref=job_ref,
            max_run_time_seconds=max_run_time_seconds,
            provider=provider,
            script_id=script_id,
            script_type=script_type,
            version=version,
            default_trigger=default_trigger,
            deployment_module=deployment_module,
            description=description,
            freshness=freshness,
            interval_end=interval_end,
            interval_start=interval_start,
            name=name,
            pipeline_name=pipeline_name,
            profile=profile,
            triggers=triggers,
        )

        script_version_response.additional_properties = d
        return script_version_response

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
