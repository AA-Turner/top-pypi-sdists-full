from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.job import Job


T = TypeVar("T", bound="JobResource")


@_attrs_define
class JobResource:
    """JSON:API resource envelope for a job. The caller supplies `id` on create.

    Example:
        {'attributes': {'concurrency_policy': 'ALLOW', 'configuration': {'body': '{"scope":"all"}', 'headers': [{'name':
            'Authorization', 'value': 'Bearer s3cr3t'}], 'method': 'POST', 'success_status': '2xx', 'timeout': 30,
            'tls_verify': True, 'url': 'https://api.example.com/cache/warm'}, 'description': 'Warms the product cache every
            night at 02:00 UTC.', 'environments': {'production': {'enabled': True}, 'staging': {'configuration': {'body':
            '{"scope":"all"}', 'headers': [{'name': 'Authorization', 'value': 'Bearer staging'}], 'method': 'POST',
            'success_status': '2xx', 'timeout': 30, 'tls_verify': True, 'url': 'https://staging.example.com/cache/warm'},
            'enabled': True, 'schedule': '0 3 * * *'}}, 'name': 'Nightly cache warm', 'schedule': '0 2 * * *', 'type':
            'http'}, 'id': 'nightly-cache-warm', 'type': 'job'}

    Attributes:
        attributes (Job): A scheduled unit of work: an HTTP request run on a schedule.

            The job is the definition; each time it fires the service records a run
            capturing the request, response, timing, and outcome. A job runs per
            environment: set `environments[<env>].enabled` to schedule runs there, and
            optionally give that environment its own `schedule` or `configuration`. A
            recurring (cron) job may be enabled in several environments at once and
            fires once per enabled environment, each on its own next-fire schedule; a
            one-off (`now` or future datetime) job runs a single time in the environment
            it was created in.
        id (None | str | Unset):
        type_ (str | Unset):  Default: 'job'.
    """

    attributes: Job
    id: None | str | Unset = UNSET
    type_: str | Unset = "job"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job import Job

        d = dict(src_dict)
        attributes = Job.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        type_ = d.pop("type", UNSET)

        job_resource = cls(
            attributes=attributes,
            id=id,
            type_=type_,
        )

        job_resource.additional_properties = d
        return job_resource

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
