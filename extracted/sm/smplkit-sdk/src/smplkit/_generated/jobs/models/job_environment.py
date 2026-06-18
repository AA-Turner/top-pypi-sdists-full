from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.job_http_configuration import JobHttpConfiguration


T = TypeVar("T", bound="JobEnvironment")


@_attrs_define
class JobEnvironment:
    """Per-environment override for a job's enablement and configuration.

    Attributes:
        enabled (bool | Unset): Whether the job schedules runs in this environment. A job runs in an environment only
            via this field; it is disabled in every environment by default. Default: False.
        configuration (JobHttpConfiguration | None | Unset): Per-environment HTTP request override. Omit to inherit the
            job's base `configuration`. When present, it fully replaces the base configuration for runs in this environment.
    """

    enabled: bool | Unset = False
    configuration: JobHttpConfiguration | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_http_configuration import JobHttpConfiguration

        enabled = self.enabled

        configuration: dict[str, Any] | None | Unset
        if isinstance(self.configuration, Unset):
            configuration = UNSET
        elif isinstance(self.configuration, JobHttpConfiguration):
            configuration = self.configuration.to_dict()
        else:
            configuration = self.configuration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_http_configuration import JobHttpConfiguration

        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        def _parse_configuration(data: object) -> JobHttpConfiguration | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                configuration_type_0 = JobHttpConfiguration.from_dict(data)

                return configuration_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobHttpConfiguration | None | Unset, data)

        configuration = _parse_configuration(d.pop("configuration", UNSET))

        job_environment = cls(
            enabled=enabled,
            configuration=configuration,
        )

        job_environment.additional_properties = d
        return job_environment

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
