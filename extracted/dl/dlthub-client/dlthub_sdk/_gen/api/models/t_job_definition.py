from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.t_job_definition_refresh import TJobDefinitionRefresh
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.t_deliver_spec import TDeliverSpec
    from ..models.t_entry_point import TEntryPoint
    from ..models.t_execute_spec import TExecuteSpec
    from ..models.t_expose_spec import TExposeSpec
    from ..models.t_interval_spec import TIntervalSpec
    from ..models.t_require_spec import TRequireSpec


T = TypeVar("T", bound="TJobDefinition")


@_attrs_define
class TJobDefinition:
    """
    Attributes:
        entry_point (TEntryPoint):
        execute (TExecuteSpec):
        job_ref (str):
        triggers (list[str]):
        allow_external_schedulers (bool | Unset):
        config_keys (list[str] | Unset):
        default_trigger (str | Unset):
        deliver (TDeliverSpec | Unset):
        description (str | Unset):
        expose (TExposeSpec | Unset):
        freshness (list[str] | Unset):
        interval (TIntervalSpec | Unset):
        refresh (TJobDefinitionRefresh | Unset):
        require (TRequireSpec | Unset):
    """

    entry_point: TEntryPoint
    execute: TExecuteSpec
    job_ref: str
    triggers: list[str]
    allow_external_schedulers: bool | Unset = UNSET
    config_keys: list[str] | Unset = UNSET
    default_trigger: str | Unset = UNSET
    deliver: TDeliverSpec | Unset = UNSET
    description: str | Unset = UNSET
    expose: TExposeSpec | Unset = UNSET
    freshness: list[str] | Unset = UNSET
    interval: TIntervalSpec | Unset = UNSET
    refresh: TJobDefinitionRefresh | Unset = UNSET
    require: TRequireSpec | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entry_point = self.entry_point.to_dict()

        execute = self.execute.to_dict()

        job_ref = self.job_ref

        triggers = self.triggers

        allow_external_schedulers = self.allow_external_schedulers

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

        interval: dict[str, Any] | Unset = UNSET
        if not isinstance(self.interval, Unset):
            interval = self.interval.to_dict()

        refresh: str | Unset = UNSET
        if not isinstance(self.refresh, Unset):
            refresh = self.refresh.value

        require: dict[str, Any] | Unset = UNSET
        if not isinstance(self.require, Unset):
            require = self.require.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entry_point": entry_point,
                "execute": execute,
                "job_ref": job_ref,
                "triggers": triggers,
            }
        )
        if allow_external_schedulers is not UNSET:
            field_dict["allow_external_schedulers"] = allow_external_schedulers
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
        if interval is not UNSET:
            field_dict["interval"] = interval
        if refresh is not UNSET:
            field_dict["refresh"] = refresh
        if require is not UNSET:
            field_dict["require"] = require

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.t_deliver_spec import TDeliverSpec
        from ..models.t_entry_point import TEntryPoint
        from ..models.t_execute_spec import TExecuteSpec
        from ..models.t_expose_spec import TExposeSpec
        from ..models.t_interval_spec import TIntervalSpec
        from ..models.t_require_spec import TRequireSpec

        d = dict(src_dict)
        entry_point = TEntryPoint.from_dict(d.pop("entry_point"))

        execute = TExecuteSpec.from_dict(d.pop("execute"))

        job_ref = d.pop("job_ref")

        triggers = cast(list[str], d.pop("triggers"))

        allow_external_schedulers = d.pop("allow_external_schedulers", UNSET)

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

        _interval = d.pop("interval", UNSET)
        interval: TIntervalSpec | Unset
        if isinstance(_interval, Unset):
            interval = UNSET
        else:
            interval = TIntervalSpec.from_dict(_interval)

        _refresh = d.pop("refresh", UNSET)
        refresh: TJobDefinitionRefresh | Unset
        if isinstance(_refresh, Unset):
            refresh = UNSET
        else:
            refresh = TJobDefinitionRefresh(_refresh)

        _require = d.pop("require", UNSET)
        require: TRequireSpec | Unset
        if isinstance(_require, Unset):
            require = UNSET
        else:
            require = TRequireSpec.from_dict(_require)

        t_job_definition = cls(
            entry_point=entry_point,
            execute=execute,
            job_ref=job_ref,
            triggers=triggers,
            allow_external_schedulers=allow_external_schedulers,
            config_keys=config_keys,
            default_trigger=default_trigger,
            deliver=deliver,
            description=description,
            expose=expose,
            freshness=freshness,
            interval=interval,
            refresh=refresh,
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
