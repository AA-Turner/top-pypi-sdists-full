from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.job_environments_additional_property import JobEnvironmentsAdditionalProperty


T = TypeVar("T", bound="JobEnvironments")


@_attrs_define
class JobEnvironments:
    """Per-environment overrides keyed by environment key (e.g. `production`, `staging`). Each entry is a flat, sparse
    overlay: only the leaves that differ from the base definition are present, and everything absent is inherited. Set
    `enabled` to `true` to run the job in that environment (the base is disabled everywhere; an environment with no
    entry, or an entry without `enabled: true`, does not run). Overridable leaves are `url`, `method`, `timeout`,
    `body`, `success_status`, `tls_verify`, `ca_cert`, `schedule` and `timezone` (recurring jobs only), `retry_policy`
    (the `id` of a retry policy), and an individual header as `headers.<name>` (e.g. `headers.Authorization`). On read,
    each entry also reports the read-only `next_run_at` for that environment (the next fire time, or `null`). For a
    recurring or manual job, supply this map to choose where it runs. For a one-off job, name its target environment(s)
    here as the map keys — one run is enqueued per named environment; when the map is empty a single-environment
    credential implies the one environment. Every referenced environment must exist for the account.

    """

    additional_properties: dict[str, JobEnvironmentsAdditionalProperty] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_environments_additional_property import JobEnvironmentsAdditionalProperty

        d = dict(src_dict)
        job_environments = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = JobEnvironmentsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        job_environments.additional_properties = additional_properties
        return job_environments

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> JobEnvironmentsAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: JobEnvironmentsAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
