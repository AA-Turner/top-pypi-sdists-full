from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.job_environment import JobEnvironment


T = TypeVar("T", bound="JobEnvironments")


@_attrs_define
class JobEnvironments:
    """Per-environment overrides keyed by environment key (e.g. `production`, `staging`). Each entry sets `enabled`
    (whether the job is enabled — scheduled, for a recurring job, or triggerable, for a manual job — in that
    environment), an optional `schedule` override (a cron expression for recurring jobs; omit to inherit the base
    `schedule`), an optional `timezone` override (an IANA zone for recurring jobs; omit to inherit the base `timezone`,
    else UTC), and an optional `configuration` override (omit to inherit the base `configuration`); it also reports the
    read-only `next_run_at` for that environment. A job with no entry for an environment is disabled there. For a
    recurring or manual job, supply this map to choose where it runs. For a one-off job, the environment it is created
    in is recorded here automatically — name it with the `X-Smplkit-Environment` header. Every referenced environment
    must exist for the account.

    """

    additional_properties: dict[str, JobEnvironment] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_environment import JobEnvironment

        d = dict(src_dict)
        job_environments = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = JobEnvironment.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        job_environments.additional_properties = additional_properties
        return job_environments

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> JobEnvironment:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: JobEnvironment) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
