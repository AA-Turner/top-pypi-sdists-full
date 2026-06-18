from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.job_create_resource import JobCreateResource


T = TypeVar("T", bound="JobCreateRequest")


@_attrs_define
class JobCreateRequest:
    """JSON:API request envelope for creating a job (caller-supplied `data.id`).

    Attributes:
        data (JobCreateResource): JSON:API resource envelope for creating a job (id required). Example: {'attributes':
            {'concurrency_policy': 'ALLOW', 'configuration': {'body': '{"scope":"all"}', 'headers': [{'name':
            'Authorization', 'value': 'Bearer s3cr3t'}], 'method': 'POST', 'success_status': '2xx', 'timeout': 30,
            'tls_verify': True, 'url': 'https://api.example.com/cache/warm'}, 'description': 'Warms the product cache every
            night at 02:00 UTC.', 'environments': {'production': {'enabled': True}, 'staging': {'configuration': {'body':
            '{"scope":"all"}', 'headers': [{'name': 'Authorization', 'value': 'Bearer staging'}], 'method': 'POST',
            'success_status': '2xx', 'timeout': 30, 'tls_verify': True, 'url': 'https://staging.example.com/cache/warm'},
            'enabled': True}}, 'name': 'Nightly cache warm', 'schedule': '0 2 * * *', 'type': 'http'}, 'id': 'nightly-cache-
            warm', 'type': 'job'}.
    """

    data: JobCreateResource
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
        from ..models.job_create_resource import JobCreateResource

        d = dict(src_dict)
        data = JobCreateResource.from_dict(d.pop("data"))

        job_create_request = cls(
            data=data,
        )

        job_create_request.additional_properties = d
        return job_create_request

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
