from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.retry_policy_resource import RetryPolicyResource


T = TypeVar("T", bound="RetryPolicyResponse")


@_attrs_define
class RetryPolicyResponse:
    """JSON:API single-resource response for a retry policy.

    Attributes:
        data (RetryPolicyResource): JSON:API resource envelope for a retry policy. The caller supplies `id` on create.
            Example: {'attributes': {'backoff': 'exponential', 'delay_seconds': 2, 'max_delay_seconds': 60, 'max_retries':
            5, 'name': 'Retry on server errors', 'retry_on_connection_error': True, 'retry_on_timeout': True,
            'retry_statuses': ['429', '5xx'], 'retry_statuses_except': ['501']}, 'id': 'retry-on-5xx', 'type':
            'retry_policy'}.
    """

    data: RetryPolicyResource
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
        from ..models.retry_policy_resource import RetryPolicyResource

        d = dict(src_dict)
        data = RetryPolicyResource.from_dict(d.pop("data"))

        retry_policy_response = cls(
            data=data,
        )

        retry_policy_response.additional_properties = d
        return retry_policy_response

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
