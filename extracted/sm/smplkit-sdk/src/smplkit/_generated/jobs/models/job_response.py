from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.job_resource import JobResource


T = TypeVar("T", bound="JobResponse")


@_attrs_define
class JobResponse:
    """JSON:API single-resource response for a job.

    Attributes:
        data (JobResource): JSON:API resource envelope for a job. The caller supplies `id` on create. Example:
            {'attributes': {'concurrency_policy': 'ALLOW', 'configuration': {'body': '{"scope":"all"}', 'headers': [{'name':
            'Authorization', 'value': 'Bearer s3cr3t'}], 'method': 'POST', 'success_status': '2xx', 'timeout': 30,
            'tls_verify': True, 'url': 'https://api.example.com/cache/warm'}, 'description': 'Warms the product cache every
            night at 02:00 UTC.', 'enabled': True, 'name': 'Nightly cache warm', 'schedule': '0 2 * * *', 'type': 'http'},
            'id': 'nightly-cache-warm', 'type': 'job'}.
    """

    data: JobResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_resource import JobResource

        d = dict(src_dict)
        data = JobResource.from_dict(d.pop("data"))

        job_response = cls(
            data=data,
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
