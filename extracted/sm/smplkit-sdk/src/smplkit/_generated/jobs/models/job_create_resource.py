from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.job import Job


T = TypeVar("T", bound="JobCreateResource")


@_attrs_define
class JobCreateResource:
    """JSON:API resource envelope for creating a job (id required).

    Example:
        {'attributes': {'concurrency_policy': 'ALLOW', 'configuration': {'body': '{"scope":"all"}', 'headers': [{'name':
            'Authorization', 'value': 'Bearer s3cr3t'}], 'method': 'POST', 'success_status': '2xx', 'timeout': 30,
            'tls_verify': True, 'url': 'https://api.example.com/cache/warm'}, 'description': 'Warms the product cache every
            night at 02:00 UTC.', 'enabled': True, 'name': 'Nightly cache warm', 'schedule': '0 2 * * *', 'type': 'http'},
            'id': 'nightly-cache-warm', 'type': 'job'}

    Attributes:
        id (str): Client-supplied resource id.
        attributes (Job): A scheduled unit of work: an HTTP request run on a schedule.

            The job is the definition; each time it fires the service records a run
            capturing the request, response, timing, and outcome.
        type_ (Literal['job'] | Unset):  Default: 'job'.
    """

    id: str
    attributes: Job
    type_: Literal["job"] | Unset = "job"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        attributes = self.attributes.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "attributes": attributes,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job import Job

        d = dict(src_dict)
        id = d.pop("id")

        attributes = Job.from_dict(d.pop("attributes"))

        type_ = cast(Literal["job"] | Unset, d.pop("type", UNSET))
        if type_ != "job" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'job', got '{type_}'")

        job_create_resource = cls(
            id=id,
            attributes=attributes,
            type_=type_,
        )

        job_create_resource.additional_properties = d
        return job_create_resource

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
