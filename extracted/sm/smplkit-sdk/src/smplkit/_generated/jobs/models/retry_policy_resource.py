from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.retry_policy import RetryPolicy


T = TypeVar("T", bound="RetryPolicyResource")


@_attrs_define
class RetryPolicyResource:
    """JSON:API resource envelope for a retry policy. The caller supplies `id` on create.

    Example:
        {'attributes': {'backoff': 'exponential', 'delay_seconds': 2, 'max_delay_seconds': 60, 'max_retries': 5, 'name':
            'Retry on server errors', 'retry_on_connection_error': True, 'retry_on_timeout': True, 'retry_statuses': ['429',
            '5xx'], 'retry_statuses_except': ['501']}, 'id': 'retry-on-5xx', 'type': 'retry_policy'}

    Attributes:
        attributes (RetryPolicy): A named, reusable automatic-retry policy.

            A policy decides whether and how a failed run is retried. Reference it from
            a job's `retry_policy` (and optionally override it per environment). A job
            that references no policy is never retried.
        id (None | str | Unset):
        type_ (str | Unset):  Default: 'retry_policy'.
    """

    attributes: RetryPolicy
    id: None | str | Unset = UNSET
    type_: str | Unset = "retry_policy"
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
        from ..models.retry_policy import RetryPolicy

        d = dict(src_dict)
        attributes = RetryPolicy.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        type_ = d.pop("type", UNSET)

        retry_policy_resource = cls(
            attributes=attributes,
            id=id,
            type_=type_,
        )

        retry_policy_resource.additional_properties = d
        return retry_policy_resource

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
