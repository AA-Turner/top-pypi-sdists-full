from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.t_job_definition_auto_refresh_pipeline_mode import (
    TJobDefinitionAutoRefreshPipelineMode,
)
from ..models.t_job_definition_incremental_mode import TJobDefinitionIncrementalMode
from ..models.t_job_definition_refresh_propagation import (
    TJobDefinitionRefreshPropagation,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.t_agent_definition import TAgentDefinition
    from ..models.t_deliver_spec import TDeliverSpec
    from ..models.t_entry_point import TEntryPoint
    from ..models.t_execute_spec import TExecuteSpec
    from ..models.t_expose_spec import TExposeSpec
    from ..models.t_interval_spec import TIntervalSpec
    from ..models.t_job_definition_inputs import TJobDefinitionInputs
    from ..models.t_job_definition_output import TJobDefinitionOutput
    from ..models.t_require_spec import TRequireSpec
    from ..models.t_workspace_access import TWorkspaceAccess


T = TypeVar("T", bound="TJobDefinition")


@_attrs_define
class TJobDefinition:
    """Full job definition from dlt deployment manifest

    Attributes:
        engine_version (int):
        entry_point (TEntryPoint):
        execute (TExecuteSpec):
        job_ref (str):
        triggers (list[str]):
        access (TWorkspaceAccess | Unset):
        agent (TAgentDefinition | Unset):
        auto_refresh_pipeline_mode (TJobDefinitionAutoRefreshPipelineMode | Unset):
        config_keys (list[str] | Unset):
        default_trigger (str | Unset):
        deliver (TDeliverSpec | Unset):
        description (str | Unset):
        expose (TExposeSpec | Unset):
        freshness (list[str] | Unset):
        incremental_mode (TJobDefinitionIncrementalMode | Unset):
        inputs (TJobDefinitionInputs | Unset):
        interval (TIntervalSpec | Unset):
        output (TJobDefinitionOutput | Unset):
        refresh_propagation (TJobDefinitionRefreshPropagation | Unset):
        require (TRequireSpec | Unset):
    """

    engine_version: int
    entry_point: TEntryPoint
    execute: TExecuteSpec
    job_ref: str
    triggers: list[str]
    access: TWorkspaceAccess | Unset = UNSET
    agent: TAgentDefinition | Unset = UNSET
    auto_refresh_pipeline_mode: TJobDefinitionAutoRefreshPipelineMode | Unset = UNSET
    config_keys: list[str] | Unset = UNSET
    default_trigger: str | Unset = UNSET
    deliver: TDeliverSpec | Unset = UNSET
    description: str | Unset = UNSET
    expose: TExposeSpec | Unset = UNSET
    freshness: list[str] | Unset = UNSET
    incremental_mode: TJobDefinitionIncrementalMode | Unset = UNSET
    inputs: TJobDefinitionInputs | Unset = UNSET
    interval: TIntervalSpec | Unset = UNSET
    output: TJobDefinitionOutput | Unset = UNSET
    refresh_propagation: TJobDefinitionRefreshPropagation | Unset = UNSET
    require: TRequireSpec | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        engine_version = self.engine_version

        entry_point = self.entry_point.to_dict()

        execute = self.execute.to_dict()

        job_ref = self.job_ref

        triggers = self.triggers

        access: dict[str, Any] | Unset = UNSET
        if not isinstance(self.access, Unset):
            access = self.access.to_dict()

        agent: dict[str, Any] | Unset = UNSET
        if not isinstance(self.agent, Unset):
            agent = self.agent.to_dict()

        auto_refresh_pipeline_mode: str | Unset = UNSET
        if not isinstance(self.auto_refresh_pipeline_mode, Unset):
            auto_refresh_pipeline_mode = self.auto_refresh_pipeline_mode.value

        config_keys: list[str] | Unset = UNSET
        if not isinstance(self.config_keys, Unset):
            config_keys = self.config_keys

        default_trigger = self.default_trigger

        deliver: dict[str, Any] | Unset = UNSET
        if not isinstance(self.deliver, Unset):
            deliver = self.deliver.to_dict()

        description = self.description

        expose: dict[str, Any] | Unset = UNSET
        if not isinstance(self.expose, Unset):
            expose = self.expose.to_dict()

        freshness: list[str] | Unset = UNSET
        if not isinstance(self.freshness, Unset):
            freshness = self.freshness

        incremental_mode: str | Unset = UNSET
        if not isinstance(self.incremental_mode, Unset):
            incremental_mode = self.incremental_mode.value

        inputs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.inputs, Unset):
            inputs = self.inputs.to_dict()

        interval: dict[str, Any] | Unset = UNSET
        if not isinstance(self.interval, Unset):
            interval = self.interval.to_dict()

        output: dict[str, Any] | Unset = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        refresh_propagation: str | Unset = UNSET
        if not isinstance(self.refresh_propagation, Unset):
            refresh_propagation = self.refresh_propagation.value

        require: dict[str, Any] | Unset = UNSET
        if not isinstance(self.require, Unset):
            require = self.require.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "engine_version": engine_version,
                "entry_point": entry_point,
                "execute": execute,
                "job_ref": job_ref,
                "triggers": triggers,
            }
        )
        if access is not UNSET:
            field_dict["access"] = access
        if agent is not UNSET:
            field_dict["agent"] = agent
        if auto_refresh_pipeline_mode is not UNSET:
            field_dict["auto_refresh_pipeline_mode"] = auto_refresh_pipeline_mode
        if config_keys is not UNSET:
            field_dict["config_keys"] = config_keys
        if default_trigger is not UNSET:
            field_dict["default_trigger"] = default_trigger
        if deliver is not UNSET:
            field_dict["deliver"] = deliver
        if description is not UNSET:
            field_dict["description"] = description
        if expose is not UNSET:
            field_dict["expose"] = expose
        if freshness is not UNSET:
            field_dict["freshness"] = freshness
        if incremental_mode is not UNSET:
            field_dict["incremental_mode"] = incremental_mode
        if inputs is not UNSET:
            field_dict["inputs"] = inputs
        if interval is not UNSET:
            field_dict["interval"] = interval
        if output is not UNSET:
            field_dict["output"] = output
        if refresh_propagation is not UNSET:
            field_dict["refresh_propagation"] = refresh_propagation
        if require is not UNSET:
            field_dict["require"] = require

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.t_agent_definition import TAgentDefinition
        from ..models.t_deliver_spec import TDeliverSpec
        from ..models.t_entry_point import TEntryPoint
        from ..models.t_execute_spec import TExecuteSpec
        from ..models.t_expose_spec import TExposeSpec
        from ..models.t_interval_spec import TIntervalSpec
        from ..models.t_job_definition_inputs import TJobDefinitionInputs
        from ..models.t_job_definition_output import TJobDefinitionOutput
        from ..models.t_require_spec import TRequireSpec
        from ..models.t_workspace_access import TWorkspaceAccess

        d = dict(src_dict)
        engine_version = d.pop("engine_version")

        entry_point = TEntryPoint.from_dict(d.pop("entry_point"))

        execute = TExecuteSpec.from_dict(d.pop("execute"))

        job_ref = d.pop("job_ref")

        triggers = cast(list[str], d.pop("triggers"))

        _access = d.pop("access", UNSET)
        access: TWorkspaceAccess | Unset
        if isinstance(_access, Unset):
            access = UNSET
        else:
            access = TWorkspaceAccess.from_dict(_access)

        _agent = d.pop("agent", UNSET)
        agent: TAgentDefinition | Unset
        if isinstance(_agent, Unset):
            agent = UNSET
        else:
            agent = TAgentDefinition.from_dict(_agent)

        _auto_refresh_pipeline_mode = d.pop("auto_refresh_pipeline_mode", UNSET)
        auto_refresh_pipeline_mode: TJobDefinitionAutoRefreshPipelineMode | Unset
        if isinstance(_auto_refresh_pipeline_mode, Unset):
            auto_refresh_pipeline_mode = UNSET
        else:
            auto_refresh_pipeline_mode = TJobDefinitionAutoRefreshPipelineMode(
                _auto_refresh_pipeline_mode
            )

        config_keys = cast(list[str], d.pop("config_keys", UNSET))

        default_trigger = d.pop("default_trigger", UNSET)

        _deliver = d.pop("deliver", UNSET)
        deliver: TDeliverSpec | Unset
        if isinstance(_deliver, Unset):
            deliver = UNSET
        else:
            deliver = TDeliverSpec.from_dict(_deliver)

        description = d.pop("description", UNSET)

        _expose = d.pop("expose", UNSET)
        expose: TExposeSpec | Unset
        if isinstance(_expose, Unset):
            expose = UNSET
        else:
            expose = TExposeSpec.from_dict(_expose)

        freshness = cast(list[str], d.pop("freshness", UNSET))

        _incremental_mode = d.pop("incremental_mode", UNSET)
        incremental_mode: TJobDefinitionIncrementalMode | Unset
        if isinstance(_incremental_mode, Unset):
            incremental_mode = UNSET
        else:
            incremental_mode = TJobDefinitionIncrementalMode(_incremental_mode)

        _inputs = d.pop("inputs", UNSET)
        inputs: TJobDefinitionInputs | Unset
        if isinstance(_inputs, Unset):
            inputs = UNSET
        else:
            inputs = TJobDefinitionInputs.from_dict(_inputs)

        _interval = d.pop("interval", UNSET)
        interval: TIntervalSpec | Unset
        if isinstance(_interval, Unset):
            interval = UNSET
        else:
            interval = TIntervalSpec.from_dict(_interval)

        _output = d.pop("output", UNSET)
        output: TJobDefinitionOutput | Unset
        if isinstance(_output, Unset):
            output = UNSET
        else:
            output = TJobDefinitionOutput.from_dict(_output)

        _refresh_propagation = d.pop("refresh_propagation", UNSET)
        refresh_propagation: TJobDefinitionRefreshPropagation | Unset
        if isinstance(_refresh_propagation, Unset):
            refresh_propagation = UNSET
        else:
            refresh_propagation = TJobDefinitionRefreshPropagation(_refresh_propagation)

        _require = d.pop("require", UNSET)
        require: TRequireSpec | Unset
        if isinstance(_require, Unset):
            require = UNSET
        else:
            require = TRequireSpec.from_dict(_require)

        t_job_definition = cls(
            engine_version=engine_version,
            entry_point=entry_point,
            execute=execute,
            job_ref=job_ref,
            triggers=triggers,
            access=access,
            agent=agent,
            auto_refresh_pipeline_mode=auto_refresh_pipeline_mode,
            config_keys=config_keys,
            default_trigger=default_trigger,
            deliver=deliver,
            description=description,
            expose=expose,
            freshness=freshness,
            incremental_mode=incremental_mode,
            inputs=inputs,
            interval=interval,
            output=output,
            refresh_propagation=refresh_propagation,
            require=require,
        )

        t_job_definition.additional_properties = d
        return t_job_definition

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
